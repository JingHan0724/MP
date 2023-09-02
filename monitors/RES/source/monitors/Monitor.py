from abc import ABC, abstractmethod

class AbstractMonitor(ABC):
   
    def __init__(self):
      super().__init__()
    
    @abstractmethod
    def get_field_names(self):
        pass
    
    @abstractmethod
    def monitor(self):
        pass