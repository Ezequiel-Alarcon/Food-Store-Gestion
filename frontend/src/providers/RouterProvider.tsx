import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { ReactNode } from 'react'

interface RouterProviderProps {
  children: ReactNode
}

export function RouterProvider({ children }: RouterProviderProps) {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={children} />
      </Routes>
    </BrowserRouter>
  )
}

export { BrowserRouter, Routes, Route }