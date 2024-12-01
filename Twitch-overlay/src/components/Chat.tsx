import { useEffect, useState } from "react"

import useWebSocket from "react-use-websocket"

export type message = {
    name: string,
    content: string,
    expiry: number
    color: string,
    id: number
}

type propsType = {
    name: string,
    content: string,
    expiry: number
}

const Chat = () => {
    const [messages, setMessages] = useState<message[]>([])

    const { readyState, getWebSocket, lastMessage } = useWebSocket('ws://localhost:5000',
                                                                    {share: true}
    )

    const handleMessage = (event: MessageEvent) => {
        const received_message = JSON.parse(event.data)
        console.log(received_message.data)
        if (received_message.event === 'getChat') {

            console.log("Message Received")
            if ('content' in received_message.data && 'expiry' in received_message.data) {
                    
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
    }}

    useEffect(() => {
        if (lastMessage !== null) {
            handleMessage(lastMessage)
        }
    }, [lastMessage])
    // MESSAGE LIMIT
    useEffect(() => {
        if (messages.length >= 4) {
            setMessages(prevMessages => prevMessages.slice(1))
        }
    }, [messages])

    const content = (
        <>
            <div className="div__chat_window">
                {messages.map(message => {
                    return (
                        <p key={message.id} className="p__chat_message">
                            <span style={{color: message.color}}>{message.name}: </span>
                            <span>{message.content}</span>
                        </p>
                    )
                })}
            </div>
        </>
    )

    return content
}

export default Chat