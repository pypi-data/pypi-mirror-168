'''Functionality for length conversion and length equality checks.
Values of two different temperatures recorded in different measurements are considered equal
if the converted values within a relative tolerance or absolute tolerance of float_point_tol.
The default for float_point_tol is 1e-05.
'''

from math import isclose, floor, ceil
from measuring_tools import Measurement

def __dir__():
    return ('Length', 'MARATHON', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__')

class Length(Measurement):
    '''Length Converter for Metric and English Imperial Units'''

    def __init__(self, value: int | float, measurement: str='meter'):
        if not measurement in ('meter', 'kilometer', 'yard', 'mile'):
            raise ValueError('Value must be meter, kilometer, yard, or mile')
        super().__init__(value, measurement)

    def __round__(self, ndigits):
        return Length(round(self.value, ndigits=ndigits), self.measurement)

    def __abs__(self):
        return Length(abs(self.value), self.measurement)

    def __floor__(self):
        return Length(floor(self.value), self.measurement)

    def __ceil__(self):
        return Length(ceil(self.value), self.measurement)

    def __eq__(self, other):
        match self.measurement:
            case 'meter':
                return isclose(self.value, other.to_meter().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'yard':
                return isclose(self.value, other.to_yard().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'mile':
                return isclose(self.value, other.to_mile().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'kilometer':
                return isclose(self.value, other.to_kilometer().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
        
    def __ne__(self, other):
        match self.measurement:
            case 'meter':
                return not self.value == other.to_meter().value
            case 'yard':
                return not self.value == other.to_yard().value
            case 'mile':
                return not self.value == other.to_mile().value
            case 'kilometer':
                return not self.value == other.to_kilometer().value

    def __lt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'meter':
                return self.value < other.to_meter().value
            case 'yard':
                return self.value < other.to_yard().value
            case 'mile':
                return self.value < other.to_mile().value
            case 'kilometer':
                return self.value < other.to_kilometer().value

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'meter':
                return self.value > other.to_meter().value
            case 'yard':
                return self.value > other.to_yard().value
            case 'mile':
                return self.value > other.to_mile().value
            case 'kilometer':
                return self.value > other.to_kilometer().value

    def __ge__(self, other):
        return self == other or self > other

    def __add__(self, other):
        match self.measurement:
            case 'meter':
                total = self.value + other.to_meter().value
            case 'yard':
                total = self.value + other.to_yard().value
            case 'mile':
                total = self.value + other.to_mile().value
            case 'kilometer':
                total = self.value + other.to_kilometer().value
        return Length(total, self.measurement)

    def __sub__(self, other):
        match self.measurement:
            case 'meter':
                diff = self.value - other.to_meter().value
            case 'yard':
                diff = self.value - other.to_yard().value
            case 'mile':
                diff = self.value - other.to_mile().value
            case 'kilometer':
                diff = self.value - other.to_kilometer().value
        return Length(diff, self.measurement)

    def __mul__(self, other):
        match self.measurement:
            case 'meter':
                product = self.value * other.to_meter().value
            case 'yard':
                product = self.value * other.to_yard().value
            case 'mile':
                product = self.value * other.to_mile().value
            case 'kilometer':
                product = self.value * other.to_kilometer().value
        return Length(product, self.measurement)

    def __truediv__(self, other):
        match self.measurement:
            case 'meter':
                result = self.value / other.to_meter().value
            case 'yard':
                result = self.value / other.to_yard().value
            case 'mile':
                result = self.value / other.to_mile().value
            case 'kilometer':
                result = self.value / other.to_kilometer().value
        return Length(result, self.measurement)

    def __floordiv__(self, other):
        match self.measurement:
            case 'meter':
                result = self.value // other.to_meter().value
            case 'yard':
                result = self.value // other.to_yard().value
            case 'mile':
                result = self.value // other.to_mile().value
            case 'kilometer':
                result = self.value // other.to_kilometer().value
        return Length(result, self.measurement)

    def to_meter(self):
        '''Convert the length to meter'''
        measure = 'meter'
        match self.measurement:
            case 'meter':
                return self
            case 'yard':
                return Length((self.value * 0.9144), measurement=measure)
            case 'mile':
                return Length((self.value * 1_609.344), measurement=measure)
            case 'kilometer':
                return Length((self.value * 1_000), measurement=measure)

    def to_yard(self):
        '''Convert the length to yard'''
        measure = 'yard'
        match self.measurement:
            case 'yard':
                return self
            case 'meter':
                return Length((self.value / 0.9144), measurement=measure)
            case 'mile':
                return Length((self.value * 1_760), measurement=measure)
            case 'kilometer':
                return Length((self.value * 1_093.613), measurement=measure)

    def to_mile(self):
        '''Convert the length to mile'''
        measure = 'mile'
        match self.measurement:
            case 'mile':
                return self
            case 'meter':
                return Length((self.value / 1_609.344), measurement=measure)
            case 'yard':
                return Length((self.value / 1_760), measurement=measure)
            case 'kilometer':
                return Length((self.value / 1.609344), measurement=measure)

    def to_kilometer(self):
        '''Convert the length to kilometer'''
        measure = 'kilometer'
        match self.measurement:
            case 'kilometer':
                return self
            case 'meter':
                return Length((self.value / 1_000), measurement=measure)
            case 'yard':
                return Length((self.value / 1_093.613), measurement=measure)
            case 'mile':
                return Length((self.value * 1.609344 ), measurement=measure)

MARATHON = Length(42.195, measurement='kilometer')