# from flowvid.core.filters.basefilter import Filter
import copy


class FilterableIterator:
    def __init__(self, obj):
        self._index = -1
        self._max = len(obj)
        self._obj = obj

    def __next__(self):
        self._index = self._index + 1
        if self._index == self._max:
            raise StopIteration
        return self._obj[self._index]


class Filterable:
    def __init__(self):
        self._filters = []

    def __iter__(self):
        return FilterableIterator(self)

    def __len__(self):
        raise NotImplementedError

    def __getitem__(self, index):
        return self._apply_filters(self._getitem(index))

    def _getitem(self, index):
        raise NotImplementedError

    def _add_filter(self, new_filter):
        # if not issubclass(new_filter, Filter):
        #     raise AssertionError('TODO')
        other = copy.copy(self)
        other._filters.append(new_filter)
        return other

    def _apply_filters(self, data):
        for f in self._filters:
            data = f.apply(data)
        return data
