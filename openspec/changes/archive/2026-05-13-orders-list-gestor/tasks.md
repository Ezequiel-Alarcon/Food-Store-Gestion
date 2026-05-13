## 1. Contract And Schemas

- [x] 1.1 Confirm endpoint shape and query params match `specs/orders-list-gestor/spec.md`
- [x] 1.2 Add/adjust Pydantic schemas for paginated response (`items/total/page/size/pages`)
- [x] 1.3 Add order list item schema for operational listing (includes `cliente_email` for PEDIDOS/ADMIN)

## 2. Repository Query

- [x] 2.1 Implement repository method to list orders with filters (`estado`, `desde`, `hasta`, `q`) and pagination
- [x] 2.2 Ensure query avoids N+1 (joins/selectinload as appropriate) and uses deterministic ordering
- [x] 2.3 Add repository method to count total results for pagination metadata

## 3. Service Layer (RBAC + Scoping)

- [x] 3.1 Implement service function for listing that applies scoping rules (ADMIN/PEDIDOS all orders; CLIENT own orders)
- [x] 3.2 Validate and normalize filters (date parsing, allowed states, empty q)

## 4. Router Integration

- [x] 4.1 Expose `GET /api/v1/pedidos` listing with `response_model` set to the paginated schema
- [x] 4.2 Add `require_role(["ADMIN","PEDIDOS","CLIENT"])` and wire `get_current_user` dependency
- [x] 4.3 Ensure errors are returned as RFC 7807-compatible responses for 401/403/422

## 5. Documentation And Verification

- [x] 5.1 Verify OpenAPI docs show query params, pagination and response models correctly
- [x] 5.2 Add or update backend tests for listing RBAC, filters, pagination and ordering (do not run in this phase)
