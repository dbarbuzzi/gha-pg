#!/usr/bin/env python

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
