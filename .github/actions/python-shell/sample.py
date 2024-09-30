import subprocess
from pathlib import Path

print("shell=[default]")
subprocess.run("env")
subprocess.run("env", cwd=Path.cwd())

print("shell=True")
subprocess.run("env", shell=True)
subprocess.run("env", cwd=Path.cwd(), shell=True)
