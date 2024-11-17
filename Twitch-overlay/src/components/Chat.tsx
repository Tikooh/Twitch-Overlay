import { useEffect, useState } from "react"
import { use_ws_context } from "../context/wsContext"

type message = {
    name: string,
    content: string,
    expiry: number
    id: number
}

type propsType = {
    name: string,
    content: string,
    expiry: number
}

type socketEvent = {
    event: string
    data: propsType
}

const Chat = () => {
    // const [auth_token, set_auth_token] = use_auth_token_context()
    const [messages, setMessages] = useState<message[]>([])
    const [socket, setSocket] = useState<WebSocket>()

    const ws = use_ws_context()

    useEffect(() => {
        setSocket(ws)

        ws.onmessage = (event) => {
            const received_message: socketEvent = JSON.parse(event.data)

            if (received_message.event === 'getChat') {
                const msg: message = {
                    ...received_message.data,
                    id: Date.now()
                }

                setMessages(prevMessages => [...prevMessages, msg])

                setTimeout(() => {
                    setMessages(prevMessages => prevMessages.filter(item => item.id !== msg.id))
                }, (received_message.data.expiry))
            }
        }
    }, []) 


    // MESSAGE LIMIT
    useEffect(() => {
        if (messages.length >= 10) {
            setMessages(prevMessages => prevMessages.slice(1))
        }
    }, [messages])

    const content = (
        <>
            <div>
                <p>Chat:</p>
                {messages.map(message => {
                    return (
                        <p>{message.name}: {message.content}</p>
                    )
                })}
            </div>
        </>
    )

    return content
}

export default Chat