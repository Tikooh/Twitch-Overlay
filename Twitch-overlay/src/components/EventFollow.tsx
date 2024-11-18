import { useEffect, useState } from "react"
import OnMessage, { messageType } from "../context/OnMessage"

const EventFollow = () => {

    const [user, setUser] = useState('')
    const { addListener, removeListener}  = OnMessage()

    const handleMessage = (event: messageType) => {
        const received_message: messageType = event

        console.log(received_message)

        if (received_message.event === 'follow') {
            console.log(user)
            setUser(received_message.data.name)
        }
    }

    useEffect(() => {
        addListener(handleMessage)

        return () => {
            removeListener(handleMessage)
        }
    },[addListener, removeListener])


    const content = (
        <>
            <p className="p__follow">Thanks for the follow! {user}</p>
        </>
    )
    
    return content
}

export default EventFollow