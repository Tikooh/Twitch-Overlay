import { createContext, ReactElement, useContext } from "react"

type WebSocketType = WebSocket

const ws = new WebSocket('ws://localhost:5000')

const ws_context = createContext<WebSocketType>(ws)

export const use_ws_context = (): WebSocketType => {
    const context = useContext(ws_context)

    return context
}

type ChildrenType = {
    children?: ReactElement
}

export const WsProvider = ({ children }: ChildrenType) => {
    return (
        <ws_context.Provider value={ws}>
            {children}
        </ws_context.Provider>    
    )
}
