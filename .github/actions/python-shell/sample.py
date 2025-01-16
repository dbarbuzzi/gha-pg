#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
from typing import Any


def print_env_vars(**kwargs):
    res = subprocess.check_output("env", cwd=Path.cwd(), encoding="utf-8", **kwargs)
    print("\n".join(sorted(res.splitlines())))


groups: dict[str, dict[str, Any]] = {
    "kwargs={}": {},
    "kwargs={shell=True}": {"shell": True},
    "kwargs={shell=True,env=os.environ}": {"shell": True, "env": os.environ},
}

for label, kwargs in groups.items():
    print(f"::group::{label}")
    print_env_vars(**kwargs)
    print("::endgroup::")
