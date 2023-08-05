from __future__ import annotations

import os
from typing import List
from .Repository import Repository
from dataclasses import dataclass, field

@dataclass
class Directory(Repository):
    """
    Composite class que representa um diretório. O diretório pode conter vários filhos
    sendo eles outros diretórios ou arquivos.
    """
    _children: List[Repository] = field(default_factory=lambda : [])


    def add(self, component: Repository) -> None:
        """
        Um objeto composite pode adicionar ou remover outros componentes.
        """
        self._children.append(component)
        component.parent = self

    def remove(self, component: Repository) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def get_path(self) -> str:
        if self.parent != None:
            return f"{self.parent.get_path()}{os.sep}{self.name}"
        return f"{self.name}"

    def get_dirs_list(self) -> List[str]:
        if self.parent != None:
            result = self.parent.get_dirs_list()
            result.append(self.name)
            return result 
        return [f"{self.name}"]
