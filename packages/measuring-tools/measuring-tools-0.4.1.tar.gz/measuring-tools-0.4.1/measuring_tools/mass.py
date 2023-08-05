'''Functionality for mass conversion and mass equality checks.
Values of two different temperatures recorded in different measurements are considered equal
if the converted values within a relative tolerance or absolute tolerance of float_point_tol.
The default for float_point_tol is 1e-05.
'''

from math import isclose, floor, ceil
from measuring_tools import Measurement

def __dir__():
    return ('Mass', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__')

class Mass(Measurement):
    '''Mass Converter class'''

    def __init__(self, value: int | float, measurement: str='gram'):
        if not measurement in ('gram', 'kilogram', 'ton_us', 'pound'):
            raise ValueError('Value must be gram, kilogram, ton_us, or pound')
        super().__init__(value, measurement)

    def __round__(self, ndigits):
        return Mass(round(self.value, ndigits=ndigits), self.measurement)

    def __abs__(self):
        return Mass(abs(self.value), self.measurement)

    def __floor__(self):
        return Mass(floor(self.value), self.measurement)

    def __ceil__(self):
        return Mass(ceil(self.value), self.measurement)

    def __eq__(self, other):
        match self.measurement:
            case 'gram':
                return isclose(self.value, other.to_gram().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'ton_us':
                return isclose(self.value, other.to_ton_us().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'pound':
                return isclose(self.value, other.to_pound().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
            case 'kilogram':
                return isclose(self.value, other.to_kilogram().value, rel_tol=self.float_point_tol, abs_tol=self.float_point_tol)
        
    def __ne__(self, other):
        match self.measurement:
            case 'gram':
                return not self.value == other.to_gram().value
            case 'ton_us':
                return not self.value == other.to_ton_us().value
            case 'pound':
                return not self.value == other.to_pound().value
            case 'kilogram':
                return not self.value == other.to_kilogram().value

    def __lt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'gram':
                return self.value < other.to_gram().value
            case 'ton_us':
                return self.value < other.to_ton_us().value
            case 'pound':
                return self.value < other.to_pound().value
            case 'kilogram':
                return self.value < other.to_kilogram().value

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if self == other:
            return False
        match self.measurement:
            case 'gram':
                return self.value > other.to_gram().value
            case 'ton_us':
                return self.value > other.to_ton_us().value
            case 'pound':
                return self.value > other.to_pound().value
            case 'kilogram':
                return self.value > other.to_kilogram().value

    def __ge__(self, other):
        return self == other or self > other

    def __add__(self, other):
        match self.measurement:
            case 'gram':
                total = self.value + other.to_gram().value
            case 'ton_us':
                total = self.value + other.to_ton_us().value
            case 'pound':
                total = self.value + other.to_pound().value
            case 'kilogram':
                total = self.value + other.to_kilogram().value
        return Mass(total, self.measurement)

    def __sub__(self, other):
        match self.measurement:
            case 'gram':
                diff = self.value - other.to_gram().value
            case 'ton_us':
                diff = self.value - other.to_ton_us().value
            case 'pound':
                diff = self.value - other.to_pound().value
            case 'kilogram':
                diff = self.value - other.to_kilogram().value
        return Mass(diff, self.measurement)

    def __mul__(self, other):
        match self.measurement:
            case 'gram':
                product = self.value * other.to_gram().value
            case 'ton_us':
                product = self.value * other.to_ton_us().value
            case 'pound':
                product = self.value * other.to_pound().value
            case 'kilogram':
                product = self.value * other.to_kilogram().value
        return Mass(product, self.measurement)

    def __truediv__(self, other):
        match self.measurement:
            case 'gram':
                result = self.value / other.to_gram().value
            case 'ton_us':
                result = self.value / other.to_ton_us().value
            case 'pound':
                result = self.value / other.to_pound().value
            case 'kilogram':
                result = self.value / other.to_kilogram().value
        return Mass(result, self.measurement)

    def __floordiv__(self, other):
        match self.measurement:
            case 'gram':
                result = self.value // other.to_gram().value
            case 'ton_us':
                result = self.value // other.to_ton_us().value
            case 'pound':
                result = self.value // other.to_pound().value
            case 'kilogram':
                result = self.value // other.to_kilogram().value
        return Mass(result, self.measurement)

    def to_gram(self):
            '''Convert the length to gram'''
            measure = 'gram'
            match self.measurement:
                case 'gram':
                    return self
                case 'ton_us':
                    return Mass((self.value / 907_184.74) , measurement=measure)
                case 'pound':
                    return Mass((self.value / 453.59237) , measurement=measure)
                case 'kilogram':
                    return Mass((self.value / 1_000) , measurement=measure)

    def to_ton_us(self):
        '''Convert the length to ton_us'''
        measure = 'ton_us'
        match self.measurement:
            case 'ton_us':
                return self
            case 'gram':
                return Mass((self.value * 907_184.74) , measurement=measure)
            case 'pound':
                return Mass((self.value * 2_000) , measurement=measure)
            case 'kilogram':
                return Mass((self.value * 907.18474) , measurement=measure)

    def to_pound(self):
        '''Convert the length to pound'''
        measure = 'pound'
        match self.measurement:
            case 'pound':
                return self
            case 'gram':
                return Mass((self.value * 453.59237) , measurement=measure)
            case 'ton_us':
                return Mass((self.value / 2_000) , measurement=measure)
            case 'kilogram':
                return Mass((self.value / 2.2046226218) , measurement=measure)

    def to_kilogram(self):
        '''Convert the length to kilogram'''
        measure = 'kilogram'
        match self.measurement:
            case 'kilogram':
                return self
            case 'gram':
                return Mass((self.value * 1_000), measurement=measure)
            case 'ton_us':
                return Mass((self.value / 907.18474) , measurement=measure)
            case 'pound':
                return Mass((self.value * 2.2046226218) , measurement=measure)