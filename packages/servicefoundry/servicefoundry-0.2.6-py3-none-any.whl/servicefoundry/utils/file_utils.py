import os
import tarfile
from tarfile import TarFile
from typing import Callable, List, Optional

from servicefoundry.logger import logger


def make_executable(file_path):
    mode = os.stat(file_path).st_mode
    mode |= (mode & 0o444) >> 2
    os.chmod(file_path, mode)


def create_file_from_content(file_path, content, executable=False):
    with open(file_path, "w") as text_file:
        text_file.write(content)
    if executable:
        make_executable(file_path)


def make_tarfile(
    output_filename: str,
    source_dir: str,
    additional_directories: List[str],
    is_path_ignored: Optional[Callable[[str], bool]] = None,
) -> None:
    if not is_path_ignored:
        # if no callback handler present assume that every file needs to be added
        is_path_ignored = lambda *_: False

    with tarfile.open(output_filename, "w:gz") as tar:
        _add_files_in_tar(
            is_path_ignored=is_path_ignored,
            source_dir=source_dir,
            tar=tar,
        )
        for additional_directory in additional_directories:
            _add_files_in_tar(
                is_path_ignored=is_path_ignored,
                source_dir=additional_directory,
                tar=tar,
            )


def _add_files_in_tar(
    is_path_ignored: Callable[[str], bool],
    source_dir: str,
    tar: TarFile,
) -> None:
    for root, dirs, files in os.walk(source_dir, topdown=True):
        if is_path_ignored(root):
            logger.debug("Ignoring directory %s", root)

            # NOTE: we can safely ignore going through the sub-dir
            # if root itself is excluded.
            dirs.clear()
            continue
        logger.debug("Adding contents of the directory %s", root)
        for file in files:
            file_path = os.path.join(root, file)
            if not is_path_ignored(file_path):
                arcname = os.path.relpath(file_path, source_dir)
                tar.add(file_path, arcname=arcname)
                logger.debug("Adding %s with arcname %r", file_path, arcname)
            else:
                logger.debug("Ignoring %s", file_path)
