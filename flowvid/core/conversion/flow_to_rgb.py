import numpy as np
from ..filterable import Filterable
from ..util.color_flow import flow_to_rgb

# All this code is adapted from the one available at:
# https://people.csail.mit.edu/celiu/OpticalFlow/
# which uses the following color circle idea:
# http://www.quadibloc.com/other/colint.htm


class FlowToRGB(Filterable):
    """
        Convert Flow data into RGB data using this color circle:
        http://www.quadibloc.com/other/colint.htm
    """

    def __init__(self, flo_data):
        Filterable.__init__(self)
        if not isinstance(flo_data, Filterable):
            raise AssertionError('flo_data should contain a list of flo data')
        flo_data.assert_type('flo')

        self._flo_data = flo_data

    def _items(self):
        return (flow_to_rgb(flo) for flo in self._flo_data)

    def __len__(self):
        return len(self._flo_data)

    def get_type(self):
        return 'rgb'
