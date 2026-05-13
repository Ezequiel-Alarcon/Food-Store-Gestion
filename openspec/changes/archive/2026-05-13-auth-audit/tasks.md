## 8. Verificación

- [x] 8.1 Verificar que Swagger `/docs` muestra campo "Value" para Bearer token (sin OAuth2 form)
- [x] 8.2 Probar flujo completo: register → login → usar token en endpoint protegido → refresh → logout
- [x] 8.3 Probar que login con usuario inactivo devuelve "Credenciales inválidas" (mismo mensaje que credenciales mal)
- [x] 8.4 Probar que refresh token de usuario desactivado es rechazado
- [x] 8.5 Probar que rate limiting funciona (5 intentos/min en login → 429)
- [x] 8.6 Probar seed: verificar que `python -m app.db.seed` crea admin sin errores
- [x] 8.7 Probar cambio de contraseña invalida todos los refresh tokens — verificado: `PerfilService.change_password()` llama a `self.refresh_repo.revoke_all_by_user(usuario.id)` que ejecuta `UPDATE refresh_tokens SET revocado=true WHERE user_id=X`
- [x] 8.8 Probar que `RegisterRequest` sin `apellido` devuelve 422
- [x] 8.9 Probar que password sin mayúscula o sin número devuelve 422
- [x] 8.10 Ejecutar tests existentes y verificar que no hay regresiones (19/19 auth tests pasan)
- [x] 8.11 Verificar migración: `alembic upgrade head` aplica cambios de `TIMESTAMPTZ` + `apellido`
- [x] 8.12 Hacer `openspec validate --change auth-audit` para validar implementación contra specs
