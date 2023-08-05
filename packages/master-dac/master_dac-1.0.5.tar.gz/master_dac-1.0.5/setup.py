from distutils.core import setup
import sys
import os

def is_venv():
    return (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
        (os.environ.get("CONDA_PREFIX", None) is not None)
    )

assert is_venv(), "L'installation doit se faire dans un environnement virtuel: python -m venv ...REPERTOIRE..."

# Let's go
setup()