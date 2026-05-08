## 1. Fix auth router forward ref

- [x] 1.1 Eliminar `from __future__ import annotations` de `backend/app/modules/auth/router.py`
- [x] 1.2 Verificar que no hay otros `router.py` en `backend/app/modules/*/` que tengan `from __future__ import annotations` y corregirlos (7 routers corregidos: sucursales, ingredientes, direcciones, categorias, usuarios, perfil, patterns_example)

## 2. Fix seed imports

- [x] 2.1 Envolver imports de `Rol`, `UsuarioRol` en `backend/app/db/seed.py` con `try/except ImportError`, asignar `None` si fallan
- [x] 2.2 Envolver imports de `EstadoPedido`, `FormaPago` en `backend/app/db/seed.py` con `try/except ImportError`
- [x] 2.3 Agregar guard clause en `seed_roles()` para skipear si `Rol` es `None`
- [x] 2.4 Agregar guard clause en `seed_estados_pedido()` para skipear si `EstadoPedido` es `None`
- [x] 2.5 Agregar guard clause en `seed_formas_pago()` para skipear si `FormaPago` es `None`
- [x] 2.6 Agregar guard clause en `seed_usuario_admin()` para skipear si `UsuarioRol` es `None`

## 3. Verification

- [x] 3.1 Ejecutar `docker compose up` y verificar que el backend arranca sin errores de importación
- [x] 3.2 Verificar que las migraciones corren correctamente
- [x] 3.3 Verificar que el seed se ejecuta (o se saltea gracefulmente si los modelos no existen)
- [x] 3.4 Verificar que el frontend sigue funcionando en `localhost:5173`
