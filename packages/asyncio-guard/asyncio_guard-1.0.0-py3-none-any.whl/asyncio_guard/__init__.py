import asyncio
from types import TracebackType
from typing import Awaitable, Callable, Generic, Optional, Type, TypeVar

T = TypeVar("T")


class Guard(Generic[T]):
    def __init__(
        self,
        obj: Optional[T] = None,
        update_func: Optional[Callable[[], Awaitable[T]]] = None,
    ) -> None:
        if obj is None and update_func is None:
            raise ValueError("cant init Guard class, either obj or update_func should be not None")

        self._obj = obj
        self._update_func = update_func
        self._mutex = asyncio.Lock()

    async def set(self, obj: T) -> None:
        async with self._mutex:
            self._obj = obj

    async def update(self) -> None:
        async with self._mutex:
            await self._update()

    async def _update(self) -> T:
        # should be run under mutex
        if self._update_func is None:
            raise ValueError(f"cant update guard, because update_func is None")

        obj = await self._update_func()
        self._obj = obj
        return obj

    async def __aenter__(self) -> T:
        await self._mutex.acquire()
        if self._obj is not None:
            return self._obj
        return await self._update()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self._mutex.release()
