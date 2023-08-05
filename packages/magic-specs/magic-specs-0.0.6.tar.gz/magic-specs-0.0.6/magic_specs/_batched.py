from itertools import islice
from typing import Any, Generator, KeysView, Mapping, Sequence, TypeVar, ValuesView


__all__ = [
    "batched",
]


T = TypeVar("T", Sequence, Mapping, KeysView, ValuesView)


def batched(iterable: T, batch_size: int) -> Generator[T, Any, None]:
    if batch_size <= 0:
        raise ValueError("Batch size must be positive.")

    while iterable:
        try:
            iterable, batch = iterable[batch_size:], iterable[:batch_size]

        except TypeError:
            if isinstance(iterable, Mapping):
                try:
                    iterable, batch = (
                        iterable.__class__(islice(iterable.items(), batch_size, len(iterable))),  # type: ignore
                        iterable.__class__(islice(iterable.items(), 0, batch_size)),  # type: ignore
                    )
                except TypeError:
                    iterable, batch = (
                        iterable.__class__(**dict(islice(iterable.items(), batch_size, len(iterable)))),  # type: ignore
                        iterable.__class__(**dict(islice(iterable.items(), 0, batch_size))),  # type: ignore
                    )
            else:
                try:
                    iterable, batch = (
                        iterable.__class__(islice(iter(iterable), batch_size, len(iterable))),
                        iterable.__class__(islice(iter(iterable), 0, batch_size)),
                    )
                except TypeError:
                    iterable, batch = (
                        list(islice(iter(iterable), batch_size, len(iterable))),
                        list(islice(iter(iterable), 0, batch_size)),
                    )

        yield batch
