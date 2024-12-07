import { useEffect } from "react"
import { PetType, usePetContext } from "../context/PetContext"

const WALK_SPEED = 100
const POLL_INTERVAL = 4000

const ChangePosition = (position: number) => {
    const direction = Math.random() < 0.5 ? -1: 1

    const new_pos = position + (WALK_SPEED * direction)
    return position + (WALK_SPEED * direction)
}

const UserLogic = () => {
    const { pet_list, set_pet_list } = usePetContext()

    useEffect(() => {
        const intervalID = setInterval(() => {

            pet_list.map((user) => {
                if (user.isWalking) {
                    console.log(user.position)
                    const random_start = Math.floor(Math.random() * 2000) + 500
                    setTimeout(() => {

                        set_pet_list((prevPetList) => prevPetList.map((pet) => 
                            user.name === pet.name
                            ? { ...pet, position: ChangePosition(pet.position)}
                            : pet))

                    }, random_start)
                }
            })
        }, POLL_INTERVAL) 
        
        return () => clearInterval(intervalID)
    }, [pet_list])
}

export default UserLogic