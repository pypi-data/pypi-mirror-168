from fnmatch import fnmatch
import os
from typing import List

from kamino.constants import DEFAULT_RUN_DIR

from .respository.File import File
from .respository.Directory import Directory

def climb(dir_tree: Directory) ->Directory:
  """
    Sobe um diretório na hierarquia de pastas
  """
  if dir_tree.parent is not None:
    return dir_tree.parent
  return dir_tree

def climb_tree(dir_tree: Directory, new_dir_name: str, path: str) ->Directory:
  
  while f"{dir_tree.get_path()}{os.sep}{new_dir_name}" != path:
    dir_tree = climb(dir_tree)
  return dir_tree

def create_file(dirpath: str, filename: str):
  fname = os.path.join(dirpath,filename)

  try:
    with open(fname, encoding="utf-8") as myfile:
      result = File(name=filename, content=myfile.read())
  except:
    with open(fname, 'rb') as myfile:
      result = File(name=filename, content=myfile.read())
  return result

def create_dir(parent_dir: Directory, dir_name: str) -> Directory:
  """
    Cria um diretório e delega um diretório pai a ele.
  """
  new_dir = Directory(name=dir_name)
  parent_dir.add(new_dir)
  return new_dir

def match_patterns(patterns: List[str], to_match: str) -> bool:
  """
    checks if a file matches a unix pattern
  """
  result = False
  for pattern in patterns:
    result = fnmatch(to_match, pattern)
    if result ==True: 
      break
  
  return result

def remove_from_loading(patterns: List[str], items: List[str], dirpath: str):
  for item in items:
    itempath=os.path.join(dirpath, item)
    if match_patterns(patterns, itempath):
      items.remove(item)
  return items


def load_repository(root_dir: str, patterns: List[str]) -> Directory:
  if root_dir == DEFAULT_RUN_DIR:
    root_dir_name = os.path.basename(os.getcwd())
  else:
    root_dir_name = root_dir.split(os.sep)[-1]

  root = Directory(name='.')
  tree_head = root

  for dirpath, dirs, files in os.walk(f"{root_dir}"):	
    dirs_list = dirpath.split(os.sep)
    current_dir = dirs_list[-1]

    if dirpath != f"{root_dir}" and not match_patterns(patterns, dirpath):
      tree_head = climb_tree(tree_head, current_dir, dirpath)
      print(f"Copying dir: {dirpath}")
      tree_head = create_dir(tree_head, current_dir)

    for filename in files:
      if not match_patterns(patterns, os.path.join(dirpath,filename)):
        print(f"Reading: {filename}")
        new_file = create_file(dirpath, filename)
        tree_head.add(new_file)

  root.name = root_dir_name
  return root
