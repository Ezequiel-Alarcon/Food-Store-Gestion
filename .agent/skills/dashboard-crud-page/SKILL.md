---
name: dashboard-crud-page
description: >
  Standardizes Dashboard CRUD pages with consistent structure, hooks, and UI patterns.
  Trigger: When creating any CRUD page in the Dashboard sub-project (src/pages/).
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating a new page under `Dashboard/src/pages/`
- Adding list + create/edit/delete functionality to the Dashboard
- Any page that manages a resource with a table, modal form, and delete confirmation

## Critical Patterns

### 1. Required Hook Trio (NEVER use raw useState for these)

| Need | Hook | Import |
|------|------|--------|
| Modal state + form data | `useFormModal<FormData, Entity>` | `../hooks/useFormModal` |
| Delete confirmation state | `useConfirmDialog<Entity>` | `../hooks/useConfirmDialog` |
| Pagination | `usePagination(sortedItems)` | `../hooks/usePagination` |

### 2. HelpButton — MANDATORY on every page

Every page MUST pass `helpContent` to `PageContainer`. Content lives in `Dashboard/src/utils/helpContent.tsx`, never inline on the page itself.

Every create/edit modal MUST have a small `HelpButton` (`size="sm"`) as the first element inside the form.

### 3. React 19 Form Submission — useActionState (NEVER useState + handler)

Use `useActionState` for all form submissions. The action reads from `FormData`, validates, calls the store async action, returns `FormState<T>`. Close the modal by checking `state.isSuccess` at render time (not inside the action).

### 4. Zustand — Selectors always, useShallow for filtered arrays

Never destructure from a store call. For filtered/computed arrays use `useShallow`. For derived data from already-extracted state use `useMemo`.

### 5. Branch-scoped entities

If the entity belongs to a branch, guard the page render and filter data:
- Show a "select branch first" card when `!selectedBranchId`
- Filter in `useMemo` using `selectedBranchId`
- Pass `selectedBranchId` to `openCreate` as part of the initial form data

### 6. Loading skeleton

Show `<TableSkeleton>` while the store's `isLoading` flag is true, not an empty table.

### 7. Cascade delete

Use wrapper functions from `../services/cascadeService` (e.g., `deleteCategoryWithCascade`). Show `<CascadePreviewList>` inside `<ConfirmDialog>` when there are affected items.

### 8. Columns definition

Define `columns: TableColumn<Entity>[]` with `useMemo`. Include `deleteDialog` (not `deleteDialog.open`) in the deps array to satisfy the React Compiler.

### 9. React Compiler lint rules

- Call all hooks unconditionally — never inside an `if`
- Use the whole `deleteDialog` object in `useMemo` deps, not a property of it
- Avoid `setState` inside `useEffect`; prefer derived state with `useMemo`

---

## Mandatory Page Structure

```
useDocumentTitle
store selectors (never destructure)
branch selectors (if branch-scoped)
permission checks
useFormModal + useConfirmDialog
useEffect → fetch on branch change (if branch-scoped)
useMemo → filter by branch (if branch-scoped)
useMemo → sort
usePagination
useActionState (submitAction + useCallback)
state.isSuccess guard → modal.close()
openCreate / openEdit handlers (useCallback)
handleDelete handler (useCallback, async)
columns (useMemo)
--- guard: !selectedBranchId → fallback card ---
return JSX:
  <> <title/> <meta/>
    <PageContainer helpContent={...} actions={...}>
      <Card>
        {isLoading ? <TableSkeleton> : <Table>}
        <Pagination>
      </Card>
      <Modal footer={Cancel + Submit}>
        <form id="entity-form" action={formAction}>
          HelpButton (size="sm") + label
          ... form fields using modal.formData ...
        </form>
      </Modal>
      <ConfirmDialog>
        <CascadePreviewList> (if applicable)
      </ConfirmDialog>
    </PageContainer>
  </>
```

---

## Code Examples

### Hook trio setup

```typescript
const modal = useFormModal<EntityFormData, Entity>(initialFormData)
const deleteDialog = useConfirmDialog<Entity>()

const {
  paginatedItems,
  currentPage,
  totalPages,
  totalItems,
  itemsPerPage,
  setCurrentPage,
} = usePagination(sortedItems)
```

### useActionState form handling

