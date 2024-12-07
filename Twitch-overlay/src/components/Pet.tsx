import { useEffect } from "react"
import { PetType, usePetContext } from "../context/PetContext"
import artistGif from '/home/george/Twitch-Overlay/Twitch-overlay/src/images/people/Artist/Artist-idle.gif'

const Pet = () => {

    const {pet_list, set_pet_list } = usePetContext()

    return (
        <>
            {pet_list.map((user) => {
                return (
                    <div key={user.name} className="user"

                        style = {{
                            transform: `translateX(${user.position}px)`
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