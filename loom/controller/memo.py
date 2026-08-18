from abc import ABC, abstractmethod


class Memento:
    def __init__(self, originator:"Originator", state):
        self.originator = originator
        self.__state = state
        
    def get_state(self, requester:"Originator"):
        self.check_permission(requester)
        return self.__state

    def check_permission(self, requester:"Originator"):
        if requester is not self.originator:
            raise PermissionError(f"Объект: {requester} не имеет доступа!" +
                                    " Только хозяин воспоминания может получить доступ.")

class Originator(ABC):
    @abstractmethod
    def set_memento(self, memento:Memento):
        """Устанавливает состояние хранителя в хозяина"""
        raise NotImplementedError()
    @abstractmethod
    def create_memento(self)->Memento:
        """Возвращает хранителя соответствующего текущему состоянию"""
        raise NotImplementedError()