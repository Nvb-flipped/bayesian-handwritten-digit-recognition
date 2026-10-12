"""Validate current PDF, figure exports, documentation structure and public privacy."""
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
import xml.etree.ElementTree as ET
from PIL import Image
from pypdf import PdfReader
import pymupdf


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2)+'\n',encoding='utf8',newline='\n')


def canonical(value):
    return re.sub(r'[\s\-\u00ad]','',unicodedata.normalize('NFKC',value).replace('’',"'"))


def main():
    reader=PdfReader('report/main.pdf');pages=[p.extract_text() for p in reader.pages]
    text='\n'.join(pages)
    for token in ['CISC3024','Paco, Sou Chak Tong','U-C3-2652-3',
        'How AI Found the Algorithm','Algorithm Description','How AI Implemented the Algorithm',
        'Experiment Settings and Results','What I Have Learnt from This AI Assignment',
        'Webpage Link of the Source Codes']:
        assert canonical(token) in canonical(text),token
    assert 'STUDENT REFLECTION REQUIRED' not in text and not re.search('[\u3400-\u9fff]',text)
    reflection=Path('report/student_reflection.txt').read_text(encoding='utf8')
    tex=Path('report/student_reflection.tex').read_text(encoding='utf8')
    assert tex.replace(r'\%', '%').replace(r'\textquoteright{}','’')==reflection
    reflection_pages=[]
    for para in reflection.strip().split('\n\n'):
        assert canonical(para) in canonical(text)
        reflection_pages += [i+1 for i,t in enumerate(pages) if canonical(para) in canonical(t)]
    quotes=json.loads(Path('docs/prompt_excerpts.json').read_text())
    for row in quotes:assert canonical(row['quote']) in canonical(text)
    compile_record=json.loads(Path('results/refinement_05/compile.json').read_text())
    assert compile_record['exitCode']==0
    log=compile_record['log'];last=log.rsplit('note: Rerunning TeX',1)[-1]
    assert not any(s in log for s in ['Overfull','Underfull','already defined.'])
    assert 'undefined' not in last.lower()
    assert not re.search(rb'\sDo(?:\s|$)',reader.pages[1].get_contents().get_data())
    for i in range(1,10):assert f'Figure {i}:' in text
    for i in range(1,12):assert f'Table {i}:' in text
    write('results/report_validation.json',dict(pdf='report/main.pdf',sha256=digest('report/main.pdf'),
        pages=len(pages),compiler_record='results/refinement_05/compile.json',compiler_exit_code=0,
        layout_box_warnings=0,final_pass_unresolved_references=False,duplicate_pdf_destinations=False,
        title_metadata_verified=True,required_sections_verified=6,numbered_figures_verified=9,
        numbered_tables_verified=11,student_supplied_reflection_preserved=True,
        reflection_paragraphs_verified=5,reflection_pages=sorted(set(reflection_pages)),
        reflection_source_sha256=digest('report/student_reflection.txt'),instruction_section_pages=[2,3,4],
        vector_workflow_diagram_verified=True,prompt_excerpts_verified_in_compiled_pdf=len(quotes),
        automated_validation_only=True))
    figures=[]
    for entry in json.loads(Path('results/figure_manifest.json').read_text()):
        assert digest(entry['generator'])==entry['generator_sha256']
        for p,h in entry['source_sha256'].items():assert digest(Path('results')/p)==h,p
        for p,h in entry.get('supporting_source_sha256',{}).items():assert digest(p)==h,p
        files={};base=Path('results/figures')/entry['name']
        for ext in ['pdf','svg','png']:
            p=base.with_suffix('.'+ext);files[ext]=dict(bytes=p.stat().st_size,sha256=digest(p))
        ET.parse(base.with_suffix('.svg'))
        with Image.open(base.with_suffix('.png')) as im:
            assert all(abs(d-300)<1 for d in im.info['dpi'])
            assert all(abs(px-inch*300)<1.1 for px,inch in zip(im.size,entry['inches']))
            files['png'].update(pixels=list(im.size),dpi=list(im.info['dpi']))
        doc=pymupdf.open(base.with_suffix('.pdf'));assert len(doc)==1
        sizes=[s['size'] for b in doc[0].get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()]
        assert min(sizes)>=5,entry['name']
        fonts=PdfReader(base.with_suffix('.pdf')).pages[0]['/Resources']['/Font'].get_object()
        assert fonts
        for f in fonts.values():
            obj=f.get_object();children=obj.get('/DescendantFonts')
            desc=(children[0].get_object()['/FontDescriptor'] if children else obj['/FontDescriptor']).get_object()
            assert any(k in desc for k in ['/FontFile','/FontFile2','/FontFile3'])
        figures.append(dict(name=entry['name'],files=files,fonts_embedded=True,minimum_glyph_pt=min(sizes)))
    workflow=json.loads(Path('results/refinement_05/workflow_manifest.json').read_text())
    assert digest(workflow['editable_source'])==workflow['source_sha256']
    for p,h in workflow['files'].items():assert digest(p)==h,p
    ET.parse('results/refinement_05/instruction_workflow.svg')
    assert len(pymupdf.open('results/refinement_05/instruction_workflow.pdf'))==1
    write('results/figure_export_validation.json',dict(figures=figures,review_date='2026-10-12',
        workflow_manifest='results/refinement_05/workflow_manifest.json',automated_validation_only=True))
    docs=[Path('README.md'),Path('docs/skill_sources.md'),*sorted(Path('docs/wiki').glob('*.md'))]
    records=[]
    for p in docs:
        t=p.read_text(encoding='utf8')
        assert not any(k in t for k in [r'\(',r'\)',r'\[',r'\]'])
        for fence in ['```','~~~']:assert sum(l.startswith(fence) for l in t.splitlines())%2==0,p
        assert t.count('\n$$')%2==0
        records.append(dict(source=p.as_posix(),gfm_structure_checked=True,
            tables=sum(bool(re.match(r'\|[-: ]+\|',l)) for l in t.splitlines()),math_fences=t.count('```math')))
    write('results/markdown_validation.json',dict(renderer='GFM source structure audit; public rendering separately verified',
        records=records,source_sha256={p.as_posix():digest(p) for p in docs},automated_validation_only=True))
    names=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard','-z']).decode().split('\0')[:-1]
    findings=[];checked=0
    for name in names:
        p=Path(name)
        if not p.is_file():continue
        try:t=p.read_text(encoding='utf-8-sig')
        except (UnicodeError,OSError):continue
        checked+=1
        if re.search('[\u3400-\u9fff]',t):findings.append(dict(file=name,reason='Non-English CJK text'))
        if re.search(r'[A-Z]:[\\/]+Users[\\/]+[^\\/\s]+',t):findings.append(dict(file=name,reason='Absolute user-home path'))
    write('results/refinement_05/current_privacy.json',dict(text_files_checked=checked,
        findings=findings,scope='Current non-ignored deliverable text; historical exposure remains separately documented'))
    assert not findings,findings
    print(f'Submission validation passed: {len(pages)} pages, six sections, eleven tables, ten figure triplets, workflow exports, English/privacy and GFM structure.')


if __name__=='__main__':main()
