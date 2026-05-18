"""
app.modules.productos.router

Router para endpoints de productos.
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.core.database import get_session
from app.core.deps import get_current_user, require_role
from app.modules.auth.schemas import MessageResponse
from app.modules.productos.schemas import (
    CategoriaSimple,
    IngredienteSimple,
    PaginatedProductoResponse,
    ProductoCatalogoResponse,
    ProductoCreate,
    ProductoListResponse,
    ProductoResponse,
    ProductoStockUpdate,
    ProductoUpdate,
)
from app.modules.productos.service import ProductoService

router = APIRouter()


# ============================================================
# ENDPOINTS PÚBLICOS (sin autenticación)
# ============================================================
# IMPORTANTE: Las rutas literales deben ir ANTES que las parametrizadas
# para que FastAPI no matchee /catalogo como /{producto_id}


@router.get(
    "/catalogo",
    summary="Catálogo público de productos",
    description="Obtiene el catálogo público de productos con filtros. No requiere autenticación.",
)
def get_catalogo(
    skip: int = Query(0, ge=0, description="Offset para paginación"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    disponibles: bool = Query(True, description="Solo productos con stock"),
    excluir_alergenos: bool = Query(False, description="Excluir productos con alérgenos"),
    ingrediente_ids: Optional[str] = Query(
        None,
        description="IDs de ingredientes a excluir (comma-separated)",
    ),
    session: Session = Depends(get_session),
) -> PaginatedProductoResponse:
    """Obtiene el catálogo público de productos."""
    service = ProductoService(session)

    # Parsear ingrediente_ids
    ing_ids = None
    if ingrediente_ids:
        try:
            ing_ids = [int(x.strip()) for x in ingrediente_ids.split(",") if x.strip()]
        except ValueError:
            pass

    result = service.get_catalogo(
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
        disponibles_only=disponibles,
        excluir_alergenos=excluir_alergenos,
        ingrediente_ids_excluir=ing_ids,
    )

    # Convertir cada producto a formato catálogo público
    items = []
    for producto in result.items:
        rel = service.get_with_relations(producto.id)
        items.append({
            "id": rel["producto"].id,
            "nombre": rel["producto"].nombre,
            "descripcion": rel["producto"].descripcion,
            "precio": rel["producto"].precio,
            "imagen_url": rel["producto"].imagen_url,
            "disponible": rel["producto"].stock > 0,
            "categorias": [
                CategoriaSimple(id=c.id, nombre=c.nombre)
                for c in rel["categorias"]
            ],
        })

    return PaginatedProductoResponse(
        items=items,
        total=result.total,
        skip=result.skip,
        limit=result.limit,
    )


# ============================================================
# ENDPOINTS ADMIN (requieren AUTH + rol ADMIN o STOCK)
# ============================================================


@router.post(
    "/",
    response_model=ProductoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto",
    description="Crea un nuevo producto. Requiere rol ADMIN o STOCK.",
)
def create_producto(
    data: ProductoCreate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> dict:
    """Crea un nuevo producto."""
    service = ProductoService(session)
    producto = service.create(data)

    # Obtener relaciones
    result = service.get_with_relations(producto.id)

    return {
        "id": result["producto"].id,
        "nombre": result["producto"].nombre,
        "descripcion": result["producto"].descripcion,
        "precio": result["producto"].precio,
        "imagen_url": result["producto"].imagen_url,
        "stock": result["producto"].stock,
        "activo": result["producto"].activo,
        "creado_en": result["producto"].creado_en,
        "actualizado_en": result["producto"].actualizado_en,
        "categorias": [
            CategoriaSimple(id=c.id, nombre=c.nombre)
            for c in result["categorias"]
        ],
        "ingredientes": [
            IngredienteSimple(id=i.id, nombre=i.nombre)
            for i in result["ingredientes"]
        ],
    }


@router.get(
    "/",
    summary="Listar productos (admin)",
    description="Lista todos los productos activos. Requiere rol ADMIN o STOCK.",
)
def list_productos(
    skip: int = Query(0, ge=0, description="Offset para paginación"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> PaginatedProductoResponse:
    """Lista todos los productos (para admin)."""
    service = ProductoService(session)
    result = service.list_all(
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
    )

    # Convertir cada producto a diccionario con relaciones
    items = []
    for producto in result.items:
        rel = service.get_with_relations(producto.id)
        items.append({
            "id": rel["producto"].id,
            "nombre": rel["producto"].nombre,
            "descripcion": rel["producto"].descripcion,
            "precio": rel["producto"].precio,
            "imagen_url": rel["producto"].imagen_url,
            "stock": rel["producto"].stock,
            "activo": rel["producto"].activo,
            "categorias": [
                CategoriaSimple(id=c.id, nombre=c.nombre)
                for c in rel["categorias"]
            ],
        })

    return PaginatedProductoResponse(
        items=items,
        total=result.total,
        skip=result.skip,
        limit=result.limit,
    )


@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Obtener producto (admin)",
    description="Obtiene un producto por ID. Requiere rol ADMIN o STOCK.",
)
def get_producto(
    producto_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> dict:
    """Obtiene un producto por ID."""
    service = ProductoService(session)
    result = service.get_with_relations(producto_id)

    return {
        "id": result["producto"].id,
        "nombre": result["producto"].nombre,
        "descripcion": result["producto"].descripcion,
        "precio": result["producto"].precio,
        "imagen_url": result["producto"].imagen_url,
        "stock": result["producto"].stock,
        "activo": result["producto"].activo,
        "creado_en": result["producto"].creado_en,
        "actualizado_en": result["producto"].actualizado_en,
        "categorias": [
            CategoriaSimple(id=c.id, nombre=c.nombre)
            for c in result["categorias"]
        ],
        "ingredientes": [
            IngredienteSimple(id=i.id, nombre=i.nombre)
            for i in result["ingredientes"]
        ],
    }


@router.put(
    "/{producto_id}",
    response_model=ProductoResponse,
    summary="Actualizar producto",
    description="Actualiza un producto existente. Requiere rol ADMIN o STOCK.",
)
def update_producto(
    producto_id: int,
    data: ProductoUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> dict:
    """Actualiza un producto."""
    service = ProductoService(session)
    producto = service.update(producto_id, data)

    # Obtener relaciones actualizadas
    result = service.get_with_relations(producto.id)

    return {
        "id": result["producto"].id,
        "nombre": result["producto"].nombre,
        "descripcion": result["producto"].descripcion,
        "precio": result["producto"].precio,
        "imagen_url": result["producto"].imagen_url,
        "stock": result["producto"].stock,
        "activo": result["producto"].activo,
        "creado_en": result["producto"].creado_en,
        "actualizado_en": result["producto"].actualizado_en,
        "categorias": [
            CategoriaSimple(id=c.id, nombre=c.nombre)
            for c in result["categorias"]
        ],
        "ingredientes": [
            IngredienteSimple(id=i.id, nombre=i.nombre)
            for i in result["ingredientes"]
        ],
    }


@router.patch(
    "/{producto_id}/stock",
    response_model=ProductoResponse,
    summary="Actualizar stock",
    description="Actualiza el stock de un producto. Requiere rol ADMIN o STOCK.",
)
def update_stock(
    producto_id: int,
    data: ProductoStockUpdate,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN", "STOCK")),
) -> dict:
    """Actualiza el stock de un producto."""
    service = ProductoService(session)
    producto = service.update_stock(producto_id, data)

    # Obtener relaciones
    result = service.get_with_relations(producto.id)

    return {
        "id": result["producto"].id,
        "nombre": result["producto"].nombre,
        "descripcion": result["producto"].descripcion,
        "precio": result["producto"].precio,
        "imagen_url": result["producto"].imagen_url,
        "stock": result["producto"].stock,
        "activo": result["producto"].activo,
        "creado_en": result["producto"].creado_en,
        "actualizado_en": result["producto"].actualizado_en,
        "categorias": [
            CategoriaSimple(id=c.id, nombre=c.nombre)
            for c in result["categorias"]
        ],
        "ingredientes": [
            IngredienteSimple(id=i.id, nombre=i.nombre)
            for i in result["ingredientes"]
        ],
    }


@router.delete(
    "/{producto_id}",
    response_model=MessageResponse,
    summary="Eliminar producto",
    description="Elimina (soft-delete) un producto. Requiere rol ADMIN.",
)
def delete_producto(
    producto_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role("ADMIN")),
) -> dict:
    """Elimina (soft-delete) un producto."""
    service = ProductoService(session)
    service.soft_delete(producto_id)
    return {"message": "Producto eliminado correctamente"}


# ============================================================
# ENDPOINT PÚBLICO CON PARÁMETRO (después de rutas admin)
# ============================================================


@router.get(
    "/{producto_id}/publico",
    summary="Obtener producto público",
    description="Obtiene el detalle de un producto sin revelar stock exacto. No requiere autenticación.",
)
def get_producto_publico(
    producto_id: int,
    session: Session = Depends(get_session),
) -> dict:
    """Obtiene un producto para el público (sin stock exacto)."""
    service = ProductoService(session)
    producto = service.get_by_id_publico(producto_id)

    # Obtener relaciones
    result = service.get_with_relations(producto.id)

    # No revelar stock exacto, solo si está disponible
    return {
        "id": result["producto"].id,
        "nombre": result["producto"].nombre,
        "descripcion": result["producto"].descripcion,
        "precio": result["producto"].precio,
        "imagen_url": result["producto"].imagen_url,
        "disponible": result["producto"].stock > 0,
        "categorias": [
            CategoriaSimple(id=c.id, nombre=c.nombre)
            for c in result["categorias"]
        ],
        "ingredientes": [
            IngredienteSimple(id=i.id, nombre=i.nombre)
            for i in result["ingredientes"]
        ],
    }