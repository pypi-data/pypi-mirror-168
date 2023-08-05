'''Functionality for volume conversion and volume equality checks.
Values of two different temperatures recorded in different measurements are considered equal
if the converted values within a relative tolerance or absolute tolerance of float_point_tol.
The default for float_point_tol is 1e-05.
'''

from math import isclose, floor, ceil
from measuring_tools import Measurement

def __dir__():
    return ('Volume', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__')

class Volume(Measurement):
    '''Volume class comparing and converting Metric, British Imperial Units, and US Units'''

    def __init__(self, value: int | float, measurement: str='liter'):
        if not measurement in ('liter', 'gallon', 'gallon_us'):
            raise ValueError('Value must be liter, gallon, gallon_us')
        super().__init__(value, measurement)

    def __round__(self, ndigits):
        return Volume(round(self.value, ndigits=ndigits), self.measurement)

    def __abs__(self):
        return Volume(abs(self.value), self.measurement)

    def __floor__(self):
        return Volume(floor(self.value), self.measurement)

    def __ceil__(self):
        return Volume(ceil(self.value), self.measurement)

    def __eq__(self, other):
        match self.measurement:
            case 'liter':
                return isclose(self.value, other.to_liter().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'gallon':
                return isclose(self.value, other.to_gallon().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'gallon_us':
                return isclose(self.value, other.to_gallon_us().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)

    def __ne__(self, other):
        match self.measurement:
            case 'liter':
                return not self.value == other.to_liter().value
            case 'gallon':
                return not self.value == other.to_gallon().value
            case 'gallon_us':
                return not self.value == other.to_gallon_us().value

    def __lt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'liter':
                return self.value < other.to_liter().value
            case 'gallon':
                return self.value < other.to_gallon().value
            case 'gallon_us':
                return self.value < other.to_gallon_us().value

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if self == other: return False
        match self.measurement:
            case 'liter':
                return self.value > other.to_liter().value
            case 'gallon':
                return self.value > other.to_gallon().value
            case 'gallon_us':
                return self.value > other.to_gallon_us().value

    def __ge__(self, other):
        return self == other or self > other

    def __add__(self, other):
        match self.measurement:
            case 'liter':
                total = self.value + other.to_liter().value
            case 'gallon':
                total = self.value + other.to_gallon().value
            case 'gallon_us':
                total = self.value + other.to_gallon_us().value
        return Volume(total, self.measurement)

    def __sub__(self, other):
        match self.measurement:
            case 'liter':
                diff = self.value - other.to_liter().value
            case 'gallon':
                diff = self.value - other.to_gallon().value
            case 'gallon_us':
                diff = self.value - other.to_gallon_us().value
        return Volume(diff, self.measurement)

    def __mul__(self, other):
        match self.measurement:
            case 'liter':
                product = self.value * other.to_liter().value
            case 'gallon':
                product = self.value * other.to_gallon().value
            case 'gallon_us':
                product = self.value * other.to_gallon_us().value
        return Volume(product, self.measurement)

    def __truediv__(self, other):
        match self.measurement:
            case 'liter':
                result = self.value / other.to_liter().value
            case 'gallon':
                result = self.value / other.to_gallon().value
            case 'gallon_us':
                result = self.value / other.to_gallon_us().value
        return Volume(result, self.measurement)

    def __floordiv__(self, other):
        match self.measurement:
            case 'liter':
                result = self.value // other.to_liter().value
            case 'gallon':
                result = self.value // other.to_gallon().value
            case 'gallon_us':
                result = self.value // other.to_gallon_us().value
        return Volume(result, self.measurement)

    def to_liter(self):
        '''Convert the volume to liter'''
        measure = 'liter'
        match self.measurement:
            case 'liter':
                return self
            case 'gallon':
                return Volume((self.value * 4.54609513), measurement=measure)
            case 'gallon_us':
                return Volume((self.value * 3.78541178), measurement=measure)

    def to_gallon(self):
        '''Convert the volume to British Imperial Gallons'''
        measure = 'gallon'
        match self.measurement:
            case 'gallon':
                return self
            case 'liter':
                return Volume((self.value * 0.219969157), measurement=measure)
            case 'gallon_us':
                return Volume((self.value * 0.8326741846), measurement=measure)

    def to_gallon_us(self):
        '''Convert the volume to US Gallons'''
        measure = 'gallon_us'
        match self.measurement:
            case 'gallon_us':
                return self
            case 'liter':
                return Volume((self.value * 0.264172052), measurement=measure)
            case 'gallon':
                return Volume((self.value * 1.200949925), measurement=measure)
