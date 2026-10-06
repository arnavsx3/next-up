import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { createQueue, joinQueue } from "../services/api"

function Home() {
  const [roomCode, setRoomCode] = useState("")
  const [message, setMessage] = useState("")
  const navigate = useNavigate()

  async function handleCreate() {
  try {
    const queue = await createQueue()
    navigate(`/queue/${queue.room_code}`)
  } catch {
    setMessage("FAILED TO CREATE QUEUE")
  }
}

  async function handleJoin() {
  try {
    await joinQueue(roomCode)
    navigate(`/queue/${roomCode}`)
  } catch {
    setMessage("QUEUE NOT FOUND")
  }
}

  return (
    <main className="min-h-screen bg-[#12002b] text-green-400 font-mono flex items-center justify-center p-6">
      <div className="w-full max-w-2xl border-4 border-green-400 bg-black p-8 shadow-[8px_8px_0_#ff00ff]">
        <h1 className="text-6xl font-black tracking-widest text-center">
          NEXTUP
        </h1>

        <p className="mt-4 text-center text-yellow-300">
          THE INTERNET'S MOST SERIOUS QUEUE
        </p>

        <div className="mt-10 flex flex-col gap-4">
          <button
            onClick={handleCreate}
            className="border-4 border-green-400 bg-green-400 px-6 py-4 text-black font-black hover:bg-black hover:text-green-400"
          >
            CREATE QUEUE
          </button>

          <input
            value={roomCode}
            onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
            placeholder="ENTER ROOM CODE"
            className="border-4 border-cyan-400 bg-black px-6 py-4 text-cyan-400 outline-none"
          />

          <button
            onClick={handleJoin}
            className="border-4 border-cyan-400 bg-cyan-400 px-6 py-4 text-black font-black hover:bg-black hover:text-cyan-400"
          >
            JOIN QUEUE
          </button>
        </div>

        {message && (
          <p className="mt-8 text-center text-pink-500">
            ★ {message} ★
          </p>
        )}

        <p className="mt-10 text-center text-sm text-pink-500">
          ★ NO LOGIN • NO ACCOUNT • JUST QUEUE ★
        </p>
      </div>
    </main>
  )
}

export default Home