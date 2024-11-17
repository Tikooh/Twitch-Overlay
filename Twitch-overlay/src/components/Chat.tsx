import { useEffect, useState } from "react"

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

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:5000')
        setSocket(ws)

        ws.onmessage = (event) => {
            const received_message: socketEvent = JSON.parse(event.data)

            if (received_message.event === 'getChat') {
                const msg: message = {
                    ...received_message.data,
                    id: Date.now()
                }

                console.log(msg)
                setMessages(prevMessages => [...prevMessages, msg])

                setTimeout(() => {
                    setMessages(prevMessages => prevMessages.filter(item => item.id !== msg.id))
                }, (received_message.data.expiry))
            }
        }
    }, []) 

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