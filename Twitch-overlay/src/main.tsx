import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import PetContextProvider from './context/PetContext.tsx'

createRoot(document.getElementById('root')!).render(
  <PetContextProvider>
    <App />
  </PetContextProvider>
)
