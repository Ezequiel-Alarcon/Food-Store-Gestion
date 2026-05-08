"""app.modules.direcciones.router

Endpoints:
- User addresses (owner)
- Branch pickup addresses (public list + admin management)
"""


from fastapi import APIRouter, Depends, status

from app.core.deps import get_current_user, require_role
from app.modules.direcciones.schemas import (
    BranchAddressCreate,
    BranchAddressResponse,
    BranchAddressUpdate,
    UserAddressCreate,
    UserAddressResponse,
    UserAddressUpdate,
)
from app.modules.direcciones.service import BranchAddressesService, UserAddressesService


router = APIRouter()


# User addresses
@router.get(
    "/user/addresses",
    response_model=list[UserAddressResponse],
    summary="Listar direcciones del usuario",
)
def list_user_addresses(current_user=Depends(get_current_user)) -> list[UserAddressResponse]:
    service = UserAddressesService()
    addrs = service.list_active(current_user=current_user)
    return [UserAddressResponse.model_validate(a) for a in addrs]


@router.post(
    "/user/addresses",
    response_model=UserAddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear dirección del usuario",
)
def create_user_address(
    data: UserAddressCreate,
    current_user=Depends(get_current_user),
) -> UserAddressResponse:
    service = UserAddressesService()
    addr = service.create(current_user=current_user, data=data)
    return UserAddressResponse.model_validate(addr)


@router.patch(
    "/user/addresses/{address_id}",
    response_model=UserAddressResponse,
    summary="Actualizar dirección del usuario",
)
def update_user_address(
    address_id: int,
    data: UserAddressUpdate,
    current_user=Depends(get_current_user),
) -> UserAddressResponse:
    service = UserAddressesService()
    addr = service.update(current_user=current_user, address_id=address_id, data=data)
    return UserAddressResponse.model_validate(addr)


@router.delete(
    "/user/addresses/{address_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar (soft-delete) dirección del usuario",
)
def delete_user_address(
    address_id: int,
    current_user=Depends(get_current_user),
) -> None:
    service = UserAddressesService()
    service.soft_delete(current_user=current_user, address_id=address_id)
    return None


@router.post(
    "/user/addresses/{address_id}/default",
    response_model=UserAddressResponse,
    summary="Marcar dirección como predeterminada",
)
def set_default_user_address(
    address_id: int,
    current_user=Depends(get_current_user),
) -> UserAddressResponse:
    service = UserAddressesService()
    addr = service.set_default(current_user=current_user, address_id=address_id)
    return UserAddressResponse.model_validate(addr)


# Branch pickup addresses
@router.get(
    "/branches/addresses",
    response_model=list[BranchAddressResponse],
    summary="Listar direcciones activas de sucursales",
)
def list_branch_addresses() -> list[BranchAddressResponse]:
    service = BranchAddressesService()
    addrs = service.list_active()
    return [BranchAddressResponse.model_validate(a) for a in addrs]


@router.post(
    "/branches/{branchId}/address",
    response_model=BranchAddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear/reemplazar dirección de sucursal",
)
def create_branch_address(
    branchId: int,
    data: BranchAddressCreate,
    _admin=Depends(require_role("ADMIN")),
) -> BranchAddressResponse:
    service = BranchAddressesService()
    addr = service.create_or_replace(branch_id=branchId, data=data)
    return BranchAddressResponse.model_validate(addr)


@router.patch(
    "/branches/{branchId}/address",
    response_model=BranchAddressResponse,
    summary="Actualizar dirección de sucursal",
)
def update_branch_address(
    branchId: int,
    data: BranchAddressUpdate,
    _admin=Depends(require_role("ADMIN")),
) -> BranchAddressResponse:
    service = BranchAddressesService()
    addr = service.update(branch_id=branchId, data=data)
    return BranchAddressResponse.model_validate(addr)


@router.delete(
    "/branches/{branchId}/address",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar (soft-delete) dirección de sucursal",
)
def delete_branch_address(
    branchId: int,
    _admin=Depends(require_role("ADMIN")),
) -> None:
    service = BranchAddressesService()
    service.soft_delete(branch_id=branchId)
    return None
