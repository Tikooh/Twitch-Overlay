import { useEffect, useState } from "react"
import axios from 'axios'

type message = {
    name: string,
    content: string
}


const Chat = () => {
    // const [auth_token, set_auth_token] = use_auth_token_context()
    const [messages, setMessages] = useState<message[]>([])


    const fetchMessages = async () => {
        const response = await axios.get('http://localhost:5000/getChat')

        console.log(response.data.messages)
        
        setMessages(response.data.messages)
    }

    useEffect(() => {
        const intervalId = setInterval(() => {
            fetchMessages()
        }, 5000)

        return () => clearInterval(intervalId)
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