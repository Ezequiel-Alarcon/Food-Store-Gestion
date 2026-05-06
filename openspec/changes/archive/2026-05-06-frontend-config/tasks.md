# tasks.md -- frontend-config

## Setup del Proyecto Frontend

- [x] **T001** Crear `frontend/package.json` con todas las dependencias (react, vite, typescript, tailwind, Zustand, TanStack Query, axios, etc.)
- [x] **T002** Crear `frontend/vite.config.ts` con plugin react y proxy hacia backend
- [x] **T003** Crear `frontend/tsconfig.json` con strict:true y opciones completas
- [x] **T004** Crear `frontend/tailwind.config.js` con contenido y plugins necesarios
- [x] **T005** Crear `frontend/postcss.config.js` con tailwind y autoprefixer
- [x] **T006** Crear `frontend/index.html` con estructura base
- [x] **T007** Crear `frontend/src/main.tsx` como punto de entrada
- [x] **T008** Crear `frontend/src/App.tsx` con providers (QueryClient, Router, Toast)
- [x] **T009** Crear `frontend/src/vite-env.d.ts` para tipados de Vite

## Variables de Entorno

- [x] **T010** Crear `frontend/.env.example` con VITE_API_BASE_URL y VITE_MERCADOPAGO_PUBLIC_KEY
- [x] **T011** Crear `frontend/.env` con valores de desarrollo (opcional)

## Zustand Stores

- [x] **T012** Crear `frontend/src/stores/authStore.ts` con login, logout, updateTokens, selectores, persist (solo accessToken)
- [x] **T013** Crear `frontend/src/stores/cartStore.ts` con addItem, removeItem, updateQuantity, clearCart, selectores, persist (items)
- [x] **T014** Createar `frontend/src/stores/paymentStore.ts` con startCheckout, setPreference, updatePaymentStatus, reset (SIN persistencia)
- [x] **T015** Crear `frontend/src/stores/uiStore.ts` con theme, sidebar, cart, modal, toasts, persist (solo theme)
- [x] **T016** Crear `frontend/src/lib/api.ts` con instancia Axios baseURL configurada
- [x] **T017** Agregar interceptor de request que agrega Authorization: Bearer <token>
- [x] **T018** Agregar interceptor de response que maneja 401 con refresh automático + retry

## Providers

- [x] **T019** Crear `frontend/src/providers/QueryProvider.tsx` con QueryClientProvider
- [x] **T020** Crear `frontend/src/providers/RouterProvider.tsx` con React Router y rutas base

## Verificación

- [x] **T021** Ejecutar `npm install` sin errores
- [x] **T022** Ejecutar `npm run dev` y verificar que levante en puerto 5173
- [x] **T023** Verificar que no haya errores TypeScript con strict
- [x] **T024** Ejecutar `npm run build` y verificar output en dist/

## Documentación

- [x] **T025** Crear `frontend/README.md` con instrucciones de setup y comandos disponibles