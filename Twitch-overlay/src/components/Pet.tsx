import { usePetContext } from "../context/PetContext"


const Pet = () => {

    const {pet_list, set_pet_list } = usePetContext()
    
    console.log(pet_list)
    return (
        <>
            
        </>
    )
}

export default Pet