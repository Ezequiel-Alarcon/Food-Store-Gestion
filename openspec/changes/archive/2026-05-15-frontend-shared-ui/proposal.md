## Why

El frontend actual carece de componentes UI reutilizables consistentes. Cada feature implementa sus propios botones, inputs y modales sin un sistema unificado, lo que genera inconsistencias visuales, duplicación de código y mantenimiento dificultoso. La Fase 4 requiere crear una HomePage y ProfilePage que necesitan componentes base是一致的.

## What Changes

- Crear biblioteca de componentes UI base en `frontend/src/shared/ui/`
- Implementar 4 componentes fundamentales: Button, Input, Modal, Card
- Cada componente incluye variantes, estados (loading, disabled, error) y accesibilidad
- Exportar desde barrel `index.ts` para imports limpios
- Tipado completo con TypeScript (strict mode)

## Capabilities

### New Capabilities

- `shared-button`: Botón reusable con variantes (primary, secondary, ghost, danger), sizes (sm, md, lg), estados (loading, disabled), y variantes de ícono
- `shared-input`: Input con label, helper text, error message, tipos (text, email, password, number), y validaciones base
- `shared-modal`: Modal con overlay, header, body, footer, cierre por escape/clic outside, y animaciones
- `shared-card`: Tarjeta con shadow variants, padding configurable, hover effect opcional, y children flexible

### Modified Capabilities

- Ninguno (son componentes nuevos que no modifican specs existentes)

## Impact

- Nuevo directorio: `frontend/src/shared/ui/` con 4 componentes + index.ts
- Dependencias: Ninguna nueva (solo Tailwind ya existente)
- Afecta: Cualquier feature futura que use estos componentes (home-page, profile-page, etc.)