import os
from typing import List
from .Repository import Repository
class File(Repository):
    """
    The Leaf class represents the end objects of a composition. A leaf can't
    have any children.

    Usually, it's the Leaf objects that do the actual work, whereas Composite
    objects only delegate to their sub-components.
    """

    def get_extension(self):
        name_as_list = self.name.split('.')
        return f".{name_as_list[-1]}"

    def get_path(self) -> str :
        if self.parent == None:
            return f"./{self.name}"
        return f"{self.parent.get_path()}{os.sep}{self.name}"

    def get_dirs_list(self) -> List[str]:
        result = self.parent.get_dirs_list()
        result.append(self.name)
        return result
