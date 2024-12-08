import { useEffect, useState } from "react"
import { PetType, usePetContext } from "../context/PetContext"

const MAX_WALK_SPEED = 100
const POLL_INTERVAL = 4000
const LEFT_MAX = 300
const RIGHT_MAX = -300

const ChangePosition = (position: number) => {
    const direction = Math.random() < 0.5 ? -1: 1

    const new_pos = position + (Math.random() * MAX_WALK_SPEED * direction)

    if (new_pos >= LEFT_MAX) {
        new_pos - 200
    }
    if (new_pos <= RIGHT_MAX) {
        new_pos + 200
    }

    return new_pos
}

const UserLogic = () => {

    const { pet_list, set_pet_list } = usePetContext()

    useEffect(() => {
        const intervalID = setInterval(() => {

            pet_list.map((user) => {
                if (user.WALKING_EVENT) {
                    const random_start = Math.floor(Math.random() * 2000) + 500
                    setTimeout(() => {

                        set_pet_list((prevPetList) => prevPetList.map((pet) => 
                            user.name === pet.name
                            ? { ...pet, isWalking: true, position: ChangePosition(pet.position)}
                            : pet))

                        setTimeout(() => {
                            set_pet_list((prevPetList) => prevPetList.map((pet) => 
                                user.name === pet.name
                                ? { ...pet, isWalking: false}
                                : pet))
                        }, 2000);

                    }, random_start)
                }
            })
        }, POLL_INTERVAL) 
        
        return () => clearInterval(intervalID)
    }, [pet_list])
}

export default UserLogic