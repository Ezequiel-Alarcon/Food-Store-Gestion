# Design: intentional-bug-recommendations

## Approach

Cambio de solo documentación. No se modifica código. Cada desviación se explica con:
- Qué dice la spec
- Qué hace el código
- Por qué se dejó así
- Prioridad para resolver
- Change sugerido

Las desviaciones se agrupan en tres categorías:
1. **Endpoints faltantes o movidos** (D1-D6): rutas que la spec pide pero no existen o están en otro path
2. **Response/status divergentes** (D7-D9): status codes, response models o campos extra
3. **Funcionalidad no documentada** (D10-D12): endpoints o campos que el código tiene pero la spec no menciona
