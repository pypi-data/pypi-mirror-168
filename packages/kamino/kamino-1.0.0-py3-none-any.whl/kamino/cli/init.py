from argparse import _SubParsersAction
import argparse

from kamino.constants import DEFAULT_CONFIG_NAME, DEFAULT_OUT_DIR

def set_init_arguments(parser: argparse.ArgumentParser):
  parser.add_argument("-f", "--filename", type=str, default=DEFAULT_CONFIG_NAME, help="Name of the config file.")
  parser.add_argument("-o", "--outDir", type=str, default=DEFAULT_OUT_DIR, help="Exit directory.")

def add_subparser(
    subparsers: _SubParsersAction
) -> None:
  """
  add all init parsers.

    Args:
      subparsers: subparser we are going to attach to
  """
  init_parser = subparsers.add_parser(
    "init",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    help="Creates an initial json configuration containing 'ignore' and 'tags' keys"
    )
  init_parser.set_defaults(func=init)

  set_init_arguments(init_parser)




def init(args: argparse.Namespace) -> None:
  """
  Creates a new configuration json file

  Args:
    filename: name of the configuration file
    outDir: name of the directory to save the configurations
  """
  from kamino import init_configuration
  init_configuration(args.filename, args.outDir)

