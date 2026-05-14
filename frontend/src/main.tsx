import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { initMercadoPago } from '@mercadopago/sdk-react'
import { QueryProvider } from './providers/QueryProvider'
import { RouterProvider } from './providers/RouterProvider'
import App from './App'
import './index.css'

initMercadoPago(import.meta.env.VITE_MP_PUBLIC_KEY || '', { locale: 'es-AR' })

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryProvider>
      <RouterProvider>
        <App />
      </RouterProvider>
    </QueryProvider>
  </StrictMode>,
)