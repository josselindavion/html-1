const messagesDiv = document.getElementById("messages");
const form = document.getElementById("message-form");
const input = document.getElementById("message-input");

function appendMessage({ username, content, timestamp }) {
  const isSelf = username === USERNAME;
  const time = new Date(timestamp).toLocaleTimeString("fr-FR", {
    hour: "2-digit",
    minute: "2-digit",
  });

  const div = document.createElement("div");
  div.className = "message" + (isSelf ? " message-self" : "");

  const avatarColor = window.avatarColor ? avatarColor(username) : "#00a884";

  div.innerHTML = isSelf
    ? `<div class="msg-bubble">
         <span class="msg-content">${content}</span>
         <span class="msg-time">${time}</span>
       </div>`
    : `<div class="msg-avatar" data-name="${username}" style="background:${getColor(username)}">${username[0].toUpperCase()}</div>
       <div class="msg-bubble">
         <span class="msg-author">${username}</span>
         <span class="msg-content">${content}</span>
         <span class="msg-time">${time}</span>
       </div>`;

  messagesDiv.appendChild(div);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function getColor(name) {
  const palette = [
    "#e17055","#d63031","#a29bfe","#6c5ce7",
    "#74b9ff","#0984e3","#55efc4","#00b894",
    "#fdcb6e","#e67e22","#fd79a8","#e84393",
  ];
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = (hash * 31 + name.charCodeAt(i)) & 0x7fffffff;
  return palette[hash % palette.length];
}

async function loadHistory() {
  const res = await fetch(`/rooms/${ROOM_ID}/messages`);
  const messages = await res.json();
  messages.forEach(appendMessage);
}

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
