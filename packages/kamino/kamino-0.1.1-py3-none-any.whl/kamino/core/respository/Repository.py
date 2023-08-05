from __future__ import annotations
from abc import ABC
from dataclasses import dataclass
from typing import List


@dataclass
class Repository(ABC):
  name: str
  parent: Repository = None
  content: str = None

  def get_path(self) -> str:
    return ''

  def get_dirs_list(self) -> List[str]:
    return []

  def is_composite(self) -> bool:
        return False

  def add(self, component: Repository) -> None:
      pass

  def remove(self, component: Repository) -> None:
      pass

