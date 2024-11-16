import { useEffect, useState } from "react"

type message = {
    name: string,
    content: string
}

const Chat = () => {
    // const [auth_token, set_auth_token] = use_auth_token_context()
    const [messages, setMessages] = useState<message[]>([])
    const [socket, setSocket] = useState<WebSocket>()

    useEffect(() => {
        const ws = new WebSocket('ws://localhost:5000')
        setSocket(ws)

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data)
            const { event: eventName, data: messageData } = data

            if (eventName === 'getChat') {
                setMessages(messageData)
            }
        }
    }) 

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