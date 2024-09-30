#!/usr/bin/env python

import os
import subprocess
from pathlib import Path

print("::group::shell=[default]", flush=True)
# subprocess.run("env")
subprocess.run("env", cwd=Path.cwd())
print("::endgroup::")

print("::group::shell=True", flush=True)
# subprocess.run("env", shell=True)
subprocess.run("env", cwd=Path.cwd(), shell=True)
print("::endgroup::")

print('::group::shell=True & env={"PATH": os.getenv("PATH", "")}', flush=True)
# subprocess.run("env", shell=True)
subprocess.run("env", cwd=Path.cwd(), shell=True, env={"PATH": os.getenv("PATH", "")})
print("::endgroup::")
