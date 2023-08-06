from typing import List


def si() -> int:
    """Get single int input."""
    return int(input())


def mi(s="") -> List[int]:
    """Get multi int input. TODO split param."""
    return list(map(int, input().split(s)))


def ss() -> str:
    """Get single str input."""
    return input()


def ms(s="") -> List[str]:
    """Get multi str input. TODO split param."""
    return input().split(s)
