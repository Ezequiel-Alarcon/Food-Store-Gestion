## ADDED Requirements

### Requirement: Pydantic v2 ConfigDict migration

All Pydantic schemas in backend modules SHALL use `model_config = ConfigDict(...)` instead of the deprecated inner `class Config:` for configuration.

**Rationale:** Pydantic v2 deprecated `class Config` in favor of `ConfigDict`. The inner class pattern generates deprecation warnings and blocks migration to Pydantic v3. `ConfigDict` is the official path forward.

#### Scenario: producto schemas use ConfigDict
- **WHEN** `ProductoCreate`, `ProductoUpdate`, `ProductoResponse`, `ProductoListResponse`, or `ProductoCatalogoResponse` are defined
- **THEN** they use `model_config = ConfigDict(from_attributes=True)` instead of `class Config: from_attributes = True`

#### Scenario: sucursales schemas use ConfigDict
- **WHEN** `SucursalResponse` is defined
- **THEN** it uses `model_config = ConfigDict(from_attributes=True)` instead of `class Config: from_attributes = True`

#### Scenario: ingredientes schemas use ConfigDict
- **WHEN** `IngredienteResponse` or `IngredienteSimple` are defined
- **THEN** they use `model_config = ConfigDict(from_attributes=True)` instead of `class Config: from_attributes = True`

#### Scenario: direcciones schemas use ConfigDict
- **WHEN** `UserAddressResponse` or `BranchAddressResponse` are defined
- **THEN** they use `model_config = ConfigDict(from_attributes=True)` instead of `class Config: from_attributes = True`

#### Scenario: categorias schemas use ConfigDict
- **WHEN** `CategoriaResponse` or `CategoriaSimple` are defined
- **THEN** they use `model_config = ConfigDict(from_attributes=True)` instead of `class Config: from_attributes = True`

#### Scenario: core schemas use ConfigDict
- **WHEN** `ErrorDetail` or similar core schemas are defined
- **THEN** they use `model_config = ConfigDict(...)` instead of `class Config:`