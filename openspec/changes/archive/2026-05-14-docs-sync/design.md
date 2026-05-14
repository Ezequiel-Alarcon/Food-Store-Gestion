## Context

El code review de documentación encontró 9 inconsistencias críticas entre los documentos y el código real. Estas inconsistencias incluyen naming de campos, estados FSM, módulos documentados vs existentes, y formatos de ejemplos de código. Todas deben resolverse para mantener la documentación como source of truth confiable.

## Goals / Non-Goals

**Goals:**
- Unificar naming de todos los documentos al formato usado en el código real
- Documentar el módulo `sucursales` que existe pero no está en docs
- Corregir los ejemplos de código en CONTRIBUTING.md
- Actualizar contadores y estados en AUDITORIA-ROADMAP.md y CHANGES-ROADMAP.md

**Non-Goals:**
- No cambiar código — solo documentación
- No agregar nuevas funcionalidades a ningún documento
- No modificar la arquitectura documentada (solo limpiar inconsistencias)

## Decisions

### D1: Soft delete field — `deleted_at` como estándar

**Decisión:** Usar `deleted_at` como nombre estándar en todos los documentos (ya es el usado en el código).

**Archivos afectados:** Integrador.txt, Descripcion.txt, Historias_de_usuario.txt

### D2: FSM states — `EN_PREP` como estándar

**Decisión:** Unificar todos los estados FSM a formato `EN_PREP` (snake_case, sin tilde, mayúsculas).

**Rationale:** El código usa `EN_PREP`, los tests usan `EN_PREP`, CHANGES-ROADMAP usa `EN_PREP`. Descripcion.txt usa `EN_PREPARACIÓN` con tilde y descripción — debe actualizarse a `EN_PREP`.

### D3: Endpoint de transición FSM — `/pedidos/{id}/estado`

**Decisión:** Unificar al endpoint que usa el código real: `PATCH /api/v1/pedidos/{id}/estado`.

**Rationale:** La implementación real usa este endpoint. Historias_de_usuario.txt dice `/avanzar` pero eso no existe en el código.

### D4: Módulo `sucursales` — documentar existente

**Decisión:** Agregar `sucursales/` a la lista de módulos en Integrador.txt sección 2.1.

### D5: CONTRIBUTING.md — corregir ejemplos de código

**Decisión:** Corregir los ejemplos para que usen `async with uow:` (ya que los repositorios son async) y `uow.commit()` (no automático en todos los casos).

## Files to Modify

| Archivo | Cambio |
|---------|--------|
| `docs/Integrador.txt` | Secciones 2.1, 3.3, 5.3 — sync naming |
| `docs/Descripcion.txt` | Secciones de soft delete, FSM, endpoints |
| `docs/Historias_de_usuario.txt` | RN-FS02, RN-PE02, RN-DI01, RN-AU06 |
| `docs/CHANGES-ROADMAP.md` | Verificar estado de 23 changes |
| `docs/AUDITORIA-ROADMAP.md` | Actualizar contador y fecha |
| `CONTRIBUTING.md` | Ejemplos de código línea 54, 62, 65 |