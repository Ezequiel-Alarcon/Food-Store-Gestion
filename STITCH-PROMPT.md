# Stitch AI — Prompt para UI Completa de Food Store

## PROYECTO: Food Store — Plataforma E-Commerce de Comida

Stack objetivo: React 19 + TypeScript + Tailwind CSS v4 + Vite
Librerías: TanStack Query 5, TanStack Form, Zustand 4, recharts 2, @mercadopago/sdk-react, class-variance-authority, clsx, tailwind-merge
Metodología: Feature-Sliced Design (FSD)
Configuración CSS: Tailwind v4 CSS-first con `@theme` + OKLCH tokens + `@custom-variant dark`

---

## 1. IDENTIDAD VISUAL (Design System)

### Paleta de Colores

| Token | Tailwind Class | Uso |
|-------|---------------|-----|
| **Primary** | `indigo-600`, `indigo-700` | Botones CTA, links activos, navbar accent, focus rings |
| **Primary Light** | `indigo-50`, `indigo-100` | Badges, chips, hover states |
| **Page BG** | `gray-50` | Fondo de todas las páginas |
| **Surface** | `white` | Cards, navbar, modales, drawers, tablas |
| **Text Primary** | `gray-900` | Títulos principales, texto importante |
| **Text Secondary** | `gray-600`, `gray-700` | Subtítulos, descripciones, labels |
| **Text Muted** | `gray-400`, `gray-500` | Placeholders, texto secundario, empty states |
| **Border** | `gray-200`, `gray-300` | Bordes de inputs, cards, separadores |
| **Success** | `green-50/100/800` | Toast success, badge CONFIRMADO, ENTREGADO |
| **Error** | `red-50/100/200/500/700/800` | Toast error, badge CANCELADO, errores de validación |
| **Warning** | `yellow-50/100/800`, `amber-700` | Toast warning, badge PENDIENTE |
| **Info** | `blue-50/100/800` | Toast info, badge EN_PREP |
| **Orange** | `orange-100/800` | Badge EN_CAMINO |
| **Emerald** | `emerald-100/800` | Badge ENTREGADO |
| **Overlay** | `black/40`, `black/50` | Modales, drawers, backdrop blur |

### Tipografía
- Font family: Work Sans (headlines + body), system sans-serif fallback
- Escala semántica con tokens CSS: `--text-xs` (labels), `--text-sm` (cuerpo), `--text-base` (general), `--text-lg` (subtítulos), `--text-xl` (títulos sección), `--text-2xl` (títulos página), `--text-3xl` (hero)
- Font weights: `font-normal` (cuerpo), `font-medium` (links, botones), `font-semibold` (títulos card), `font-bold` (títulos página, precios)
- Usar clases semánticas: `text-foreground`, `text-muted-foreground`, `text-primary` en vez de `text-gray-900`, `text-gray-500`

### Bordes y Sombras
- Border radius: `rounded-md` (inputs, botones), `rounded-lg` (cards, modales, drawers), `rounded-full` (badges, avatares)
- Sombras: `shadow-sm` (cards default), `shadow-md` (cards hover), `shadow-lg` (modales), `shadow-xl` (drawers con overlay), `shadow-2xl` (cart drawer)
- Focus: `focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500`

### Animaciones
- Transiciones: `transition-colors` (botones), `transition-shadow` (cards), `duration-200`, `duration-300`
- Cart drawer: slide-in derecha `translate-x-0` ↔ `translate-x-full` con `duration-300 ease-in-out`
- Toasts: slide-in desde abajo con `animate-slide-in`
- Spinners: `animate-spin` con `border-b-2 border-indigo-600`

---

## 2. ESTRUCTURA DE PÁGINAS — 12 Rutas

### Layout Global (persistente en todas las páginas)

```
┌─────────────────────────────────────────────────────┐
│ NAVBAR (fixed top, h-16, bg-white shadow, z-30)     │
│ [Logo "Food Store"] ... [Menú por rol] ... [Carrito] │
├─────────────────────────────────────────────────────┤
│                                                     │
│              CONTENIDO DE PÁGINA                     │
│         (max-w-7xl mx-auto px-4 py-8)               │
│                                                     │
├─────────────────────────────────────────────────────┤
│ TOASTS (fixed bottom-4 right-4, z-50)               │
│ CART DRAWER (slide-in derecha, z-50)                │
│ CONFIRM MODAL (overlay centrado, z-50)              │
│ ORDER DETAIL DRAWER (slide-in derecha, z-50)        │
└─────────────────────────────────────────────────────┘
```

### NAVBAR (componente `Navigation`)

**Sin autenticar:**
- Logo "Food Store" (indigo-600, text-xl font-bold) → link a `/`
- Links: "Productos" → `/productos`
- Botones derecha: "Ingresar" (text-gray-700 hover:text-indigo-600) + "Registrarse" (bg-indigo-600 text-white rounded-md px-4 py-2)

**Autenticado como CLIENTE:**
- Logo "Food Store"
- Links: "Productos" `/productos`, "Mis Pedidos" `/pedidos`, "Mis Direcciones" `/direcciones`, "Puntos de Retiro" `/puntos-retiro`
- Carrito icono + badge (bg-indigo-600 text-white text-xs font-bold rounded-full w-5 h-5 con contador, muestra "99+" si >99)
- Derecha: "Hola, {nombre}" + "Cerrar sesión" (text-gray-500 hover:text-gray-700)

