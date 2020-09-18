from typing import Union

from colorama import init
from termcolor import colored
import pprint
from pathlib import Path

class LoggingBase:

    def __init__(self, log_dir: Union[str, Path]) -> None:
        init()
        self.log_txt_fname = Path(log_dir) / 'log.txt'

    def log_text(self, str: str, stream_to_file: bool = True,
                 stream_to_stdout: bool = True, pretty: bool = False,
                 fpath: Union[str, Path] = None):
        if fpath:
            stream = open(fpath, 'a')
        else:
            stream = open(self.log_txt_fname, 'a')

        if pretty:
            printfn = pprint.pprint
        else:
            printfn = print

        if stream_to_file:
            printfn(str, file=stream)
        if stream_to_stdout:
            printfn(str)

        stream.close()

    def log(self, *args, **kwargs):
        return self.log_text(*args, **kwargs)

    def debug(self, str, stream_to_file=True, stream_to_stdout=True, pretty=False, fpath=None):
        msg = colored('[DEBUG] ', 'red') + str
        self.log_text(msg, stream_to_file, stream_to_stdout, pretty, fpath)

    def info(self, str, stream_to_file=True, stream_to_stdout=True, pretty=False, fpath=None):
        msg = colored('[INFO] ', 'green') + str
        self.log_text(msg, stream_to_file, stream_to_stdout, pretty, fpath)


