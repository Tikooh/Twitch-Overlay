import { useEffect } from "react"
import { PetType, usePetContext } from "../context/PetContext"
import artistGif from '/home/george/Twitch-Overlay/Twitch-overlay/src/images/people/Artist/Artist-idle.gif'

const Pet = () => {

    const {pet_list, set_pet_list } = usePetContext()
    const walk_speed = 5

    const PetLogic = ({ pet }) => {
        useEffect(() => {
            const moveSprite = (user: PetType) => {
    
                const direction = Math.random() < 0.5 ? -1: 1
                user.position = user.position + (walk_speed * direction)
    
                setTimeout(()=> {
                    user.isActive = false
                }, Math.floor(Math.random() * 2000) + 500)
    
            pet_list.map(user => {
                if (user.isActive) {
                    moveSprite(user)
                }
                else {
                    const random_interval = Math.floor(Math.random() * 2000) + 500
                    const setWalk = setTimeout(()=> {
                        user.isActive = true
                    }, random_interval)
                }
            })
    
            }
        }, [pet.isActive] )
    }

    useEffect(() => {
        pet_list.forEach(pet => {
            PetLogic(pet)
        })
    })
    return (
        <>
            {pet_list.map((user) => {
                return (
                    <div key={user.name} className="user"
                        style = {{
                            transform: `translateX(${user.position}px)`,

                        }}>
                        <p className="username">{user.name}</p>
                        <img src={artistGif} alt="" className="person" />
                        <p className="user_message">{user.message}</p>
                    </div>
                )
            })}
        </>
    )
}   

export default Pet