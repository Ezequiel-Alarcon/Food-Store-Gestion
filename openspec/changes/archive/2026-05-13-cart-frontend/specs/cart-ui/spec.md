## ADDED Requirements

### Requirement: Product Catalog Page
The system SHALL provide a public product catalog page at `/productos` displaying available products in a responsive grid.

#### Scenario: Catalog displays products
- **WHEN** a user navigates to `/productos`
- **THEN** the system displays a grid of product cards with image, name, price, and stock status
- **AND** products are fetched from `GET /api/v1/productos`

#### Scenario: Empty catalog
- **WHEN** no products are available
- **THEN** the system displays a friendly empty state message with a link to browse categories

#### Scenario: Catalog pagination
- **WHEN** there are more than 12 products
- **THEN** the system displays pagination controls (page number, next/prev)

### Requirement: Add to Cart from Catalog
The system SHALL allow adding products to the cart directly from the product catalog page.

#### Scenario: Add product with default quantity
- **WHEN** a user clicks "Agregar" on a product card without ingredients
- **THEN** the product is added to the cart with quantity 1
- **AND** a toast notification confirms the action
- **AND** the cart badge updates to show the new item count

#### Scenario: Add product with ingredients opens exclusion modal
- **WHEN** a user clicks "Agregar" on a product that has ingredients
- **THEN** a modal displays the list of ingredients with checkboxes
- **AND** the user can uncheck ingredients to exclude them
- **AND** upon confirming, the product is added with the excluded ingredient IDs in `personalizacion`

### Requirement: Cart Drawer
The system SHALL provide a cart drawer accessible from any page via the navigation bar cart icon.

#### Scenario: Open cart drawer
- **WHEN** a user clicks the cart icon in the navigation bar
- **THEN** a drawer slides in from the right side of the screen
- **AND** an overlay backdrop appears behind the drawer
- **AND** the drawer displays the cart contents

#### Scenario: Close cart drawer
- **WHEN** the drawer is open and the user clicks the backdrop or a close button
- **THEN** the drawer slides out and the overlay disappears

#### Scenario: Empty cart drawer
- **WHEN** the cart has no items
- **THEN** the drawer shows a message "Tu carrito está vacío"
- **AND** a link to `/productos` is displayed

### Requirement: Cart Summary
The system SHALL display a summary of cart items inside the cart drawer with item details, quantities, and totals.

#### Scenario: Cart item display
- **WHEN** the cart has items
- **THEN** each item shows: product name, unit price, quantity selector, excluded ingredients (if any), and subtotal
- **AND** the bottom of the drawer shows the cart total with 2 decimal places

#### Scenario: Update quantity in drawer
- **WHEN** a user changes the quantity of an item in the drawer
- **THEN** the subtotal updates immediately
- **AND** setting quantity to 0 removes the item

#### Scenario: Remove item from drawer
- **WHEN** a user clicks the remove button on an item
- **THEN** the item is removed from the cart
- **AND** the total recalculates immediately

#### Scenario: Clear entire cart
- **WHEN** a user clicks "Vaciar carrito"
- **THEN** a confirmation dialog appears
- **AND** upon confirming, all items are removed from the cart

### Requirement: Cart Badge in Navigation
The system SHALL display an item count badge on the cart icon in the navigation bar.

#### Scenario: Badge shows item count
- **WHEN** the cart has N items
- **THEN** the cart icon in the navigation bar displays a badge with the number N

#### Scenario: Badge hidden when cart is empty
- **WHEN** the cart has 0 items
- **THEN** no badge is displayed on the cart icon
