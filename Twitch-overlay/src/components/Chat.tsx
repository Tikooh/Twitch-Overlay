import { useEffect, useState } from "react"
import axios from 'axios'
import { use_auth_token_context } from "../context/AuthGet"

type message = {
    user: string,
    message: string
}

const [messages, setMessages] = useState<message[]>([])

const fetchMessages = async () => {
    const response = await axios.get('http://localhost:5000/')
}
useEffect(() => {

})

const Chat = () => {
    const [auth_token, set_auth_token] = use_auth_token_context()
    
    const content = (
        <>

        </>
    )

    return content
}

export default Chat