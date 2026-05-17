import { useState, useEffect } from 'react'
import { usePerfil, useUpdatePerfil, useChangePassword } from '../entities/perfil/queries'

export function ProfilePage() {
  const { data, isLoading, error, refetch } = usePerfil()
  const updateMut = useUpdatePerfil()
  const passwordMut = useChangePassword()

  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({ nombre: '', apellido: '', telefono: '' })
  const [passwordForm, setPasswordForm] = useState({ current_password: '', new_password: '' })
  const [profileSuccess, setProfileSuccess] = useState(false)
  const [passwordSuccess, setPasswordSuccess] = useState(false)
  const [passwordError, setPasswordError] = useState('')

  useEffect(() => {
    if (profileSuccess) {
      const timer = setTimeout(() => setProfileSuccess(false), 3000)
      return () => clearTimeout(timer)
    }
  }, [profileSuccess])

  useEffect(() => {
    if (passwordSuccess) {
      const timer = setTimeout(() => setPasswordSuccess(false), 3000)
      return () => clearTimeout(timer)
    }
  }, [passwordSuccess])

  const startEdit = () => {
    if (!data) return
    setForm({
      nombre: data.nombre,
      apellido: data.apellido,
      telefono: data.telefono ?? '',
    })
    setEditing(true)
  }

  const cancelEdit = () => {
    setEditing(false)
  }

  const handleProfileSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await updateMut.mutateAsync({
        nombre: form.nombre || null,
        apellido: form.apellido || null,
        telefono: form.telefono || null,
      })
      setEditing(false)
      setProfileSuccess(true)
    } catch {
      // error handled by mutation state
    }
  }

  const handlePasswordSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setPasswordError('')
    if (passwordForm.new_password.length < 8) {
      setPasswordError('La nueva contraseña debe tener al menos 8 caracteres')
      return
    }
    try {
      await passwordMut.mutateAsync(passwordForm)
      setPasswordForm({ current_password: '', new_password: '' })
      setPasswordSuccess(true)
    } catch {
      // error handled by mutation state
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-indigo-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8 max-w-4xl mx-auto text-center">
        <p className="text-red-600 mb-4">No se pudo cargar el perfil</p>
        <button
          onClick={() => refetch()}
          className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700"
        >
          Reintentar
        </button>
      </div>
    )
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Mi Perfil</h1>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <section className="bg-white rounded shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Datos Personales</h2>

          {profileSuccess && (
            <p className="text-green-600 text-sm mb-4">Perfil actualizado correctamente</p>
          )}

          {updateMut.error && (
            <p className="text-red-600 text-sm mb-4">
              {updateMut.error instanceof Error ? updateMut.error.message : 'Error al actualizar el perfil'}
            </p>
          )}

          {!editing ? (
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-500">Nombre</p>
                <p className="font-medium">{data?.nombre}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Apellido</p>
                <p className="font-medium">{data?.apellido}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="font-medium">{data?.email}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Teléfono</p>
                <p className="font-medium">{data?.telefono || 'No registrado'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Rol</p>
                <p className="font-medium">{data?.rol}</p>
              </div>
              <button
                onClick={startEdit}
                className="mt-4 px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700"
              >
                Editar
              </button>
            </div>
          ) : (
            <form onSubmit={handleProfileSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
                <input
                  value={form.nombre}
                  onChange={(e) => setForm((p) => ({ ...p, nombre: e.target.value }))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Apellido</label>
                <input
                  value={form.apellido}
                  onChange={(e) => setForm((p) => ({ ...p, apellido: e.target.value }))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <input
                  value={data?.email}
                  disabled
                  className="w-full border rounded px-3 py-2 bg-gray-100 text-gray-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                <input
                  value={form.telefono}
                  onChange={(e) => setForm((p) => ({ ...p, telefono: e.target.value }))}
                  className="w-full border rounded px-3 py-2"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Rol</label>
                <input
                  value={data?.rol}
                  disabled
                  className="w-full border rounded px-3 py-2 bg-gray-100 text-gray-500"
                />
              </div>
              <div className="flex gap-3">
                <button
                  type="submit"
                  disabled={updateMut.isPending}
                  className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
                >
                  Guardar
                </button>
                <button
                  type="button"
                  onClick={cancelEdit}
                  className="px-4 py-2 rounded bg-gray-200 text-gray-800 hover:bg-gray-300"
                >
                  Cancelar
                </button>
              </div>
            </form>
          )}
        </section>

        <section className="bg-white rounded shadow p-6">
          <h2 className="text-lg font-semibold mb-4">Cambiar Contraseña</h2>

          {passwordSuccess && (
            <p className="text-green-600 text-sm mb-4">Contraseña actualizada correctamente</p>
          )}

          {passwordError && (
            <p className="text-red-600 text-sm mb-4">{passwordError}</p>
          )}

          {passwordMut.error && (
            <p className="text-red-600 text-sm mb-4">
              {passwordMut.error instanceof Error
                ? passwordMut.error.message
                : 'Error al cambiar la contraseña'}
            </p>
          )}

          <form onSubmit={handlePasswordSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Contraseña actual
              </label>
              <input
                type="password"
                value={passwordForm.current_password}
                onChange={(e) =>
                  setPasswordForm((p) => ({ ...p, current_password: e.target.value }))
                }
                required
                className="w-full border rounded px-3 py-2"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Nueva contraseña
              </label>
              <input
                type="password"
                value={passwordForm.new_password}
                onChange={(e) =>
                  setPasswordForm((p) => ({ ...p, new_password: e.target.value }))
                }
                required
                className="w-full border rounded px-3 py-2"
              />
              <p className="text-xs text-gray-500 mt-1">Mínimo 8 caracteres</p>
            </div>
            <button
              type="submit"
              disabled={passwordMut.isPending}
              className="px-4 py-2 rounded bg-indigo-600 text-white hover:bg-indigo-700 disabled:opacity-50"
            >
              Cambiar contraseña
            </button>
          </form>
        </section>
      </div>
    </div>
  )
}
