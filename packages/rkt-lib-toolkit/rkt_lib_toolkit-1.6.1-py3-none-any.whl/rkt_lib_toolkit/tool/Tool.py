import os
from typing import Optional


class Singleton(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Tool:

    @staticmethod
    def formatted_from_os(path) -> str:
        if os.name == "nt":
            sep = "\\"
            res = f'{path.replace("/", sep)}{sep if path[-1] != sep else ""}'
        else:
            res = f'{path}{"/" if path[-1] != "/" else ""}'

        return res

    def get_cwd(self) -> str:
        return self.formatted_from_os(os.getcwd())

    def get_dir(self, folder, root: Optional[str] = None) -> Optional[str]:
        root = self.get_cwd() if not root else self.formatted_from_os(root)

        for element in os.listdir(root):
            if os.path.isdir(f"{root}{element}") and element == folder:
                return self.formatted_from_os(f"{root}{element}")

        for element in os.listdir(root):
            if os.path.isdir(f"{root}{element}"):
                found = self.get_dir(folder, self.formatted_from_os(f"{root}{element}"))
                if found:
                    return found

        return None
