import argparse
import os
import sys

from kamino.cli import (
  init,
  run
)


def create_argument_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    prog="kamino",
    description="An easy repository replication tool"
  )

  subparsers = parser.add_subparsers(help="kamino commands")
  init.add_subparser(subparsers)
  run.add_subparser(subparsers)

  return parser

def main():
  arg_parser = create_argument_parser()
  cmdline_arguments = arg_parser.parse_args()

  # insert current path in syspath so custom modules are found
  sys.path.insert(1, os.getcwd())
  try:
    if hasattr(cmdline_arguments, "func"):
        cmdline_arguments.func(cmdline_arguments)
  except Exception as e:
    print(e)

if __name__ == "__main__":
  main()