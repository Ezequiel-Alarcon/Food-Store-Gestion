## Context

El dominio `pedidos` ya contempla:

- FSM de 6 estados y reglas RN-FSxx.
- RBAC con 4 roles y dependencias `get_current_user` / `require_role`.
- Convencion de paginacion global en la API.

Sin embargo, para el rol **PEDIDOS** falta un contrato especifico de listado operacional: filtros soportados, ordenamiento, datos minimos por item, y estructura de respuesta consistente (incluyendo errores RFC 7807).

Restricciones:

- Este change es **solo backend** (FASE 2).
- No se introducen dependencias externas.
- No se tocan reglas de transicion (RN-FS02 se mantiene: CONFIRMADO solo automatico por pago aprobado).

## Goals / Non-Goals

**Goals:**

- Definir un listado de pedidos para rol **PEDIDOS** (y ADMIN) con paginacion, filtros operativos y ordenamiento.
- Establecer modelos de respuesta estables para UI/operacion (sin necesidad de pedir detalle por cada item).
- Asegurar cumplimiento RBAC: PEDIDOS ve todos los pedidos; CLIENT sigue viendo solo propios (fuera de alcance del change pero no debe romperse).
- Especificar errores estandar RFC 7807 (401/403/422) para el endpoint.

**Non-Goals:**

- No se define ni implementa UI/Frontend.
- No se modifica el modelo ERD ni se agregan migraciones.
- No se redefinen endpoints de detalle/avance/cancelacion; solo se especifica el listado operacional.
- No se agregan funcionalidades de exportacion (CSV/PDF) ni reportes.

## Decisions

- Ruta: reutilizar `GET /api/v1/pedidos` como listado canonical y habilitar comportamiento por rol.
  - Alternativa: crear `GET /api/v1/admin/pedidos` o `GET /api/v1/pedidos/gestion`.
  - Razon: la spec base ya documenta `GET /api/v1/pedidos` como listado para CLIENT o todos para ADMIN/PEDIDOS; este change formaliza el contrato para PEDIDOS sin fragmentar la API.

- Autorizacion: `require_role(["ADMIN", "PEDIDOS", "CLIENT"])` a nivel endpoint, con control de visibilidad en service.
  - Alternativa: endpoints separados por rol.
  - Razon: evita duplicacion de rutas; mantiene un unico punto de entrada con logica de scoping por rol.

- Paginacion: adoptar la convencion del integrador (`page`/`size` y metadatos `items/total/page/size/pages`).
  - Alternativa: `skip/limit`.
  - Razon: el documento tecnico define explicitamente `page`/`size` como contrato global; se respeta como fuente de verdad.

- Performance: el repository debe devolver items de listado con joins minimos y sin N+1.
  - Ejemplo de datos del item: `id`, `estado_codigo`, `total`, `created_at`, `usuario` resumido, `forma_pago_codigo`, `mp_status` (si existe), `direccion` resumida.
  - Razon: el gestor necesita contexto para priorizar; pero el detalle completo (items/historial completo) se mantiene en `GET /pedidos/{id}`.

## Risks / Trade-offs

- [Riesgo] Filtros y ordenamiento pueden producir queries costosas (joins + condiciones) → Mitigacion: limitar filtros a campos indexables, documentar defaults, y recomendar indices (por ejemplo, `estado_codigo`, `created_at`).
- [Riesgo] Datos insuficientes para operacion si el item resumido es demasiado chico → Mitigacion: definir explicitamente el response model de item con los campos operativos minimos; el detalle completo queda disponible por endpoint existente.
- [Riesgo] Ambiguedad entre "listado para PEDIDOS" y "listado para CLIENT" → Mitigacion: especificar reglas de scoping por rol (ADMIN/PEDIDOS ven todos; CLIENT solo propios) y mantenerlos en specs.

## Migration Plan

- No aplica: sin cambios de BD ni dependencias externas. El cambio es aditivo a nivel de contrato y endpoints.

## Open Questions

- Definicion final de filtros: busqueda por `pedido_id` (num), por `email` del cliente, por rango de fechas, y/o por `mp_status`.
- Ordenamiento default: `created_at desc` vs prioridad por estado (por ejemplo, CONFIRMADO primero).
