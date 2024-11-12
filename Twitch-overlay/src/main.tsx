import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { AuthTokenProvider } from './context/AuthGet.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthTokenProvider>
      <App />
    </AuthTokenProvider>
  </StrictMode>,
)
