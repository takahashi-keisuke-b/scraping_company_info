from typing import TypeVar, Generic, Optional

T = TypeVar('T')

class Result(Generic[T]):
    def __init__(
        self, 
        is_success: bool,
        value: Optional[T] = None,
        error_message: Optional[str] = None
    ):
        self.is_success = is_success
        self.value = value
        self.error_message = error_message

    @classmethod
    def success(cls, value: T) -> 'Result[T]':
        return cls(is_success=True, value=value)

    @classmethod
    def fail(cls, message: str) -> 'Result[T]':
        return cls(is_success=False, error_message=message)

    @classmethod
    def not_found(cls) -> 'Result[T]':
        return cls(is_success=False, error_message="Fail: Not found")

    @classmethod
    def invalid_url(cls) -> 'Result[T]':
        return cls(is_success=False, error_message="Fail: Invalid URL")

    def __repr__(self) -> str:
        if self.is_success:
            return f"Result(Success: {self.value})"
        return f"Result(Fail: {self.error_message})"