```typescript
const submitAction = useCallback(
  async (_prevState: FormState<EntityFormData>, formData: FormData): Promise<FormState<EntityFormData>> => {
    const data: EntityFormData = {
      name: formData.get('name') as string,
      is_active: formData.get('is_active') === 'on',
    }

    const validation = validateEntity(data)
    if (!validation.isValid) {
      return { errors: validation.errors, isSuccess: false }
    }

    try {
      if (modal.selectedItem) {
        await updateEntityAsync(modal.selectedItem.id, data)
        toast.success('Actualizado correctamente')
      } else {
        await createEntityAsync(data)
        toast.success('Creado correctamente')
      }
      return { isSuccess: true, message: 'Guardado correctamente' }
    } catch (error) {
      const message = handleError(error, 'EntityPage.submitAction')
      toast.error(`Error al guardar: ${message}`)
      return { isSuccess: false, message: `Error: ${message}` }
    }
  },
  [modal.selectedItem, updateEntityAsync, createEntityAsync]
)

const [state, formAction, isPending] = useActionState<FormState<EntityFormData>, FormData>(
  submitAction,
  { isSuccess: false }
)

// Close modal on success — at render time, not inside the action
if (state.isSuccess && modal.isOpen) {
  modal.close()
}
```

### Branch-scoped guard

```typescript
if (!selectedBranchId) {
  return (
    <PageContainer
      title="Entidades"
      description="Selecciona una sucursal para ver sus entidades"
      helpContent={helpContent.entities}
    >
      <Card className="text-center py-12">
        <p className="text-[var(--text-muted)] mb-4">
          Selecciona una sucursal desde el Dashboard para ver sus entidades
        </p>
        <Button onClick={() => navigate('/')}>Ir al Dashboard</Button>
      </Card>
    </PageContainer>
  )
}
```

### Columns with correct deps

```typescript
const columns: TableColumn<Entity>[] = useMemo(
  () => [
    {
      key: 'name',
      label: 'Nombre',
      render: (item) => <span className="font-medium">{item.name}</span>,
    },
    {
      key: 'is_active',
      label: 'Estado',
      width: 'w-24',
      render: (item) =>
        item.is_active ? (
          <Badge variant="success"><span className="sr-only">Estado:</span> Activo</Badge>
        ) : (
          <Badge variant="danger"><span className="sr-only">Estado:</span> Inactivo</Badge>
        ),
    },
    {
      key: 'actions',
      label: 'Acciones',
      width: 'w-28',
      render: (item) => (
        <div className="flex items-center gap-1">
          {canEdit && (
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => { e.stopPropagation(); openEditModal(item) }}
              aria-label={`Editar ${item.name}`}
            >
              <Pencil className="w-4 h-4" aria-hidden="true" />
            </Button>
          )}
          {canDeleteEntity && (
            <Button
              variant="ghost"
              size="sm"
              onClick={(e) => { e.stopPropagation(); deleteDialog.open(item) }}
              className="text-[var(--danger-icon)] hover:text-[var(--danger-text)] hover:bg-[var(--danger-border)]/10"
              aria-label={`Eliminar ${item.name}`}
            >
              <Trash2 className="w-4 h-4" aria-hidden="true" />
            </Button>
          )}
        </div>
      ),
    },
  ],
  // CORRECT: use deleteDialog object, not deleteDialog.open
  [openEditModal, deleteDialog, canEdit, canDeleteEntity]
)
```

### Modal with HelpButton inside form

```typescript
<Modal
  isOpen={modal.isOpen}
  onClose={modal.close}
  title={modal.selectedItem ? 'Editar Entidad' : 'Nueva Entidad'}
  size="md"
  footer={
    <>
      <Button variant="ghost" onClick={modal.close}>Cancelar</Button>
      <Button type="submit" form="entity-form" isLoading={isPending}>
        {modal.selectedItem ? 'Guardar' : 'Crear'}
      </Button>
    </>
  }
>
  <form id="entity-form" action={formAction} className="space-y-4">
    {/* HelpButton MUST be first element in every modal form */}
    <div className="flex items-center gap-2 mb-2">
      <HelpButton
        title="Formulario de Entidad"
        size="sm"
        content={
          <div className="space-y-3">
            <p><strong>Completa los siguientes campos</strong> para crear o editar:</p>
            <ul className="list-disc pl-5 space-y-2">
              <li><strong>Nombre:</strong> Descripcion del campo.</li>
            </ul>
          </div>
        }
      />
      <span className="text-sm text-[var(--text-tertiary)]">Ayuda sobre el formulario</span>
    </div>

    <Input
      label="Nombre"
      name="name"
      value={modal.formData.name}
      onChange={(e) => modal.setFormData((prev) => ({ ...prev, name: e.target.value }))}
      error={state.errors?.name}
    />

    <Toggle
      label="Activo"
      name="is_active"
      checked={modal.formData.is_active}
      onChange={(e) => modal.setFormData((prev) => ({ ...prev, is_active: e.target.checked }))}
    />
  </form>
</Modal>
```

