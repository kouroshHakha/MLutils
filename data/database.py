from typing import Type, Sequence, Any, Dict

from collections import OrderedDict
from datetime import datetime

from utils.immutable import combine_hash, to_immutable

T = Type

class Database:
    """
    This is a database of hashable objects. It will keep track of the frequency and uniqueness of
    objects added along with their last modified time stamp.
    check for existence of a design O(1)
    asking for a certain top property O(n)
    asking for a sorted list return O(nlogn)
    insertion new elements O(1)
    """

    def __init__(self, ttype: T, allow_repeat: bool = False):

        # TODO: The following won't work as it is rn.
        # if not isinstance(ttype, Hashable):
        #     raise ValueError('Database only supports hashable objects')

        self._T = ttype
        self._repeat = allow_repeat

        self._freq_dict: OrderedDict[T, int] = OrderedDict()
        self._list: Dict[datetime, T] = {}
        self._rlist: Dict[T, datetime] = {}

    def add(self, dsn: object):
        dt =  datetime.utcnow()
        if not isinstance(dsn, self._T):
            raise ValueError(f'Database of type {self._T.__name__} cannot accept '
                             f'type {dsn.__class__.__name__}')

        if dsn in self._freq_dict:
            if self._repeat:
                self._freq_dict[dsn] += 1
                self._rlist[dsn] = dt
                self._list[dt] = dsn
            else:
                # update time stamp
                old_dt = self._rlist[dsn]
                del self._list[old_dt]
                self._list[dt] = dsn
                self._rlist[dsn] = dt
        else:
            self._rlist[dsn] = dt
            self._list[dt] = dsn
            self._freq_dict[dsn] = 1

    def extend(self, designs: Sequence[object]):
        for dsn in designs:
            self.add(dsn)

    def __len__(self):
        return len(self._list)

    def __contains__(self, item: T):
        return item in self._freq_dict

    def __repr__(self) -> str:
        nb = len(self._list)
        nu = len(self._freq_dict)

        rep = f'Database[{nb} elements ({nu} unique)]\n'

        if nu == 0:
            return rep

        for i, dsn in enumerate(self._freq_dict):
            rep += f'    {dsn},\n'
            if i > 2:
                break

        if nu > 4:
            rep += '    ...\n'
            last_dsn = next(reversed(self._freq_dict.keys()))
            rep += f'    {last_dsn}'

        return rep

    def __hash__(self):
        cur_hash = combine_hash(hash(self._T), hash(to_immutable(self._freq_dict)))
        cur_hash = combine_hash(cur_hash, hash(self._repeat))
        return cur_hash

    def __eq__(self, other):
        return hash(self)== hash(other)

    def __iter__(self):
        return iter(self._list.values())

    def __getitem__(self, item: Any):
        """indexing base in index / time stamp / object [returns time-stamp]"""
        if isinstance(item, int):
            return list(self._list.values())[item]

        if isinstance(item, datetime):
            return self._list[item]

        return self._rlist[item]










