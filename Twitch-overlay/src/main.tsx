import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { WsProvider } from './context/wsContext.tsx'

createRoot(document.getElementById('root')!).render(
  <WsProvider>
    <App />
  </WsProvider>
)