**Autenticado como ADMIN:**
- Links: "Dashboard" `/admin`, "Productos" `/productos`, "Gestión Usuarios" `/admin/usuarios`, "Puntos de Retiro" `/puntos-retiro`
- Icono carrito con badge

**Autenticado como STOCK:**
- Links: "Productos" `/productos`, "Gestión de Stock" `/admin/stock`

**Autenticado como PEDIDOS:**
- Links: "Productos" `/productos`, "Gestión de Pedidos" `/admin/pedidos`

**Mobile:** Menú hamburguesa que despliega todos los links en dropdown.

---

### RUTA 1: `/` — Home / Landing Page

Dos estados:

**No autenticado — Hero Page:**
```
┌──────────────────────────────────────────────────┐
│                                                  │
│         🍔 Food Store                            │
│    Tu comida favorita, a un click de distancia   │
│                                                  │
│    [Ingresar]   [Registrarse]                    │
│                                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
│  │ 🛒      │  │ 🚀      │  │ 📦      │         │
│  │ Pedí    │  │ Rápido  │  │ Seguí   │         │
│  │ online  │  │ y fácil │  │ tu orden│         │
│  └─────────┘  └─────────┘  └─────────┘         │
│                                                  │
│  Categorías destacadas (grid de 3-4 cards)      │
│  Productos populares (grid de 4 cards)          │
│                                                  │
└──────────────────────────────────────────────────┘
```

**Autenticado — Dashboard personal:**
- Mensaje de bienvenida: "¡Hola, {nombre}!"
- Resumen rápido: último pedido (estado, total), productos favoritos
- Acceso rápido: "Seguir comprando" → catálogo, "Mis pedidos", "Mis direcciones"

---

### RUTA 2: `/login` — Iniciar Sesión

```
┌──────────────────────────────────────────┐
│                                          │
│          Iniciar Sesión                  │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Email                             │  │
│  │  [________________________]         │  │
│  │                                    │  │
│  │  Contraseña                        │  │
│  │  [________________________]         │  │
│  │                                    │  │
│  │  [Iniciar Sesión]  (indigo-600)    │  │
│  │                                    │  │
│  │  ¿No tenés cuenta? Registrate →    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  Error state: banner rojo arriba         │
│  Loading state: botón "Cargando..."      │
│                                          │
└──────────────────────────────────────────┘
```
- Validación client-side: email regex, password requerido
- Rate limiting visual feedback si 5 intentos fallidos
- Layout: `min-h-screen flex items-center justify-center bg-gray-50`
- Card: `max-w-md w-full bg-white rounded-lg shadow-md p-8`
- Link "Registrate" al final del form

---

### RUTA 3: `/register` — Registro

```
┌──────────────────────────────────────────┐
│          Crear Cuenta                    │
│                                          │
│  ┌────────────────────────────────────┐  │
│  │  Nombre    [_____________]          │  │
│  │  Apellido  [_____________]          │  │
│  │  Email     [_____________]          │  │
│  │  Contraseña[_____________]          │  │
│  │  Confirmar  [_____________]         │  │
│  │                                    │  │
│  │  [Crear Cuenta]  (indigo-600)      │  │
│  │  ¿Ya tenés cuenta? Ingresá →       │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```
- Validación: nombre/apellido requeridos, email regex, password ≥8 chars, confirmación coincide
- Misma estética que login

---

### RUTA 4: `/productos` — Catálogo de Productos

**ESTA ES LA PÁGINA PRINCIPAL DE VENTA.** Debe ser visualmente atractiva.

```
┌──────────────────────────────────────────────────────┐
│  Catálogo                                            │
│                                                      │
│  [🔍 Buscar productos...        ]  [Filtros ▾]      │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │  [IMG]   │ │  [IMG]   │ │  [IMG]   │ │ [IMG]  │ │
│  │          │ │          │ │          │ │        │ │
│  │ Nombre   │ │ Nombre   │ │ Nombre   │ │ Nombre │ │
│  │ Descrip. │ │ Descrip. │ │ Descrip. │ │ Desc.  │ │
│  │ [Cat1]   │ │ [Cat2]   │ │ [Cat1]   │ │ [Cat3] │ │
│  │ $599     │ │ $450     │ │ $720     │ │ $350   │ │
│  │ [Agregar]│ │ [Agregar]│ │ [Agotado]│ │[Agreg.]│ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│                                                      │
│  ← Anterior   Página 1 de 3   Siguiente →           │
│                                                      │
│  Empty: "No hay productos disponibles."              │
│  Error: banner rojo con mensaje                      │
│  Loading: spinner centrado animado                   │
└──────────────────────────────────────────────────────┘
```

**ProductCard (componente reutilizable):**
- Imagen: `w-full h-48 object-cover rounded-t-lg`, fallback a placeholder gris si error
- Nombre: `font-semibold text-gray-900 truncate` (max 2 líneas)
- Descripción: `text-sm text-gray-500 line-clamp-2`
- Categorías: chips `bg-indigo-50 text-indigo-700 text-xs px-2 py-0.5 rounded-full`
- Precio: `text-lg font-bold text-indigo-600`
- Footer: botón "Agregar" (`bg-indigo-600 text-white rounded-lg w-full`) o "Agotado" (disabled `bg-gray-300`)
- Card completa: `bg-white rounded-lg shadow-sm hover:shadow-md transition-shadow overflow-hidden`
- Grid: 1 col mobile, 2 sm, 3 lg, 4 xl

