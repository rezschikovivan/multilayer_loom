from abc import ABC, abstractmethod
from collections.abc import Iterable
from enum import StrEnum
from typing import Any, TypeVar


class MultiStrEnum(StrEnum):
    """Строковое перечисление, с возможностью понимать разные регистры"""
    @classmethod
    def _missing_(cls, value):
        if not isinstance(value, str):
            return None
        value_lower = value.strip().lower()
        for member in cls:
            if member.value.strip().lower() == value_lower:
                return member
        return None

    
Side = MultiStrEnum("Side", ("right","left", "top", "bottom"))

class IObserver(ABC):
    @abstractmethod
    def notify(self, subject, *args):
        pass

class Subject:
    def __init__(self):
        self.observers: list[IObserver] = []

    def register_observer(self, o: IObserver):
        self.observers.append(o)

    def remove_observer(self, o: IObserver):
        self.observers.remove(o)
        
    def notify_observers(self, *args):
        for o in self.observers:
            o.notify(self, *args)

class WeftGridSubject(Subject):
    def notify_observers(self, *args):
        for o in self.observers:
            o.notify(self, *args)

def notifying(func):
    """Уведомляет наблюдателей с возвращаемым значением в качесте аргумента оповещения"""
    def wrapper(self:Subject, *args, **kwargs):
        f_args = func(self, *args, **kwargs)
        if isinstance(f_args, Iterable) and not isinstance(f_args, str):
            self.notify_observers(*f_args)    
        else:
            self.notify_observers(f_args)
    return wrapper

class TextileType:
    pass

class Textile:
    """Базовый класс для всех элементов ткани"""
    def __init__(self, textile_type:"TextileType"):
        self._textile_type:TextileType = textile_type
        super().__init__()

class TextileContainer(ABC, Textile):
    """
    Интерфейс составных объектов текстиля 
    """
    @abstractmethod
    def increase(self, side:Side, repeats:int=1):
        """
        Добавляется новый элемент с тем же _textile_type
        что и у контейнера.
        """
        raise NotImplementedError()
    @abstractmethod
    def reduce(self, side:Side, repeats:int=1):
        """Убавляются хранимые элементы. Не может опуститься ниже 1"""
        raise NotImplementedError()
    @property
    def textile_type(self):
        return self._textile_type

    @textile_type.setter
    def textile_type(self, new_value:TextileType):
        self._set_textile_type(new_value)

    @abstractmethod
    def _set_textile_type(self, new_textile):
        raise NotImplementedError()
    
FactoryProduct = TypeVar("FactoryProduct")

class InstanceFactory:
    """
    Экземпляры фабрики предоставляют единую точку доступа
    для получения экземпляров агрегируемого класса. \n
    Фабрика возвращает одинаковый экземпляр для одинаковых 
    аргументов метода get_instance.\n
    Подобный инструмент позволяет экономить память при
    наличии множества подобных объектов не требующих
    идентичности.
    """
    def __init__(self, class_to_instantiate:FactoryProduct):
        self._instances:list[FactoryProduct] = []
        self._keys: list[list[Any]] = []
        self.cls_to_instantiate = class_to_instantiate
    def get_instance(self, *constructor_args)->FactoryProduct:
        """Возвращает экземпляр соответствующий переданным аргументам"""
        if constructor_args in self._keys:
            return self.__get_inst_by_key(constructor_args)
        try:
            instance = self.cls_to_instantiate(*constructor_args)
        except TypeError as err:
            raise TypeError(f"Не валидные аргументы: {constructor_args}," + 
                           f"для создания экземпляра класса {self.cls_to_instantiate.__name__}") from err
        self.__append_inst(constructor_args, instance)
        return instance
    
    def __get_inst_by_key(self, key:list)->FactoryProduct:
        if key in self._keys:
            return self._instances[self._keys.index(key)]
        else: 
            raise KeyError("Не удалось получить экземпляр по этому ключу")
    
    def __append_inst(self, key:list, inst:FactoryProduct):
        self._keys.append(key)
        self._instances.append(inst)
