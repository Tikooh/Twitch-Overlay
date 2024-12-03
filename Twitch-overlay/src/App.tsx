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
      <Pet></Pet>
      <AddUser></AddUser>
    </div>
    </>
  )

  return content
}

export default App
