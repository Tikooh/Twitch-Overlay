import Chat from "./components/Chat"
import EventFollow from "./components/EventFollow"
import Pet from "./components/Pet"
import AddUser from "./lib/AddUser"

function App() {

  const content = (
    <>
    <div className="grid">
      <Chat></Chat>
      <EventFollow></EventFollow>
      <AddUser></AddUser>
      <Pet></Pet>
    </div>
    </>
  )

  return content
}

export default App
