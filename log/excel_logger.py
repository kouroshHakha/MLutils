from typing import Union, Mapping, Any, Dict, List, Tuple


from pathlib import Path
import pandas as pd
from utils.immutable import ImmutableSortedDict, ImmutableList
from utils.file import read_yaml, write_yaml

class LoggerBase:

    def __init__(self, root_dir: Union[str, Path], fname: str = ''):

        self._root_path = Path(root_dir)

        self.fname = self._root_path / (fname or 'experiments')
        self._cache_fname = self._root_path / 'cache.yaml'

        if not self.fname.suffix:
            self.fname = self.fname.with_suffix('.xlsx')

        self._new_entries: List[Tuple[Mapping[str, Any], Mapping[str, Any]]] = []

    def __contains__(self, item):
        if self._contains_none(item):
            raise ValueError('Entry cannot contain None value, because of hashing issues.')
        cache = self._read_cache()
        return item in cache

    def __getitem__(self, item):
        cache = self._read_cache()
        return cache[item]

    @property
    def root(self) -> str:
        return str(self._root_path)

    def add_entry(self, idx: str, identifier: Mapping[str, Any], results: Mapping[str, Any],
                  **kwargs):
        entry = dict(idx=idx, **identifier, **results, **kwargs)
        self._new_entries.append((entry, identifier))


    def save_records(self):
        # read
        df = self._read_excel()
        cache = self._read_cache()

        # update the records
        for entry, ident in self._new_entries:
            if self._contains_none(ident):
                raise ValueError('Entry cannot contain None value, because of hashing issues.')
            cache.update({ident: entry['idx']})
            df = df.append(entry, ignore_index=True)

        # write back
        df.to_excel(self.fname, na_rep='NaN', float_format='%.6f')
        write_yaml(self._cache_fname, cache)

        # clear memory
        self._new_entries.clear()


    def _read_excel(self) -> pd.DataFrame:
        if self.fname.exists():
            return pd.read_excel(self.fname, index_col=0)
        return pd.DataFrame()

    def _read_cache(self) -> Dict[ImmutableSortedDict, str]:
        if self._cache_fname.exists():
            return read_yaml(self._cache_fname)
        return {}

    def _contains_none(self, obj: object):
        if isinstance(obj, (dict, ImmutableSortedDict)):
            for val in obj.values():
                ans = self._contains_none(val)
                if ans:
                    return ans
            return False
        elif isinstance(obj, (list, tuple, set, ImmutableList)):
            for val in obj:
                ans = self._contains_none(val)
                if ans:
                    return ans
            return False

        return obj is None


