import os
from pathlib import Path


def get_directory_root() -> Path:
    root_dir = Path(os.path.dirname(os.path.abspath("dummy.txt")))
    has_init = lambda p: (p / "__init__.py").exists()
    while has_init(root_dir.parent):
        root_dir = root_dir.parent
    return root_dir.parent if has_init(root_dir) else root_dir
