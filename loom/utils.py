

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
    
class BottomlessStack:
    """Stack with auto clearing. If len arcoss the max_len, first item is deleting."""
    def __init__(self, max_len=10):
        self.enum = []
        self.max_len = max_len
    def __getitem__(self, key):
          return self.enum[key]
    def append(self, item):
         if len(self.enum) >= self.max_len:
              self.enum.pop(0)
         self.enum.append(item)
    def __iter__(self):
        return self.enum.__iter__()
    def pop(self, index=-1):
        return self.enum.pop(index)
    def __len__(self):
         return self.enum.__len__()