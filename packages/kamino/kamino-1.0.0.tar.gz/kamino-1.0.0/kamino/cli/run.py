from kamino import load_repository, save_repository
from kamino.constants import DEFAULT_CONFIG_FILE, DEFAULT_CONFIG_NAME
from ..core.traverse_directory import ReplaceAllTags
from ..core.load_configuration import load_configuration
from . import *

def set_run_arguments(parser: argparse.ArgumentParser):
  parser.add_argument(
    "-d",
    "--directory",
    type=str,
    default='.',
    help="Directory of where kamino must execute the replication."
  )

  parser.add_argument(
    "-c",
    "--config",
    type=str,
    default=DEFAULT_CONFIG_FILE,
    help="Path to the configuration file that kamino should use to replicate."
  )
  parser.add_argument(
    "-o",
    "--out",
    type=str,
    default='./kamino',
    help="Directory of where kamino should send the replication result."
  )

def add_subparser(subparsers: SubParsersAction):
  run_parser = subparsers.add_parser(
  "run",
  formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  help="Executes kamino's replication."
  )
  run_parser.set_defaults(func=run)

  set_run_arguments(run_parser)

def run(args: argparse.Namespace):
  """
  1. verifica se há um arquivo de config
    - caso não haja arquivo especificado, usar padrão
    - caso haja arquivo especificado, usar o mesmo
  2. validar arquivo de config
  3. carrega o arquivo de config com base no argumento
  4. carrega repositório
    - se configuracao possuir ignore patterns, não carregar diretórios/arquivos que se encaixam nos patterns
  5. executa troca de tags por seus valores
  6. salva novo repositório no caminho especificado
    - se não houver caminho especificado, usar saída padrão './out'
    - se houver caminho de saída especificado, usar saída especificada
  """
  print("loading configurations...")
  configurations = load_configuration(args.config)
  print("configurations loaded.")

  print("loading repository...")
  repository = load_repository(args.directory, configurations['ignore'])
  print("repository loaded.")

  replacer = ReplaceAllTags(configurations['tags'])
  replacer.traverse_repository(repository)
  print("Saving repository")
  save_repository(repository, args.out, configurations['project']['name'])
  print("Repository Replication concluded!!!")