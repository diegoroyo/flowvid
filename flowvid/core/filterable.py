from ..core.filters.base_filter import Filter
import copy


class Filterable:
    """
        Base class for inputs and operators.
        Filterable means iterable list of data (from an input or operator)
          where filters can be applied on iterations.
        Filterables should implement the following:
        - _items
        - __len__
        - get_type, which should return a string from this list:
            * flo, rgb, rect, point, epe, figure
        Optionally, it can also implement the __getitem__ function
          if the elements can be indexed
    """

    def __init__(self):
        self._filters = []

    def __iter__(self):
        return (self._apply_filters(item) for item in self._items())

    def _items(self):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")

    def __len__(self):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")

    def get_type(self):
        raise NotImplementedError("Whoops. Contact the owner of the repo.")

    def __getitem__(self, index):
        raise TypeError("'{s}' object can't be indexed, use an iterator instead".format(
            s=self.__class__.__name__))

    def assert_type(self, *args):
        if self.get_type() not in args:
            raise AssertionError('Data type is {d1} but was expected to be one of: {d2}'.format(
                d1=self.get_type(), d2=' '.join(args)))
        return True

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
        other = copy.deepcopy(self)
        other._filters.append(new_filter)
        return other

    def _apply_filters(self, data):
        for f in self._filters:
            data = f.apply(data)
        return data