**Filtros (modal/dropdown):**
- Por categoría (checkboxes, jerárquico)
- Por alergenos (excluir ingredientes alergénicos)
- Por disponibilidad (solo disponibles)
- Rango de precio

**Modal de personalización (IngredientsModal):**
- Al hacer click en "Agregar" de un producto con ingredientes:
- Modal overlay con lista de ingredientes (checkbox toggle)
- Ingredientes excluidos: `line-through text-gray-400`
- Ingredientes alergenos: badge `(alergeno)` en red-500 text-xs
- Botones: "Cancelar" + "Agregar al carrito (X items)"

**Paginación:**
- Botones Anterior/Siguiente con estado disabled
- Indicador: "Mostrando 1-12 de 36 productos"

---

### RUTA 5: `/productos/:id` — Detalle de Producto (NUEVA)

```
┌──────────────────────────────────────────────────────┐
│  ← Volver al catálogo                                │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ ┌──────────┐                                   │  │
│  │ │          │  Nombre del Producto              │  │
│  │ │  IMAGEN  │  ★★★★★ (4.5) opcional            │  │
│  │ │  GRANDE  │                                   │  │
│  │ │          │  $599.00                          │  │
│  │ └──────────┘                                   │  │
│  │                                                │  │
│  │  Descripción completa del producto...          │  │
│  │                                                │  │
│  │  Categorías: [Hamburguesas] [Clásicas]        │  │
│  │                                                │  │
│  │  Ingredientes:                                  │  │
│  │  ✓ Lechuga  ✓ Tomate  ✓ Queso Cheddar         │  │
│  │  ✓ Bacon  ⚠ Cebolla (alergeno)               │  │
│  │                                                │  │
│  │  Cantidad: [-]  1  [+]                        │  │
│  │                                                │  │
│  │  [Personalizar Ingredientes]                   │  │
│  │  [Agregar al Carrito — $599]                   │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Productos relacionados (grid de 4)                  │
└──────────────────────────────────────────────────────┘
```

---

### RUTA 6: `/carrito` — Carrito (Página Completa)

```
┌──────────────────────────────────────────────────────┐
│  Mi Carrito (3 items)                                │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ [IMG]  Hamburguesa Clásica      $599           │  │
│  │ 80x80  Sin cebolla              [-] 1 [+]  🗑  │  │
│  ├────────────────────────────────────────────────┤  │
│  │ [IMG]  Pizza Margherita         $850           │  │
│  │ 80x80  Sin aceitunas            [-] 2 [+]  🗑  │  │
│  ├────────────────────────────────────────────────┤  │
│  │ [IMG]  Coca-Cola 500ml          $250           │  │
│  │ 80x80                           [-] 1 [+]  🗑  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Subtotal (4 items)               $2,449.00    │  │
│  │  Costo de envío                     $50.00     │  │
│  │  ─────────────────────────────────────────     │  │
│  │  Total                            $2,499.00    │  │
│  │                                                │  │
│  │  [Vaciar Carrito]   [Ir al Checkout →]        │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Empty: "Tu carrito está vacío" + [Ver Productos]   │
└──────────────────────────────────────────────────────┘
```

### Cart Drawer (slide-in lateral)
- Mismo contenido que la página pero compacto (w-80, 320px)
- Animación slide-in desde derecha
- Overlay `bg-black/40 backdrop-blur-sm`
- Header: "Carrito (X)" + botón cerrar
- Lista compacta: thumbnail 48x48, nombre truncado, controles +/- inline
- Footer sticky: total + [Vaciar] + [Ir al carrito →]

---

### RUTA 7: `/checkout` — Checkout / Crear Pedido (NUEVA - FLUJO CRÍTICO)

```
┌──────────────────────────────────────────────────────┐
│  Finalizar Pedido                                    │
│                                                      │
│  PASO 1: Dirección de Entrega                        │
│  ┌────────────────────────────────────────────────┐  │
│  │ ○ Casa — Calle Falsa 123, CABA               │  │
│  │ ○ Oficina — Av. Siempreviva 742, CABA        │  │
│  │ + Agregar nueva dirección                     │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  PASO 2: Resumen del Pedido                          │
│  ┌────────────────────────────────────────────────┐  │
│  │  1x Hamburguesa Clásica (sin cebolla)  $599   │  │
│  │  2x Pizza Margherita (sin aceitunas) $1,700   │  │
│  │  1x Coca-Cola 500ml                     $250   │  │
│  │  ─────────────────────────────────────────    │  │
│  │  Subtotal      $2,549.00                      │  │
│  │  Envío           $50.00                       │  │
│  │  Total         $2,599.00                      │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  PASO 3: Método de Pago                              │
│  ┌────────────────────────────────────────────────┐  │
│  │ ○ MercadoPago (tarjeta, Rapipago, Pago Fácil)│  │
│  │                                                │  │
│  │  [Pagar con MercadoPago]  ← botón grande      │  │
│  │   🔒 Pago seguro · PCI SAQ-A compliant        │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Estado: idle → creating → redirecting → processing  │
│          → approved ✅ / rejected ❌                  │
└──────────────────────────────────────────────────────┘
```

**Estados del checkout:**
- `idle`: formulario completo, botón habilitado
- `creating`: botón "Creando orden..." con spinner, inputs disabled
- `redirecting`: pantalla completa "Redirigiendo a MercadoPago..." con spinner
- `approved`: pantalla de éxito con ✅ gigante, número de pedido, botón "Ver mis pedidos"
- `rejected`: pantalla de error con ❌, motivo, botón "Reintentar pago" + "Volver al carrito"

