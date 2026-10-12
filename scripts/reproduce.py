"""Verify the included study and regenerate publication assets portably."""
import argparse
import os
from pathlib import Path
import subprocess
import sys


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compile',action='store_true',help='Compile using tectonic on PATH')
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    environment=dict(os.environ,PYTHONPATH=str(root/'src'))
    commands=[['-m','pip','check'],['-m','pytest','-q'],
        ['-m','bayes_digits.experiment','--config','configs/smoke.json'],
        ['scripts/audit_results.py'],['scripts/paired_analysis.py'],
        ['-m','bayes_digits.figures'],['scripts/build_report.py'],
        ['scripts/audit_review.py'],['scripts/audit_refinement.py'],
        ['scripts/audit_instruction_section.py'],['scripts/audit_paired.py']]
    for command in commands:
        print('python '+' '.join(command),flush=True)
        subprocess.run([sys.executable,*command],cwd=root,env=environment,check=True)
    if args.compile:
        for document in ['main.tex','workflow_export.tex']:
            subprocess.run(['tectonic','-X','compile','--untrusted',document],cwd=root/'report',check=True)
        subprocess.run([sys.executable,'scripts/export_workflow.py'],cwd=root,check=True)
    for command in ['scripts/validate_submission.py','scripts/check_artifacts.py']:
        print('python '+command,flush=True)
        subprocess.run([sys.executable,command],cwd=root,env=environment,check=True)
    print('Reproduction completed; inspect the final PDF visually after compilation.')


if __name__=='__main__':
    main()
