import useWebSocket from "react-use-websocket"
import { usePetContext } from "../context/PetContext"
import { useEffect } from "react"

const AddUser = () => {

    const { pet_list, set_pet_list } = usePetContext()

    const { lastMessage } = useWebSocket('ws://localhost:5000',
        {share: true})
    
    const handleMessage = (event: MessageEvent) => {
        const received_message = JSON.parse(event.data)

        if (received_message.event === "newUser") {
            // console.log("here")
            console.log(received_message.data.name)
            set_pet_list((prevPetList) => [
            ...prevPetList, { color: received_message.data.color,
                                name: received_message.data.name,
                                message: '',
                                isActive: true}])

        }   

        if (received_message.event === "getChat") {
            pet_list.forEach((user, index) => {
                if (user.name === received_message.data.name) {
                    pet_list[index] = { ...pet_list[index], message: received_message.data.message}
                    setTimeout(() => {
                        pet_list[index] = { ...pet_list[index], message: ''}
                    }, received_message.data.expiry)
                }
            })
        }
    }

    useEffect(() => {
        if (lastMessage !== null) {
            handleMessage(lastMessage)
        }
    }, [lastMessage])
    

    return 0
}

export default AddUser