---

### RUTA 8: `/pedidos` — Mis Pedidos (Cliente)

```
┌──────────────────────────────────────────────────────┐
│  Mis Pedidos                                         │
│                                                      │
│  Filtros: [Todos] [Pendiente] [Confirmado]           │
│           [En Preparación] [En Camino]               │
│           [Entregado] [Cancelado]                    │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ #1042 | 12/05/2026 | 🟡 Pendiente  | $2,499  │  │
│  ├────────────────────────────────────────────────┤  │
│  │ #1038 | 10/05/2026 | 🟢 Confirmado  | $1,850  │  │
│  ├────────────────────────────────────────────────┤  │
│  │ #1035 | 08/05/2026 | 🟣 Entregado   | $3,200  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ← Anterior   Página 1 de 2   Siguiente →           │
│                                                      │
│  Empty: "No tenés pedidos todavía" con ilustración   │
│  Error: banner rojo                                  │
│  Loading: spinner                                    │
└──────────────────────────────────────────────────────┘
```

**Chips de estado con color semántico:**
| Estado | Color | Badge Class |
|--------|-------|-------------|
| PENDIENTE | Amarillo | `bg-yellow-100 text-yellow-800` |
| CONFIRMADO | Verde | `bg-green-100 text-green-800` |
| EN_PREPARACION | Azul | `bg-blue-100 text-blue-800` |
| EN_CAMINO | Naranja | `bg-orange-100 text-orange-800` |
| ENTREGADO | Esmeralda | `bg-emerald-100 text-emerald-800` |
| CANCELADO | Rojo | `bg-red-100 text-red-800` |

**Mobile: cards apiladas** en vez de tabla. Misma info, layout vertical.

**Order Detail Drawer (slide-in derecha):**
- Header: #Pedido + badge estado + fecha
- Lista de items: producto_id, nombre, cantidad, precio unitario, subtotal
- Exclusiones aplicadas (si hay): "Sin: cebolla, tomate"
- Dirección de entrega completa formateada
- Totales: subtotal, envío, total
- Timeline de estados (historial):
  ```
  PENDIENTE → CONFIRMADO → EN_PREP → EN_CAMINO → ENTREGADO
    12/05      12/05       12/05      12/05       12/05
    14:30      14:32       14:45      15:10       15:35
  ```

---

### RUTA 9: `/direcciones` — Mis Direcciones (Cliente)

```
┌──────────────────────────────────────────────────────┐
│  Mis Direcciones                                     │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ 🏠 Casa              [PREDETERMINADA]          │  │
│  │ Calle Falsa 123, Piso 3°B                      │  │
│  │ CABA, Buenos Aires (C1425)                     │  │
│  │ Ref: Entre Av. Corrientes y Lavalle            │  │
│  │ [Editar]  [Eliminar]  [Marcar Default]         │  │
│  ├────────────────────────────────────────────────┤  │
│  │ 🏢 Oficina                                     │  │
│  │ Av. Siempreviva 742                             │  │
│  │ CABA, Buenos Aires (C1000)                     │  │
│  │ Ref: Piso 5, oficina 502                       │  │
│  │ [Editar]  [Eliminar]  [Marcar Default]         │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌─ Nueva Dirección ──────────────────────────────┐  │
│  │ Etiqueta: [Casa/Oficina/Otro___]               │  │
│  │ País:     [Argentina ▾]                        │  │
│  │ Calle:    [________________]  N°: [____]       │  │
│  │ Piso/Depto: [__________]                       │  │
│  │ CP:       [____]  Ciudad: [________]           │  │
│  │ Provincia: [_______________]                   │  │
│  │ Referencias: [_____________________]           │  │
│  │                                                │  │
│  │ [Guardar Dirección]  [Cancelar]                │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Badge PREDETERMINADA: bg-green-100 text-green-800  │
│  Sin default: warning "No tenés dirección predet."  │
└──────────────────────────────────────────────────────┘
```

---

### RUTA 10: `/puntos-retiro` — Puntos de Retiro (Público)

```
┌──────────────────────────────────────────────────────┐
│  Puntos de Retiro                                    │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ 📍 Sucursal Centro                             │  │
│  │ Av. Corrientes 1234, CABA (C1043)              │  │
│  │ Ref: Frente al Obelisco                        │  │
│  ├────────────────────────────────────────────────┤  │
│  │ 📍 Sucursal Norte                              │  │
│  │ Av. Cabildo 2850, CABA (C1428)                 │  │
│  │ Ref: A 2 cuadras de Juramento                  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Empty: "No hay puntos de retiro disponibles."       │
└──────────────────────────────────────────────────────┘
```

---

### RUTA 11: `/admin` — Dashboard Admin (MÉTRICAS + KPIs)

