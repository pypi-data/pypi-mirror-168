from datetime import datetime, time, timedelta, timezone
from math import ceil
from types import TracebackType
from typing import (
    AsyncIterable,
    AsyncIterator,
    Generic,
    Iterable,
    MutableMapping,
    Optional,
    Type,
    TypeVar,
    Union,
)
from uuid import uuid4

from aiostream.stream import chain, iterate, preserve, take

T = TypeVar("T")


class CachingAsyncIterable(AsyncIterable[T], Generic[T]):
    _iterable: AsyncIterable[T]
    _cache: MutableMapping[str, T]
    _prefix: str
    _watermark: int

    def __init__(
        self,
        iterable: AsyncIterable[T],
        cache: Optional[MutableMapping[str, T]] = None,
        prefix: Optional[str] = None,
    ):
        self._iterable = iterable
        self._cache = cache if cache is not None else {}
        self._prefix = prefix if prefix is not None else uuid4().hex
        self._watermark = 0

    def _make_key(self, i: int) -> str:
        return f"{self._prefix}-{i}"

    async def __aiter__(self) -> AsyncIterator[T]:
        for i in range(self._watermark):
            key = self._make_key(i)
            yield self._cache[key]
        async for item in self._iterable:
            key = self._make_key(self._watermark)
            self._cache[key] = item
            self._watermark += 1
            yield item

    def __enter__(self) -> "CachingAsyncIterable[T]":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> Optional[bool]:
        for i in range(self._watermark):
            key = self._make_key(i)
            del self._cache[key]
        self._watermark = 0
        return None


async def batches(
    iterable: Union[Iterable[T], AsyncIterable[T]],
    n: Optional[int],
) -> AsyncIterable[AsyncIterable[T]]:
    iterable = next(iterate(iterable)._generator)

    if n is None:
        yield iterable
        return

    async for first in iterable:

        async def afirst():
            yield first

        batch = chain(afirst(), take(preserve(iterable), n - 1))
        yield next(batch._generator)


def next_time(base: datetime, interval: timedelta) -> datetime:
    utcbase = base.astimezone(timezone.utc)
    utcnow = datetime.now(timezone.utc)
    return utcbase + interval * ceil((utcnow - utcbase) / interval)


def seconds_until(dt: datetime) -> float:
    return (dt - datetime.now(timezone.utc)).total_seconds()


def utcmidnight() -> datetime:
    now = datetime.now(timezone.utc)
    return datetime.combine(now.date(), time(), tzinfo=timezone.utc)
