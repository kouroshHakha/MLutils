from typing import Any, Union

from pathlib import Path

from ruamel.yaml import YAML

yaml = YAML(typ='unsafe')

def read_yaml(fname: Union[str, Path]) -> Any:
    """Read the given file using YAML.

    Parameters
    ----------
    fname : str
        the file name.

    Returns
    -------
    content : Any
        the object returned by YAML.
    """
    with open(fname, 'r') as f:
        content = yaml.load(f)

    return content

def write_yaml(fname: Union[str, Path], obj: object, mkdir: bool = True) -> None:
    """Writes the given object to a file using YAML format.

    Parameters
    ----------
    fname : Union[str, Path]
        the file name.
    obj : object
        the object to write.
    mkdir : bool
        If True, will create parent directories if they don't exist.

    Returns
    -------
    content : Any
        the object returned by YAML.
    """
    if isinstance(fname, str):
        fpath = Path(fname)
    else:
        fpath = fname

    if mkdir:
        fpath.parent.mkdir(parents=True, exist_ok=True)

    with open(fpath, 'w') as f:
        yaml.dump(obj, f)

def get_full_name(name: str, prefix: str = '', suffix: str = ''):
    """Returns a full name given a base name and prefix and suffix extensions

    Parameters
    ----------
    name: str
        the base name.
    prefix: str
        the prefix (default='')
    suffix
        the suffix (default='')

    Returns
    -------
    full_name: str
        the fullname
    """
    if prefix:
        name = f'{prefix}_{name}'
    if suffix:
        name = f'{name}_{suffix}'
    return name