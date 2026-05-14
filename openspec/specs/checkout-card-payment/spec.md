## ADDED Requirements

### Requirement: REQ-CP01 — Card Payment Brick Rendering
El sistema SHALL renderizar el CardPayment Brick de `@mercadopago/sdk-react` en la página de checkout con el monto correcto del pedido. El SDK de MercadoPago se inicializa una sola vez a nivel aplicación (`initMercadoPago` en el entry point). El Brick se destruye al desmontar el componente para liberar recursos.

#### Scenario: Brick loads successfully
- **GIVEN** un usuario autenticado con rol CLIENT está en la página de checkout (`/checkout`) con un pedido válido en estado PENDIENTE
- **AND** el SDK de MercadoPago fue inicializado con la public key correcta
- **WHEN** la página de checkout monta el componente de pago
- **THEN** el CardPayment Brick se renderiza dentro del contenedor designado
- **AND** el `initialization.amount` refleja `pedido.total * 100` (centavos)

#### Scenario: Brick initialization error
- **GIVEN** el SDK de MercadoPago no pudo inicializarse (public key inválida, error de red)
- **WHEN** la página de checkout intenta montar el Brick
- **THEN** se muestra un estado de error con el mensaje "No se pudo cargar el formulario de pago. Intentá de nuevo más tarde."
- **AND** se ofrece un botón para reintentar la carga

#### Scenario: Brick destroyed on unmount
- **GIVEN** el CardPayment Brick está montado y visible
- **WHEN** el usuario navega fuera de la página de checkout (back button, redirect)
- **THEN** el método `unmount()` del Brick es invocado durante el cleanup del efecto
- **AND** no quedan listeners ni iframes huérfanos en el DOM

### Requirement: REQ-CP02 — Card Tokenization Flow
El sistema SHALL delegar la tokenización de la tarjeta al CardPayment Brick de MercadoPago. Cuando el usuario completa los datos de tarjeta y envía el formulario, el Brick tokeniza la tarjeta en los servidores de MP y llama al callback `onSubmit` con `formData` que incluye `token`, `payment_method_id`, `issuer_id`, `installments`, y `transaction_amount`.

#### Scenario: Successful tokenization
- **GIVEN** el CardPayment Brick está montado y el usuario ingresó datos de tarjeta válidos
- **WHEN** el usuario hace clic en el botón de pago del Brick
- **THEN** el Brick envía los datos de tarjeta a MercadoPago para tokenización
- **AND** el callback `onSubmit` recibe `formData.token` (string no vacío)
- **AND** `formData.payment_method_id` contiene el método detectado (ej. "visa", "master")
- **AND** `formData.installments` contiene la cantidad de cuotas seleccionada

#### Scenario: Tokenization failure in Brick
- **GIVEN** el usuario ingresó datos de tarjeta inválidos o MercadoPago rechaza la tokenización
- **WHEN** el Brick intenta tokenizar y falla
- **THEN** el Brick muestra el error inline dentro de su propio iframe (mensaje nativo de MP)
- **AND** el callback `onSubmit` NO es invocado
- **AND** el usuario puede corregir los datos y reintentar

#### Scenario: Duplicate submission prevention
- **GIVEN** el usuario ya envió el formulario y la tokenización está en progreso
- **WHEN** el usuario intenta hacer clic nuevamente en el botón de pago
- **THEN** el botón permanece deshabilitado hasta que el callback `onSubmit` complete o falle
- **AND** se muestra un spinner o texto "Procesando pago..."

### Requirement: REQ-CP03 — Payment Creation Request
El sistema SHALL enviar el token de tarjeta y payment_method_id al backend cuando `onSubmit` es invocado por el Brick. El endpoint `POST /api/v1/pagos/crear` debe aceptar un campo `token` opcional en el body. El backend reenvía el token a la API de MercadoPago para procesar el pago.

