import { useCallback, useEffect, useState } from "react";
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
    const [listeners, setListeners] = useState<Set<Listener>>(new Set())

    const addListener = useCallback((listener: Listener) => {
        setListeners(prevlisteners => new Set(prevlisteners).add(listener))
    }, [])

    const removeListener = useCallback((listener: Listener) => {
        const newListeners = new Set(listeners)
        newListeners.delete(listener)
        setListeners(new Set(newListeners))
    }, [])
    
    ws.onmessage = (event) => {
        const received_message = JSON.parse(event.data)

        listeners.forEach(listeners => console.log(listeners))
    
        listeners.forEach(listener => listener(received_message))
    }

    return { addListener, removeListener }
}

export default OnMessage

