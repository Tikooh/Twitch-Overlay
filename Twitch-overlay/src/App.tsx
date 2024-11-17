import Chat from "./components/Chat"
import EventFollow from "./components/EventFollow"

function App() {

  const content = (
    <>
    <div className="grid">
      <Chat></Chat>
      <EventFollow></EventFollow>
    </div>
    </>
  )

  return content
}

export default App
