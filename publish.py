#!/usr/bin/env python3

import os
import subprocess
from contextlib import contextmanager

@contextmanager
def chg_cwd(path: str):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)


root_absdir = os.path.dirname(os.path.abspath(__file__))

with chg_cwd('../galdebert.github.io'):
    subprocess.run(['git', 'rm', '-r', '.'])


    subprocess.run(['hugo', '-d', '../galdebert.github.io'])
    subprocess.run(['git', 'commit', '-A'])
    subprocess.run(['hugo', ])

