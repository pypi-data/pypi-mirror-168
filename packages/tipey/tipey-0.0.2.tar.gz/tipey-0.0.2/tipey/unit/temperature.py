from ..quantity import Temperature
from .base_units import u


class TemperatureUnit(u):

    def quantity():
        return Temperature
        

class Celsius(TemperatureUnit):

    def d():
        return "Celsius"


class Kelvin(TemperatureUnit):

    def d():
        return 'Kelvin'

class Fahrenheit(TemperatureUnit):

    def d():
        return 'Fahrenheit'

class Rankine(TemperatureUnit):

    def d():
        return 'Rankine'
