## 1. Migrar core/schemas.py

- [x] 1.1 Reemplazar `class Config: from_attributes = True` → `model_config = ConfigDict(from_attributes=True)` en `ErrorDetail` (u otro schema que use Config)
- [x] 1.2 Verificar que `ConfigDict` esté importado desde `pydantic`

## 2. Migrar productos/schemas.py

- [x] 2.1 Reemplazar en `CategoriaSimple` (línea 138)
- [x] 2.2 Reemplazar en `IngredienteSimple` (línea 148)
- [x] 2.3 Reemplazar en `ProductoResponse` (línea 167)
- [x] 2.4 Reemplazar en `ProductoListResponse` (línea 183)
- [x] 2.5 Reemplazar en `ProductoCatalogoResponse` (línea 213)
- [x] 2.6 Verificar que `ConfigDict` esté importado desde `pydantic`

## 3. Migrar sucursales/schemas.py

- [x] 3.1 Reemplazar en `SucursalResponse` (línea 43)
- [x] 3.2 Verificar que `ConfigDict` esté importado desde `pydantic`

## 4. Migrar ingredientes/schemas.py

- [x] 4.1 Reemplazar en `IngredienteResponse` (línea 93)
- [x] 4.2 Reemplazar en `IngredienteSimple` (línea 107)
- [x] 4.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 5. Migrar direcciones/schemas.py

- [x] 5.1 Reemplazar en `UserAddressResponse` (línea 84)
- [x] 5.2 Reemplazar en `BranchAddressResponse` (línea 151)
- [x] 5.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 6. Migrar categorias/schemas.py

- [x] 6.1 Reemplazar en `CategoriaResponse` (línea 97)
- [x] 6.2 Reemplazar en `CategoriaSimple` (línea 110)
- [x] 6.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 7. Verificación

- [x] 7.1 Ejecutar `grep -r "class Config:" backend/app/modules/**/schemas.py backend/app/core/schemas.py` — debe retornar 0 resultados
- [x] 7.2 Commit con mensaje: `refactor: migrate Pydantic schemas from class Config to model_config ConfigDict`