"""app.modules.pagos.model

Modelo SQLModel para pagos con MercadoPago.
Relación 1:N Pedido→Pago (múltiples intentos permitidos).
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Pago(SQLModel, table=True):
    """Registro de pago vinculado a un pedido."""
    __tablename__ = "pagos"

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int = Field(foreign_key="pedidos.id", index=True)
    mp_payment_id: Optional[int] = Field(default=None, unique=True, description="ID devuelto por MercadoPago")
    idempotency_key: str = Field(unique=True, max_length=64, description="UUID v4 para evitar cobros duplicados")
    external_reference: str = Field(unique=True, max_length=100, description="Referencia externa enviada a MP")
    status: str = Field(default="pending", max_length=30, description="pending|approved|rejected|in_process|cancelled|refunded")
    status_detail: Optional[str] = Field(default=None, max_length=100, description="Detalle textual de MP")
    payment_method_id: Optional[str] = Field(default=None, max_length=30, description="visa, master, rapipago, etc.")
    transaction_amount: float = Field(description="Monto de la transacción")
    creado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    actualizado_en: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
