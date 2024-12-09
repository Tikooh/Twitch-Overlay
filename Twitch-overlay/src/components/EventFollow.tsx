import { useEffect, useState } from "react"
import useWebSocket from "react-use-websocket"

const EventFollow = () => {

    const { readyState, getWebSocket, lastMessage } = useWebSocket('ws://localhost:5000',
        {share: true})

    const [user, setUser] = useState('')

    const handleMessage = (event: MessageEvent) => {
        const received_message = JSON.parse(event.data)

        // console.log(received_message)

        if (received_message.event === 'getChat') {
            // console.log(user)
            setUser(received_message.data.name)
        }
    }

    useEffect(() => {
        if (lastMessage !== null) {
            handleMessage(lastMessage)
        }
    }, [lastMessage]);


    const content = (
        <>
            {/* <p className="p__follow">Thanks for the follow! {user}</p> */}
        </>
    )
    
    return content
}

export default EventFollow