from __future__ import annotations

from abc import abstractmethod
from typing import Callable, List, Optional, Set, Tuple, Dict, TYPE_CHECKING, Generator

from .absProp import AbsPropInfo



class CombinePropInfo(AbsPropInfo):
    def __init__(self, logic: str, left: AbsPropInfo,
                 right: AbsPropInfo) -> None:
        super().__init__()
        self.left = left
        self.right = right
        self.logic = logic

    def _ex_maybe_child(self) -> Generator:
        yield self.left
        yield self.right

    def gen_expr(self) -> str:
        return f'({self.left.gen_expr()}{self.logic}{self.right.gen_expr()})'

