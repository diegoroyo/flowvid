from ..core.filters.base_filter import Filter
import copy


class FilterableIterator:
    """
        Basic indexing operator (iterates through element [0], [1], etc.)
    """

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
    """
        Base class for inputs and operators.
        Filterable means iterable list of data (from an input or operator)
        where filters can be applied on iterations.
        Filterables should implement the __len__ function and:
        - If a filterable's items can be indexed independently (i.e. element
          number i does not need element i-1 for its calculations) the subclass
          should implement the _getitem function.
        - If not, they should implement their own iterator and call _apply_filters(...)
        Filterables should also implement the get_type function and
        return a string from this list:
        - flo, rgb, rect, point
    """

    def __init__(self):
        self._filters = []

    def __iter__(self):
        return FilterableIterator(self)

    def __len__(self):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")

    def __getitem__(self, index):
        return self._apply_filters(self._getitem(index))

    def assert_type(self, data_type):
        if data_type != self.get_type():
            raise AssertionError('Data type is {d1} but was expected to be {d2}'.format(
                d1=self.get_type(), d2=data_type))
        return True

    def get_type(self):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")

    def _getitem(self, index):
        raise NotImplementedError(
            'Either this is not implemented or you should use an iterator instead')

    def _add_filter(self, new_filter):
        """
            Make a copy of the filterable and add the new filter to it
            so syntax like "flo_norm = fv.normalize_frame(flo_data)" is possible
            :param new_filter: Inherits from Filter
            :returns: Copy of the filterable
        """
        if not isinstance(new_filter, Filter):
            raise AssertionError(
                'new_filter should be a filter and inherit from it')
        other = copy.copy(self)  # shallow copy, links items
        other._filters.append(new_filter)
        return other

    def _apply_filters(self, data):
        for f in self._filters:
            data = f.apply(data)
        return data
