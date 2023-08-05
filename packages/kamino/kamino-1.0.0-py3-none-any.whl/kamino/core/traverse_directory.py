import encodings
import os
from abc import ABC
import locale
from typing import Dict

from kamino.constants import DEFAULT_OUT_DIR

from .replace_tags import replace_tags

from .respository.Directory import Directory
from .respository.File import File
from .respository.Repository import Repository


class TraverseDirectory(ABC):

  def traverse_repository(self, repository: Directory):

    for repository_item in repository._children:
      if type(repository_item) == Directory:
        self.before_enter_recursion(repository_item)
        self.traverse_repository(repository_item)
        self.after_exit_recursion(repository_item)
      self.finalize_traverse_hook(repository_item)

  def before_enter_recursion(self, repository_item):
    ...

  def after_exit_recursion(self, repository_item):
    ...
  
  def finalize_traverse_hook(self, repository_item):
    ...


class CreateRepository(TraverseDirectory):

  def create_repository(self, repository_item: Directory, out: str, repo_name: str = None):
    out_dir = Directory(out)
    if repo_name is not None:
      repository_item.name = repo_name

    out_dir.add(repository_item)

    self.create_dir(out_dir)
    self.traverse_repository(out_dir)

  def before_enter_recursion(self, repository_item: Directory):
    self.create_dir(repository_item)

  def finalize_traverse_hook(self, repository_item: Repository):
    if type(repository_item) == File:
      self.create_file(repository_item)

  def create_file(self, file: File):
    mode_encoding = ('wb', None) if type(file.content) is bytes else ('w', 'utf-8')
    with open(file.get_path(), mode_encoding[0], encoding=mode_encoding[1]) as new_file:
      new_file.write(file.content)

  def create_dir(self, dir: Directory): 
    if not os.path.exists(dir.get_path()):
      os.makedirs(dir.get_path())


class ReplaceAllTags(TraverseDirectory):

  def __init__(self, patterns: Dict) -> None:
    self.patterns = patterns
    self.ignore_extensions = [".pdf", ".jpg", ".jpeg", ".svg", ".ico", ".png", ".jar", ".keystore", ".bat", ".exe", '.ttf']
    super().__init__()

  def finalize_traverse_hook(self, repository_item: Repository):
    if type(repository_item) == File:
      if repository_item.get_extension() not in self.ignore_extensions:
        print(f"Replacing tags in {repository_item.get_path()}")
        repository_item.content = replace_tags(repository_item.content, self.patterns)