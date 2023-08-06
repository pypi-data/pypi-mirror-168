from .auto_create._input import _Input


class Input(_Input):
    def __init__(self, value: str) -> None:
        super().__init__()

        self.value = value
