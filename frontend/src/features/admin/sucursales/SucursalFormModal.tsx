import { useState, useEffect } from 'react'
import type { Branch, BranchAddress } from '../../../entities/addresses/types'

interface SucursalFormData {
  nombre: string
  calle: string
  numero: string
  piso_depto: string
  ciudad: string
  provincia: string
  codigo_postal: string
  pais: string
  referencias: string
}

interface SucursalFormModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (data: SucursalFormData) => Promise<void>
  initialData?: { branch: Branch; address?: BranchAddress | null }
  isPending?: boolean
}

const emptyForm: SucursalFormData = {
  nombre: '',
  calle: '',
  numero: '',
  piso_depto: '',
  ciudad: '',
  provincia: '',
  codigo_postal: '',
  pais: 'Argentina',
  referencias: '',
}

export function SucursalFormModal({
  isOpen,
  onClose,
  onSave,
  initialData,
  isPending = false,
}: SucursalFormModalProps) {
  const [form, setForm] = useState<SucursalFormData>(emptyForm)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (initialData) {
      const addr = initialData.address
      setForm({
        nombre: initialData.branch.nombre,
        calle: addr?.calle || '',
        numero: addr?.numero || '',
        piso_depto: addr?.piso_depto || '',
        ciudad: addr?.ciudad || '',
        provincia: addr?.provincia || '',
        codigo_postal: addr?.codigo_postal || '',
        pais: addr?.pais || 'Argentina',
        referencias: addr?.referencias || '',
      })
    } else {
      setForm(emptyForm)
    }
    setError(null)
  }, [initialData, isOpen])

  if (!isOpen) return null

  const isEdit = !!initialData

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (!form.nombre.trim()) {
      setError('El nombre de la sucursal es obligatorio')
      return
    }
    if (!form.calle.trim()) {
      setError('La calle es obligatoria')
      return
    }
    if (!form.numero.trim()) {
      setError('El número es obligatorio')
      return
    }

    try {
      await onSave({
        ...form,
        nombre: form.nombre.trim(),
        calle: form.calle.trim(),
        numero: form.numero.trim(),
      })
    } catch (err: unknown) {
      const detail =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(detail || 'Error al guardar la sucursal')
    }
  }

  const updateField = (field: keyof SucursalFormData, value: string) => {
    setForm((prev) => ({ ...prev, [field]: value }))
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-lg w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">
            {isEdit ? 'Editar sucursal' : 'Nueva sucursal'}
          </h3>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="px-6 py-4 space-y-4">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-3 py-2 rounded text-sm">
                {error}
              </div>
            )}

            {/* Sucursal */}
            <div>
              <label htmlFor="suc-nombre" className="block text-sm font-medium text-gray-700 mb-1">
                Nombre de la sucursal *
              </label>
              <input
                id="suc-nombre"
                type="text"
                value={form.nombre}
                onChange={(e) => updateField('nombre', e.target.value)}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                placeholder="Ej: Sucursal Centro"
              />
            </div>

            <fieldset className="border border-gray-200 rounded-md p-4">
              <legend className="text-sm font-medium text-gray-700 px-1">Dirección</legend>
              <div className="space-y-3 mt-2">
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div className="sm:col-span-2">
                    <label htmlFor="suc-calle" className="block text-xs text-gray-500 mb-1">
                      Calle *
                    </label>
                    <input
                      id="suc-calle"
                      type="text"
                      value={form.calle}
                      onChange={(e) => updateField('calle', e.target.value)}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="Av. Corrientes"
                    />
                  </div>
                  <div>
                    <label htmlFor="suc-numero" className="block text-xs text-gray-500 mb-1">
                      Número *
                    </label>
                    <input
                      id="suc-numero"
                      type="text"
                      value={form.numero}
                      onChange={(e) => updateField('numero', e.target.value)}
                      required
                      inputMode="numeric"
                      pattern="[0-9]*"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="1234"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="suc-piso" className="block text-xs text-gray-500 mb-1">
                    Piso / Depto
                  </label>
                  <input
                    id="suc-piso"
                    type="text"
                    value={form.piso_depto}
                    onChange={(e) => updateField('piso_depto', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                    placeholder="Opcional"
                  />
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="suc-ciudad" className="block text-xs text-gray-500 mb-1">
                      Ciudad *
                    </label>
                    <input
                      id="suc-ciudad"
                      type="text"
                      value={form.ciudad}
                      onChange={(e) => updateField('ciudad', e.target.value)}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="Buenos Aires"
                    />
                  </div>
                  <div>
                    <label htmlFor="suc-provincia" className="block text-xs text-gray-500 mb-1">
                      Provincia *
                    </label>
                    <input
                      id="suc-provincia"
                      type="text"
                      value={form.provincia}
                      onChange={(e) => updateField('provincia', e.target.value)}
                      required
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="CABA"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <div>
                    <label htmlFor="suc-cp" className="block text-xs text-gray-500 mb-1">
                      Código Postal
                    </label>
                    <input
                      id="suc-cp"
                      type="text"
                      value={form.codigo_postal}
                      onChange={(e) => updateField('codigo_postal', e.target.value)}
                      inputMode="numeric"
                      pattern="[0-9]*"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="C1000"
                    />
                  </div>
                  <div>
                    <label htmlFor="suc-pais" className="block text-xs text-gray-500 mb-1">
                      País
                    </label>
                    <input
                      id="suc-pais"
                      type="text"
                      value={form.pais}
                      onChange={(e) => updateField('pais', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                      placeholder="Argentina"
                    />
                  </div>
                </div>

                <div>
                  <label htmlFor="suc-ref" className="block text-xs text-gray-500 mb-1">
                    Referencias
                  </label>
                  <input
                    id="suc-ref"
                    type="text"
                    value={form.referencias}
                    onChange={(e) => updateField('referencias', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md sm:text-sm"
                    placeholder="Entre calles, horario, etc."
                  />
                </div>
              </div>
            </fieldset>
          </div>

          <div className="px-6 py-4 bg-gray-50 flex justify-end gap-3 rounded-b-lg">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-300 rounded text-sm text-gray-700 hover:bg-gray-100"
            >
              Cancelar
            </button>
            <button
              type="submit"
              disabled={isPending}
              className="px-4 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700 disabled:opacity-50"
            >
              {isPending ? 'Guardando...' : 'Guardar'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
