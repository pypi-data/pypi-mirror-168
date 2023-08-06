from pathlib import Path
from typing import Union
from zipfile import ZipFile


def parse_bfx_file_type(filepath: Union[str, Path], from_dir: bool = True):
    """Returns bioinformatics file type by parsing its path.

    Args:
        filepath (Union[str,Path]): Path to the file to be parsed.
        from_dir (bool): If True, parses bfx file type based on the file's
        directory (versus the file name).

    Returns:
        str: String with the identified file type.
    """
    filepath = Path(filepath)
    if from_dir:
        dirpath = filepath.parent.resolve()
        file_type = str(dirpath).split("/")[-1]
        return file_type
    else:
        if any(i in {".gz"} for i in filepath.suffixes):
            return filepath.suffixes[0]
        else:
            return filepath.suffix


def get_bfx_files_from_dir(dirpath: Union[str, Path]) -> list:
    """Parses dir and returns files that can be mapped to a bioinformatics file type.

    Args:
        dirpath (Union[str,Path]): Path to dir.

    Returns:
        list: List with bioinformatics file paths.
    """
    dirpath = Path(dirpath)

    if dirpath.suffix == ".zip":
        with ZipFile(dirpath, "r") as zipObj:
            filelist = zipObj.namelist()
            return [file for file in filelist if not file.endswith("/")]
    bfx_files_in_dir = [
        file.as_posix() for file in dirpath.rglob("*") if file.is_file()
    ]

    return bfx_files_in_dir