```
┌──────────────────────────────────────────────────────┐
│  Panel de Administración                             │
│                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
│  │ 📦       │ │ 💰       │ │ 🧾       │ │ 👥     │ │
│  │ Pedidos  │ │ Ingresos │ │ Ticket   │ │Clientes│ │
│  │   156    │ │ $45,230  │ │  $289    │ │  1,240 │ │
│  │ ↑12%     │ │ ↑8%      │ │ Prom.    │ │  ↑5%   │ │
│  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
│                                                      │
│  ┌──────────────────────┐ ┌──────────────────────┐  │
│  │ Ventas últimos 30 días│ │ Pedidos por Estado   │  │
│  │ 📈 gráfico de líneas  │ │ 🍩 gráfico de torta  │  │
│  │  (recharts)           │ │  (recharts)          │  │
│  └──────────────────────┘ └──────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ Top 10 Productos Más Vendidos                  │  │
│  │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │  │
│  │ 1. Hamburguesa Clásica    ████████████  89     │  │
│  │ 2. Pizza Margherita       ██████████    76     │  │
│  │ 3. Coca-Cola 500ml        ████████      65     │  │
│  │ ...                                            │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Accesos rápidos:                                    │
│  [Gestionar Productos]  [Gestionar Usuarios]         │
│  [Gestionar Pedidos]    [Ver Catálogo]               │
└──────────────────────────────────────────────────────┘
```

**KPIs con indicadores de tendencia:**
- Flecha ↑ verde si positivo, ↓ roja si negativo
- Porcentaje de cambio respecto al período anterior

---

### RUTA 12: `/admin/usuarios` — Gestión de Usuarios (Admin)

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Usuarios                                 │
│                                                      │
│  [🔍 Buscar...]  [Filtro: Todos ▾]  [+ Nuevo]      │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ ID │ Nombre         │ Email            │ Rol   │  │
│  │ 1  │ Admin Sistema  │ admin@food...    │ ADMIN │  │
│  │ 2  │ Juan Pérez     │ juan@gmail...    │ CLIENT│  │
│  │ 3  │ María Gestora  │ maria@food...    │ STOCK │  │
│  │ 4  │ Pedro Repart.  │ pedro@food...    │PEDIDOS│  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ← Anterior   Página 1 de 4   Siguiente →           │
│                                                      │
│  Modal Editar Usuario:                               │
│  ┌────────────────────────────────────────────────┐  │
│  │  Nombre: [Juan Pérez         ]                 │  │
│  │  Email:  [juan@gmail.com     ]                 │  │
│  │  Rol:    [CLIENT ▾]                            │  │
│  │  Activo: [✓]                                   │  │
│  │  [Guardar]  [Cancelar]  [Eliminar Usuario]    │  │
│  └────────────────────────────────────────────────┘  │
```

**Badges de rol con color:**
- ADMIN: `bg-purple-100 text-purple-800`
- STOCK: `bg-blue-100 text-blue-800`
- PEDIDOS: `bg-orange-100 text-orange-800`
- CLIENT: `bg-gray-100 text-gray-800`

---

### RUTA 13: `/admin/stock` — Gestión de Stock (Admin/Stock)

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Stock                                    │
│                                                      │
│  [🔍 Buscar...]  [Filtro: Categoría ▾]  [+ Nuevo]  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ IMG │ Producto           │ Stock  │ Disp.│ Acc.│  │
│  │ 🍔  │ Hamburguesa Clásica│  45   │  ✅  │ ⋯  │  │
│  │ 🍕  │ Pizza Margherita  │  12   │  ✅  │ ⋯  │  │
│  │ 🥤  │ Coca-Cola 500ml   │   0   │  ❌  │ ⋯  │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Quick actions en dropdown (⋯):                      │
│  • Editar producto                                   │
│  • Actualizar stock (+/- cantidad o setear)          │
│  • Cambiar disponibilidad (toggle ✅/❌)             │
│  • Eliminar (soft-delete)                            │
│                                                      │
│  Modal Actualizar Stock:                             │
│  ┌────────────────────────────────────┐             │
│  │  Producto: Hamburguesa Clásica     │             │
│  │  Stock actual: 45                  │             │
│  │                                    │             │
│  │  Operación: [Agregar ▾]            │             │
│  │  Cantidad:  [____]                 │             │
│  │  Nuevo stock: 55                   │             │
│  │                                    │             │
│  │  [Aplicar]  [Cancelar]             │             │
│  └────────────────────────────────────┘             │
└──────────────────────────────────────────────────────┘
```

---

### RUTA 14: `/admin/pedidos` — Gestión de Pedidos (Admin/Pedidos)

```
┌──────────────────────────────────────────────────────┐
│  Gestión de Pedidos                                  │
│                                                      │
│  [🔍 Buscar...]  [Filtro: Todos ▾]                  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ #ID  │ Cliente    │ Fecha      │ Estado│ Total │  │
│  │ 1042 │ juan@gm..  │ 12/05 14:30│ 🟡    │$2,499│  │
│  │ 1041 │ maria@ho.. │ 12/05 13:15│ 🟢    │$1,850│  │
│  │ 1040 │ pedro@gm.. │ 12/05 12:00│ 🔵    │$3,200│  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  Click en pedido → drawer detalle + FSM actions:     │
│  ┌────────────────────────────────────────────────┐  │
│  │  Pedido #1042 — 🟡 PENDIENTE                   │  │
│  │  Cliente: juan@gmail.com                       │  │
│  │  ───────────────────────────────               │  │
│  │  Items: (lista con snapshots)                  │  │
│  │  Dirección: Calle Falsa 123, CABA              │  │
│  │  Total: $2,499.00                              │  │
│  │  ───────────────────────────────               │  │
│  │  Historial:                                    │  │
│  │  • 14:30 — PENDIENTE (creado)                  │  │
│  │  ───────────────────────────────               │  │
│  │  Transiciones disponibles:                     │  │
│  │  [✓ Confirmar]  [✗ Cancelar]                  │  │
│  │  Motivo (si cancela): [__________]             │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  FSM Actions visibles según rol y estado actual:     │
│  PENDIENTE  → [Confirmar] [Cancelar]                 │
│  CONFIRMADO → [En Preparación] [Cancelar]            │
│  EN_PREP    → [En Camino] [Cancelar]                 │
│  EN_CAMINO  → [Entregado]                            │
│  ENTREGADO  → (terminal, sin acciones)               │
│  CANCELADO  → (terminal, sin acciones)               │
│                                                      │
│  Cancelación requiere MOTIVO (textarea obligatorio)  │
└──────────────────────────────────────────────────────┘
```

