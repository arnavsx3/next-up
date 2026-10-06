const API_URL = "http://localhost:8000";

export async function createQueue() {
  const response = await fetch(`${API_URL}/queues/`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Failed to create queue");
  }

  return response.json();
}

export async function joinQueue(roomCode: string) {
  const response = await fetch(`${API_URL}/queues/${roomCode}/join`, {
    method: "POST",
  });

  if (!response.ok) {
    throw new Error("Queue not found");
  }

  return response.json();
}

export async function getQueue(roomCode: string) {
  const response = await fetch(`${API_URL}/queues/${roomCode}`);

  if (!response.ok) {
    throw new Error("Queue not found");
  }

  return response.json();
}
