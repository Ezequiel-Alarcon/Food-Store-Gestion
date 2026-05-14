"""
Tests de integración para CRUD de categorías.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session


class TestCategoriaCRUD:
    """Tests de integración para CRUD de /api/v1/categorias/"""

    def test_create_root_category(self, client: TestClient, create_admin_token):
        """Crear categoría raíz debe devolver 201."""
        response = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas", "descripcion": "Platos principales"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Comidas"
        assert data["categoria_padre_id"] is None
        assert data["activa"] is True

    def test_create_child_category(self, client: TestClient, create_admin_token):
        """Crear categoría hija debe devolver 201."""
        # Crear padre
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        parent_id = parent_resp.json()["id"]

        # Crear hijo
        response = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["nombre"] == "Italiana"
        assert data["categoria_padre_id"] == parent_id

    def test_create_duplicate_name_same_level(self, client: TestClient, create_admin_token):
        """Crear categoría con nombre duplicado en mismo nivel debe devolver 409."""
        # Crear padre
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        parent_id = parent_resp.json()["id"]

        # Primera categoría
        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        # Duplicate
        response = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 409
        assert "nombre" in str(response.json()["detail"]).lower()

    def test_create_invalid_parent(self, client: TestClient, create_admin_token):
        """Crear categoría con padre inválido debe devolver 404."""
        response = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Test", "categoria_padre_id": 9999},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 404
        assert "padre" in str(response.json()["detail"]).lower()

    def test_list_all_active_categories(self, client: TestClient, create_admin_token):
        """Listar todas las categorías debe devolver solo las activas."""
        # Crear algunas categorías
        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Bebidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        response = client.get(
            "/api/v1/categorias/",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 2
        # Verificar que todos son activos
        assert all(cat["activa"] for cat in data)

    def test_get_single_category(self, client: TestClient, create_admin_token):
        """Obtener una categoría por ID debe devolver los datos completos."""
        # Crear categoría
        create_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Test Category"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        cat_id = create_resp.json()["id"]

        response = client.get(
            f"/api/v1/categorias/{cat_id}",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == cat_id
        assert data["nombre"] == "Test Category"

    def test_get_nonexistent_category(self, client: TestClient, create_admin_token):
        """Obtener categoría inexistente debe devolver 404."""
        response = client.get(
            "/api/v1/categorias/9999",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 404

    def test_update_category(self, client: TestClient, create_admin_token):
        """Actualizar categoría debe devolver los datos actualizados."""
        # Crear categoría
        create_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Old Name"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        cat_id = create_resp.json()["id"]

        # Actualizar
        response = client.put(
            f"/api/v1/categorias/{cat_id}",
            json={"nombre": "New Name"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["nombre"] == "New Name"

    def test_soft_delete(self, client: TestClient, create_admin_token):
        """Soft-delete debe marcar la categoría como inactiva."""
        # Crear categoría
        create_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "To Delete"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        cat_id = create_resp.json()["id"]

        # Eliminar
        response = client.delete(
            f"/api/v1/categorias/{cat_id}",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 204

        # Verificar que la categoría ya no es accesible via GET (soft-delete la oculta)
        get_response = client.get(
            f"/api/v1/categorias/{cat_id}",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        # El soft-delete marca activa=False y el endpoint GET filtra por activa=True → 404
        assert get_response.status_code == 404

    def test_soft_delete_cascade(self, client: TestClient, create_admin_token):
        """Soft-delete debe propagarse a los descendientes."""
        # Crear jerarquía: Comidas -> Italiana -> Pizzas
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        parent_id = parent_resp.json()["id"]

        child_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        child_id = child_resp.json()["id"]

        grandchild_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Pizzas", "categoria_padre_id": child_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        grandchild_id = grandchild_resp.json()["id"]

        # Eliminar padre
        response = client.delete(
            f"/api/v1/categorias/{parent_id}",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 204

        # Verificar que todos están inactivos (invisibles via GET normal)
        for check_id in [parent_id, child_id, grandchild_id]:
            get_resp = client.get(
                f"/api/v1/categorias/{check_id}",
                headers={"Authorization": f"Bearer {create_admin_token}"},
            )
            # El soft-delete marca activa=False → el endpoint GET filtra por activa=True → 404
            assert get_resp.status_code == 404


# Fixture para crear token de admin
@pytest.fixture(name="create_admin_token")
def fixture_create_admin_token(session: Session):
    """Crea un usuario admin directamente en BD y devuelve su token JWT."""
    from app.core.security import create_access_token, hash_password
    from app.modules.auth.model import Usuario

    admin = Usuario(
        email="admin_test@example.com",
        nombre="Admin",
        apellido="Test",
        password_hash=hash_password("Admin123!"),
        rol="ADMIN",
        activo=True,
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)

    token = create_access_token(data={"sub": str(admin.id), "rol": admin.rol})
    return token