"""app.core.uow

Unit of Work (UoW) para delimitar transacciones.

Patrón esperado:
Router -> Service -> UnitOfWork -> Repository -> Model

El Service abre un `with UnitOfWork(...)` y ejecuta su caso de uso.
Si no hay errores, el UoW comitea exactamente una vez.
Si hay una excepción, hace rollback y nunca comitea.
"""

from __future__ import annotations

from typing import Callable, Optional

from sqlmodel import Session


class UnitOfWork:
    """Unidad de trabajo transaccional como context manager."""

    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory
        self.session: Optional[Session] = None
        self._committed = False

    def __enter__(self) -> "UnitOfWork":
        self.session = self._session_factory()
        self._committed = False
        return self

    def commit(self) -> None:
        if self.session is None:
            raise RuntimeError("UnitOfWork no inicializado (falta __enter__)\n")
        if self._committed:
            return
        self.session.commit()
        self._committed = True

    def rollback(self) -> None:
        if self.session is None:
            return
        self.session.rollback()

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ) -> bool:
        try:
            if exc_type is None:
                self.commit()
            else:
                self.rollback()
        finally:
            if self.session is not None:
                self.session.close()
                self.session = None
        # No suprimimos la excepción
        return False
