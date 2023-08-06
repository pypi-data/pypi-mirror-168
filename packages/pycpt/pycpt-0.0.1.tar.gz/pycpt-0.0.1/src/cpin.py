from typing import List


def si() -> int:
    """Get single int input value.

    Returns:
        int: Input as int value.
    Raises:
        ValueError - Raised when Input value is not of instance int.
    """
    return int(input())


def mi(sep=None, maxsplit=-1) -> List[int]:
    """Get multiple int input values.

    Parameters:
        sep: Delimiter string - By default, any whitespace is a separator.
        maxsplit: Number of splits that are done at most.
    Returns:
        List[int]: Input as list of int values.
    Raises:
        ValueError - Raised when not all input values are of instance int.
    """
    return list(map(int, input().split(sep=sep, maxsplit=maxsplit)))


def ss() -> str:
    """Get single str input value.

    Returns:
        int: Input as str value.
    """
    return input()


def ms(sep=None, maxsplit=-1) -> List[str]:
    """Get multiple str input values.

    Parameters:
        sep: Delimiter string - By default, any whitespace is a separator.
        maxsplit: Number of splits that are done at most.
    Returns:
        List[str]: Input as list of str values.
    """
    return input().split(sep=sep, maxsplit=maxsplit)
