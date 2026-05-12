"""app.modules.pedidos.fsm

Motor de la máquina de estados (FSM) de pedidos.

La transición PENDIENTE→CONFIRMADO está reservada para el webhook de pagos
(payments-integration). No se expone en este módulo.

Códigos de estado (según seed): PENDIENTE, CONFIRMADO, EN_PREP, EN_CAMINO,
ENTREGADO, CANCELADO.
"""
from __future__ import annotations

from app.core.exceptions import ForbiddenError, ValidationError

TRANSICIONES_VALIDAS: dict[str, list[str]] = {
    "PENDIENTE": ["CANCELADO"],
    "CONFIRMADO": ["EN_PREP", "CANCELADO"],
    "EN_PREP": ["EN_CAMINO", "CANCELADO"],  # CANCELADO desde EN_PREP solo ADMIN
    "EN_CAMINO": ["ENTREGADO"],
    "ENTREGADO": [],
    "CANCELADO": [],
}

# Roles que pueden cancelar desde cada estado (RN-FS08, RN-RB08)
_CANCEL_ROLES: dict[str, set[str]] = {
    "PENDIENTE": {"CLIENT", "PEDIDOS", "ADMIN"},
    "CONFIRMADO": {"PEDIDOS", "ADMIN"},
    "EN_PREP": {"ADMIN"},
}


def validate_transition(estado_actual: str, estado_destino: str) -> None:
    """Valida que la transición sea válida según el mapa FSM.

    Lanza ValidationError si:
    - El estado destino es CONFIRMADO (reservado para webhook de pagos).
    - El estado actual es terminal (sin salidas).
    - La transición no está permitida.
    """
    if estado_destino == "CONFIRMADO":
        raise ValidationError(
            "La transición a CONFIRMADO es exclusiva del webhook de pagos (RN-FS02)"
        )

    transiciones = TRANSICIONES_VALIDAS.get(estado_actual)
    if transiciones is None:
        raise ValidationError(f"Estado desconocido: '{estado_actual}'")

    if not transiciones:
        raise ValidationError(
            f"El estado '{estado_actual}' es terminal; no se permiten más transiciones"
        )

    if estado_destino not in transiciones:
        raise ValidationError(
            f"Transición inválida: '{estado_actual}' → '{estado_destino}'. "
            f"Permitidas: {transiciones}"
        )


def check_cancel_permission(estado_actual: str, rol_actor: str) -> None:
    """Verifica que el rol del actor pueda cancelar el pedido desde el estado actual.

    Lanza ForbiddenError si el rol no tiene permiso (RN-FS08, RN-RB08).
    """
    roles_permitidos = _CANCEL_ROLES.get(estado_actual)
    if roles_permitidos is None:
        raise ForbiddenError(
            f"No se puede cancelar un pedido en estado '{estado_actual}'"
        )
    if rol_actor not in roles_permitidos:
        raise ForbiddenError(
            f"El rol '{rol_actor}' no tiene permiso para cancelar pedidos en estado '{estado_actual}'"
        )


def confirmar_pedido(estado_actual: str) -> None:
    """Valida que el pedido pueda ser confirmado por el SISTEMA (pago aprobado).
    
    Solo permite transicion PENDIENTE->CONFIRMADO.
    Lanza ValidationError si el estado actual no es PENDIENTE.
    """
    if estado_actual != "PENDIENTE":
        raise ValidationError(
            f"Solo pedidos PENDIENTE pueden confirmarse, estado actual: '{estado_actual}'"
        )
