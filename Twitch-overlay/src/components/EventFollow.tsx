import { useEffect, useState } from "react"
import useWebSocket from "react-use-websocket"
import Engineer from '../images/engineer/engine-engineer.gif'
import { playSound } from "../lib/SoundEffect"

const EventFollow = () => {

    const { readyState, getWebSocket, lastMessage } = useWebSocket('ws://localhost:5000',
        {share: true})

    const [follow_content, set_follow_content] = useState<JSX.Element | null>(null)

    const handleMessage = (event: MessageEvent) => {
        const received_message = JSON.parse(event.data)

        // console.log(received_message)

        if (received_message.event === 'follow') {
            playSound()
            const content = (
                <>
                    <div className="follow_box">
                        <img src={Engineer} alt="" className="follow_image" />
                        <h2 className="follow_message">{received_message.data.user_name} has followed!</h2>
                    </div>
                </>
            )

            setTimeout(() => {
                set_follow_content(null)
            }, 5000)

            set_follow_content(content)
        }
        
        
    }

    useEffect(() => {
        if (lastMessage !== null) {
            handleMessage(lastMessage)
        }
    }, [lastMessage]);
    
    return follow_content
}

export default EventFollow