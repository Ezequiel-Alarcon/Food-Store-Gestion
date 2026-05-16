"""
app.modules.productos.service

Servicio para operaciones de productos.
"""
from datetime import datetime, timezone
from typing import Optional

from fastapi import HTTPException, status
from sqlmodel import Session, select

from app.modules.productos.model import (
    Producto,
    ProductoCategoria,
    ProductoIngrediente,
)
from app.modules.productos.repository import ProductoRepository
from app.modules.productos.schemas import (
    PaginatedProductoResponse,
    ProductoCreate,
    ProductoStockUpdate,
    ProductoUpdate,
)


class CategoriaSimple:
    """Helper para construir categoría simple desde modelo."""
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre


class IngredienteSimple:
    """Helper para construir ingrediente simple desde modelo."""
    def __init__(self, id: int, nombre: str):
        self.id = id
        self.nombre = nombre


def _get_categorias_from_producto(session: Session, producto_id: int) -> list[CategoriaSimple]:
    """Obtiene las categorías de un producto como objetos simples."""
    stmt = (
        select(ProductoCategoria)
        .where(ProductoCategoria.producto_id == producto_id)
    )
    relaciones = session.exec(stmt).all()

    categorias = []
    for rel in relaciones:
        # Obtener la categoría
        from app.modules.categorias.model import Categoria
        cat = session.get(Categoria, rel.categoria_id)
        if cat and cat.activa:
            categorias.append(CategoriaSimple(id=cat.id, nombre=cat.nombre))

    return categorias


def _get_ingredientes_from_producto(session: Session, producto_id: int) -> list[IngredienteSimple]:
    """Obtiene los ingredientes de un producto como objetos simples."""
    stmt = (
        select(ProductoIngrediente)
        .where(ProductoIngrediente.producto_id == producto_id)
    )
    relaciones = session.exec(stmt).all()

    ingredientes = []
    for rel in relaciones:
        # Obtener el ingrediente
        from app.modules.ingredientes.model import Ingrediente
        ing = session.get(Ingrediente, rel.ingrediente_id)
        if ing and ing.eliminado_en is None:
            ingredientes.append(IngredienteSimple(id=ing.id, nombre=ing.nombre))

    return ingredientes


