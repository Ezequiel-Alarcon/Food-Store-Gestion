"""
app.modules.categorias.repository

Repository para operaciones de categorías jerárquicas.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Session, select
from sqlalchemy import text

from app.core.repository import BaseRepository
from app.modules.categorias.model import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    """
    Repository para operaciones de categorías.

    Hereda de BaseRepository y agrega métodos específicos para jerarquía.
    """

    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_by_slug(self, slug: str) -> Optional[Categoria]:
        """Busca una categoría por slug."""
        stmt = select(Categoria).where(
            Categoria.slug == slug,
            Categoria.eliminado_en == None,
        )
        return self.session.exec(stmt).first()

    def get_by_id_with_trash(self, entity_id: int) -> Optional[Categoria]:
        """Obtiene categoría incluyendo eliminadas (para soft-delete cascade)."""
        return self.session.get(Categoria, entity_id)

    def get_by_id_active(self, entity_id: int) -> Optional[Categoria]:
        """Obtiene categoría solo si está activa."""
        stmt = select(Categoria).where(
            Categoria.id == entity_id,
            Categoria.eliminado_en == None,
        )
        return self.session.exec(stmt).first()

    def get_children(self, parent_id: int) -> list[Categoria]:
        """Obtiene hijos directos de una categoría."""
        stmt = select(Categoria).where(
            Categoria.padre_id == parent_id,
            Categoria.eliminado_en == None,
        ).order_by(Categoria.orden, Categoria.nombre)
        return list(self.session.exec(stmt).all())

    def get_descendants_cte(
        self, category_id: int, max_depth: Optional[int] = None
    ) -> list[Categoria]:
        """
        Obtiene todos los descendientes de una categoría usando CTE recursivo.

        Args:
            category_id: ID de la categoría raíz
            max_depth: Profundidad máxima (None = sin límite)

        Returns:
            Lista de categorías descendientes
        """
        # Usamos texto plano para el CTE ya que SQLModel no tiene soporte directo
        if max_depth is not None:
            cte_query = text("""
            WITH RECURSIVE descendants AS (
                SELECT id, nombre, slug, descripcion, padre_id, orden, eliminado_en, created_at, updated_at, 1 as depth
                FROM categorias
                WHERE id = :category_id AND eliminado_en IS NULL

                UNION ALL

                SELECT c.id, c.nombre, c.slug, c.descripcion, c.padre_id, c.orden, c.eliminado_en, c.created_at, c.updated_at, d.depth + 1
                FROM categorias c
                INNER JOIN descendants d ON c.padre_id = d.id
                WHERE c.eliminado_en IS NULL AND d.depth <= :max_depth
            )
            SELECT id, nombre, slug, descripcion, padre_id, orden, eliminado_en, created_at, updated_at
            FROM descendants
            WHERE id != :category_id_exclude
            """).bindparams(category_id=category_id, max_depth=max_depth, category_id_exclude=category_id)
            result = self.session.exec(cte_query)
        else:
            cte_query = text("""
            WITH RECURSIVE descendants AS (
                SELECT id, nombre, slug, descripcion, padre_id, orden, eliminado_en, created_at, updated_at, 1 as depth
                FROM categorias
                WHERE id = :category_id AND eliminado_en IS NULL

                UNION ALL

                SELECT c.id, c.nombre, c.slug, c.descripcion, c.padre_id, c.orden, c.eliminado_en, c.created_at, c.updated_at, d.depth + 1
                FROM categorias c
                INNER JOIN descendants d ON c.padre_id = d.id
                WHERE c.eliminado_en IS NULL
            )
            SELECT id, nombre, slug, descripcion, padre_id, orden, eliminado_en, created_at, updated_at
            FROM descendants
            WHERE id != :category_id_exclude
            """).bindparams(category_id=category_id, category_id_exclude=category_id)
            result = self.session.exec(cte_query)
        rows = result.fetchall()

        if not rows:
            return []

        # Mapear resultados a objetos Categoria
        categorias = []
        for row in rows:
            cat = Categoria(
                id=row[0],
                nombre=row[1],
                slug=row[2],
                descripcion=row[3],
                padre_id=row[4],
                orden=row[5],
                eliminado_en=row[6],
                created_at=row[7],
                updated_at=row[8],
            )
            categorias.append(cat)

        return categorias

    def check_cycle(self, category_id: int, new_parent_id: int) -> bool:
        """
        Verifica si establecer new_parent_id como padre de category_id crearía un ciclo.

        Un ciclo se forma si new_parent_id es un descendiente de category_id.

        Returns:
            True si hay ciclo, False si es seguro
        """
        if category_id == new_parent_id:
            return True

        # Buscar si new_parent_id es descendiente de category_id
        descendants = self.get_descendants_cte(category_id)
        descendant_ids = {desc.id for desc in descendants}

        return new_parent_id in descendant_ids

    def soft_delete_with_descendants(self, category_id: int) -> list[Categoria]:
        """
        Realiza soft-delete en cascada: marca como inactivas la categoría y todos sus descendientes.

        Uses direct SQL UPDATE to avoid ORM datetime serialization issues with CTE-mapped objects.

        Returns:
            Lista de categorías afectadas
        """
        # Obtener la categoría principal
        categoria = self.get_by_id_with_trash(category_id)
        if not categoria:
            return []

        affected = [categoria]

        # Obtener todos los descendientes
        descendants = self.get_descendants_cte(category_id)

        now = datetime.now(timezone.utc)

        # Marcar como inactivas usando SQL directo para evitar problemas de datetime con objetos ORM
        # Primero marcar descendientes
        if descendants:
            for desc in descendants:
                self.session.exec(
                    text("UPDATE categorias SET eliminado_en = :now WHERE id = :id").bindparams(now=now, id=desc.id)
                )
                affected.append(desc)

        # Marcar la categoría principal como inactiva
        self.session.exec(
            text("UPDATE categorias SET eliminado_en = :now WHERE id = :id").bindparams(now=now, id=category_id)
        )

        self.session.flush()
        return affected

    def get_siblings(self, parent_id: Optional[int], exclude_id: Optional[int] = None) -> list[Categoria]:
        """
        Obtiene hermanos de una categoría (mismo padre).

        Args:
            parent_id: ID del padre (None para categorías raíz)
            exclude_id: ID a excluir (para operaciones de update)
        """
        if parent_id is None:
            # Hermanos en la raíz
            stmt = select(Categoria).where(
                Categoria.padre_id == None,
                Categoria.eliminado_en == None,
            )
        else:
            stmt = select(Categoria).where(
                Categoria.padre_id == parent_id,
                Categoria.eliminado_en == None,
            )

        if exclude_id is not None:
            stmt = stmt.where(Categoria.id != exclude_id)

        stmt = stmt.order_by(Categoria.orden, Categoria.nombre)
        return list(self.session.exec(stmt).all())

    def get_all_active(self) -> list[Categoria]:
        """Obtiene todas las categorías activas."""
        stmt = select(Categoria).where(
            Categoria.eliminado_en == None,
        ).order_by(Categoria.padre_id, Categoria.orden, Categoria.nombre)
        return list(self.session.exec(stmt).all())

    def get_root_categories(self) -> list[Categoria]:
        """Obtiene categorías raíz (sin padre)."""
        stmt = select(Categoria).where(
            Categoria.padre_id == None,
            Categoria.eliminado_en == None,
        ).order_by(Categoria.orden, Categoria.nombre)
        return list(self.session.exec(stmt).all())

    def exists_by_name_and_parent(
        self, nombre: str, padre_id: Optional[int], exclude_id: Optional[int] = None
    ) -> bool:
        """Verifica si existe una categoría con el mismo nombre bajo el mismo padre."""
        if padre_id is None:
            stmt = select(Categoria).where(
                Categoria.nombre == nombre,
                Categoria.padre_id == None,
                Categoria.eliminado_en == None,
            )
        else:
            stmt = select(Categoria).where(
                Categoria.nombre == nombre,
                Categoria.padre_id == padre_id,
                Categoria.eliminado_en == None,
            )

        if exclude_id is not None:
            stmt = stmt.where(Categoria.id != exclude_id)

        return self.session.exec(stmt).first() is not None