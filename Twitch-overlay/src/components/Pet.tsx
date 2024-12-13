import { useEffect } from "react"
import { PetType, usePetContext } from "../context/PetContext"
import artistGif from '../images/people/Artist/Artist-idle.gif'
import artistWalking from '../images/people/Artist/Artist-walk.gif'
import noble_woman_Gif from '../images/people/Noble-Woman/Noble-woman-idle.gif'
import noble_woman_walking from '../images/people/Noble-Woman/Noble-woman-walk.gif'
import { MessageRenderer } from "./Chat"

const Pet = () => {

    const {pet_list, set_pet_list } = usePetContext()

    return (
        <>
        <div className="Spawn_box">
            {pet_list.map((user) => {
                    return (
                        <div key={user.name} className="user"
    
                            style = {{
                                transform: `translateX(${user.position}px)`,
                            }}>
                            <p className="username">{user.name}</p>
                            <img src={user.isWalking? artistWalking : artistGif} alt="" className="person" />
                            <p className="user_message">{<MessageRenderer content={user.message}></MessageRenderer>}</p>
                        </div>
                    )
                })}
        </div>
        </>
    )
}   

export default Pet