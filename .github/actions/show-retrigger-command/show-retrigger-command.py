#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pyyaml>=6.0.3",
# ]
# ///
"""Print a command to retrigger the workflow to the GitHub Actions summary.

usage: show-retrigger-command.py [-h] --repo REPO --ref REF --workflow-ref WORKFLOW_REF --inputs INPUTS

Print a command to retrigger the workflow to the GitHub Actions summary.

options:
  -h, --help            show this help message and exit
  --repo REPO           Name of the repository where the workflow was run
  --ref REF             git ref used in the workflow
  --workflow-ref WORKFLOW_REF
                        Value from ${{ github.workflow_ref }}
  --inputs INPUTS       JSON-serialized inputs as they were passed to the workflow
"""

import argparse
import json
import os
import shlex
from dataclasses import dataclass
from pathlib import Path

from yaml import safe_load


@dataclass
class Config:
    repo: str
    workflow_file: str
    inputs: str

    @staticmethod
    def from_args(args: argparse.Namespace) -> "Config":
        return Config(
            repo=args.repo,
            workflow_file=args.workflow_file,
            inputs=args.inputs,
        )

    @property
    def ref(self) -> str:
        # if GITHUB_HEAD_REF is set, it's a PR and the one we want
        if (ref := os.environ.get("GITHUB_HEAD_REF", "")):
            return ref
        # otherwise, GITHUB_HEAD_REF is empty and we want GITHUB_REF_NAME
        return os.environ.get("GITHUB_REF_NAME", "")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a command to retrigger the workflow to the GitHub Actions summary."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Name of the repository where the workflow was run",
    )
    parser.add_argument(
        "--workflow-file", required=True, help="Filename of workflow to be retriggered"
    )
    parser.add_argument(
        "--inputs",
        required=True,
        help="JSON-serialized inputs as they were passed to the workflow",
    )
    return parser.parse_args()


def get_input_names(workflow_file: str) -> list[str]:
    file = Path("./.github/workflows").joinpath(workflow_file)
    with file.open() as f:
        data = safe_load(f)

    # pyyaml uses yaml 1.1 so even 'on' as a map key is parsed as 'True'
    if "workflow_dispatch" not in data[True]:
        raise ValueError(
            f"workflow '{workflow_file}' is not dispatchable - does not contain a 'workflow_dispatch' trigger"
        )

    return data[True]["workflow_dispatch"]["inputs"].keys()


def build_retrigger_command(config: Config, input_names: list[str]) -> str:
    lines: list[str] = [
        f"gh workflow run {config.workflow_file} \\",
        f"    --repo {config.repo} \\",
        f"    --ref {config.ref} \\",
    ]
    for k, v in json.loads(config.inputs).items():
        print(f"{k=} in {input_names=}? {k in input_names=}")
        if k not in input_names:
            continue
        if isinstance(v, bool):
            v = str(v).lower()
        elif len(v) == 0:
            v = '""'
        flag_value = shlex.quote(f"{k}={v}")
        lines.append(f"    -f {flag_value} \\")

    return "\n".join(lines).rstrip(" \\")


def print_retrigger_summary(command: str):
    summary = f"""<details>
<summary>🔄 Retrigger this job</summary>

```bash
{command}
```

</details>
"""
    print(summary)


if __name__ == "__main__":
    args = parse_args()
    config = Config.from_args(args)
    input_names = get_input_names(config.workflow_file)
    print(f"{input_names=}")
    retrigger_command = build_retrigger_command(config=config, input_names=input_names)
    print_retrigger_summary(retrigger_command)
