"""Tests para schemas PedidoDetailResponse y PedidoHistorialEntry.

Verifica:
  - PedidoDetailItem se construye correctamente
  - PedidoDetailResponse acepta todos los campos
  - PedidoDetailResponse maneja valores None
  - PedidoHistorialEntry se construye correctamente
  - PedidoHistorialEntry maneja valores None
  - GeneralMetricsResponse incluye total_usuarios
"""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from app.modules.admin.schemas import (
    GeneralMetricsResponse,
    OrdersByStatusEntry,
    PedidoDetailItem,
    PedidoDetailResponse,
    PedidoHistorialEntry,
    SalesChartEntry,
    SalesChartResponse,
    TopProductEntry,
)


# ── PedidoDetailItem ─────────────────────────────────────────────────

def test_pedido_detail_item_completo():
    """PedidoDetailItem con todos los campos."""
    item = PedidoDetailItem(
        id=1,
        producto_id=10,
        cantidad=2,
        precio_unitario=50.0,
        exclusiones=[1, 2, 3],
    )

    assert item.id == 1
    assert item.producto_id == 10
    assert item.cantidad == 2
    assert item.precio_unitario == 50.0
    assert item.exclusiones == [1, 2, 3]


def test_pedido_detail_item_exclusiones_default():
    """PedidoDetailItem sin exclusiones usa lista vacía."""
    item = PedidoDetailItem(
        id=1,
        producto_id=10,
        cantidad=1,
        precio_unitario=25.0,
    )

    assert item.exclusiones == []


# ── PedidoDetailResponse ─────────────────────────────────────────────

def test_pedido_detail_response_completo():
    """PedidoDetailResponse con todos los campos."""
    now = datetime.now(timezone.utc)
    item = PedidoDetailItem(id=1, producto_id=10, cantidad=2, precio_unitario=50.0)

    response = PedidoDetailResponse(
        id=100,
        cliente_id=5,
        estado_codigo="ENTREGADO",
        cliente_email="test@test.com",
        cliente_nombre="Juan",
        cliente_apellido="Pérez",
        direccion_calle="Calle",
        direccion_numero="123",
        direccion_piso_depto="2B",
        direccion_ciudad="Buenos Aires",
        direccion_provincia="CABA",
        direccion_codigo_postal="1000",
        direccion_pais="Argentina",
        direccion_referencias="Frente a la plaza",
        total=150.0,
        costo_envio=10.0,
        items=[item],
        creado_en=now,
        actualizado_en=now,
    )

    assert response.id == 100
    assert response.cliente_email == "test@test.com"
    assert len(response.items) == 1
    assert response.total == 150.0


def test_pedido_detail_response_valores_none():
    """PedidoDetailResponse maneja campos opcionales como None."""
    response = PedidoDetailResponse(
        id=100,
        cliente_id=5,
        estado_codigo="PENDIENTE",
        cliente_email=None,
        cliente_nombre=None,
        cliente_apellido=None,
        direccion_calle="Test",
        direccion_numero="123",
        direccion_piso_depto=None,
        direccion_ciudad="Test",
        direccion_provincia="Test",
        direccion_codigo_postal=None,
        direccion_pais="Argentina",
        direccion_referencias=None,
        total=100.0,
        costo_envio=None,
        items=[],
        creado_en=None,
        actualizado_en=None,
    )

    assert response.cliente_email is None
    assert response.costo_envio is None
    assert response.creado_en is None
    assert response.items == []


# ── PedidoHistorialEntry ─────────────────────────────────────────────

def test_pedido_historial_entry_completo():
    """PedidoHistorialEntry con todos los campos."""
    now = datetime.now(timezone.utc)

    entry = PedidoHistorialEntry(
        id=1,
        estado_anterior_codigo="PENDIENTE",
        estado_nuevo_codigo="CONFIRMADO",
        actor_id=5,
        actor_tipo="USUARIO",
        motivo="Pedido confirmado",
        creado_en=now,
    )

    assert entry.id == 1
    assert entry.estado_anterior_codigo == "PENDIENTE"
    assert entry.estado_nuevo_codigo == "CONFIRMADO"
    assert entry.actor_tipo == "USUARIO"


def test_pedido_historial_entry_estado_anterior_none():
    """PedidoHistorialEntry para primer estado (sin anterior)."""
    entry = PedidoHistorialEntry(
        id=1,
        estado_anterior_codigo=None,
        estado_nuevo_codigo="PENDIENTE",
        actor_id=None,
        actor_tipo="SISTEMA",
        motivo=None,
        creado_en=datetime.now(timezone.utc),
    )

    assert entry.estado_anterior_codigo is None
    assert entry.actor_id is None
    assert entry.motivo is None


# ── GeneralMetricsResponse ───────────────────────────────────────────

def test_general_metrics_incluye_total_usuarios():
    """GeneralMetricsResponse incluye campo total_usuarios."""
    metrics = GeneralMetricsResponse(
        total_pedidos=10,
        total_revenue=5000.0,
        ticket_promedio=500.0,
        total_clientes=5,
        total_usuarios=42,
    )

    assert metrics.total_usuarios == 42


def test_general_metrics_todos_los_campos():
    """GeneralMetricsResponse con todos los campos."""
    metrics = GeneralMetricsResponse(
        total_pedidos=0,
        total_revenue=0.0,
        ticket_promedio=0.0,
        total_clientes=0,
        total_usuarios=0,
    )

    assert metrics.total_pedidos == 0
    assert metrics.total_revenue == 0.0
    assert metrics.ticket_promedio == 0.0
    assert metrics.total_clientes == 0
    assert metrics.total_usuarios == 0


# ── Schemas existentes (regresión) ───────────────────────────────────

def test_sales_chart_entry():
    """SalesChartEntry se construye correctamente."""
    entry = SalesChartEntry(
        fecha=datetime.now(timezone.utc),
        total_pedidos=5,
        revenue=250.0,
    )

    assert entry.total_pedidos == 5
    assert entry.revenue == 250.0


def test_sales_chart_response():
    """SalesChartResponse se construye correctamente."""
    response = SalesChartResponse(
        datos=[],
        dias=30,
    )

    assert response.dias == 30
    assert response.datos == []


def test_top_product_entry():
    """TopProductEntry se construye correctamente."""
    entry = TopProductEntry(
        producto_id=1,
        nombre="Pizza",
        cantidad_vendida=100,
    )

    assert entry.producto_id == 1
    assert entry.cantidad_vendida == 100


def test_orders_by_status_entry():
    """OrdersByStatusEntry se construye correctamente."""
    entry = OrdersByStatusEntry(
        estado_codigo="ENTREGADO",
        cantidad=10,
    )

    assert entry.estado_codigo == "ENTREGADO"
    assert entry.cantidad == 10