---

### RUTA 15: `/perfil` — Mi Perfil

```
┌──────────────────────────────────────────────────────┐
│  Mi Perfil                                           │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │ 👤  [Foto/avatar placeholder]                  │  │
│  │                                                │  │
│  │  Nombre:    [Juan           ]                  │  │
│  │  Apellido:  [Pérez          ]                  │  │
│  │  Email:     juan@gmail.com   (no editable)     │  │
│  │  Teléfono:  [11 5555-1234   ]                  │  │
│  │                                                │  │
│  │  [Guardar Cambios]                             │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Cambiar Contraseña                            │  │
│  │  Contraseña actual:  [_______________]         │  │
│  │  Nueva contraseña:   [_______________]         │  │
│  │  Confirmar nueva:    [_______________]         │  │
│  │  [Cambiar Contraseña]                          │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## 3. COMPONENTES TRANSVERSALES (TODAS las páginas)

### Toast Notifications
- Posición: `fixed bottom-4 right-4 z-50`
- Tipos: success (green), error (red), info (blue), warning (yellow/amber)
- Auto-dismiss: 5 segundos con fade out
- Botón X para cerrar manualmente
- Máximo 3 toasts visibles simultáneos (stack vertical con gap-2)

### Confirm Modal
- Overlay: `bg-black/50`
- Card centrada: `bg-white rounded-lg shadow-xl max-w-sm p-6`
- Título + mensaje + 2 botones (Cancelar / Confirmar en indigo)
- Usos: "Vaciar carrito", "Eliminar dirección", "Cancelar pedido", "Eliminar usuario"

### Cart Drawer
- Slide-in desde derecha, 320px ancho (w-80), altura completa
- Overlay: `bg-black/40 backdrop-blur-sm`
- Animación: `transform transition-transform duration-300 ease-in-out`
- Abierto/cerrado manejado por uiStore

### Loading States (unificar en 2 patrones):
1. **Spinner full-page:** `flex justify-center py-12` con círculo `animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600`
2. **Skeleton loaders:** Cards fantasma con `animate-pulse bg-gray-200 rounded-lg` para:
   - Product cards (imagen, 2 líneas texto, botón)
   - Order list rows
   - Address cards
   - Dashboard KPIs

### Empty States (patrón consistente):
```
┌──────────────────────────────────────┐
│                                      │
│         [ícono grande gris]          │
│                                      │
│     Mensaje principal amigable       │
│     Subtítulo explicativo            │
│                                      │
│        [Botón de acción CTA]         │
│                                      │
└──────────────────────────────────────┘
```
- Íconos SVG inline (sin dependencia de librería)
- Texto: `text-gray-400` para ícono, `text-gray-900` para título, `text-gray-500` para subtítulo

### Error States
- Banner: `bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg`
- Con ícono ⚠️ y botón "Reintentar" si aplica
- Errores de validación de formularios: `text-red-500 text-xs mt-1` debajo del campo

### Badges de Estado
- Forma: `px-2.5 py-0.5 rounded-full text-xs font-medium`
- Todos los estados de pedido + roles + disponibilidad

---

## 4. PATRONES DE INTERACCIÓN

### Formularios
- Validación client-side ANTES de submit (mostrar errores inline en tiempo real)
- Botón submit disabled durante loading
- Feedback visual: spinner en botón + texto "Guardando..." / "Creando..."
- Éxito: toast verde + redirección si aplica
- Error: toast rojo con mensaje del servidor

### Navegación
- React Router v6 con `<Link>` y `<NavLink>` (active state: `text-indigo-600 font-medium`)
- Protected routes: redirección a `/login` con `state={{ from: location }}` para volver post-login
- Breadcrumbs en páginas admin: Dashboard > Gestión de Usuarios

### Búsqueda y Filtros
- Debounce 300ms en búsqueda por texto
- Filtros como chips toggleables
- Indicador de filtros activos: "3 filtros aplicados · [Limpiar]"

### Paginación
- Botones Anterior/Siguiente con disabled cuando corresponde
- Info: "Mostrando X-Y de Z resultados"
- Page size: 12 para productos, 10 para tablas admin

### Feedback Inmediato
- Agregar al carrito: toast "X agregado al carrito" + bounce en icono carrito
- Eliminar item: toast "X eliminado del carrito"
- Transición de estado: toast + actualización optimista
- Pago aprobado: pantalla de celebración
- Pago rechazado: mensaje claro con motivo + opción de reintentar

---

## 5. FLUJOS COMPLETOS

### Flujo de Compra (End-to-End)
```
Catálogo → ProductCard "Agregar" 
  → (si tiene ingredientes) IngredientsModal → confirmar exclusiones
  → Item en carrito (toast feedback)
  → (repetir para más items)
  → Carrito (drawer o página) → "Ir al Checkout"
  → Checkout:
      1. Seleccionar dirección (o crear nueva)
      2. Revisar resumen (items, subtotales, total)
      3. Seleccionar método de pago → "Pagar con MercadoPago"
  → Redirección a MercadoPago (externo)
  → Webhook → actualiza estado
  → Vuelta al sitio → pantalla de éxito con #pedido
  → "Ver mis pedidos" → tracking en tiempo real
