from typing import Sequence, Generator, TypeVar

T = TypeVar("T")


def chunks(lst: Sequence[T], n: int) -> Generator[Sequence[T], None, None]:
    """
    Yield successive n-sized chunks from lst.
    """
    for i in range(0, len(lst), n):
        yield lst[i: i + n]
