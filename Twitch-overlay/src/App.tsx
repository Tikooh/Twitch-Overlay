import Chat from "./components/Chat"
import EventFollow from "./components/EventFollow"
import Pet from "./components/Pet"
import AddUser from "./lib/AddUser"
import UserLogic from "./lib/UserLogic"

function App() {

  const content = (
    <>
    <div className="grid">
      <Chat></Chat>
      <EventFollow></EventFollow>
      <AddUser></AddUser>
      <Pet></Pet>
      <UserLogic></UserLogic>
    </div>
    </>
  )

  return content
}

export default App
