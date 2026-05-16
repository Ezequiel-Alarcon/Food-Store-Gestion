"""Tests unitarios para AdminService con session mockeada.

Verifica:
  - get_general_metrics pasa filtros al repo
  - get_sales_chart pasa filtros al repo
  - get_top_products pasa filtros y limit al repo
  - get_orders_by_status pasa filtros al repo
  - get_total_usuarios_registrados delega al repo
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

import pytest

from app.modules.admin.service import AdminService
from app.modules.admin.schemas import GeneralMetricsResponse


@pytest.fixture(name="mock_session")
def fixture_mock_session():
    return MagicMock()


@pytest.fixture(name="service")
def fixture_service(mock_session):
    return AdminService(mock_session)


# ── get_general_metrics ────────────────────────────────────────────────

def test_get_general_metrics_sin_filtros(service, mock_session):
    """Sin filtros, llama al repo sin parámetros."""
    with patch.object(service.repo, "get_general_metrics", return_value={
        "total_pedidos": 10,
        "total_revenue": 5000.0,
        "ticket_promedio": 500.0,
        "total_clientes": 5,
    }) as mock_repo:
        result = service.get_general_metrics()

        mock_repo.assert_called_once_with(desde=None, hasta=None)
        assert isinstance(result, GeneralMetricsResponse)
        assert result.total_pedidos == 10


def test_get_general_metrics_con_filtros(service, mock_session):
    """Con filtros, pasa desde/hasta al repo."""
    desde = datetime.now(timezone.utc) - timedelta(days=30)
    hasta = datetime.now(timezone.utc)

    with patch.object(service.repo, "get_general_metrics", return_value={
        "total_pedidos": 5,
        "total_revenue": 2500.0,
        "ticket_promedio": 500.0,
        "total_clientes": 3,
    }) as mock_repo:
        result = service.get_general_metrics(desde=desde, hasta=hasta)

        mock_repo.assert_called_once_with(desde=desde, hasta=hasta)
        assert result.total_pedidos == 5


# ── get_sales_chart ───────────────────────────────────────────────────

def test_get_sales_chart_sin_filtros(service, mock_session):
    """Sin filtros, llama al repo sin parámetros."""
    with patch.object(service.repo, "get_sales_chart", return_value=[]) as mock_repo:
        result = service.get_sales_chart()

        mock_repo.assert_called_once_with(desde=None, hasta=None)
        assert result.dias == 30
        assert result.datos == []


def test_get_sales_chart_con_filtros(service, mock_session):
    """Con filtros, pasa desde/hasta al repo."""
    desde = datetime.now(timezone.utc) - timedelta(days=14)
    hasta = datetime.now(timezone.utc)

    with patch.object(service.repo, "get_sales_chart", return_value=[]) as mock_repo:
        result = service.get_sales_chart(desde=desde, hasta=hasta)

        mock_repo.assert_called_once_with(desde=desde, hasta=hasta)


# ── get_top_products ──────────────────────────────────────────────────

def test_get_top_products_sin_filtros(service, mock_session):
    """Sin filtros, usa limit default."""
    with patch.object(service.repo, "get_top_products", return_value=[]) as mock_repo:
        result = service.get_top_products()

        mock_repo.assert_called_once_with(limit=10, desde=None, hasta=None)


def test_get_top_products_con_filtros(service, mock_session):
    """Con filtros, pasa todos los parámetros."""
    desde = datetime.now(timezone.utc) - timedelta(days=7)
    hasta = datetime.now(timezone.utc)

    with patch.object(service.repo, "get_top_products", return_value=[]) as mock_repo:
        result = service.get_top_products(limit=5, desde=desde, hasta=hasta)

        mock_repo.assert_called_once_with(limit=5, desde=desde, hasta=hasta)


# ── get_orders_by_status ──────────────────────────────────────────────

def test_get_orders_by_status_sin_filtros(service, mock_session):
    """Sin filtros, llama al repo sin parámetros."""
    with patch.object(service.repo, "get_orders_by_status", return_value=[]) as mock_repo:
        result = service.get_orders_by_status()

        mock_repo.assert_called_once_with(desde=None, hasta=None)


def test_get_orders_by_status_con_filtros(service, mock_session):
    """Con filtros, pasa desde/hasta al repo."""
    desde = datetime.now(timezone.utc) - timedelta(days=30)
    hasta = datetime.now(timezone.utc)

    with patch.object(service.repo, "get_orders_by_status", return_value=[]) as mock_repo:
        result = service.get_orders_by_status(desde=desde, hasta=hasta)

        mock_repo.assert_called_once_with(desde=desde, hasta=hasta)


# ── get_total_usuarios_registrados ────────────────────────────────────

def test_get_total_usuarios_registrados(service, mock_session):
    """Delega al repo y retorna el conteo."""
    with patch.object(service.repo, "get_total_usuarios_registrados", return_value=42) as mock_repo:
        result = service.get_total_usuarios_registrados()

        mock_repo.assert_called_once()
        assert result == 42
