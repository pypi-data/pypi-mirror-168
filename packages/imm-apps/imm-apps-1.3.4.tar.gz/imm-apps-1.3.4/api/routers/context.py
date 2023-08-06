import os, sys
from pathlib import Path

# Get project's home directory,
# BASEDIR=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BASEDIR = Path(__file__).parents[3]
# All data directory
DATADIR = BASEDIR / "data"
# Insert the BASEDIR to system path
sys.path.insert(0, os.fspath(BASEDIR))
