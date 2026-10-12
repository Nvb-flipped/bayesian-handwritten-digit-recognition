# Portable wrapper: use the independently installed project environment.
$ErrorActionPreference = 'Stop'
$taskRoot = Split-Path $PSScriptRoot -Parent
$taskPython = Join-Path $taskRoot '.venv/Scripts/python.exe'
if (-not (Test-Path -LiteralPath $taskPython)) { throw 'Create .venv and install requirements first.' }
& $taskPython (Join-Path $taskRoot 'scripts/reproduce.py') @args
if ($LASTEXITCODE -ne 0) { throw "Reproduction failed with exit code $LASTEXITCODE" }
