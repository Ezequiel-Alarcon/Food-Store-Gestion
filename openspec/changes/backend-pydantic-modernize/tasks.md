## 1. Migrar core/schemas.py

- [ ] 1.1 Reemplazar `class Config: from_attributes = True` → `model_config = ConfigDict(from_attributes=True)` en `ErrorDetail` (u otro schema que use Config)
- [ ] 1.2 Verificar que `ConfigDict` esté importado desde `pydantic`

## 2. Migrar productos/schemas.py

- [ ] 2.1 Reemplazar en `CategoriaSimple` (línea 138)
- [ ] 2.2 Reemplazar en `IngredienteSimple` (línea 148)
- [ ] 2.3 Reemplazar en `ProductoResponse` (línea 167)
- [ ] 2.4 Reemplazar en `ProductoListResponse` (línea 183)
- [ ] 2.5 Reemplazar en `ProductoCatalogoResponse` (línea 213)
- [ ] 2.6 Verificar que `ConfigDict` esté importado desde `pydantic`

## 3. Migrar sucursales/schemas.py

- [ ] 3.1 Reemplazar en `SucursalResponse` (línea 43)
- [ ] 3.2 Verificar que `ConfigDict` esté importado desde `pydantic`

## 4. Migrar ingredientes/schemas.py

- [ ] 4.1 Reemplazar en `IngredienteResponse` (línea 93)
- [ ] 4.2 Reemplazar en `IngredienteSimple` (línea 107)
- [ ] 4.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 5. Migrar direcciones/schemas.py

- [ ] 5.1 Reemplazar en `UserAddressResponse` (línea 84)
- [ ] 5.2 Reemplazar en `BranchAddressResponse` (línea 151)
- [ ] 5.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 6. Migrar categorias/schemas.py

- [ ] 6.1 Reemplazar en `CategoriaResponse` (línea 97)
- [ ] 6.2 Reemplazar en `CategoriaSimple` (línea 110)
- [ ] 6.3 Verificar que `ConfigDict` esté importado desde `pydantic`

## 7. Verificación

- [ ] 7.1 Ejecutar `grep -r "class Config:" backend/app/modules/**/schemas.py backend/app/core/schemas.py` — debe retornar 0 resultados
- [ ] 7.2 Commit con mensaje: `refactor: migrate Pydantic schemas from class Config to model_config ConfigDict`