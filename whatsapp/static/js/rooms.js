async function toggleSubscription(roomId, userId, action) {
  const method = action === "subscribe" ? "POST" : "DELETE";
  const res = await fetch(`/rooms/${roomId}/subscribe?user_id=${userId}`, { method });
  if (res.ok) {
    location.reload();
  }
}
