"""
Tests de integración para jerarquía de categorías.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestCategoriaHierarchy:
    """Tests de integración para jerarquía de categorías."""

    def test_get_full_tree_structure(self, client: TestClient, create_admin_token):
        """Obtener árbol completo debe devolver estructura anidada."""
        # Crear estructura: Comidas -> Italiana -> Pizzas, Bebidas -> Alcohol
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        parent_id = parent_resp.json()["id"]

        child1_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        child1_id = child1_resp.json()["id"]

        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Pizzas", "categoria_padre_id": child1_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        # Bebidas
        bebidas_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Bebidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        bebidas_id = bebidas_resp.json()["id"]

        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Con Alcohol", "categoria_padre_id": bebidas_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        response = client.get(
            "/api/v1/categorias/arbol",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()

        # Verificar estructura
        assert len(data) == 2  # Comidas y Bebidas

        # Buscar Comidas
        comidas = next(cat for cat in data if cat["nombre"] == "Comidas")
        assert len(comidas["hijos"]) == 1
        assert comidas["hijos"][0]["nombre"] == "Italiana"
        assert len(comidas["hijos"][0]["hijos"]) == 1
        assert comidas["hijos"][0]["hijos"][0]["nombre"] == "Pizzas"

    def test_empty_tree(self, client: TestClient, create_admin_token):
        """Árbol vacío debe devolver array vacío."""
        response = client.get(
            "/api/v1/categorias/arbol",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    def test_get_subcategorias_with_depth(self, client: TestClient, create_admin_token):
        """Obtener subcategorías con profundidad debe limitar la profundidad."""
        # Crear: Comidas -> Italiana -> Pizzas -> Napolitana
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        parent_id = parent_resp.json()["id"]

        child1_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": parent_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        child1_id = child1_resp.json()["id"]

        child2_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Pizzas", "categoria_padre_id": child1_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        child2_id = child2_resp.json()["id"]

        client.post(
            "/api/v1/categorias/",
            json={"nombre": "Napolitana", "categoria_padre_id": child2_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        # Obtener con profundidad 2
        response = client.get(
            f"/api/v1/categorias/{parent_id}/subcategorias?profundidad=2",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        # Debe devolver Italiana y Pizzas, pero no Napolitana (nivel 3)
        nombres = [cat["nombre"] for cat in data]
        assert "Italiana" in nombres
        assert "Pizzas" in nombres
        assert "Napolitana" not in nombres

    def test_cycle_prevention_self_parent(self, client: TestClient, create_admin_token):
        """No se puede establecer una categoría como su propio padre."""
        # Crear categoría
        create_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Test"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        cat_id = create_resp.json()["id"]

        # Intentar setear como su propio padre
        response = client.put(
            f"/api/v1/categorias/{cat_id}",
            json={"categoria_padre_id": cat_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 400
        assert "ciclo" in str(response.json()["detail"]).lower() or "descendente" in str(response.json()["detail"]).lower()

    def test_cycle_prevention_descendant_as_parent(self, client: TestClient, create_admin_token):
        """No se puede establecer un descendiente como padre."""
        # Crear: Comidas -> Italiana -> Pizzas
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

        # Intentar hacer Pizzas padre de Comidas (crearía ciclo)
        response = client.put(
            f"/api/v1/categorias/{parent_id}",
            json={"categoria_padre_id": grandchild_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 400

    def test_move_category_to_different_branch(self, client: TestClient, create_admin_token):
        """Se puede mover una categoría a diferente rama."""
        # Crear: Comidas -> Italiana, Bebidas
        parent_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Comidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        comidas_id = parent_resp.json()["id"]

        italiana_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Italiana", "categoria_padre_id": comidas_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        italiana_id = italiana_resp.json()["id"]

        bebidas_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Bebidas"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        bebidas_id = bebidas_resp.json()["id"]

        # Mover Italiana bajo Bebidas
        response = client.put(
            f"/api/v1/categorias/{italiana_id}",
            json={"categoria_padre_id": bebidas_id},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["categoria_padre_id"] == bebidas_id

    def test_public_tree_no_auth(self, client: TestClient):
        """El árbol público no requiere autenticación."""
        # Intentar acceder sin token
        response = client.get("/api/v1/categorias/publico/arbol")

        assert response.status_code == 200

    def test_leaf_category_subcategorias(self, client: TestClient, create_admin_token):
        """Categoría sin hijos devuelve array vacío."""
        # Crear categoría sin hijos
        create_resp = client.post(
            "/api/v1/categorias/",
            json={"nombre": "Leaf"},
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )
        cat_id = create_resp.json()["id"]

        response = client.get(
            f"/api/v1/categorias/{cat_id}/subcategorias",
            headers={"Authorization": f"Bearer {create_admin_token}"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data == []


# Fixture para crear token de admin
@pytest.fixture(name="create_admin_token")
def fixture_create_admin_token(client: TestClient):
    """Crea un usuario admin y devuelve su token."""
    from app.core.security import create_access_token

    token = create_access_token({"sub": "1", "email": "admin@test.com", "role": "ADMIN"})
    return token