#### Scenario: Card payment created with token
- **GIVEN** el callback `onSubmit` fue invocado con `formData.token = "abc123"` y `formData.payment_method_id = "visa"`
- **WHEN** el frontend llama a `POST /api/v1/pagos/crear` con `{ pedido_id: 42, payment_method_id: "visa", token: "abc123" }`
- **THEN** el backend recibe el token, lo incluye en el request a MercadoPago API (`payment_data["token"] = token`)
- **AND** el backend retorna `201` con el `PagoResponse` (id, mp_payment_id, status, status_detail, etc.)
- **AND** el frontend almacena el `PagoResponse` en el estado local para mostrar el resultado

#### Scenario: Payment creation fails — pedido not PENDIENTE
- **GIVEN** el pedido con id=42 ya fue pagado y su estado es CONFIRMADO
- **WHEN** el frontend llama a `POST /api/v1/pagos/crear`
- **THEN** el backend retorna `422` con mensaje "Solo pedidos en estado PENDIENTE pueden iniciar pago"
- **AND** el frontend muestra un toast de error y redirige al detalle del pedido

#### Scenario: Payment creation fails — network error
- **GIVEN** el callback `onSubmit` fue invocado correctamente
- **WHEN** el frontend intenta llamar a `POST /api/v1/pagos/crear` pero hay un error de red (timeout, conexión rechazada)
- **THEN** se muestra un toast de error: "Error de conexión. Verificá tu internet y reintentá."
- **AND** el botón de pago del Brick se rehabilita para permitir reintento
- **AND** NO se descarta el token (el Brick mantiene el formulario lleno)

#### Scenario: Backend PagoCreate schema updated with token field
- **GIVEN** el backend expone `POST /api/v1/pagos/crear`
- **WHEN** el schema `PagoCreate` es inspeccionado
- **THEN** incluye el campo `token: Optional[str] = None`
- **AND** el service extrae el token y lo agrega al `payment_data` enviado a MercadoPago: `payment_data["token"] = data.token`
- **AND** el endpoint mantiene compatibilidad hacia atrás (pagos sin token, ej. Rapipago, siguen funcionando)

### Requirement: REQ-CP04 — Payment Status Polling
El sistema SHALL pollear `GET /api/v1/pagos/{pedido_id}` cada 3 segundos después de crear un pago, hasta que el status sea `"approved"` o `"rejected"`, con un máximo de 30 intentos (90 segundos). Durante el polling se muestra un estado de carga.

#### Scenario: Payment transitions to approved
- **GIVEN** se creó un pago vía `POST /api/v1/pagos/crear` y el `status` inicial es `"pending"`
- **WHEN** el frontend inicia el polling a `GET /api/v1/pagos/42`
- **THEN** cada 3 segundos se consulta el endpoint
- **AND** cuando el status cambia a `"approved"`, se detiene el polling
- **AND** se muestra la pantalla de éxito con los detalles del pago

#### Scenario: Payment transitions to rejected
- **GIVEN** el pago fue creado pero MercadoPago rechaza la transacción
- **WHEN** el polling detecta `status: "rejected"`
- **THEN** se detiene el polling inmediatamente
- **AND** se muestra la pantalla de rechazo con `status_detail` explicativo

#### Scenario: Polling timeout — payment stays pending too long
- **GIVEN** el pago fue creado y el status sigue siendo `"pending"` o `"in_process"`
- **WHEN** el polling alcanza 30 intentos (90 segundos) sin resolución
- **THEN** se detiene el polling
- **AND** se muestra un mensaje: "Tu pago está siendo procesado. Te notificaremos cuando se confirme."
- **AND** se ofrece un botón "Ver estado del pedido" que redirige al detalle del pedido

#### Scenario: Polling interrupted by navigation
- **GIVEN** el polling está activo (intervalo corriendo)
- **WHEN** el usuario navega fuera de la página de checkout (back button, cierre de pestaña)
- **THEN** el intervalo de polling se limpia (`clearInterval`)
- **AND** no quedan requests en vuelo que actualicen estado de un componente desmontado

