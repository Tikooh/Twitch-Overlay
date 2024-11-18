import { useEffect } from "react";
import { message } from "../components/Chat";
import { use_ws_context } from "./wsContext";


type followType = {
    name: string
}

type MessageData = | message | followType

export type messageType = {
    event: string;
    data: MessageData
}

type Listener = (message: messageType) => void

const OnMessage = () => {

    const ws = use_ws_context()
    const listeners: Set<Listener> = new Set()

    ws.onmessage = (event) => {
        const received_message = JSON.parse(event.data)
    
        listeners.forEach(listener => listener(received_message))
    }

    return {
        addListener: (listener: Listener) => listeners.add(listener),
        removeListener: (listener: Listener) => listeners.delete(listener)
    }
}

export default OnMessage

