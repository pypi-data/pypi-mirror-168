'''Provides a check for a Python version greater than or equal to 3.10.
Provides the Measurement base class.
'''

import platform

if int(platform.python_version_tuple()[1]) < 10:
    raise ImportError('measuring-tools requires Python versions 3.10 or later.')
del platform

class Measurement:
    '''Base Class for other measurments'''

    float_point_tol = 1e-05

    def __init__(self, value: int | float, measurement: str):
        self.value = value
        self.measurement = measurement

    def __repr__(self):
        return f'{self.__class__.__name__}(value={self.value}, measurement={self.measurement!r})'

    def __str__(self):
        return f'{self.value} {self.measurement}(s)'

    def __int__(self):
        return int(self.value)

    def __float__(self):
        return float(self.value)

    def __iadd__(self, other_value):
        self.value += other_value
        return self

    def __isub__(self, other_value):
        self.value -= other_value
        return self

    def __imul__(self, other_value):
        self.value *= other_value
        return self

    def __itruediv__(self, other_value):
        self.value /= other_value
        return self

    def __ifloordiv__(self, other_value):
        self.value //= other_value
        return self