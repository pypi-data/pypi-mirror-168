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
    is_file_ignored: Optional[Callable[[str], bool]] = None,
) -> None:
    if not is_file_ignored:
        # if no callback handler present assume that every file needs to be added
        is_file_ignored = lambda *_: False

    with tarfile.open(output_filename, "w:gz") as tar:
        _add_files_in_tar(
            is_file_ignored=is_file_ignored,
            source_dir=source_dir,
            tar=tar,
        )
        for additional_directory in additional_directories:
            _add_files_in_tar(
                is_file_ignored=is_file_ignored,
                source_dir=additional_directory,
                tar=tar,
            )


def _add_files_in_tar(
    is_file_ignored: Callable[[str], bool],
    source_dir: str,
    tar: TarFile,
) -> None:
    for root, _, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_file_ignored(file_path):
                tar.add(file_path, arcname=file_path)
            else:
                logger.debug("Ignoring %s", file_path)
