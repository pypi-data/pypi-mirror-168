from abc import ABCMeta, abstractmethod
from ..quantity import Mass
import scipy.constants

class u(metaclass=ABCMeta):

    @staticmethod
    @abstractmethod
    def quantity():
        pass

    @staticmethod
    @abstractmethod
    def d():
        pass

class MassUnit(u):

    def quantity():
        return Mass


class Kilogram(MassUnit):
    def d():
        return "Kilogram"

    @staticmethod
    def in_kilogram():
        return 1


class Gram(MassUnit):
    def d():
        return "gram" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.gram

class MetricTon(MassUnit):
    def d():
        return "metric_ton" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.metric_ton

class Grain(MassUnit):
    def d():
        return "grain" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.grain

class Lb(MassUnit):
    def d():
        return "lb" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.lb

class Blob(MassUnit):
    def d():
        return "blob" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.blob

class Slug(MassUnit):
    def d():
        return "slug" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.slug

class Oz(MassUnit):
    def d():
        return "oz" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.oz

class Stone(MassUnit):
    def d():
        return "stone" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.stone

class LongTon(MassUnit):
    def d():
        return "long_ton" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.long_ton

class ShortTon(MassUnit):
    def d():
        return "short_ton" 
    
    @staticmethod
    def in_kilogram():
        return scipy.constants.short_ton

