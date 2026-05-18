# Design: intentional-bug-recommendations

## Context

La auditoría completa del proyecto (2026-05-18) encontró 20 discrepancias entre la especificación SDD v5.0 (`docs/Integrador.txt`) y el código implementado. El change `audit-bugfixes` aplicó 8 fixes inmediatos (S1-S8: FSM + guards de seguridad). Las 12 restantes (D1-D12) requieren refactors significativos que el equipo decidió postergar como deuda técnica intencional. Este change las cataloga para visibilidad y planificación futura.

## Goals / Non-Goals

**Goals:**
- Enumerar las 12 desviaciones con su justificación técnica
- Clasificar cada una por severidad, esfuerzo estimado e impacto
- Proveer contexto para que futuros changes puedan resolverlas individualmente
- Servir como referencia cruzada entre spec, código y roadmap

**Non-Goals:**
- NO implementar fixes (es un change de documentación)
- NO modificar specs existentes
- NO cambiar código

## Decisions

### D1 — RBAC: UsuarioRol N:M no implementado
- **Decisión:** Simplificar RBAC a un solo campo `rol` en Usuario (en vez de tabla pivot N:M)
- **Racional:** El MVP solo requiere 1 rol por usuario. La tabla pivot agrega complejidad de migración, queries JOIN, y reescritura completa de `require_role()`.
- **Alternativa considerada:** Implementar N:M completo → descartado por esfuerzo (3-4 días) y riesgo de regresión en todos los guards de auth.
- **Esfuerzo estimado:** 3-4 días (migración + migración de datos + rewrite de guards)

### D2 — FormaPago no existe
- **Decisión:** Omitir el catálogo FormaPago; el pago siempre se asume MercadoPago
- **Racional:** La integración actual solo soporta MercadoPago. Agregar EFECTIVO y TRANSFERENCIA requiere flujos de pago alternativos que no están implementados.
- **Alternativa considerada:** Crear modelo + seed → descartado porque sin UI/backend para otros métodos, es código muerto.
- **Esfuerzo estimado:** 1-2 días (modelo + migración + seed + integración con Pedido)

### D3 — RefreshToken sin SHA-256
- **Decisión:** Almacenar JWT plano con flag `revocado` booleano (en vez de hash + timestamp)
- **Racional:** Simplifica la lógica de búsqueda y revocación. El hash SHA-256 agrega una capa de seguridad pero complica el lookup (hay que hashear el token entrante para comparar).
- **Riesgo:** Si la DB se compromete, todas las sesiones activas quedan expuestas.
- **Alternativa considerada:** Implementar hash → descartado por complejidad de migración (tokens existentes sin hash).
- **Esfuerzo estimado:** 1 día (migración de esquema + rewrite de service)

### D4 — costo_envío = 0
- **Decisión:** No cobrar envío (default 0.0 en vez de 50.00)
- **Racional:** Simplifica el MVP. El costo de envío fijo requiere lógica adicional (¿varía por distancia? ¿por sucursal?). Se posterga hasta tener reglas de negocio claras.
- **Alternativa considerada:** Hardcodear 50.00 → descartado porque el equipo no definió la política de envíos.
- **Esfuerzo estimado:** 0.5 días (cambio de default + migración)

### D5 — DireccionEntrega → UserAddress
- **Decisión:** Usar naming en inglés (`UserAddress`, `is_default`, `etiqueta`) en vez del español de la spec
- **Racional:** Consistencia con el resto del código (todo en inglés: `User`, `Product`, `Order`). La spec usa español por ser documento académico.
- **Alternativa considerada:** Renombrar todo a español → descartado por inconsistencia con el resto del codebase.
- **Esfuerzo estimado:** N/A (decisión de naming, no se va a cambiar)

### D6 — GET /auth/me → GET /perfil
- **Decisión:** Separar perfil en módulo independiente (no dentro de auth)
- **Racional:** Arquitectura feature-first: perfil tiene su propio model/service/router. Mantenerlo en auth violaría SRP.
- **Alternativa considerada:** Agregar `/me` al router de auth → descartado porque duplicaría lógica con perfil.
- **Esfuerzo estimado:** 0.5 días (agregar endpoint proxy en auth)

