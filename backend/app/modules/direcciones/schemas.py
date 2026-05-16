"""app.modules.direcciones.schemas"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip_or_none(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    return v or None


class UserAddressCreate(BaseModel):
    etiqueta: str | None = Field(default=None, max_length=60)
    calle: str = Field(..., min_length=1, max_length=120)
    numero: str = Field(..., min_length=1, max_length=30)
    piso_depto: str | None = Field(default=None, max_length=60)
    ciudad: str = Field(..., min_length=1, max_length=120)
    provincia: str = Field(..., min_length=1, max_length=120)
    codigo_postal: str | None = Field(default=None, max_length=20)
    pais: str = Field(..., min_length=1, max_length=120)
    referencias: str | None = Field(default=None, max_length=500)

    @field_validator(
        "etiqueta",
        "calle",
        "numero",
        "piso_depto",
        "ciudad",
        "provincia",
        "codigo_postal",
        "pais",
        "referencias",
    )
    @classmethod
    def _cleanup(cls, v: str | None) -> str | None:
        return _strip_or_none(v)


class UserAddressUpdate(BaseModel):
    etiqueta: str | None = Field(default=None, max_length=60)
    calle: str | None = Field(default=None, min_length=1, max_length=120)
    numero: str | None = Field(default=None, min_length=1, max_length=30)
    piso_depto: str | None = Field(default=None, max_length=60)
    ciudad: str | None = Field(default=None, min_length=1, max_length=120)
    provincia: str | None = Field(default=None, min_length=1, max_length=120)
    codigo_postal: str | None = Field(default=None, max_length=20)
    pais: str | None = Field(default=None, min_length=1, max_length=120)
    referencias: str | None = Field(default=None, max_length=500)

    @field_validator(
        "etiqueta",
        "calle",
        "numero",
        "piso_depto",
        "ciudad",
        "provincia",
        "codigo_postal",
        "pais",
        "referencias",
    )
    @classmethod
    def _cleanup(cls, v: str | None) -> str | None:
        return _strip_or_none(v)


class UserAddressResponse(BaseModel):
    id: int
    user_id: int
    etiqueta: str | None
    calle: str
    numero: str
    piso_depto: str | None
    ciudad: str
    provincia: str
    codigo_postal: str | None
    pais: str
    referencias: str | None
    is_default: bool
    activa: bool

    model_config = ConfigDict(from_attributes=True)


class BranchAddressCreate(BaseModel):
    calle: str = Field(..., min_length=1, max_length=120)
    numero: str = Field(..., min_length=1, max_length=30)
    piso_depto: str | None = Field(default=None, max_length=60)
    ciudad: str = Field(..., min_length=1, max_length=120)
    provincia: str = Field(..., min_length=1, max_length=120)
    codigo_postal: str | None = Field(default=None, max_length=20)
    pais: str = Field(..., min_length=1, max_length=120)
    referencias: str | None = Field(default=None, max_length=500)

    @field_validator(
        "calle",
        "numero",
        "piso_depto",
        "ciudad",
        "provincia",
        "codigo_postal",
        "pais",
        "referencias",
    )
    @classmethod
    def _cleanup(cls, v: str | None) -> str | None:
        return _strip_or_none(v)


class BranchAddressUpdate(BaseModel):
    calle: str | None = Field(default=None, min_length=1, max_length=120)
    numero: str | None = Field(default=None, min_length=1, max_length=30)
    piso_depto: str | None = Field(default=None, max_length=60)
    ciudad: str | None = Field(default=None, min_length=1, max_length=120)
    provincia: str | None = Field(default=None, min_length=1, max_length=120)
    codigo_postal: str | None = Field(default=None, max_length=20)
    pais: str | None = Field(default=None, min_length=1, max_length=120)
    referencias: str | None = Field(default=None, max_length=500)

    @field_validator(
        "calle",
        "numero",
        "piso_depto",
        "ciudad",
        "provincia",
        "codigo_postal",
        "pais",
        "referencias",
    )
    @classmethod
    def _cleanup(cls, v: str | None) -> str | None:
        return _strip_or_none(v)


class BranchAddressResponse(BaseModel):
    id: int
    branch_id: int
    calle: str
    numero: str
    piso_depto: str | None
    ciudad: str
    provincia: str
    codigo_postal: str | None
    pais: str
    referencias: str | None
    activa: bool

    model_config = ConfigDict(from_attributes=True)
