class Filter:
    def __init__(self):
        self._next_filter = None

    def then(self, next_filter):
        # if not issubclass(next_filter, Filter):
        #     raise AssertionError('Cannot concatenate a filter with a non-filter')
        # _next_filter = next_filter
        # return self
        # TODO
        pass

    def apply(self, data):
        if self._next_filter is None:
            return data
        else:
            return self._next_filter.apply(data)