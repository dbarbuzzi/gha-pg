#!/usr/bin/env python

import os
import subprocess
from pathlib import Path


def print_env_vars(**kwargs):
    res = subprocess.check_output("env", cwd=Path.cwd(), encoding="utf-8", **kwargs)
    print(sorted(res.splitlines()))


print("::group::shell=[default]", flush=True)
# subprocess.run("env")
print_env_vars()
print("::endgroup::")

print("::group::shell=True", flush=True)
# subprocess.run("env", shell=True)
print_env_vars(shell=True)
print("::endgroup::")

print("::group::shell=True & env=os.environ", flush=True)
# subprocess.run("env", shell=True)
print_env_vars(shell=True, env=os.environ)
print("::endgroup::")
