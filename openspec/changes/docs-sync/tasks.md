## 1. Soft Delete Field Unification

- [ ] 1.1 Identificar usages de `eliminado_en` y `deletedAt` en docs
- [ ] 1.2 Reemplazar por `deleted_at` en Integrador.txt, Descripcion.txt, Historias_de_usuario.txt

## 2. FSM States Unification

- [ ] 2.1 Identificar usages de `EN_PREPARACIÓN`, `EN_PREPARACION` en docs
- [ ] 2.2 Reemplazar por `EN_PREP` en Integrador.txt, Descripcion.txt, Historias_de_usuario.txt, TEAM-ASSIGNMENT.md

## 3. Endpoint FSM Unification

- [ ] 3.1 Identificar usages de `/avanzar` en docs
- [ ] 3.2 Reemplazar por `/pedidos/{id}/estado` en Descripcion.txt, Historias_de_usuario.txt

## 4. Documentar Módulo Sucursales

- [ ] 4.1 Agregar `sucursales/` a lista de módulos en Integrador.txt sección 2.1
- [ ] 4.2 Agregar descripción breve del módulo

## 5. Rate Limiting Unification

- [ ] 5.1 Verificar en el código cuál es el valor real (debería ser 5/15minutes)
- [ ] 5.2 Actualizar todos los docs que digan `5/minute` a `5/15minutes`

## 6. CONTRIBUTING.md Code Examples

- [ ] 6.1 Corregir ejemplo línea 54: `with uow:` → `async with uow:`
- [ ] 6.2 Corregir ejemplo línea 62: `uow.usuarios.add(user)` → `uow.usuarios.create(user)`
- [ ] 6.3 Verificar que el ejemplo de commit es correcto

## 7. Audit Documentation Updates

- [ ] 7.1 Actualizar AUDITORIA-ROADMAP.md: cambiar "18 changes" a "23/24 changes", fecha a 2026-05-14
- [ ] 7.2 Verificar CHANGES-ROADMAP.md: confirmar que los 23 changes están marcados correctamente

## 8. Verification

- [ ] 8.1 Commit con conventional commits: `docs: sync documentation — unify naming, fix code examples, update counters`