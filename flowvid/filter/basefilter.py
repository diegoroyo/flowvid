class Filter:
    def __init__(self):
        self._next_filter = None

    def set_next(self, next_filter):
        if self._next_filter is None:
            self._next_filter = next_filter
        else:
            self._next_filter.set_next(next_filter)

    def apply(self, data):
        if self._next_filter is None:
            return data
        else:
            return self._next_filter.apply(data)