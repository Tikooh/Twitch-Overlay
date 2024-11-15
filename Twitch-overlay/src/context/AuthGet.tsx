// import axios from 'axios'
// import { createContext, ReactElement, useContext, useEffect, useState } from 'react'

// type auth_token = string

// const initial_auth_token: auth_token = ''

// const auth_token_context = createContext<auth_token>(initial_auth_token)

// export const use_auth_token_context = (): auth_token => {
//     const context = useContext(auth_token_context)

//     return context
// }

// type childrenType = {
//     children?: ReactElement
// }

// export const AuthTokenProvider = ({ children }: childrenType): ReactElement => {
//     const [auth_token, set_auth_token] = useState('')

//     const fetchAuthToken = async () => {
//         const response = await axios.get('http://localhost:5000/getAuth')
//         .then(response => {
//             set_auth_token(response.data.auth_token)
//         })

//         return response
//     }

//     useEffect(() => {
//         fetchAuthToken()
//     }, [])


//     return (
//         <auth_token_context.Provider value={auth_token}>
//             {children}
//         </auth_token_context.Provider>
//     )
// }