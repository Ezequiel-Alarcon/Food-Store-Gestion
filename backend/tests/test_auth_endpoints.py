"""
Tests de integración para endpoints de autenticación.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


class TestAuthEndpoints:
    """Tests de integración para /api/v1/auth/"""

    def test_health_check(self, client: TestClient):
        """Verificar que el health endpoint funciona."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_register_success(self, client: TestClient):
        """Registro exitoso debe devolver 201 y tokens."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "integ@example.com",
                "password": "Password1",
                "nombre": "Integration User",
            },
        )

        data = response.json()
        assert response.status_code == 201
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_register_duplicate_email(self, client: TestClient):
        """Registro con email duplicado debe devolver 409."""
        payload = {
            "email": "dup@example.com",
            "password": "Password1",
            "nombre": "First User",
        }
        client.post("/api/v1/auth/register", json=payload)
        response = client.post("/api/v1/auth/register", json=payload)

        assert response.status_code == 409
        assert "ya está registrado" in str(response.json()["detail"])

    def test_register_invalid_email(self, client: TestClient):
        """Registro con email inválido debe devolver 422."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "not-an-email",
                "password": "Password1",
                "nombre": "Bad Email",
            },
        )
        assert response.status_code == 422

    def test_register_weak_password(self, client: TestClient):
        """Registro con contraseña corta debe devolver 422."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "weak@example.com",
                "password": "123",
                "nombre": "Weak Pass",
            },
        )
        assert response.status_code == 422

    def test_login_success(self, client: TestClient):
        """Login exitoso debe devolver tokens."""
        # Registrar primero
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "login@example.com",
                "password": "Password1",
                "nombre": "Login User",
            },
        )

        # Login
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "login@example.com", "password": "Password1"},
        )

        data = response.json()
        assert response.status_code == 200
        assert "access_token" in data
        assert "refresh_token" in data

    def test_login_wrong_password(self, client: TestClient):
        """Login con password incorrecto debe devolver 401."""
        client.post(
            "/api/v1/auth/register",
            json={
                "email": "wrong@example.com",
                "password": "Password1",
                "nombre": "Wrong",
            },
        )

        response = client.post(
            "/api/v1/auth/login",
            json={"email": "wrong@example.com", "password": "WrongPass"},
        )
        assert response.status_code == 401

    def test_refresh_token(self, client: TestClient):
        """Refresh token válido debe devolver nuevos tokens."""
        register_resp = client.post(
            "/api/v1/auth/register",
            json={
                "email": "refresh@example.com",
                "password": "Password1",
                "nombre": "Refresh User",
            },
        )
        refresh_token = register_resp.json()["refresh_token"]

        response = client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_logout(self, client: TestClient):
        """Logout debe ser exitoso."""
        register_resp = client.post(
            "/api/v1/auth/register",
            json={
                "email": "logout@example.com",
                "password": "Password1",
                "nombre": "Logout User",
            },
        )
        refresh_token = register_resp.json()["refresh_token"]

        response = client.post(
            "/api/v1/auth/logout",
            json={"refresh_token": refresh_token},
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Sesión cerrada correctamente"
