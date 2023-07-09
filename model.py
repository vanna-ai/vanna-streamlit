from dataclasses import dataclass
from typing import List, Union

@dataclass
class State:
    current_question: str = ''

    _my_var: int = 0
    
    @property
    def my_var(self):
        return self._my_var
    
    @my_var.setter
    def my_var(self, value):
        self._my_var = value
        self.after_set_function()
        
    def after_set_function(self):
        # Your code here
        print("After set function called")