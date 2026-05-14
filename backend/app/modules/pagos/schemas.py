"""app.modules.pagos.schemas

Schemas Pydantic v2 para el módulo de pagos.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PagoCreate(BaseModel):
    """Schema para crear un pago."""
    pedido_id: int
    payment_method_id: str = "account_money"
    token: Optional[str] = Field(None, description="Token de tarjeta generado por MP SDK (solo para pagos con tarjeta)")


class PagoResponse(BaseModel):
    """Schema de respuesta con datos del pago."""
    id: int
    pedido_id: int
    mp_payment_id: Optional[int] = None
    idempotency_key: str
    external_reference: str
    status: str
    status_detail: Optional[str] = None
    payment_method_id: Optional[str] = None
    transaction_amount: float
    creado_en: datetime
    actualizado_en: datetime
    model_config = {"from_attributes": True}


class WebhookPayload(BaseModel):
    """Schema para validar el payload del webhook IPN."""
    topic: Optional[str] = None
    resource_id: Optional[str] = None
    type: Optional[str] = None
    id: Optional[str] = None
