#!/usr/bin/env python

import os
import subprocess
from pathlib import Path
from typing import Any


def get_env_vars(**kwargs) -> list[str]:
    res = subprocess.check_output("env", cwd=Path.cwd(), encoding="utf-8", **kwargs)
    return sorted(res.splitlines())


groups: dict[str, dict[str, Any]] = {
    "kwargs={}": {},
    "kwargs={shell=True}": {"shell": True},
    "kwargs={shell=True,env=os.environ}": {"shell": True, "env": os.environ},
}

for label, kwargs in groups.items():
    print(f"::group::{label}")
    env_vars = get_env_vars(**kwargs)
    print(f"found {len(env_vars)} env vars:")
    print("\n".join(sorted(env_vars)))
    print("::endgroup::")
