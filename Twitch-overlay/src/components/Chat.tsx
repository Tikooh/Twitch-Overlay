import { useEffect, useState } from "react"
import OnMessage, { messageType } from "../context/OnMessage"

export type message = {
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

const Chat = () => {
    // const [auth_token, set_auth_token] = use_auth_token_context()
    const [messages, setMessages] = useState<message[]>([])

    const {addListener, removeListener} = OnMessage()

    const handleMessage = (event: messageType) => {
        const received_message: messageType = event

        if (received_message.event === 'getChat') {

            console.log("Message Received")
            if ('content' in received_message.data && 'expiry' in received_message.data) {
                    
                const msg: message = {
                    ...received_message.data,
                    id: Date.now()
                }
    
                setMessages(prevMessages => [...prevMessages, msg])
    
                setTimeout(() => {
                    setMessages(prevMessages => prevMessages.filter(item => item.id !== msg.id))
                }, (received_message.data.expiry))
            }
    }}

    useEffect(() => {
        addListener(handleMessage)

        return () => {
            removeListener(handleMessage)
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