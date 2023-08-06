from abc import abstractmethod, ABCMeta
from scipy.constants import convert_temperature
from currency_converter import CurrencyConverter, ECB_URL
import datetime


def ensure_unit_comparator(comparation):
    def comparation_wrapper(a,b):
        if not isinstance(a, q):
            a = I(a)
        if not isinstance(b, q):
            b = I(b)

        if a.unit is not None:
            b = b @ a.unit

        elif b.unit is not None:
            a = a @ b.unit
            
        return comparation(a,b)
    
    return comparation_wrapper

def ensure_unit_operator(operation):
    def operation_wrapper(a, b, *args, **kwargs):
        if a.unit is not None:
            b = b @ a.unit
            qty = type(a)
            unit = a.unit

        elif b.unit is not None:
            a = a @ b.unit
            qty = type(b)
            unit = b.unit
            
        return qty(
            operation(a, b, *args, **kwargs),
            unit=unit
        )

    return operation_wrapper


class q(metaclass=ABCMeta):

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    def __init__(self, value, unit):
        self._value = float(value)
        self._unit = unit

    @abstractmethod
    def convert(self, other):
        pass        

    def __matmul__(self, unit):
        '''Convert the unit of the quantity to the unit given by `unit`. This is NOT matrix multiplication.'''
        assert unit.quantity() == type(self), 'conversion only possible between equal quantities.'
        return self.convert(unit)

    @ensure_unit_operator
    def __add__(self, other, *args, **kwargs):
        return self.value.__add__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __sub__(self, other, *args, **kwargs):
        return self.value.__sub__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __mul__(self, other, *args, **kwargs):
        return self.value.__mul__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __truediv__(self, other, *args, **kwargs):
        return self.value.__truediv__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __floordiv__(self, other, *args, **kwargs):
        return self.value.__floordiv__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __mod__(self, other, *args, **kwargs):
        return self.value.__mod__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __divmod__(self, other, *args, **kwargs):
        return self.value.__divmod__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __pow__(self, other, *args, **kwargs):
        return self.value.__pow__(other.value, *args, **kwargs)

    @ensure_unit_operator        
    def __lshift__(self, other, *args, **kwargs):
        return NotImplemented()

    @ensure_unit_operator        
    def __rshift__(self, other, *args, **kwargs):
        return NotImplemented()

    @ensure_unit_operator        
    def __and__(self, other, *args, **kwargs):
        return NotImplemented()

    @ensure_unit_operator        
    def __xor__(self, other, *args, **kwargs):
        return NotImplemented()

    @ensure_unit_operator        
    def __or__(self, other, *args, **kwargs):
        return NotImplemented()

    @ensure_unit_operator
    def __abs__(self, other, *args, **kwargs):
        return self.value.__abs__(other.value, *args, **kwargs)
        
    @ensure_unit_operator
    def __round__(self, other, *args, **kwargs):
        return self.value.__round__(other.value, *args, **kwargs)
        
    @ensure_unit_operator
    def __trunc__(self, other, *args, **kwargs):
        return self.value.__trunc__(other.value, *args, **kwargs)
        
    @ensure_unit_operator
    def __floor__(self, other, *args, **kwargs):
        return self.value.__floor__(other.value, *args, **kwargs)
        
    @ensure_unit_operator
    def __ceil__(self, other, *args, **kwargs):
        return self.value.__ceil__(other.value, *args, **kwargs)
    
    @ensure_unit_comparator
    def __lt__(self, other):
        return self.value.__lt__(other.value)
    @ensure_unit_comparator    
    def __le__(self, other):
        return self.value.__le__(other.value) 
    @ensure_unit_comparator    
    def __eq__(self, other):
        return self.value.__eq__(other.value)
    @ensure_unit_comparator    
    def __ne__(self, other):
        return self.value.__ne__(other.value) 
    @ensure_unit_comparator    
    def __gt__(self, other):
        return self.value.__gt__(other.value) 
    @ensure_unit_comparator    
    def __ge__(self, other):
        return self.value.__ge__(other.value) 

    def __repr__(self):
        return self.value.__repr__()

    def __str__(self):
        return f'{self.value.__str__()} {self.unit.d()}'

    def __radd__(self, other):
        return NotImplemented()

    def __rsub__(self, other):
        return NotImplemented()

    def __rmul__(self, other):
        return NotImplemented()

    def __rmatmul__(self, other):
        return NotImplemented()

    def __rtruediv__(self, other):
        return NotImplemented()

    def __rfloordiv__(self, other):
        return NotImplemented()

    def __rmod__(self, other):
        return NotImplemented()

    def __rdivmod__(self, other):
        return NotImplemented()

    def __rpow__(self, other, *args):
        return NotImplemented()

    def __rlshift__(self, other):
        return NotImplemented()

    def __rrshift__(self, other):
        return NotImplemented()

    def __rand__(self, other):
        return NotImplemented()

    def __rxor__(self, other):
        return NotImplemented()

    def __ror__(self, other):
        return NotImplemented()

    def __iadd__(self, other):
        return NotImplemented()

    def __isub__(self, other):
        return NotImplemented()

    def __imul__(self, other):
        return NotImplemented()

    def __imatmul__(self, other):
        return NotImplemented()

    def __itruediv__(self, other):
        return NotImplemented()

    def __ifloordiv__(self, other):
        return NotImplemented()

    def __imod__(self, other):
        return NotImplemented()

    def __ipow__(self, other, *args):
        return NotImplemented()

    def __ilshift__(self, other):
        return NotImplemented()

    def __irshift__(self, other):
        return NotImplemented()

    def __iand__(self, other):
        return NotImplemented()

    def __ixor__(self, other):
        return NotImplemented()

    def __ior__(self, other):
        return NotImplemented()

    def __neg__(self):
        return NotImplemented()

    def __pos__(self):
        return NotImplemented()

    def __invert__(self):
        return NotImplemented()

    def __complex__(self):
        return NotImplemented()

    def __int__(self):
        return NotImplemented()

    def __float__(self):
        return NotImplemented()

    def __index__(self):
        return NotImplemented()


class I(q):

    def __init__(self, value):

        super().__init__(
            value=value,
            unit=None
        )

    def convert(self, unit):

        return unit.quantity()(
            value=self.value,
            unit=unit
        )

    def __matmul__(self, unit):
        return self.convert(unit)

class Temperature(q):

    def __init__(self, value, unit):

        super().__init__(
            value=value,
            unit=unit
        )

    def convert(self, unit):
        return Temperature(
            value=convert_temperature(
                self.value, 
                self.unit.d(),
                unit.d()
            ),
            unit=unit
        )


class Currency(q):

    def __init__(self, value, unit, date=None, force_reload=False):

        if date is None:
            date = datetime.date.today()

        self.converter = CurrencyConverter()

        _, last_dates = zip(*self.converter.bounds.values())
        if date > max(last_dates) or force_reload:
            self.converter = CurrencyConverter(
                currency_file=ECB_URL
            )
        
        self.date = date

        super().__init__(
            value=value,
            unit=unit
        )


    def convert(self, unit):

        return Currency(
            self.converter.convert(
                self.value,
                self.unit.d(),
                unit.d(),
                date=self.date
            ),
            unit=unit
        )


class Mass(q):

    def __init__(self, value, unit):

        super().__init__(
            value=value,
            unit=unit
        )
    
    def convert(self, unit):

        return Mass(
            self.value*self.unit.in_kilogram()/unit.in_kilogram(),
            unit=unit
        )