class ProductoService:
    """Servicio de productos."""

    def __init__(self, session: Session):
        self.session = session
        self.repo = ProductoRepository(session)

    def create(self, data: ProductoCreate) -> Producto:
        """
        Crea un nuevo producto.

        Args:
            data: Schema de creación

        Returns:
            Producto creado

        Raises:
            HTTPException 400: Si el precio o stock son inválidos
            HTTPException 404: Si alguna categoría o ingrediente no existe
        """
        # RN-ST01: El precio debe ser mayor a 0
        if data.precio <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0",
            )

        # RN-ST02: El stock inicial no puede ser negativo
        if data.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock inicial no puede ser negativo",
            )

        # Validar que las categorías existen
        if data.categoria_ids:
            from app.modules.categorias.model import Categoria
            for cat_id in data.categoria_ids:
                cat = self.session.get(Categoria, cat_id)
                if not cat or not cat.activa:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"La categoría con ID {cat_id} no existe",
                    )

        # Validar que los ingredientes existen
        if data.ingrediente_ids:
            from app.modules.ingredientes.model import Ingrediente
            for ing_id in data.ingrediente_ids:
                ing = self.session.get(Ingrediente, ing_id)
                if not ing or ing.eliminado_en is not None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"El ingrediente con ID {ing_id} no existe",
                    )

        # Crear producto
        producto = Producto(
            nombre=data.nombre,
            descripcion=data.descripcion,
            precio=data.precio,
            imagen_url=data.imagen_url,
            stock=data.stock,
            activo=data.activo,
        )

        self.repo.add(producto)
        self.session.flush()

        # Asociar categorías
        for cat_id in data.categoria_ids:
            self.repo.add_categoria(producto.id, cat_id)

        # Asociar ingredientes
        for ing_id in data.ingrediente_ids:
            self.repo.add_ingrediente(producto.id, ing_id)

        return producto

    def get_by_id(self, producto_id: int) -> Producto:
        """
        Obtiene un producto por ID (para admin).

        Args:
            producto_id: ID del producto

        Returns:
            Producto encontrado

        Raises:
            HTTPException 404: Si no existe
        """
        producto = self.repo.get_by_id_with_trash(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return producto

    def get_by_id_publico(self, producto_id: int) -> Producto:
        """
        Obtiene un producto por ID (público - solo activos).

        Args:
            producto_id: ID del producto

        Returns:
            Producto encontrado

        Raises:
            HTTPException 404: Si no existe o no está activo
        """
        producto = self.repo.get_by_id_active(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )
        return producto

    def list_all(
        self,
        skip: int = 0,
        limit: int = 20,
        categoria_id: Optional[int] = None,
    ) -> PaginatedProductoResponse:
        """
        Lista todos los productos activos (para admin).

        Args:
            skip: Offset para paginación
            limit: Límite de resultados
            categoria_id: Filtrar por categoría

        Returns:
            Respuesta paginada de productos
        """
        productos, total = self.repo.get_all_active(
            skip=skip,
            limit=limit,
            categoria_id=categoria_id,
        )
        return PaginatedProductoResponse(
            items=productos,
            total=total,
            skip=skip,
            limit=limit,
        )

    def get_catalogo(
        self,
        skip: int = 0,
        limit: int = 20,
        categoria_id: Optional[int] = None,
        disponibles_only: bool = True,
        excluir_alergenos: bool = False,
        ingrediente_ids_excluir: Optional[list[int]] = None,
    ) -> PaginatedProductoResponse:
        """
        Obtiene el catálogo público de productos con filtros.

        Args:
            skip: Offset para paginación
            limit: Límite de resultados
            categoria_id: Filtrar por categoría
            disponibles_only: Solo productos con stock > 0
            excluir_alergenos: Excluir productos con alérgenos
            ingrediente_ids_excluir: IDs de ingredientes a excluir

        Returns:
            Respuesta paginada del catálogo
        """
        productos, total = self.repo.get_catalogo_publico(
            skip=skip,
            limit=limit,
            categoria_id=categoria_id,
            disponibles_only=disponibles_only,
            excluir_alergenos=excluir_alergenos,
            ingrediente_ids_excluir=ingrediente_ids_excluir,
        )
        return PaginatedProductoResponse(
            items=productos,
            total=total,
            skip=skip,
            limit=limit,
        )

    def update(self, producto_id: int, data: ProductoUpdate) -> Producto:
        """
        Actualiza un producto.

        Args:
            producto_id: ID del producto
            data: Schema de actualización

        Returns:
            Producto actualizado

        Raises:
            HTTPException 404: Si no existe
            HTTPException 400: Si se intenta editar un producto eliminado
            HTTPException 400: Si el precio o stock son inválidos
            HTTPException 404: Si alguna categoría o ingrediente no existe
        """
        producto = self.repo.get_by_id_with_trash(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        # RN-ST03: No se puede editar un producto eliminado
        if producto.eliminado_en is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede editar un producto eliminado",
            )

        # Validar precio si se proporciona
        if data.precio is not None and data.precio <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio debe ser mayor a 0",
            )

        # Validar stock si se proporciona
        if data.stock is not None and data.stock < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock no puede ser negativo",
            )

        # Validar categorías si se proporcionan
        if data.categoria_ids is not None:
            from app.modules.categorias.model import Categoria
            for cat_id in data.categoria_ids:
                cat = self.session.get(Categoria, cat_id)
                if not cat or not cat.activa:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"La categoría con ID {cat_id} no existe",
                    )

        # Validar ingredientes si se proporcionan
        if data.ingrediente_ids is not None:
            from app.modules.ingredientes.model import Ingrediente
            for ing_id in data.ingrediente_ids:
                ing = self.session.get(Ingrediente, ing_id)
                if not ing or ing.eliminado_en is not None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"El ingrediente con ID {ing_id} no existe",
                    )

        # Aplicar cambios
        if data.nombre is not None:
            producto.nombre = data.nombre

        if data.descripcion is not None:
            producto.descripcion = data.descripcion

        if data.precio is not None:
            producto.precio = data.precio

        if data.imagen_url is not None:
            producto.imagen_url = data.imagen_url

        if data.stock is not None:
            producto.stock = data.stock

        if data.activo is not None:
            producto.activo = data.activo

        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()

        # Actualizar categorías si se proporcionan
        if data.categoria_ids is not None:
            self.repo.set_categorias(producto_id, data.categoria_ids)

        # Actualizar ingredientes si se proporcionan
        if data.ingrediente_ids is not None:
            self.repo.set_ingredientes(producto_id, data.ingrediente_ids)

        return producto

    def update_stock(self, producto_id: int, data: ProductoStockUpdate) -> Producto:
        """
        Actualiza el stock de un producto.

        Args:
            producto_id: ID del producto
            data: Schema de actualización de stock

        Returns:
            Producto con stock actualizado

        Raises:
            HTTPException 404: Si no existe
            HTTPException 400: Si la operación no es válida o el stock queda negativo
        """
        producto = self.repo.get_by_id_with_trash(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        # RN-ST04: Si operacion es 'subtract', el stock no puede quedar negativo
        if data.operacion == "set":
            if data.stock < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El stock no puede ser negativo",
                )
            producto.stock = data.stock

        elif data.operacion == "add":
            producto.stock += data.stock

        elif data.operacion == "subtract":
            if producto.stock < data.stock:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No hay suficiente stock disponible",
                )
            producto.stock -= data.stock

        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()

        return producto

    def soft_delete(self, producto_id: int) -> None:
        """
        Realiza soft-delete de un producto.

        Args:
            producto_id: ID del producto

        Raises:
            HTTPException 404: Si no existe
        """
        producto = self.repo.get_by_id_with_trash(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        self.repo.soft_delete(producto_id)

    def get_with_relations(self, producto_id: int) -> dict:
        """
        Obtiene un producto con sus categorías e ingredientes.

        Args:
            producto_id: ID del producto

        Returns:
            Diccionario con el producto y sus relaciones
        """
        producto = self.repo.get_by_id_with_trash(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado",
            )

        categorias = _get_categorias_from_producto(self.session, producto_id)
        ingredientes = _get_ingredientes_from_producto(self.session, producto_id)

        return {
            "producto": producto,
            "categorias": categorias,
            "ingredientes": ingredientes,
        }