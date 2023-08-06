"""Repr helpers"""


def get_properties(cls: type):
    """get the data descriptor (properties) names of a class"""
    return (x for x in dir(cls) if hasattr(getattr(cls, x), "__set__"))
