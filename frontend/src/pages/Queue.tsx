import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getQueue } from "../services/api";

type QueueUser = {
  username: string;
  position: number;
};

type QueueData = {
  room_code: string;
  users: QueueUser[];
};

function Queue() {
  const { roomCode } = useParams();
  const [queue, setQueue] = useState<QueueData | null>(null);

  useEffect(() => {
    if (!roomCode) return;

    const fetchQueue = async () => {
      try {
        const data = await getQueue(roomCode);
        setQueue(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchQueue();

    const interval = setInterval(fetchQueue, 2000);

    return () => clearInterval(interval);
  }, [roomCode]);

  if (!queue) {
    return (
      <div className="min-h-screen bg-black text-green-400 p-8">LOADING...</div>
    );
  }

  return (
    <main className="min-h-screen bg-[#12002b] text-green-400 font-mono p-6">
      <div className="max-w-2xl mx-auto border-4 border-green-400 bg-black p-8 shadow-[8px_8px_0_#ff00ff]">
        <h1 className="text-4xl font-black">ROOM: {queue.room_code}</h1>

        <p className="mt-2 text-yellow-300">
          PEOPLE IN LINE: {queue.users.length}
        </p>

        <div className="mt-8 space-y-3">
          {queue.users.map((user) => (
            <div
              key={user.position}
              className="border-2 border-cyan-400 p-4 flex justify-between"
            >
              <span>
                #{user.position} {user.username}
              </span>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}

export default Queue;
