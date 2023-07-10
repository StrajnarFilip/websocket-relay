from subprocess import run
from sys import executable

run([executable, "-m", "pip", "install", "hatch"])
run([executable, "-m", "pip", "install", "pyproject.toml"])