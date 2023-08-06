from abc import ABCMeta, abstractmethod

class Validator(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'validate') and 
                callable(subclass.validate) or 
                NotImplemented)
    
    @abstractmethod
    def validate(self, value: str) -> bool:
        pass