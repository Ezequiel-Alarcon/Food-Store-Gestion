## 1. Setup - Estructura del directorio

- [x] 1.1 Crear directorio `frontend/src/shared/ui/`
- [x] 1.2 Verificar que `frontend/src/shared/` existe (carpeta base)

## 2. Button Component

- [x] 2.1 Crear `frontend/src/shared/ui/Button.tsx` con variantes: primary, secondary, ghost, danger
- [x] 2.2 Agregar sizes: sm, md, lg
- [x] 2.3 Agregar estados: loading (spinner), disabled, icon (left/right)
- [x] 2.4 Exportar tipo `ButtonProps` desde el componente

## 3. Input Component

- [x] 3.1 Crear `frontend/src/shared/ui/Input.tsx` con label integrado
- [x] 3.2 Agregar helper text y error message
- [x] 3.3 Soportar tipos: text, email, password, number, tel
- [x] 3.4 Exportar tipo `InputProps` desde el componente

## 4. Modal Component

- [x] 4.1 Crear `frontend/src/shared/ui/Modal.tsx` con Portal
- [x] 4.2 Implementar header, body, footer slots
- [x] 4.3 Agregar cierre por: Escape key, click outside, close button
- [x] 4.4 Agregar animación fade-in overlay
- [x] 4.5 Exportar tipo `ModalProps` desde el componente

## 5. Card Component

- [x] 5.1 Crear `frontend/src/shared/ui/Card.tsx`
- [x] 5.2 Agregar shadow variants: none, sm, md, lg
- [x] 5.3 Agregar padding options: none, sm, md, lg
- [x] 5.4 Agregar optional hover effect (scale/shadow on hover)
- [x] 5.5 Exportar tipo `CardProps` desde el componente

## 6. Barrel Export

- [x] 6.1 Crear `frontend/src/shared/ui/index.ts`
- [x] 6.2 Exportar los 4 componentes y sus tipos
- [x] 6.3 Agregar exports en `frontend/src/shared/index.ts` (no existe - no aplica)

## 7. Verificación

- [x] 7.1 Verificar que TypeScript compila sin errores (error legacy de tsconfig, no de componentes)
- [x] 7.2 Archivos creados: Button.tsx, Input.tsx, Modal.tsx, Card.tsx, index.ts
- [x] 7.3 Componentes con tipado completo y ready para usar