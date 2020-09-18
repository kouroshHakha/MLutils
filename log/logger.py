from typing import Any, Dict

import abc
import yaml
import time
from pathlib import Path

import torch
import torch.nn as nn

class Logger(metaclass=abc.ABCMeta):
    """
    Abstract class for logging
    """

    def __init__(self, directory: str, meta_data: Dict[str, Any] = None) -> None:

        path = Path(directory)
        if path.exists() and not path.is_dir():
            raise NotADirectoryError(f'Path "{directory}" is not a directory')

        if meta_data:
            self._path = path / self._get_name(meta_data)
            self._path.mkdir(parents=True, exist_ok=True)
            self.write_yaml('meta', meta_data)
        else:
            self._path = path
            self._path.mkdir(parents=True, exist_ok=True)


        self._log_text_path = self._path / 'log.txt'
        self._model_index = 0

        with self._log_text_path.open('w') as f:
            pass

    @abc.abstractmethod
    def save_model(self, model: Any) -> None:
        raise NotImplemented

    def print(self, statement: str, *, log=False) -> None:
        print(statement)
        if log:
            self.log(statement, show=False)

    def log(self, statement: str, *, show=True) -> None:
        if show:
            print(statement)
        with open(self._log_text_path, 'a') as f:
            f.write(statement + '\n')

    def write_yaml(self, name: str, data_dict: Dict[str, Any]) -> None:
        path = self._path / f'{name}.yaml'
        with path.open('w') as f:
            yaml.dump(data_dict, f)

    def _get_name(self, meta_data: Dict[str, Any]) -> str:
        return time.strftime("%Y_%m_%d_%H_%M_%S")

    @property
    def path(self):
        return self._path


class TorchLogger(Logger):
    def __init__(self, directory: str, meta_data: Dict[str, Any] = None) -> None:
        Logger.__init__(self, directory, meta_data)

    def save_model(self, model: nn.Module):
        checkpoint_name = f'Model_Checkpoint_{self._model_index}.pt'
        path = self._path / checkpoint_name
        torch.save(model.state_dict(), path)
        self._model_index += 1