### Requirement: REQ-CP05 — Success Result Display
El sistema SHALL mostrar una pantalla de éxito cuando el pago es aprobado, con los detalles relevantes: método de pago, monto, cuotas (si aplica), y número de pedido. Se debe ofrecer un botón para ver el detalle del pedido.

#### Scenario: Payment approved — success screen
- **GIVEN** el polling detectó `status: "approved"` con `payment_method_id: "visa"` y `transaction_amount: 3500.00`
- **WHEN** se renderiza la pantalla de resultado
- **THEN** se muestra un ícono de check verde con el texto "¡Pago aprobado!"
- **AND** se muestran los detalles: método de pago (Visa), monto ($3.500,00), número de pedido (#42)
- **AND** se muestra un botón "Ver pedido" que redirige a `/pedidos/42`
- **AND** se muestra un botón "Seguir comprando" que redirige a `/productos`

#### Scenario: Payment approved with installments
- **GIVEN** el pago fue aprobado con `installments: 3` y `transaction_amount: 4500.00`
- **WHEN** se muestra la pantalla de éxito
- **THEN** se incluye el detalle de cuotas: "3 cuotas de $1.500,00"
- **AND** el método de pago muestra la marca de la tarjeta (ej. "Mastercard")

#### Scenario: Payment approved — toast notification
- **GIVEN** el pago fue aprobado mientras el usuario está en la página de checkout
- **WHEN** se detecta el status `"approved"`
- **THEN** se dispara un toast de éxito: "¡Pago aprobado! Pedido #42 confirmado."

### Requirement: REQ-CP06 — Error/Rejection Handling
El sistema SHALL mostrar una pantalla de rechazo cuando el pago es rechazado por MercadoPago, con una explicación legible del `status_detail`. El usuario debe poder reintentar el pago con otro método o con la misma tarjeta corregida.

#### Scenario: Payment rejected — insufficient funds
- **GIVEN** el polling detectó `status: "rejected"` con `status_detail: "cc_rejected_insufficient_amount"`
- **WHEN** se renderiza la pantalla de rechazo
- **THEN** se muestra un ícono de error rojo con el texto "Pago rechazado"
- **AND** se muestra la explicación: "Fondos insuficientes. Probá con otra tarjeta."
- **AND** se muestra un botón "Reintentar con otra tarjeta" que resetea el Brick
- **AND** se muestra un botón "Cancelar pedido" que redirige al detalle del pedido

#### Scenario: Payment rejected — card declined
- **GIVEN** `status_detail: "cc_rejected_card_disabled"`
- **WHEN** se muestra la pantalla de rechazo
- **THEN** la explicación dice: "Tarjeta rechazada. Contactá a tu banco o usá otra tarjeta."
- **AND** se ofrece el botón de reintento

#### Scenario: Retry after rejection via backend endpoint
- **GIVEN** el pago fue rechazado y el usuario hace clic en "Reintentar"
- **WHEN** el frontend llama a `POST /api/v1/pagos/{pedido_id}/reintentar`
- **THEN** el backend crea un nuevo pago con nuevo `idempotency_key`
- **AND** el frontend reinicia el flujo: muestra el Brick nuevamente para ingresar otra tarjeta
- **AND** cuando el usuario envía el nuevo formulario, se llama a `POST /api/v1/pagos/crear` con el nuevo token

#### Scenario: Retry fails — payment still in process
- **GIVEN** el usuario intenta reintentar pero el último pago está en status `"pending"`
- **WHEN** el frontend llama a `POST /api/v1/pagos/{pedido_id}/reintentar`
- **THEN** el backend retorna `422` con mensaje "El pago aun esta en proceso, no se puede reintentar"
- **AND** el frontend muestra un toast de advertencia y reanuda el polling

### Requirement: REQ-CP07 — Order Creation Before Payment
El sistema SHALL garantizar que existe un pedido en estado PENDIENTE antes de mostrar el formulario de pago. El pedido se crea a partir del carrito y la dirección seleccionada al entrar a la página de checkout, usando `POST /api/v1/pedidos`. Si no hay carrito o el pedido no se puede crear, el usuario es redirigido.

#### Scenario: Checkout creates order from cart
- **GIVEN** un usuario CLIENT tiene productos en el carrito y una dirección seleccionada
- **WHEN** el usuario navega a `/checkout`
- **THEN** la página llama a `POST /api/v1/pedidos` con los items del carrito y la dirección
- **AND** si el pedido se crea exitosamente (201), se almacena el `pedido_id` en el estado local
- **AND** se procede a mostrar el formulario de pago con el monto del pedido

#### Scenario: Empty cart redirect
- **GIVEN** el carrito del usuario está vacío (no hay items en el Zustand cart store)
- **WHEN** el usuario navega a `/checkout`
- **THEN** se muestra un toast: "Tu carrito está vacío. Agregá productos antes de pagar."
- **AND** el usuario es redirigido a `/productos`

#### Scenario: Order creation fails — no address selected
- **GIVEN** el carrito tiene items pero no hay una dirección seleccionada
- **WHEN** la página de checkout intenta crear el pedido
- **THEN** no se envía el request (validación client-side)
- **AND** se muestra un mensaje: "Seleccioná una dirección de entrega para continuar."
- **AND** se redirige a la sección de selección de dirección dentro de la misma página

#### Scenario: Order creation fails — stock validation error
- **GIVEN** el backend rechaza la creación del pedido por stock insuficiente (422)
- **WHEN** la página de checkout recibe el error
- **THEN** se muestra un toast con el mensaje del backend (ej. "Stock insuficiente para 'Hamburguesa Classic'")
- **AND** el usuario es redirigido al carrito para ajustar cantidades

### Requirement: REQ-CP08 — Address Selection
El sistema SHALL permitir al usuario seleccionar una dirección de entrega desde sus direcciones guardadas (`GET /api/v1/direcciones/user/addresses`) durante el checkout. La dirección seleccionada se usa al crear el pedido.

#### Scenario: User selects a saved address
- **GIVEN** el usuario tiene 3 direcciones guardadas
- **WHEN** la página de checkout carga la sección de dirección
- **THEN** se muestran las direcciones en una lista seleccionable (radio buttons o cards)
- **AND** la dirección marcada como `es_predeterminada` aparece preseleccionada
- **AND** al seleccionar una dirección, se almacena el `direccion_id` en el estado del checkout

#### Scenario: No saved addresses
- **GIVEN** el usuario no tiene direcciones guardadas (`GET /api/v1/direcciones/user/addresses` retorna `[]`)
- **WHEN** la página de checkout carga la sección de dirección
- **THEN** se muestra un mensaje: "No tenés direcciones guardadas. Agregá una para continuar."
- **AND** se ofrece un formulario inline o un botón "Agregar dirección" que abre un modal
- **AND** al crear la dirección vía `POST /api/v1/direcciones/user/addresses`, se refresca la lista automáticamente

#### Scenario: Address fetch fails
- **GIVEN** la llamada a `GET /api/v1/direcciones/user/addresses` falla por error de red
- **WHEN** la página de checkout intenta cargar las direcciones
- **THEN** se muestra un toast de error: "No se pudieron cargar tus direcciones. Reintentá."
- **AND** se ofrece un botón "Reintentar" para volver a fetchear

### Requirement: REQ-CP09 — PCI Compliance
El sistema SHALL garantizar que los datos de tarjeta de crédito/débito nunca toquen el backend de Food Store. Solo el `token` generado por el SDK de MercadoPago se envía al backend. El CardPayment Brick maneja todos los campos PCI-sensibles en iframes seguros de MercadoPago.

#### Scenario: Only token reaches the backend
- **GIVEN** el usuario completó el formulario del Brick y la tokenización fue exitosa
- **WHEN** el frontend envía `POST /api/v1/pagos/crear`
- **THEN** el body contiene `token` (string alfanumérico generado por MP), `pedido_id`, y `payment_method_id`
- **AND** NO contiene `card_number`, `cvv`, `expiration_date`, `cardholder_name`, ni ningún dato crudo de tarjeta
- **AND** el backend recibe exclusivamente el token y lo reenvía a la API de MercadoPago

#### Scenario: Network inspection shows no card data
- **GIVEN** un atacante inspecciona el tráfico de red entre el frontend y el backend
- **WHEN** se captura el request `POST /api/v1/pagos/crear`
- **THEN** el body solo contiene `pedido_id`, `payment_method_id`, y `token`
- **AND** el token por sí solo no permite reconstruir los datos de la tarjeta

#### Scenario: MP SDK script loaded from MercadoPago CDN
- **GIVEN** la aplicación inicializa el SDK
- **WHEN** `initMercadoPago(publicKey)` es invocado
- **THEN** el script del SDK se carga desde `https://sdk.mercadopago.com/js/v2`
- **AND** los iframes del Brick se sirven desde dominios de MercadoPago, no desde el dominio de Food Store

### Requirement: REQ-CP10 — Loading, Empty, and Edge States
El sistema SHALL manejar todos los estados de la UI: carga del Brick, procesamiento de pago, polling, éxito, rechazo, error de red, carrito vacío, sin direcciones, pedido inválido, y navegación durante el proceso.

#### Scenario: Brick loading state
- **GIVEN** la página de checkout está montada pero el Brick aún no se renderizó
- **WHEN** el SDK de MercadoPago está cargando el script y creando el Brick
- **THEN** se muestra un skeleton o spinner con el texto "Cargando formulario de pago..."
- **AND** el contenido del checkout (dirección, resumen del pedido) ya es visible

#### Scenario: Payment processing state
- **GIVEN** el usuario envió el formulario del Brick y se está creando el pago + polleando
- **WHEN** el estado es `processing`
- **THEN** se muestra un overlay o sección con spinner y texto "Procesando tu pago... No cierres esta página."
- **AND** el Brick se oculta o deshabilita para evitar doble envío

#### Scenario: Browser back button during processing
- **GIVEN** el pago está en estado `processing` (polling activo)
- **WHEN** el usuario presiona el botón "Atrás" del navegador
- **THEN** se muestra un diálogo de confirmación: "Hay un pago en proceso. ¿Estás seguro de que querés salir?"
- **AND** si el usuario confirma, se limpia el polling y se redirige al carrito

#### Scenario: Order summary section always visible
- **GIVEN** la página de checkout está cargada
- **WHEN** el usuario está en cualquier estado (carga, selección de dirección, pago, resultado)
- **THEN** el resumen del pedido (items, cantidades, total) es visible en una columna lateral o sección fija
- **AND** el monto total se actualiza si el pedido cambia

### Non-functional Requirements

- **NFR-CP01 — Brick Load Time:** El CardPayment Brick debe renderizarse en menos de 3 segundos desde el mount del componente. Si excede este tiempo, se muestra un mensaje de timeout.
- **NFR-CP02 — Polling Limit:** El polling de estado de pago no debe exceder 30 requests (90 segundos máximo). Al alcanzar el límite, se informa al usuario y se detiene el polling.
- **NFR-CP03 — Responsive Design:** La página de checkout debe ser responsive (mobile-first). En desktop, el resumen del pedido se muestra en una columna lateral derecha; en mobile, el resumen colapsa arriba del formulario de pago.
- **NFR-CP04 — Toast Notifications:** Toda acción del usuario debe tener feedback visual vía toast: pago creado (info), pago aprobado (success), pago rechazado (error), error de red (error), dirección agregada (success), pedido creado (info).
- **NFR-CP05 — Accessibility:** El formulario del Brick debe ser navegable por teclado. Los mensajes de error y éxito deben ser anunciados por lectores de pantalla (`role="alert"`, `aria-live="polite"`). El contraste de color debe cumplir WCAG AA.
- **NFR-CP06 — No Card Data Logging:** El frontend no debe loguear ni almacenar en localStorage/sessionStorage ningún dato de tarjeta ni el token de pago. El token solo debe estar en memoria durante el request al backend.
