#!/usr/bin/env python3

import os
import subprocess
from distutils.dir_util import copy_tree
from contextlib import contextmanager

@contextmanager
def chg_cwd(path: str):
    old_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_cwd)

# check=True will raise an exception if returncode != 0
# it's like subprocess.chek_output() but we still want to print output even if returncode != 0
def run(cmd, check: bool):
    print(' '.join(cmd))
    completed = subprocess.run(cmd, check=check, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(completed.stdout.decode("utf-8"))
    if check and completed.returncode != 0:
        raise subprocess.CalledProcessError

blog = os.path.dirname(os.path.abspath(__file__))
generated = os.path.normpath(os.path.join(blog, '../galdebert.github.io'))
to_copy = os.path.join(blog, 'to_copy')

run(['hugo', '--cleanDestinationDir', '-d', generated], check=True)
copy_tree('./to_copy', generated)

with chg_cwd(generated):
    run(['git', 'add', '-A'], check=True)
    # git commit returns 1 if there is nothing to commit
    run(['git', 'commit', '-m', 'new generated pages'], check=False)
    run(['git', 'push'], check=True)