```

### Flujo de Gestión de Pedidos (Admin)
```
Dashboard Admin → "Gestión de Pedidos"
  → Lista con filtros por estado
  → Click en pedido → drawer detalle
  → Ver items (snapshots), dirección, timeline
  → Botones de transición FSM según estado actual
  → Confirmar transición → toast feedback
  → Pedido se mueve al nuevo estado en la lista
```

---

## 6. RESPONSIVE DESIGN

Breakpoints Tailwind:
- **Mobile** (< 640px): 1 columna, cards apiladas, drawer full-width, tablas → cards
- **Tablet** (sm, ≥ 640px): 2 columnas, navbar links visibles
- **Desktop** (lg, ≥ 1024px): 3-4 columnas, sidebar admin
- **Wide** (xl, ≥ 1280px): 4 columnas, max-w-7xl centrado

Reglas:
- Navbar: menú hamburguesa en mobile, links horizontales en desktop
- Tablas admin: colapsan a cards en mobile (cada fila es una card)
- Grid productos: 1 → 2 → 3 → 4 columnas
- Forms: campos full-width en mobile, 2-column grid en desktop
- Cart drawer: w-80 en desktop, w-full en mobile
- Modales: `mx-4` en mobile para padding lateral

---

## 7. ACCESIBILIDAD (a11y)

- Labels `sr-only` en inputs cuando el placeholder es suficiente visualmente
- Focus visibles en TODOS los elementos interactivos
- `aria-label` en botones de ícono (carrito, cerrar, eliminar)
- `role="alert"` en toasts y banners de error
- `aria-live="polite"` en actualizaciones dinámicas (contador carrito)
- Contraste de color AA mínimo
- Navegación por teclado completa

---

## 8. LO QUE NO DEBE FALTAR

1. **Icono de carrito con badge animado** (bounce al agregar items)
2. **Botón "Agregar al carrito" con feedback visual** (cambia brevemente a "✓ Agregado")
3. **Timeline visual de estados** en detalle de pedido (línea con puntos conectados)
4. **Indicador de stock bajo** (< 5 unidades: badge naranja "Pocas unidades")
5. **Producto agotado**: card con opacidad reducida, badge "Agotado", botón disabled
6. **Página 404** personalizada con ilustración y link a home
7. **Footer** simple: "Food Store © 2026 · Todos los derechos reservados"
8. **Loader de página completa** para lazy loading de rutas
9. **Transiciones suaves** entre páginas (opcional: fade)
10. **Estados hover** en TODOS los elementos clickeables

---

## 9. PATRONES DE CÓDIGO — Páginas Admin (dashboard-crud-page)

Toda página admin de gestión (CRUD) debe seguir esta estructura de código. NO usar `useState` para estado de formularios ni modales.

### Hook Trio Obligatorio

| Necesidad | Hook | Import |
|-----------|------|--------|
| Estado de modal + form data | `useFormModal<FormData, Entity>` | `../hooks/useFormModal` |
| Estado de confirmación delete | `useConfirmDialog<Entity>` | `../hooks/useConfirmDialog` |
| Paginación | `usePagination(sortedItems)` | `../hooks/usePagination` |

### React 19 Form Submission — `useActionState`

Usar `useActionState` para TODOS los submits de formularios. NUNCA `useState` + handler manual:

```tsx
const submitAction = useCallback(
  async (_prevState: FormState<EntityFormData>, formData: FormData) => {
    const data = { name: formData.get('name') as string }
    const validation = validateEntity(data)
    if (!validation.isValid) return { errors: validation.errors, isSuccess: false }
    try {
      if (modal.selectedItem) await updateEntityAsync(modal.selectedItem.id, data)
      else await createEntityAsync(data)
      toast.success('Guardado correctamente')
      return { isSuccess: true }
    } catch (error) {
      return { isSuccess: false, message: `Error: ${error}` }
    }
  },
  [modal.selectedItem]
)
const [state, formAction, isPending] = useActionState(submitAction, { isSuccess: false })
if (state.isSuccess && modal.isOpen) modal.close()
```

### Zustand — Selectores siempre, `useShallow` para arrays

```tsx
// ✅ Correcto: selector granular
const items = useStore((s) => s.items)
const addItem = useStore((s) => s.addItem)

// ✅ Arrays filtrados con useShallow
const filtered = useStore(useShallow((s) => s.items.filter(i => i.active)))

// ❌ NUNCA: destructuring del store
const { items, addItem } = useStore()
```

### Estructura de Página Admin (orden canónico)

```
useDocumentTitle → store selectors → permission checks
→ useFormModal + useConfirmDialog → useMemo (sort/filter)
→ usePagination → useActionState → columns (useMemo)
→ JSX: PageContainer > Card > {isLoading ? Skeleton : Table} > Pagination
       > Modal (form con HelpButton + fields) > ConfirmDialog
