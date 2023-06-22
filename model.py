from dataclasses import dataclass
from typing import List, Union

@dataclass
class State:
    current_question: str = ''