from enum import Enum
from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

Side = Enum("Side", ("right","left", "top", "bottom"))

class Observer(ABC):
    @abstractmethod
    def notify(self, grid, side:Side):
        pass

class Subject:
    def __init__(self):
        self.observers: list[Observer] = []
    def register_observer(self, o: Observer):
        self.observers.append(o)
    def remove_observer(self, o: Observer):
        self.observers.remove(o)
    def notify_observers(self, grid, side:Side):
        for o in self.observers:
            o.notify(grid, side)

class TextileType:
    pass

class Textile(ABC):
    """Базовый класс для всех элементов ткани"""
    def __init__(self, textile_type:"TextileType"):
        self._textile_type:"TextileType" = textile_type
        super().__init__()

class TextileContainer(Textile):
    """
    Интерфейс составных объектов текстиля 
    """
    @abstractmethod
    def increase(self, side:Side, target_value:int=1):
        raise NotImplementedError()
    @abstractmethod
    def reduce(self, side:Side, target_value:int=1):
        raise NotImplementedError()
    
FactoryProduct = TypeVar("FactoryProduct")

class InstanceFactory(Generic[FactoryProduct]):
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
        except TypeError:
            raise KeyError(f"Не валидные аргументы: {constructor_args}," + 
                           f"для создания экземпляра класса {self.cls_to_instantiate.__name__}")
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
