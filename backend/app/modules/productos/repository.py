"""
app.modules.productos.repository

Repository para operaciones de productos.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select, func

from app.core.repository import BaseRepository
from app.modules.ingredientes.model import Ingrediente
from app.modules.productos.model import Producto, ProductoCategoria, ProductoIngrediente


class ProductoRepository(BaseRepository[Producto]):
    """
    Repository para operaciones de productos.

    Hereda de BaseRepository y agrega métodos específicos para productos.
    """

    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_by_id_active(self, entity_id: int) -> Optional[Producto]:
        """Obtiene producto solo si está activo y no eliminado."""
        stmt = select(Producto).where(
            Producto.id == entity_id,
            Producto.activo == True,
            Producto.eliminado_en == None,
        )
        return self.session.exec(stmt).first()

    def get_by_id_with_trash(self, entity_id: int) -> Optional[Producto]:
        """Obtiene producto incluyendo eliminados (para admin)."""
        return self.session.get(Producto, entity_id)

    def get_all_active(
        self,
        skip: int = 0,
        limit: int = 20,
        categoria_id: Optional[int] = None,
    ) -> tuple[list[Producto], int]:
        """
        Obtiene todos los productos activos con paginación.

        Returns:
            Tupla (lista de productos, total)
        """
        # Base query: productos activos y no eliminados
        base_stmt = select(Producto).where(
            Producto.activo == True,
            Producto.eliminado_en == None,
        )

        # Si hay filtro de categoría, joins con la tabla de relación
        if categoria_id is not None:
            base_stmt = (
                base_stmt
                .join(ProductoCategoria, Producto.id == ProductoCategoria.producto_id)
                .where(ProductoCategoria.categoria_id == categoria_id)
            )

        # Contar total
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = self.session.exec(count_stmt).first() or 0

        # Obtener resultados con paginación
        stmt = base_stmt.order_by(Producto.nombre).offset(skip).limit(limit)
        productos = list(self.session.exec(stmt).all())

        return productos, total

    def get_catalogo_publico(
        self,
        skip: int = 0,
        limit: int = 20,
        categoria_id: Optional[int] = None,
        disponibles_only: bool = True,
        excluir_alergenos: bool = False,
        ingrediente_ids_excluir: Optional[list[int]] = None,
    ) -> tuple[list[Producto], int]:
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
            Tupla (lista de productos, total)
        """
        # Productos activos y no eliminados
        base_stmt = select(Producto).where(
            Producto.activo == True,
            Producto.eliminado_en == None,
        )

        # Filtro: solo disponibles (stock > 0)
        if disponibles_only:
            base_stmt = base_stmt.where(Producto.stock > 0)

        # Filtro: categoría
        if categoria_id is not None:
            base_stmt = (
                base_stmt
                .join(ProductoCategoria, Producto.id == ProductoCategoria.producto_id)
                .where(ProductoCategoria.categoria_id == categoria_id)
            )

        # Filtro: excluir alérgenos
        # Este requiere un subquery para verificar si el producto tiene ingredientes alérgenos
        if excluir_alergenos:
            # Subquery: productos que tienen al menos un ingrediente alérgeno
            productos_con_alergenos = (
                select(ProductoIngrediente.producto_id)
                .join(
                    Ingrediente,
                    ProductoIngrediente.ingrediente_id == Ingrediente.id,
                )
                .where(Ingrediente.es_alergeno == True)
            )
            base_stmt = base_stmt.where(
                Producto.id.not_in(productos_con_alergenos)
            )

        # Filtro: excluir ingredientes específicos
        if ingrediente_ids_excluir and len(ingrediente_ids_excluir) > 0:
            productos_con_ingredientes = (
                select(ProductoIngrediente.producto_id)
                .where(ProductoIngrediente.ingrediente_id.in_(ingrediente_ids_excluir))
            )
            base_stmt = base_stmt.where(
                Producto.id.not_in(productos_con_ingredientes)
            )

        # Contar total
        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total = self.session.exec(count_stmt).first() or 0

        # Obtener resultados con paginación
        stmt = base_stmt.order_by(Producto.nombre).offset(skip).limit(limit)
        productos = list(self.session.exec(stmt).all())

        return productos, total

    def get_by_categoria(self, categoria_id: int) -> list[Producto]:
        """Obtiene todos los productos de una categoría específica."""
        stmt = (
            select(Producto)
            .join(ProductoCategoria, Producto.id == ProductoCategoria.producto_id)
            .where(
                ProductoCategoria.categoria_id == categoria_id,
                Producto.activo == True,
                Producto.eliminado_en == None,
            )
            .order_by(Producto.nombre)
        )
        return list(self.session.exec(stmt).all())

    def update_stock(self, producto_id: int, nueva_cantidad: int) -> Optional[Producto]:
        """
        Actualiza el stock de un producto.

        Args:
            producto_id: ID del producto
            nueva_cantidad: Nueva cantidad de stock

        Returns:
            Producto actualizado o None si no existe
        """
        producto = self.get_by_id_with_trash(producto_id)
        if producto is None:
            return None

        producto.stock = nueva_cantidad
        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()
        return producto

    def add_stock(self, producto_id: int, cantidad: int) -> Optional[Producto]:
        """Agrega stock a un producto."""
        producto = self.get_by_id_with_trash(producto_id)
        if producto is None:
            return None

        producto.stock += cantidad
        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()
        return producto

    def subtract_stock(self, producto_id: int, cantidad: int) -> Optional[Producto]:
        """Resta stock a un producto (verificando que no quede negativo)."""
        producto = self.get_by_id_with_trash(producto_id)
        if producto is None:
            return None

        if producto.stock < cantidad:
            return None  # No hay suficiente stock

        producto.stock -= cantidad
        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()
        return producto

    def soft_delete(self, producto_id: int) -> Optional[Producto]:
        """
        Realiza soft-delete de un producto.

        Returns:
            Producto marcado como eliminado o None si no existe
        """
        producto = self.get_by_id_with_trash(producto_id)
        if producto is None:
            return None

        producto.eliminado_en = datetime.now(timezone.utc)
        producto.activo = False
        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()
        return producto

    def restore(self, producto_id: int) -> Optional[Producto]:
        """
        Restaura un producto eliminado (soft-delete reversed).

        Returns:
            Producto restaurado o None si no existe
        """
        producto = self.get_by_id_with_trash(producto_id)
        if producto is None or producto.eliminado_en is None:
            return None

        producto.eliminado_en = None
        producto.activo = True
        producto.actualizado_en = datetime.now(timezone.utc)
        self.session.add(producto)
        self.session.flush()
        return producto

    def add_categoria(self, producto_id: int, categoria_id: int) -> None:
        """Asocia una categoría a un producto."""
        relacion = ProductoCategoria(producto_id=producto_id, categoria_id=categoria_id)
        self.session.add(relacion)
        self.session.flush()

    def remove_categoria(self, producto_id: int, categoria_id: int) -> None:
        """Desasocia una categoría de un producto."""
        stmt = select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id,
            ProductoCategoria.categoria_id == categoria_id,
        )
        relacion = self.session.exec(stmt).first()
        if relacion:
            self.session.delete(relacion)
            self.session.flush()

    def set_categorias(self, producto_id: int, categoria_ids: list[int]) -> None:
        """Reemplaza todas las categorías de un producto."""
        # Eliminar relaciones existentes
        stmt = select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id
        )
        relaciones = self.session.exec(stmt).all()
        for rel in relaciones:
            self.session.delete(rel)

        # Agregar nuevas relaciones
        for cat_id in categoria_ids:
            rel = ProductoCategoria(producto_id=producto_id, categoria_id=cat_id)
            self.session.add(rel)

        self.session.flush()

    def add_ingrediente(self, producto_id: int, ingrediente_id: int) -> None:
        """Asocia un ingrediente a un producto."""
        relacion = ProductoIngrediente(
            producto_id=producto_id, ingrediente_id=ingrediente_id
        )
        self.session.add(relacion)
        self.session.flush()

    def remove_ingrediente(self, producto_id: int, ingrediente_id: int) -> None:
        """Desasocia un ingrediente de un producto."""
        stmt = select(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id,
            ProductoIngrediente.ingrediente_id == ingrediente_id,
        )
        relacion = self.session.exec(stmt).first()
        if relacion:
            self.session.delete(relacion)
            self.session.flush()

    def set_ingredientes(self, producto_id: int, ingrediente_ids: list[int]) -> None:
        """Reemplaza todos los ingredientes de un producto."""
        # Eliminar relaciones existentes
        stmt = select(ProductoIngrediente).where(
            ProductoIngrediente.producto_id == producto_id
        )
        relaciones = self.session.exec(stmt).all()
        for rel in relaciones:
            self.session.delete(rel)

        # Agregar nuevas relaciones
        for ing_id in ingrediente_ids:
            rel = ProductoIngrediente(producto_id=producto_id, ingrediente_id=ing_id)
            self.session.add(rel)

        self.session.flush()

    def get_categorias(self, producto_id: int) -> list:
        """Obtiene las categorías asociadas a un producto."""
        from app.modules.categorias.model import Categoria
        stmt = (
            select(Categoria)
            .join(
                ProductoCategoria,
                ProductoCategoria.categoria_id == Categoria.id,
            )
            .where(ProductoCategoria.producto_id == producto_id)
        )
        return list(self.session.exec(stmt).all())

    def get_ingredientes(self, producto_id: int) -> list:
        """Obtiene los ingredientes asociados a un producto."""
        from app.modules.ingredientes.model import Ingrediente
        stmt = (
            select(Ingrediente)
            .join(
                ProductoIngrediente,
                ProductoIngrediente.ingrediente_id == Ingrediente.id,
            )
            .where(ProductoIngrediente.producto_id == producto_id)
        )
        return list(self.session.exec(stmt).all())