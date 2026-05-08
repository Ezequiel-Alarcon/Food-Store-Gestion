## Context

El backend FastAPI no arranca debido a bugs de implementación descubiertos durante `docker-setup`. El error principal está en `auth/router.py`: el archivo usa `from __future__ import annotations` (PEP 563), que convierte todas las anotaciones de tipo en strings. Cuando FastAPI/Pydantic v2 intenta resolver estas forward references al decorar las rutas (en tiempo de importación del módulo), la resolución falla porque el namespace no contiene los tipos esperados.

El error específico: `NameError: name 'LoginRequest' is not defined` en `pydantic._internal._generate_schema._resolve_forward_ref`.

Un segundo bug en `seed.py` importa modelos que pertenecen a cambios aún no implementados (`Rol`, `UsuarioRol`, `EstadoPedido`, `FormaPago`), causando `ImportError` al ejecutar el seed. Aunque el entrypoint de Docker ya maneja esto como non-fatal, el seed debería ser robusto por sí mismo.

## Goals / Non-Goals

**Goals:**
- Backend arranca sin errores con `docker compose up`
- Seed no crashea si los modelos no están implementados aún
- Cero cambios en el comportamiento funcional de la API

**Non-Goals:**
- Implementar modelos faltantes (`Rol`, `EstadoPedido`, etc.) — eso es parte de sus respectivos changes
- Refactorizar el módulo auth
- Tocar schemas o lógica de negocio

## Decisions

### 1. Eliminar `from __future__ import annotations` de los routers

**Elegido**: Quitar la línea `from __future__ import annotations` de `router.py` y de cualquier otro router que lo tenga.

**Alternativa considerada**: Usar `typing.TYPE_CHECKING` + imports condicionales o forzar la resolución de forward refs con `model_rebuild()`.

**Razón**: El `from __future__ import annotations` es útil en schemas donde hay forward references entre clases del mismo módulo (ej: `UserRead` que referencia `UserRead` a sí mismo). En routers no es necesario — las anotaciones son tipos planos importados de `schemas.py`. Quitarlo es el fix más simple y no tiene efectos secundarios. La alternativa de `model_rebuild()` requeriría tocar cada modelo y es frágil.

### 2. Imports condicionales en seed.py con `try/except ImportError`

**Elegido**: Envolver cada import problemático en `try/except ImportError` y definir la variable como `None` si falla, luego verificar antes de usar.

**Alternativa considerada**: Usar `importlib.util.find_spec()` para verificar disponibilidad antes del import.

**Razón**: `try/except ImportError` es idiomático en Python, más limpio que `find_spec`, y permite que el seed siga funcionando parcialmente. Cuando los modelos se implementen en sus respectivos cambios, los imports funcionarán sin modificar seed.py de nuevo. Es future-proof.

### 3. No tocar schemas.py ni service.py

**Razón**: El `from __future__ import annotations` en `schemas.py` es necesario — los schemas pueden tener forward references entre ellos (aunque no ahora, es buena práctica dejarlo). El fix es solo en `router.py` que es donde está el problema de resolución en tiempo de importación.

## Risks / Trade-offs

- **[Riesgo] Otros routers podrían tener el mismo problema** → Mitigación: verificar todos los `router.py` del proyecto y aplicar el mismo fix si tienen `from __future__ import annotations`.
- **[Riesgo] Quitar `from __future__ import annotations` podría romper type hints que usen clases del módulo como strings** → Mitigación: los routers no definen tipos — solo importan de schemas. No hay forward references locales.
- **[Trade-off] Seed parcial** → Si los modelos no existen, el seed omite esa parte. Esto es aceptable en desarrollo. En producción, todos los modelos deberían existir.
