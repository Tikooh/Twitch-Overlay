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

    const ws = use_ws_context()

    useEffect(() => {

        ws.onmessage = (event) => {
            const received_message: socketEvent = JSON.parse(event.data)

            // console.log(received_message)
            if (received_message.event === 'getChat') {

                console.log("Message Received")
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
    }, [ws]) 


    // MESSAGE LIMIT
    useEffect(() => {
        if (messages.length >= 10) {
            setMessages(prevMessages => prevMessages.slice(1))
        }
    }, [messages])

    const content = (
        <>
            <div className="div__chat_window">
                <p>Chat:</p>
                {messages.map(message => {
                    return (
                        <p key={message.id}>{message.name}: {message.content}</p>
                    )
                })}
            </div>
        </>
    )

    return content
}

export default Chat