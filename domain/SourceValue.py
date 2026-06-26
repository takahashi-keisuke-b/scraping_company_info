from typing import Generic, TypeVar

T = TypeVar('T')
S = TypeVar('S')

class SourceValue(Generic[T,S]):
    def __init__(self, value: T, source: S):
        self._value: T = value
        self._source: S = source

    @property
    def value(self) -> T:
        return self._value

    @property
    def source(self) -> S:
        return self._source

    def __repr__(self) -> str:
        return f"SourceValue(value={self._value}, source={self._source})"