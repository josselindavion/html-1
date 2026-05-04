// Génère une couleur cohérente à partir d'un nom (même nom = même couleur)
const PALETTE = [
  "#e17055", "#d63031", "#a29bfe", "#6c5ce7",
  "#74b9ff", "#0984e3", "#55efc4", "#00b894",
  "#fdcb6e", "#e67e22", "#fd79a8", "#e84393",
];

function avatarColor(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = (hash * 31 + name.charCodeAt(i)) & 0x7fffffff;
  }
  return PALETTE[hash % PALETTE.length];
}

// Applique la couleur à tous les éléments .avatar et .room-avatar / .header-avatar
document.querySelectorAll("[data-name]").forEach((el) => {
  el.style.backgroundColor = avatarColor(el.dataset.name);
});