### ConfirmDialog with cascade preview

```typescript
<ConfirmDialog
  isOpen={deleteDialog.isOpen}
  onClose={deleteDialog.close}
  onConfirm={handleDelete}
  title="Eliminar Entidad"
  message={`¿Estas seguro de eliminar "${deleteDialog.item?.name}"?`}
  confirmLabel="Eliminar"
>
  {deleteDialog.item && (() => {
    const preview = getEntityPreview(deleteDialog.item.id)
    return preview && preview.totalItems > 0 ? (
      <CascadePreviewList preview={preview} />
    ) : null
  })()}
</ConfirmDialog>
```

### Zustand: filtered arrays

```typescript
// useShallow for inline filter in store selector
import { useShallow } from 'zustand/react/shallow'

const filteredItems = useEntityStore(
  useShallow((state) =>
    selectedBranchId ? state.items.filter((i) => i.branch_id === selectedBranchId) : []
  )
)

// useMemo for derived data from already-extracted state
const sortedItems = useMemo(
  () => [...filteredItems].sort((a, b) => a.name.localeCompare(b.name)),
  [filteredItems]
)
```

---

## helpContent Registration

After creating help content, register it in `Dashboard/src/utils/helpContent.tsx`:

```typescript
export const helpContent = {
  // ... existing entries ...
  myEntity: (
    <div className="space-y-3">
      <p>Administra <strong>entidades</strong> del sistema.</p>
      <ul className="list-disc pl-5 space-y-2">
        <li><strong>Crear:</strong> ...</li>
        <li><strong>Editar:</strong> ...</li>
        <li><strong>Eliminar:</strong> ...</li>
      </ul>
    </div>
  ),
}
```

---

## Checklist Before Submitting a New CRUD Page

- [ ] `useFormModal` used (no raw `useState` for modal/form state)
- [ ] `useConfirmDialog` used (no raw `useState` for delete dialog)
- [ ] `usePagination` used with `<Pagination>` component
- [ ] `<PageContainer helpContent={helpContent.xxx}>` — helpContent passed
- [ ] `helpContent.tsx` updated with new entry
- [ ] `HelpButton size="sm"` is first element inside modal form
- [ ] `useActionState` used for form submission (no `handleSubmit` + `useState`)
- [ ] Zustand store accessed via selectors (no destructuring)
- [ ] Filtered arrays use `useShallow` or `useMemo` (not inline filter in selector)
- [ ] `deleteDialog` (not `deleteDialog.open`) in `useMemo` column deps
- [ ] `<TableSkeleton>` shown while `isLoading`
- [ ] Branch guard (fallback card) shown when `!selectedBranchId` (if branch-scoped)
- [ ] Cascade delete uses wrapper from `cascadeService`
- [ ] `aria-label` on all icon-only buttons
- [ ] `aria-hidden="true"` on all decorative icons
- [ ] `<Badge>` includes `<span className="sr-only">Estado:</span>` prefix
- [ ] Toast messages in Spanish
- [ ] Errors caught via `handleError` from `../utils/logger`

---

## Resources

> ⚠️ **Nota**: Los archivos de referencia listados aquí se crean en el change **C-15 dashboard-menu**.
> Si aún no existen, esta skill sirve como template de diseño — seguir los patrones documentados arriba.

- **Reference implementation**: `Dashboard/src/pages/Categories.tsx` (se crea en C-15)
- **Hook sources**: `Dashboard/src/hooks/useFormModal.ts`, `useConfirmDialog.ts`, `usePagination.ts` (C-14)
- **Help content**: `Dashboard/src/utils/helpContent.tsx` (C-15)
- **Cascade service**: `Dashboard/src/services/cascadeService.ts` (C-15)
- **Form types**: `Dashboard/src/types/form.ts` (`FormState<T>`) (C-14)
- **Validation**: `Dashboard/src/utils/validation.ts` (C-14)
- **Logger**: `Dashboard/src/utils/logger.ts` (`handleError`, `logWarning`) (C-01)
