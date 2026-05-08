"""Router de ejemplo.

Este router NO está registrado por defecto en `app.main`.
Sirve como referencia de uso para:
- deps auth/RBAC (`get_current_user`, `require_role`)
- UnitOfWork + BaseRepository
"""


from fastapi import APIRouter, Depends

from app.core.database import SessionLocal
from app.core.deps import get_current_user, require_role
from app.core.uow import UnitOfWork
from app.modules.patterns_example.service import ExampleService


router = APIRouter(prefix="/patterns-example")


def _service() -> ExampleService:
    return ExampleService(uow=UnitOfWork(SessionLocal))


@router.post("/commit")
def example_commit(
    name: str,
    _principal=Depends(get_current_user),
    _admin=Depends(require_role("admin")),
    service: ExampleService = Depends(_service),
):
    item = service.create_item_and_commit(name=name)
    return {"id": item.id, "name": item.name, "result": "committed"}


@router.post("/rollback")
def example_rollback(
    name: str,
    _principal=Depends(get_current_user),
    _admin=Depends(require_role("admin")),
    service: ExampleService = Depends(_service),
):
    service.create_item_and_fail(name=name)
    return {"result": "should_not_happen"}
