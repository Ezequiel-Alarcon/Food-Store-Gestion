"""Módulo de ejemplo para demostrar el patrón Router->Service->UoW->Repo->Model.

No es un módulo de negocio. Su objetivo es dejar un ejemplo copiables para
futuros módulos.
"""

from __future__ import annotations

from typing import Optional

from sqlmodel import Field, SQLModel


class ExampleItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