```

### Columnas con dependencias correctas

```tsx
const columns: TableColumn<Entity>[] = useMemo(() => [
  { key: 'name', label: 'Nombre', render: (item) => <span className="font-medium">{item.name}</span> },
  { key: 'status', label: 'Estado', render: (item) => (
    <Badge variant={item.active ? 'success' : 'danger'}>
      <span className="sr-only">Estado:</span> {item.active ? 'Activo' : 'Inactivo'}
    </Badge>
  )},
  { key: 'actions', label: 'Acciones', render: (item) => (
    <div className="flex items-center gap-1">
      <Button variant="ghost" size="sm" onClick={() => openEdit(item)} aria-label={`Editar ${item.name}`}>
        <Pencil className="w-4 h-4" aria-hidden="true" />
      </Button>
      <Button variant="ghost" size="sm" onClick={() => deleteDialog.open(item)} aria-label={`Eliminar ${item.name}`}>
        <Trash2 className="w-4 h-4" aria-hidden="true" />
      </Button>
    </div>
  )},
], [openEdit, deleteDialog]) // ← deleteDialog (objeto), NO deleteDialog.open
```

---

## 10. DESIGN SYSTEM — Tailwind CSS v4 + CVA

Usar Tailwind CSS v4 con configuración CSS-first (`@theme`), tokens semánticos OKLCH, y `class-variance-authority` para componentes.

### Configuración Base (`app.css`)

```css
@import "tailwindcss";

@theme {
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);
  --color-primary: #4f46e5;       /* indigo-600 */
  --color-primary-foreground: #ffffff;
  --color-secondary: oklch(96% 0.01 264);
  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);
  --color-destructive: oklch(53% 0.22 27);
  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);
  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
}
```

### Componentes con CVA (Class Variance Authority)

```tsx
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-border bg-background hover:bg-accent',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'size-10',
      },
    },
    defaultVariants: { variant: 'default', size: 'default' },
  }
)

// React 19: ref es prop normal, sin forwardRef
export function Button({ className, variant, size, ref, ...props }: ButtonProps & { ref?: React.Ref<HTMLButtonElement> }) {
  return <button className={cn(buttonVariants({ variant, size, className }))} ref={ref} {...props} />
}
```

### Compound Components (Card)

```tsx
export function Card({ className, ref, ...props }: HTMLAttributes<HTMLDivElement> & { ref?: Ref<HTMLDivElement> }) {
  return <div ref={ref} className={cn('rounded-lg border bg-card text-card-foreground shadow-sm', className)} {...props} />
}
export function CardHeader({ className, ref, ...props }) { return <div ref={ref} className={cn('flex flex-col space-y-1.5 p-6', className)} {...props} /> }
export function CardTitle({ className, ref, ...props }) { return <h3 ref={ref} className={cn('text-2xl font-semibold leading-none tracking-tight', className)} {...props} /> }
export function CardContent({ className, ref, ...props }) { return <div ref={ref} className={cn('p-6 pt-0', className)} {...props} /> }
export function CardFooter({ className, ref, ...props }) { return <div ref={ref} className={cn('flex items-center p-6 pt-0', className)} {...props} /> }
```

### Responsive Grid

```tsx
const gridVariants = cva('grid', {
  variants: {
    cols: { 1: 'grid-cols-1', 2: 'grid-cols-1 sm:grid-cols-2', 3: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-3', 4: 'grid-cols-1 sm:grid-cols-2 lg:grid-cols-4' },
    gap: { sm: 'gap-2', md: 'gap-4', lg: 'gap-6' },
  },
  defaultVariants: { cols: 3, gap: 'md' },
})
```

### Toast Pattern

```tsx
// Zustand store para toasts
const useUIStore = create((set) => ({
  toasts: [] as Toast[],
  addToast: (type: 'success' | 'error' | 'info' | 'warning', message: string) =>
    set((s) => ({ toasts: [...s.toasts, { id: Date.now(), type, message }] })),
  removeToast: (id: number) => set((s) => ({ toasts: s.toasts.filter(t => t.id !== id) })),
}))
```

---

## 11. CHECKLIST DE GENERACIÓN — Lo que Stitch DEBE producir

Antes de generar cada pantalla, verificar:

### Páginas Admin (CRUD)
- [ ] `useFormModal` (NO `useState` para modal/form)
- [ ] `useConfirmDialog` (NO `useState` para delete dialog)
- [ ] `usePagination` con `<Pagination>`
- [ ] `useActionState` para form submission (NO `handleSubmit` + `useState`)
- [ ] Zustand selectores granulares (NO destructuring)
- [ ] `useShallow` para arrays filtrados
- [ ] `deleteDialog` (objeto) en deps de `useMemo`, NO `deleteDialog.open`
- [ ] `<TableSkeleton>` mientras `isLoading`
- [ ] `<Badge>` con `<span className="sr-only">Estado:</span>`
- [ ] `aria-label` en botones de ícono, `aria-hidden` en íconos decorativos
- [ ] Componentes con CVA (`buttonVariants`, `gridVariants`)
- [ ] React 19: `ref` como prop normal, sin `forwardRef`

### Todas las Páginas
- [ ] Loading: skeleton o spinner, nunca pantalla en blanco
- [ ] Empty: ícono + mensaje + CTA
- [ ] Error: banner rojo con mensaje + botón reintentar
- [ ] Estados de feedback: toast para toda acción del usuario
- [ ] Mobile-first: 1 col → 2 sm → 3 lg → 4 xl
- [ ] Focus visible en todo elemento interactivo
- [ ] Transiciones suaves: `transition-colors duration-200`
