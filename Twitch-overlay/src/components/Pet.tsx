import { PetType, usePetContext } from "../context/PetContext"
import { MessageRenderer } from "./Chat"
import { artist, nobleWoman, spriteMap } from "../lib/Sprites"

const Pet = () => {

    const { pet_list, set_pet_list } = usePetContext()
    
    const selectSprite = (user: PetType) => {
        if (user.sprite === 'artist') {
            if (user.isWalking) {
                return artist.walk
            }
            else {
                return artist.idle
            }
        }

        else {
            if (user.isWalking) {
                return nobleWoman.walk
            }
            else {
                return nobleWoman.idle
            }
        }
    }

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
                            <img src={selectSprite(user)} alt="" className="person" />
                            <p className="user_message">{<MessageRenderer content={user.message}></MessageRenderer>}</p>
                        </div>
                    )
                })}
        </div>
        </>
    )
}   

export default Pet