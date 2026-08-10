#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
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
import shlex
from dataclasses import dataclass


@dataclass
class Config:
    repo: str
    ref: str
    workflow_file: str
    inputs: str

    @staticmethod
    def from_args(args: argparse.Namespace) -> "Config":
        workflow_file = args.workflow_ref.split("@", maxsplit=1)[0].split("/")[-1]
        return Config(
            repo=args.repo,
            ref=args.ref,
            workflow_file=workflow_file,
            inputs=args.inputs,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Print a command to retrigger the workflow to the GitHub Actions summary."
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="Name of the repository where the workflow was run",
    )
    parser.add_argument("--ref", required=True, help="git ref used in the workflow")
    parser.add_argument(
        "--workflow-ref", required=True, help="Value from ${{ github.workflow_ref }}"
    )
    parser.add_argument(
        "--inputs",
        required=True,
        help="JSON-serialized inputs as they were passed to the workflow",
    )
    return parser.parse_args()


def build_retrigger_command(config: Config) -> str:
    lines: list[str] = [
        f"gh workflow run {config.workflow_file} \\",
        f"    --repo {config.repo} \\",
        f"    --ref {config.ref} \\",
    ]
    for k, v in json.loads(config.inputs).items():
        if isinstance(v, bool):
            v = str(v).lower()
        elif len(v) == 0:
            v = ""
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
    retrigger_command = build_retrigger_command(config)
    print_retrigger_summary(retrigger_command)
