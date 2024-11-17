import { useEffect, useState } from "react"
import { use_ws_context } from "../context/wsContext"

type socketEvent = {
    event: string
    data: string
}

const EventFollow = () => {

    const [user, setUser] = useState('')
    const ws = use_ws_context()

    useEffect(() => {

        ws.onmessage = (event) => {
            const received_message: socketEvent = JSON.parse(event.data)

            console.log(user)

            if (received_message.event === 'follow') {
                setUser(received_message.data)
            }
        }
    }, []) 


    const content = (
        <>
            <p className="p__follow">Thanks for the follow! {user}</p>
        </>
    )
    
    return content
}

export default EventFollow