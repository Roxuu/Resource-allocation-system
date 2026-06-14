from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class CharacterItem:
    n_gr: int = 0
    ratio: float = 0.0


@dataclass
class CharacterList:
    items: list[CharacterItem] = field(default_factory=list)

    def clear(self) -> None:
        self.items.clear()

    def count(self) -> int:
        return len(self.items)

    def add(self, n_gr: int, ratio: float) -> None:
        self.items.append(CharacterItem(n_gr=n_gr, ratio=ratio))

    def remove(self, n_gr: int) -> None:
        for i, item in enumerate(self.items):
            if item.n_gr == n_gr:
                del self.items[i]
                return

    def index_of(self, n_gr: int) -> int:
        for i, item in enumerate(self.items):
            if item.n_gr == n_gr:
                return i
        return -1

    def replace_n_gr(self, old_value: int, new_value: int) -> None:
        for item in self.items:
            if item.n_gr == old_value:
                item.n_gr = new_value

    def __getitem__(self, index: int) -> CharacterItem:
        return self.items[index]

    def __len__(self) -> int:
        return len(self.items)

    def __iter__(self):
        return iter(self.items)
