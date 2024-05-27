from typing import Any

from gyver.attrs import define


@define
class Group:
    _names: set[str]

    def flag(self, name: str) -> Any:
        pass
