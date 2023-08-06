from typing import Tuple, TypeVar, Callable, List, Dict, OrderedDict
from collections import OrderedDict

T = TypeVar("T")


def group_by(input: List[T], f: Callable[[T], str]) -> Dict[str, List[T]]:
    """given a list of objects group them by the result of some property

    Args:
        input (List[T]): a list of objects
        f (Callable[[T], str]): a function that returns the group key

    Returns:
        Dict[str, List[T]]: a dict with group keys that map to lists of objects
    """
    res = OrderedDict()
    for k, v in map(lambda x: (f(x), x), input):
        if k in res:
            res[k].append(v)
        else:
            res[k] = [v]
    return res


def partition(input: List[T], f: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    """partitions a list into two lists using a parititon function

    Args:
        input (List[T]): the list to be partitioned
        f (Callable[[T], bool]): a function that returns whether the element belongs in the first partition

    Returns:
        Tuple[List[T], List[T]]: partitioned lists with the first containing all objects where f(x) is true
    """
    return (
        [g for g in input if f(g)],
        [g for g in input if not f(g)],
    )


def flatten(l):
    return [item for sublist in l for item in sublist]


def key_by(col, key_fn):
    """given a collection, return the same collection as a dictionary key'd by the result of the key_fn

    Args:
        col (_type_): any iterable collection
        key_fn (_type_): a function that maps each element of col to a dictionary key

    Returns:
        dict: the resulting dictionary of col's elements with key defined by key_fn
    """
    return {key_fn(item): item for item in col}


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value

    return destination
