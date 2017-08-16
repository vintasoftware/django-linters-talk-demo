from typing import Any, TypeVar


T = TypeVar('T', bound='QuerySet')


class QuerySet:
    def filter(self: T, *args: Any, **kwargs: Any) -> T:
        ...
