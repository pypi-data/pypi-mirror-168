import copy
import functools
import typing as t


class Dependency:
    @classmethod
    def add(cls, name: str, service: t.Any) -> None:
        setattr(cls, f"__{name}", service)

    @classmethod
    def override(cls, name: str, service: t.Any) -> None:
        setattr(cls, f"__{name}", service)

    @classmethod
    def inject(cls, name: str) -> t.Any:
        def decorator(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                args = args + (copy.copy(getattr(cls, f"__{name}")),)
                return await func(*args, **kwargs)

            return wrapper

        return decorator
