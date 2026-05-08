"""app.modules.sucursales.router

Router minimo: listado publico y CRUD admin (si se usa).

No es requerido por addresses-module pero ayuda a operar sucursales.
"""


from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import require_role
from app.modules.sucursales.schemas import SucursalCreate, SucursalResponse, SucursalUpdate
from app.modules.sucursales.service import SucursalesService


router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("/", response_model=list[SucursalResponse])
def list_sucursales(session: Session = Depends(get_session)) -> list[SucursalResponse]:
    service = SucursalesService(session)
    return [SucursalResponse.model_validate(s) for s in service.list_active()]


@router.post("/", response_model=SucursalResponse, status_code=status.HTTP_201_CREATED)
def create_sucursal(
    data: SucursalCreate,
    session: Session = Depends(get_session),
    _admin=Depends(require_role("ADMIN")),
) -> SucursalResponse:
    service = SucursalesService(session)
    return SucursalResponse.model_validate(service.create(data))


@router.patch("/{branchId}", response_model=SucursalResponse)
def update_sucursal(
    branchId: int,
    data: SucursalUpdate,
    session: Session = Depends(get_session),
    _admin=Depends(require_role("ADMIN")),
) -> SucursalResponse:
    service = SucursalesService(session)
    return SucursalResponse.model_validate(service.update(branchId, data))
