from dataclasses import dataclass


@dataclass
class Name:
    """ holds the name of a entity """
    name: str
    description: str = None  # description optional
