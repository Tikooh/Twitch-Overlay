import { createContext, ReactElement, useContext, useMemo, useState } from "react"


export type PetType = {
    color: string,
    name: string,
    message: string,
    position: number
    isActive: boolean,
}

const pet_list_context = createContext<{
    pet_list: PetType[];
    set_pet_list: React.Dispatch<React.SetStateAction<PetType[]>>;
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

    const [pet_list, set_pet_list] = useState<PetType[]>([])


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