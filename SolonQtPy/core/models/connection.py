from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.models.character import CharacterList


if TYPE_CHECKING:
    from models.node import MyNode


@dataclass
class Connect:
    node: "MyNode | None" = None
    positive: bool = True
    direct_chkv: float = 0.0

    # У Delphi це були спеціальні масиви/списки.
    # Поки переносимо як звичайні Python-списки.
    pref: list[float] = field(default_factory=list)
    rel_dyn: list[float] = field(default_factory=list)
    sca_typ: list[int] = field(default_factory=list)

    effect_out: float = -1.0
    value_delay: int = 0
    character: CharacterList = field(default_factory=CharacterList)
    labeled: bool = False

    def __post_init__(self) -> None:
        if self.character.count() == 0:
            self.character.add(1, 0.0)


class ConnectList:
    def __init__(self) -> None:
        self._items: list[Connect] = []

    def clear(self) -> None:
        self._items.clear()

    def count(self) -> int:
        return len(self._items)

    def add(self, node: "MyNode | None") -> int:
        self.insert(self.count(), node)
        return self.count() - 1

    def insert(self, index: int, node: "MyNode | None") -> None:
        con = Connect(node=node)
        self._items.insert(index, con)

    def delete(self, index: int) -> None:
        del self._items[index]

    def remove(self, node: "MyNode | None") -> int:
        index = self.index_of(node)
        if index != -1:
            self.delete(index)
        return index

    def index_of(self, node: "MyNode | None") -> int:
        for i, con in enumerate(self._items):
            if con.node is node:
                return i
        return -1

    def __getitem__(self, index: int) -> Connect:
        return self._items[index]

    def __setitem__(self, index: int, con: Connect) -> None:
        self._items[index] = con

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
