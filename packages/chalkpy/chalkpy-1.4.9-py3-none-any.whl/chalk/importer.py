import importlib.util
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import List

from gitignore_parser import parse_gitignore
from pydantic import BaseModel

from chalk.utils.paths import get_directory_root

_logger = logging.getLogger(__name__)


def py_path_to_module(path: Path, repo_root: Path) -> str:
    p = path.relative_to(repo_root) if path.is_relative_to(repo_root) else path
    return str(p)[: -len(".py")].replace("./", "").replace("/", ".")


class FailedImport(BaseModel):
    filename: str
    module: str
    traceback: str


def import_all_python_files() -> List[FailedImport]:
    project_root = get_directory_root()
    return import_all_python_files_from_dir(project_root=project_root)


def import_all_python_files_from_dir(project_root: Path) -> List[FailedImport]:
    gitignore_path = project_root / ".gitignore"
    chalk_ignore_path = project_root / ".chalkignore"
    matching_functions = []
    if gitignore_path.exists():
        matching_functions.append(parse_gitignore(gitignore_path))

    if chalk_ignore_path.exists():
        matching_functions.append(parse_gitignore(chalk_ignore_path))

    is_relevant = lambda x: all((not match(x) for match in matching_functions))

    cwd = os.getcwd()
    os.chdir(project_root)
    repo_root = Path(project_root)

    # If we don't import both of these, we get in trouble.
    sys.path.append(str(repo_root.resolve()))
    sys.path.append(str(repo_root.parent.resolve()))

    repo_files = sorted({p.resolve() for p in repo_root.glob("**/*.py") if p.is_file()})

    _logger.debug(f"REPO_ROOT: {repo_root.resolve()}")
    # _logger.debug(f"REPO_FILES: {repo_files}")

    venv = os.environ.get("VIRTUAL_ENV")
    module_paths = [
        (py_path_to_module(repo_file, repo_root), repo_file)
        for repo_file in repo_files
        if venv is None or Path(venv) not in repo_file.parents
    ]

    errors: List[FailedImport] = []
    for (module_path, filename) in module_paths:
        if not is_relevant(filename) or module_path.startswith(".eggs") or module_path.startswith("venv"):
            continue

        try:
            importlib.import_module(module_path)
        except Exception:
            filename = filename.resolve()
            # relevant_file = any("from chalk." or "import chalk." in c for c in f)
            # if relevant_file:
            ex_type, ex_value, ex_traceback = sys.exc_info()
            tb = traceback.extract_tb(ex_traceback)
            line = 0
            for i, l in enumerate(tb):
                if filename == Path(l.filename).resolve():
                    line = i
                    break

            relevant_traceback = f"""Exception in module {module_path}:
{os.linesep.join(traceback.format_tb(ex_traceback)[line:])}
\n{ex_type and ex_type.__name__}: {str(ex_value)}
"""
            errors.append(
                FailedImport(
                    traceback=relevant_traceback,
                    filename=str(filename),
                    module=module_path,
                )
            )

            _logger.debug(f"Failed while importing {module_path}", exc_info=True)
            continue

    os.chdir(cwd)
    return errors
