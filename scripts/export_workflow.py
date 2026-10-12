"""Export the independently compiled TikZ workflow as cropped vector/raster assets."""
import hashlib
import json
from pathlib import Path
import pymupdf


def main():
    original=Path('report/workflow_export.pdf'); document=pymupdf.open(original)
    assert len(document)==1
    page=document[0]; bounds=[pymupdf.Rect(v['rect']) for v in page.get_drawings()]
    bounds += [pymupdf.Rect(b[:4]) for b in page.get_text('blocks')]
    region=bounds[0]
    for box in bounds[1:]:region |= box
    region=pymupdf.Rect(region.x0-5,region.y0-5,region.x1+5,region.y1+5)&page.rect
    page.set_cropbox(region)
    out=Path('results/refinement_05'); pdf=out/'instruction_workflow.pdf'
    document.save(pdf)
    exported=pymupdf.open(pdf); final=exported[0]
    (out/'instruction_workflow.svg').write_text(final.get_svg_image(text_as_path=False),newline='\n')
    final.get_pixmap(dpi=300).save(out/'instruction_workflow.png')
    files={p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [
        pdf,out/'instruction_workflow.svg',out/'instruction_workflow.png']}
    record=dict(editable_source='report/instruction_workflow.tex',source_sha256=hashlib.sha256(
        Path('report/instruction_workflow.tex').read_bytes()).hexdigest(),files=files,
        width_mm=final.rect.width*25.4/72,height_mm=final.rect.height*25.4/72,raster_dpi=300,
        generator='scripts/export_workflow.py',generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        generated_from='report/workflow_export.pdf',compiled_source_sha256=hashlib.sha256(original.read_bytes()).hexdigest(),
        standalone_source_sha256=hashlib.sha256(Path('report/workflow_export.tex').read_bytes()).hexdigest())
    (out/'workflow_manifest.json').write_text(json.dumps(record,indent=2)+'\n',newline='\n')
    print('Workflow PDF/SVG/300-DPI PNG exported from compiled TikZ source.')


if __name__=='__main__':
    main()