### D7 — Producto: naming y tipos
- **Decisión:** Usar `activo` + `stock` (inglés) en vez de `disponible` + `stock_cantidad` (spec en español). `precio: float` en modelo en vez de `DECIMAL`.
- **Racional:** Consistencia con naming en inglés. `float` es más simple que `Decimal` para SQLModel, aunque pierde precisión.
- **Riesgo:** `activo` está sobrecargado (soft-delete visual + disponibilidad para venta). `float` puede causar errores de redondeo en centavos.
- **Alternativa considerada:** `Decimal` en modelo → parcialmente aplicado en schemas (B12), pero no en modelo SQLModel.
- **Esfuerzo estimado:** 1 día (renombrar campos + migración + actualizar referencias)

### D8 — DELETE /pedidos/{id} missing
- **Decisión:** Fusionar cancelación de CLIENT en PATCH /estado (en vez de endpoint DELETE separado)
- **Racional:** Un solo endpoint para todas las transiciones de estado. La FSM ya valida qué roles pueden cancelar desde cada estado.
- **Problema:** El guard `require_role("ADMIN","PEDIDOS")` bloquea CLIENT antes de llegar al service. El service tiene lógica para CLIENT pero nunca se ejecuta.
- **Alternativa considerada:** Agregar CLIENT al guard → riesgo de que CLIENT pueda llamar avances (el service lo bloquea con `check_advance_permission`, pero es frágil).
- **Esfuerzo estimado:** 1 día (fix de guard + tests)

### D9 — PATCH /stock vs PATCH /disponibilidad
- **Decisión:** Exponer actualización de cantidad (`stock`) en vez de toggle booleano (`disponibilidad`)
- **Racional:** Más útil para el rol STOCK: necesitan ajustar cantidades, no solo prender/apagar.
- **Alternativa considerada:** Ambos endpoints → agregaría complejidad sin casos de uso claros.
- **Esfuerzo estimado:** 0.5 días (agregar endpoint `/disponibilidad` como alias)

### D10 — SessionLocal bypass
- **Decisión:** Usar `SessionLocal()` directo en 3 endpoints de admin/refreshtokens
- **Racional:** Los endpoints de admin fueron agregados rápido para el dashboard. Refactorizarlos a UoW requiere crear servicios específicos.
- **Riesgo:** Viola el patrón de inyección de dependencias. Las sesiones no se comparten en transacciones.
- **Alternativa considerada:** Migrar a `Depends(get_session)` → simple pero requiere crear services para admin/refreshtokens.
- **Esfuerzo estimado:** 1 día (refactor de 3 endpoints + tests)

### D11 — TokenResponse sin `user`
- **Decisión:** Devolver solo tokens en login/register; el frontend obtiene datos con request separada a `/perfil`
- **Racional:** Separación de concerns: auth maneja tokens, perfil maneja datos de usuario.
- **Problema:** Agrega latencia (2 requests en vez de 1) y el frontend debe manejar el caso donde /perfil falla después de login exitoso.
- **Alternativa considerada:** Incluir `user` en TokenResponse → 1 día de trabajo en backend + schemas.
- **Esfuerzo estimado:** 0.5 días (modificar TokenResponse schema + auth service)

### D12 — Rol GESTOR legacy
- **Decisión:** Mantener soporte para rol `GESTOR` en frontend (aunque la spec v5.0 lo eliminó)
- **Racional:** Migración gradual. El backend aún tiene referencias a GESTOR en seeds/comentarios. Eliminarlo del frontend sin limpiar el backend causa inconsistencia.
- **Alternativa considerada:** Reemplazar GESTOR por STOCK+PEDIDOS en todo el código → requiere coordinar backend + frontend + seeds.
- **Esfuerzo estimado:** 1 día (limpiar 7 archivos frontend + seeds backend)

## Risks / Trade-offs

- **[Riesgo] D3 — DB leak expone sesiones.** Si la base de datos es comprometida, todos los refresh tokens son utilizables (no están hasheados). → **Mitigación:** Priorizar D3 cuando se implemente rotación de tokens.
- **[Riesgo] D8 — CLIENT no puede cancelar pedidos.** El endpoint PATCH /estado bloquea CLIENT. → **Mitigación:** Bug documentado; los clientes deben contactar soporte para cancelar.
- **[Riesgo] D12 — GESTOR causa confusión de roles.** Nuevos desarrolladores pueden asumir que GESTOR es un rol válido. → **Mitigación:** Documentar en este change y planificar limpieza.
- **[Trade-off] D7 — `float` para precios.** Funciona para el MVP pero puede causar errores de centavos en producción con alto volumen. → **Mitigación:** Los schemas Pydantic validan con `Decimal`, pero el modelo SQLModel usa `float`.
