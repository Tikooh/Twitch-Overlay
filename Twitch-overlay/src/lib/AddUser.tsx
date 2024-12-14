import useWebSocket from "react-use-websocket"
import { PetType, usePetContext } from "../context/PetContext"
import { useEffect } from "react"
import { message } from "../components/Chat"

const AddUser = () => {

    const { pet_list, set_pet_list } = usePetContext()

    const { lastMessage } = useWebSocket('ws://localhost:5000',
        {share: true})
    
    const changeMessage = (user: PetType, received_message: message) => {
        setTimeout(() => {
            set_pet_list((prevPetList) => prevPetList.map((user) => 
                user.name === received_message.name
                ? { ...user, message: ''}
                : user))
        }, received_message.expiry)

        return { ...user, message: received_message.content}
    }

    const handleMessage = (event: MessageEvent) => {
        const received_message = JSON.parse(event.data)

        if (received_message.event === "newUser") {
            // console.log("here")
            console.log(received_message.data.name)
            set_pet_list((prevPetList) => [
            ...prevPetList, { color: received_message.data.color,
                                name: received_message.data.name,
                                message: '',
                                sprite: '',
                                position: (Math.random() * 600),
                                WALKING_EVENT: true,
                                isWalking: false}])

        }   

        if (received_message.event === "getChat") {
            // console.log(received_message.data)
            set_pet_list((prevPetList) => prevPetList.map((user) => 
                                                        user.name === received_message.data.name
                                                        ? changeMessage(user, received_message.data)
                                                        : user))
            }
        
        if (received_message.event === "changeSprite") {
            set_pet_list((prevPetList) => prevPetList.map((user) =>
                                                        user.name === received_message.data[0]
                                                        ? { ...user, sprite: received_message.data[1]}
                                                        : user))
            }
        }



    useEffect(() => {
        if (lastMessage !== null) {
            handleMessage(lastMessage)
        }
    }, [lastMessage])
    

    return 
}

export default AddUser