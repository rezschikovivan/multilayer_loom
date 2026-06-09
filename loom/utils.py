
class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls, *args, **kwargs):# call instead of the constructor
        if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.__init__(*args, **kwargs)
        return cls._instance