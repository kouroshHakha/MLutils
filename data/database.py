from typing import Sequence, Any, Dict, TypeVar, Iterable, Generic

from collections import OrderedDict
from sortedcollections import SortedList
from datetime import datetime
from copy import copy

from utils.immutable import to_immutable

T = TypeVar('T')

class Database(Generic[T]):
    """
    This is a database of hashable objects. It will keep track of the frequency and uniqueness of
    objects added along with their last modification time stamp.
    check for existence of a design O(1)
    asking for a certain top property O(1)
    asking for a sorted list return O(1)
    insertion new elements O(1) / O(nlogn)
    """

    def __init__(self, keep_sorted_list_of: Iterable[str] = None):

        self._freq_dict: OrderedDict[T, int] = OrderedDict()
        self._list: Dict[datetime, T] = {}
        self._rlist: Dict[T, datetime] = {}
        self._tot_freq = 0

        self.sorted_lists = {}
        if keep_sorted_list_of:
            for key in keep_sorted_list_of:
                self.sorted_lists[key] = SortedList(key=lambda x: x[key])

    def add(self, dsn: T):
        dt =  datetime.utcnow()
        # if not isinstance(dsn, self._T):
        #     raise ValueError(f'Database of type {self._T.__name__} cannot accept '
        #                      f'type {dsn.__class__.__name__}')

        if dsn in self._freq_dict:
            self._freq_dict[dsn] += 1
            self._rlist[dsn] = dt
            self._list[dt] = dsn
        else:
            self._rlist[dsn] = dt
            self._list[dt] = dsn
            self._freq_dict[dsn] = 1
            if self.sorted_lists:
                for key in self.sorted_lists:
                    self.sorted_lists[key].add(dsn)

        self._tot_freq += 1

    def __copy__(self):
        # this method does not recreate the design instances.
        copied = self.__class__()
        copied._freq_dict = copy(self._freq_dict)
        copied._list = copy(self._list)
        copied._rlist = copy(self._rlist)
        copied._tot_freq = copy(self._tot_freq)
        copied.sorted_lists = dict([(k, copy(v)) for k, v in self.sorted_lists.items()])
        return copied

    def extend(self, designs: Sequence[T]):
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
            rep += f'    {repr(dsn)},\n'
            if i > 2:
                break

        if nu > 4:
            rep += '    ...\n'
            last_dsn = next(reversed(self._freq_dict.keys()))
            rep += f'    {repr(last_dsn)}'

        return rep

    def __hash__(self):
        return hash(to_immutable(self._freq_dict))

    def __eq__(self, other):
        if hash(self) != hash(other):
            return False
        # hash collision
        for obj in self:
            if obj not in other:
                return False
        return True

    def __iter__(self):
        return iter(self._rlist.keys())

    def __getitem__(self, item: Any):
        """indexing base in index / time stamp / object [returns time-stamp]"""
        if isinstance(item, int):
            return list(self._list.values())[item]

        if isinstance(item, datetime):
            return self._list[item]

        return self._rlist[item]

    @property
    def tot_freq(self):
        return self._tot_freq

    @property
    def n_unique(self):
        return len(self._freq_dict)

    def picklable(self):
        return PicklableDataBase.create_from_database(self)


class PicklableDataBase(Generic[T]):

    def __init__(self, keep_sorted_list_of: Iterable[str] = None):
        self._freq_dict: Dict[T, int] = {}
        self._list: Dict[datetime, T] = {}
        self._rlist: Dict[T, datetime] = {}
        self._tot_freq = 0

        self.sorted_lists = {}
        if keep_sorted_list_of:
            for key in keep_sorted_list_of:
                self.sorted_lists[key] = []

    @classmethod
    def create_from_database(cls, db: Database):
        inst = cls(db.sorted_lists.keys())
        inst._freq_dict = dict(db._freq_dict)
        inst._list = dict(db._list)
        inst._rlist = dict(db._rlist)
        inst._tot_freq = db._tot_freq
        for key in db.sorted_lists:
            inst.sorted_lists[key] = list(db.sorted_lists[key])

        return inst

    def convert_to_database(self):
        db = Database(self.sorted_lists.keys())
        db._freq_dict  = OrderedDict(self._freq_dict)
        db._list  = self._list
        db._rlist  = self._rlist
        db._tot_freq = self._tot_freq

        for k, v in self.sorted_lists.items():
            db.sorted_lists[k].update(v)

        return db






