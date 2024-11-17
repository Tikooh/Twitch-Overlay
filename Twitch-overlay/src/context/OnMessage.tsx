import { use_ws_context } from "./wsContext";



const OnMessage = () => {

    const ws = use_ws_context()
    const listeners = new Set()
    
    ws.onmessage = (event) => {
        const received_message = JSON.parse(event.data)
    
        listeners.forEach(listener => listener(message))
    }

    return {
        addListener: (listener) => listeners.add(listener)
    }


}

export default OnMessage

