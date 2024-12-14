import { PetType, usePetContext } from "../context/PetContext"
import { MessageRenderer } from "./Chat"
import { spriteMap } from "../lib/Sprites"

const Pet = () => {

    const { pet_list, set_pet_list } = usePetContext()

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
                            <img src={user.isWalking? spriteMap[user.sprite].idle : spriteMap[user.sprite].idle} alt="" className="person" />
                            <p className="user_message">{<MessageRenderer content={user.message}></MessageRenderer>}</p>
                        </div>
                    )
                })}
        </div>
        </>
    )
}   

export default Pet