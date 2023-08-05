from .respository import Directory
from .traverse_directory import CreateRepository


def save_repository(repository: Directory, path: str = '.', repo_name: str = None):
  """
    Salva a arvore de diretórios no caminho especificado.
  """
  creator = CreateRepository()
  creator.create_repository(repository, path, repo_name)

