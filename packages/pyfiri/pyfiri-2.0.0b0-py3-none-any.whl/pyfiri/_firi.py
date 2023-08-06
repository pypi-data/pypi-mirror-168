import xarray as _xr
import os as _os


class _firi2018:
    data = None
    data_extrapolated = None

    @staticmethod
    def get_data():
        if _firi2018.data is None:
            _firi2018.data = _get_firi2018_dataarray()
        return _firi2018.data.copy(deep=True)

    @staticmethod
    def get_data_extrapolated():
        if _firi2018.data_extrapolated is None:
            _firi2018.data_extrapolated = _get_firi2018_dataarray(extrapolated=True)
        return _firi2018.data_extrapolated.copy(deep=True)


def _get_firi2018_dataarray(extrapolated=False):
    data_file = "firi2018ed3.nc" if extrapolated == False else "firi2018p182_5v1.nc"
    _path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__))
                          , "_ext", "_data", data_file)
    return _xr.load_dataarray(_path)
