"""Redact machine paths without changing non-path diagnostics or measurements."""
import re


def redact_text(value):
    # Windows absolute prefixes are recognized generically; no local username is embedded.
    value=re.sub(r'[A-Z]:[\\/](?:[^\\/\n`"\'<>]+[\\/])*?(?:bayesian-handwritten-digit-recognition|AI Assignment 2)(?=[\\/]|$)',
        '{PROJECT_ROOT}',value,flags=re.I)
    value=re.sub(r'[A-Z]:[\\/]Users[\\/][^\\/\s"\']+[\\/]\.(?:cache|codex)[\\/][^\s`"\']+',
        '{LOCAL_TOOL}',value,flags=re.I)
    value=re.sub(r'[A-Z]:[\\/]Program Files[\\/]WindowsApps[\\/][^\s`"\']+',
        '{TECTONIC}',value,flags=re.I)
    value=re.sub(r'[A-Z]:[\\/]Users[\\/][^\\/\s"\']+', '{LOCAL_HOME}',value,flags=re.I)
    return value


def redact(value):
    if isinstance(value,str):return redact_text(value)
    if isinstance(value,list):return [redact(v) for v in value]
    if isinstance(value,dict):return {k:redact(v) for k,v in value.items()}
    return value
