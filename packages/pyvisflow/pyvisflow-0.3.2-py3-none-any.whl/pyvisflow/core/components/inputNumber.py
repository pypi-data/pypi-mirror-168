from typing import Union
from .auto_create._inputNumber import _InputNumber


class InputNumber(_InputNumber):
    def __init__(self, value: float) -> None:
        super().__init__()

        self.value = value
