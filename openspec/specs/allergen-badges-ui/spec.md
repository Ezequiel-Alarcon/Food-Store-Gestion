# Spec: allergen-badges-ui

> **Rol:** Todos los usuarios  
> **Ubicación:** IngredientsModal, vista de producto

## Requisitos

### RQ-ALG01 — Tipo IngredienteSimple con es_alergeno
- Agregar `es_alergeno: boolean` a `IngredienteSimple` en `entities/producto/types.ts`

### RQ-ALG02 — Badge visual en IngredientsModal
- Si `es_alergeno === true` → mostrar ⚠️ o badge "ALÉRGENO" junto al nombre del ingrediente
- Color: rojo/ámbar para destacar

### RQ-ALG03 — Badge en vista de detalle de producto
- En `CatalogPage` y vistas de producto, mostrar indicador de alérgenos en la lista de ingredientes

## Escenarios

```
GIVEN cliente viendo producto "Hamburguesa"
AND el ingrediente "Maní" tiene es_alergeno=true
WHEN abre el modal de ingredientes
THEN ve "Maní ⚠️" con badge de alérgeno
```
