import { createContext, ReactElement, useContext, useMemo, useState } from "react"


type Pet = {
    color: string,
    name: string,
    isActive: boolean,
}

const pet_list_context = createContext<{
    pet_list: Pet[];
    set_pet_list: React.Dispatch<React.SetStateAction<Pet[]>>;
} | undefined>(undefined)

type childrenType = {
    children?: ReactElement
}

export const usePetContext = () => {
    
    const context = useContext(pet_list_context)
    if (!context) {
        throw new Error("usePetContext must be used within a PetContextProvider");
    }

    return context
}

export const PetContextProvider = ({children}: childrenType) => {

    const [pet_list, set_pet_list] = useState<Pet[]>([])


    // avoid rerendering unless pet_list changes
    const contextValue = useMemo(() => ({
        pet_list,
        set_pet_list
    }), [pet_list])

    return (
        <pet_list_context.Provider value={contextValue}>
            {children}
        </pet_list_context.Provider>

    )
}

export default PetContextProvider