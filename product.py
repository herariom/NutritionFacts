import typing
from dataclasses import dataclass


@dataclass
class Product:
    product_name: str
    file_name: str
    facts: typing.Dict[str, int]
    url: str
