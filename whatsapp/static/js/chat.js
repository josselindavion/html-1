const messagesDiv = document.getElementById("messages");
const form = document.getElementById("message-form");
const input = document.getElementById("message-input");

function appendMessage({ username, content, timestamp }) {
  const isSelf = username === USERNAME;
  const div = document.createElement("div");
  div.className = "message" + (isSelf ? " message-self" : "");

  const time = new Date(timestamp).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  div.innerHTML = `
    <span class="msg-author">${username}</span>
    <span class="msg-content">${content}</span>
    <span class="msg-time">${time}</span>
  `;
  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Chargement de l'historique via HTTP
async function loadHistory() {
  const res = await fetch(`/rooms/${ROOM_ID}/messages`);
  const messages = await res.json();
  messages.forEach(appendMessage);
}

// Connexion WebSocket pour le temps réel
const ws = new WebSocket(`ws://${window.location.host}/ws/${ROOM_ID}/${USER_ID}`);

ws.onmessage = (event) => appendMessage(JSON.parse(event.data));

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (text && ws.readyState === WebSocket.OPEN) {
    ws.send(text);
    input.value = "";
  }
});

loadHistory();
