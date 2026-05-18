import { useMemo, useState } from 'react'
import type { UserAddress, UserAddressCreate } from '../../entities/addresses/types'
import {
  useCreateUserAddress,
  useDeleteUserAddress,
  useSetDefaultUserAddress,
  useUpdateUserAddress,
  useUserAddresses,
} from '../../entities/addresses/queries'

function formatAddress(a: Pick<UserAddress, 'calle' | 'numero' | 'piso_depto' | 'ciudad' | 'provincia' | 'pais'>) {
  const line1 = `${a.calle} ${a.numero}${a.piso_depto ? `, ${a.piso_depto}` : ''}`
  const line2 = `${a.ciudad}, ${a.provincia}, ${a.pais}`
  return { line1, line2 }
}

const emptyForm: UserAddressCreate = {
  etiqueta: null,
  calle: '',
  numero: '',
  piso_depto: null,
  ciudad: '',
  provincia: '',
  codigo_postal: null,
  pais: 'Argentina',
  referencias: null,
}

export function MisDireccionesPage() {
  const { data, isLoading, error } = useUserAddresses()
  const createMut = useCreateUserAddress()
  const updateMut = useUpdateUserAddress()
  const deleteMut = useDeleteUserAddress()
  const defaultMut = useSetDefaultUserAddress()

  const [editing, setEditing] = useState<UserAddress | null>(null)
  const [form, setForm] = useState<UserAddressCreate>(emptyForm)

  const list = data ?? []
  const hasDefault = useMemo(() => list.some((a) => a.is_default), [list])

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editing) {
        await updateMut.mutateAsync({ id: editing.id, payload: form })
      } else {
        await createMut.mutateAsync(form)
      }
      setEditing(null)
      setForm(emptyForm)
    } catch {
      // error handled by mutation state
    }
  }

  const startEdit = (a: UserAddress) => {
    setEditing(a)
    setForm({
      etiqueta: a.etiqueta,
      calle: a.calle,
      numero: a.numero,
      piso_depto: a.piso_depto,
      ciudad: a.ciudad,
      provincia: a.provincia,
      codigo_postal: a.codigo_postal,
      pais: a.pais,
      referencias: a.referencias,
    })
  }

  const cancelEdit = () => {
    setEditing(null)
    setForm(emptyForm)
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Mis direcciones</h1>
        {hasDefault ? (
          <span className="text-sm text-gray-600">Tenés una dirección predeterminada</span>
        ) : (
          <span className="text-sm text-amber-700">Aún no marcaste una predeterminada</span>
        )}
      </div>

      <div className="mt-6 grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="bg-white rounded shadow p-6">
          <h2 className="text-lg font-semibold">
            {editing ? `Editar dirección #${editing.id}` : 'Nueva dirección'}
          </h2>
          <form onSubmit={onSubmit} className="mt-4 space-y-3">
            {createMut.error && (
              <p className="text-red-600 text-sm">Error al crear la dirección: {(createMut.error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Error desconocido'}</p>
            )}
            {updateMut.error && (
              <p className="text-red-600 text-sm">Error al actualizar la dirección: {(updateMut.error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Error desconocido'}</p>
            )}
            {deleteMut.error && (
              <p className="text-red-600 text-sm">Error al eliminar la dirección: {(deleteMut.error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Error desconocido'}</p>
            )}
            {defaultMut.error && (
              <p className="text-red-600 text-sm">Error al cambiar la dirección predeterminada: {(defaultMut.error as { response?: { data?: { detail?: string } } })?.response?.data?.detail || 'Error desconocido'}</p>
            )}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <input
                className="border rounded px-3 py-2"
                placeholder="Etiqueta (Casa, Trabajo)"
                value={form.etiqueta ?? ''}
                onChange={(e) => setForm((p) => ({ ...p, etiqueta: e.target.value || null }))}
              />
              <input
                className="border rounded px-3 py-2"
                placeholder="País"
                value={form.pais}
                onChange={(e) => setForm((p) => ({ ...p, pais: e.target.value }))}
                required
              />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <input
                className="border rounded px-3 py-2 sm:col-span-2"
                placeholder="Calle"
                value={form.calle}
                onChange={(e) => setForm((p) => ({ ...p, calle: e.target.value }))}
                required
              />
              <input
                className="border rounded px-3 py-2"
                placeholder="Número"
                value={form.numero}
                onChange={(e) => setForm((p) => ({ ...p, numero: e.target.value }))}
                required
                inputMode="numeric"
                pattern="[0-9]*"
                title="Solo números"
              />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <input
                className="border rounded px-3 py-2"
                placeholder="Piso / Depto (opcional)"
                value={form.piso_depto ?? ''}
                onChange={(e) => setForm((p) => ({ ...p, piso_depto: e.target.value || null }))}
              />
              <input
                className="border rounded px-3 py-2"
                placeholder="Código postal (opcional)"
                value={form.codigo_postal ?? ''}
                onChange={(e) => setForm((p) => ({ ...p, codigo_postal: e.target.value || null }))}
                inputMode="numeric"
                pattern="[0-9]*"
                title="Solo números"
              />
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <input
                className="border rounded px-3 py-2"
                placeholder="Ciudad"
                value={form.ciudad}
                onChange={(e) => setForm((p) => ({ ...p, ciudad: e.target.value }))}
                required
              />
              <input
                className="border rounded px-3 py-2"
                placeholder="Provincia"
                value={form.provincia}
                onChange={(e) => setForm((p) => ({ ...p, provincia: e.target.value }))}
                required
              />
            </div>
            <textarea
              className="border rounded px-3 py-2 w-full"
              placeholder="Referencias (opcional)"
              value={form.referencias ?? ''}
              onChange={(e) => setForm((p) => ({ ...p, referencias: e.target.value || null }))}
              rows={3}
            />

            <div className="flex gap-3">
              <button
                type="submit"
                className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
                disabled={createMut.isPending || updateMut.isPending}
              >
                {editing ? 'Guardar cambios' : 'Crear'}
              </button>
              {editing && (
                <button
                  type="button"
                  className="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300"
                  onClick={cancelEdit}
                >
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </section>

        <section className="bg-white rounded shadow p-6">
          <h2 className="text-lg font-semibold">Tus direcciones</h2>
          {isLoading ? <p className="mt-4 text-gray-600">Cargando...</p> : null}
          {error ? <p className="mt-4 text-red-600">No se pudieron cargar tus direcciones</p> : null}

          <div className="mt-4 space-y-3">
            {list.length === 0 ? (
              <p className="text-gray-600">Todavía no cargaste direcciones.</p>
            ) : (
              list.map((a) => {
                const { line1, line2 } = formatAddress(a)
                return (
                  <div key={a.id} className="border rounded p-4">
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2">
                          <p className="font-medium">{a.etiqueta ?? `Dirección #${a.id}`}</p>
                          {a.is_default ? (
                            <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-800">
                              Predeterminada
                            </span>
                          ) : null}
                        </div>
                        <p className="text-sm text-gray-800">{line1}</p>
                        <p className="text-sm text-gray-600">{line2}</p>
                        {a.referencias ? (
                          <p className="text-sm text-gray-500 mt-1">{a.referencias}</p>
                        ) : null}
                      </div>
                      <div className="flex flex-col gap-2">
                        <button
                          className="text-sm px-3 py-2 rounded bg-gray-100 hover:bg-gray-200"
                          onClick={() => startEdit(a)}
                        >
                          Editar
                        </button>
                        <button
                          className="text-sm px-3 py-2 rounded bg-red-50 text-red-700 hover:bg-red-100 disabled:opacity-50"
                          disabled={deleteMut.isPending}
                          onClick={async () => {
                            if (!confirm('¿Eliminar esta dirección?')) return
                            await deleteMut.mutateAsync(a.id)
                            if (editing?.id === a.id) cancelEdit()
                          }}
                        >
                          Eliminar
                        </button>
                        {!a.is_default ? (
                          <button
                            className="text-sm px-3 py-2 rounded bg-indigo-50 text-indigo-700 hover:bg-indigo-100 disabled:opacity-50"
                            disabled={defaultMut.isPending}
                            onClick={async () => defaultMut.mutateAsync(a.id)}
                          >
                            Marcar default
                          </button>
                        ) : null}
                      </div>
                    </div>
                  </div>
                )
              })
            )}
          </div>
        </section>
      </div>
    </div>
  )
}
