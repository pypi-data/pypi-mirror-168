from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base import Base

APIs = {}


def register(name: str, _class: Base):
    APIs[name.lower()] = _class


def Seletrans(name: str) -> Base:
    return APIs[name.lower()]
