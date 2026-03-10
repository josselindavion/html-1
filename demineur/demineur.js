// On récupère l'élément HTML qui va contenir notre grille
const gridElement = document.getElementById('grid');

// On récupère l'element HTML qui contient le compteur de mines
const compteur = document.getElementById('compteur')

// On définit la taille de notre grille (9 colonnes x 9 lignes = 81 cases)
const colonnes = 9;
const lignes = 9;
const totalCases = colonnes * lignes;
let totalMines = 10; // Nombre de mines à placer
let casesDecouvertes = 0; // Compteur de cases découvertes

// Fonction pour créer le plateau de jeu visuel
function createGrid() {
    // On fait une boucle qui va tourner 81 fois
    for (let i = 0; i < totalCases; i++) {
        
        // 1. On demande à JS de créer une nouvelle balise <div>
        const caseHTML = document.createElement('div');        
        // 2. On lui donne la classe "cell" pour que le CSS s'applique (couleur, taille, etc.)
        caseHTML.classList.add('cell');
        
        // 3. On lui donne un id unique pour pouvoir la différencier des autres cases
        caseHTML.id = i;

        // 4. On ajoute un événement "click" à chaque case pour pouvoir réagir quand l'utilisateur clique dessus
        caseHTML.addEventListener('click', gererClic);
        caseHTML.addEventListener('contextmenu', gererClicDroit);
        
        // 5. On insère cette nouvelle case à l'intérieur de notre <div id="grid">
        gridElement.appendChild(caseHTML);
    }
}

// On lance la fonction pour que la grille se dessine au chargement de la page
createGrid();

let tableau = Array(totalCases).fill(0); // Crée un tableau de 81 éléments initialisés à 0

function placeMines() {
    let minesPlaced = 0;
    while (minesPlaced < totalMines) {
        const randomIndex = Math.floor(Math.random() * totalCases);
        if (tableau[randomIndex] === 0) { // Vérifie si la case n'a pas déjà une mine
            tableau[randomIndex] = 1; // Place une mine (1)
            minesPlaced++;
        }
    }
}

placeMines();
console.log(tableau);

let tableau_voisins = Array(totalCases).fill(0); // Crée un tableau pour stocker le nombre de mines voisines

function countneighbour() {
    for (let i = 0; i < totalCases; i++) {
        if (tableau[i] === 1) { // Si la case contient une mine, on met -1 dans le tableau des voisins pour l'indiquer
            tableau_voisins[i] = -1; // On met -1 pour indiquer qu'il y a une mine
        }
        // Sinon, on compte le nombre de mines autour de cette case et on l'ajoute au tableau des voisins
        else {
            let count = 0;
            const row = Math.floor(i / colonnes);
            const col = i % colonnes;
            for (let dr = -1; dr <= 1; dr++) {
                for (let dc = -1; dc <= 1; dc++) {
                    if (dr === 0 && dc === 0) continue;
                    const newRow = row + dr;
                    const newCol = col + dc;
                    if (newRow >= 0 && newRow < lignes && newCol >= 0 && newCol < colonnes) {
                        const indexVoisin = newRow * colonnes + newCol;
                        if (tableau[indexVoisin] === 1) {
                            count++;
                        }
                    }
                }
            }
            tableau_voisins[i] = count;
        }
    }
}

countneighbour();
console.log(tableau_voisins);

function gererClic(event) {
    const caseCliquee = event.target;

    // On vérifie que la case cliquée n'est pas déjà révélée
    if (caseCliquee.classList.contains('revealed')) {
        return; // Si elle est déjà révélée, on ne fait rien
    }

    //On vérifie que la case cliquée n'est pas déjà marquée auquel cas on empeche le clic
    if (caseCliquee.classList.contains('flagged')) {
        return; // Si elle est déjà marquée, on ne fait rien - on ne peut pas cliquer sur une case marquée
    }

    // Récupération de l'index de la case cliquée à partir de son id
    const index = parseInt(caseCliquee.id);

    // On vérifie si la case contient une mine
    if (tableau_voisins[index] === -1) {
        caseCliquee.classList.add('mine'); // On ajoute une classe pour afficher la mine
        let ecranLose = document.getElementById('message-lose');
        ecranLose.classList.add('show'); // Affiche le message de défaite
        ouvertureGrille(); // Révèle toutes les cases pour montrer où étaient les mines
    }
    
    // Si la cas ne contient pas de mine et pas de voisin, on la révèle simplement et on fait la cascade
    else if (tableau_voisins[index] === 0) {
        reveler_cascade(index);
    }

    // Si la case ne contient pas de mine mais a des voisins, on affiche le nombre de mines voisines
    else {
        caseCliquee.textContent = tableau_voisins[index];
        caseCliquee.classList.add('revealed');
        casesDecouvertes++; // Incrémente le compteur de cases découvertes de 1
        caseCliquee.setAttribute('data-value', tableau_voisins[index]);
    }

    // Après chaque clic, on vérifie si le joueur a gagné en comparant le nombre de mines découvertes avec le nombre total de mines
    if (casesDecouvertes === totalCases - totalMines) {
        let ecranWin = document.getElementById('message-win');
        ecranWin.classList.add('show'); // Affiche le message de victoire
        ouvertureGrille(); // Révèle toutes les cases pour montrer où étaient les mines
    }

}

function reveler_cascade(index) {
    const caseActuelle = document.getElementById(index);

    // On vérifie que la case actuelle n'est pas déjà révélée - condition d'arrêt de la récursion
    if (caseActuelle.classList.contains('revealed')) {
        return; // Si elle est déjà révélée, on ne fait rien
    }

    // On révèle la case actuelle
    caseActuelle.classList.add('revealed');
    casesDecouvertes++; // Incrémente le compteur de cases découvertes de 1


    // On récupère sa valeur dans le tableau des voisins
    const value = tableau_voisins[index];

    // Si la case a des mines voisines, on affiche le nombre et on arrête la récursion
    if (value > 0) {
        caseActuelle.textContent = value;
        caseActuelle.setAttribute('data-value', value);
        return;
    }

    // Si la case n'a pas de mines voisines, on continue à révéler les cases autour
    const row = Math.floor(index / colonnes);
    const col = index % colonnes;
    for (let dr = -1; dr <= 1; dr++) {
        for (let dc = -1; dc <= 1; dc++) {
            if (dr === 0 && dc === 0) continue; // On ne traite pas la case actuelle
            const newRow = row + dr;
            const newCol = col + dc;
            if (newRow >= 0 && newRow < lignes && newCol >= 0 && newCol < colonnes) {
                const newIndex = newRow * colonnes + newCol;
                reveler_cascade(newIndex); // Appel récursif pour révéler la case voisine
            }
        }
    }
    

}

function gererClicDroit(event) {
    // On récupère la case sur laquelle l'utilisateur a cliqué
    caseCliquee = event.target;
    
    event.preventDefault(); // Empêche le menu contextuel de s'afficher quand on clique droit

    // On vérifie que la case cliquée n'est pas déjà révélée
    if (caseCliquee.classList.contains('revealed')) {
        return; // Si elle est déjà révélée, on ne fait rien - on ne peut pas marquer une case révélée
    }

    // Récupération de l'index de la case cliquée à partir de son id
    const index = parseInt(caseCliquee.id);

    // On vérifie si la case est déjà marquée (pour enlever le drapeau) ou pas (pour ajouter un drapeau)
    if (caseCliquee.classList.contains('flagged')) {
        caseCliquee.classList.remove('flagged'); // Si elle est déjà marquée, on enlève le drapeau
        totalMines++
        compteur.textContent = totalMines
        
    }
    else {
        caseCliquee.classList.add('flagged'); // Sinon, on ajoute un drapeau pour marquer la case
        totalMines--
        compteur.textContent = totalMines
    }
}

// Gestion du bouton "Recommencer" pour réinitialiser le jeu
const resetButton = document.getElementById('reset-button');
resetButton.addEventListener('click', reset);

function reset() {
    window.location.reload();
}

function ouvertureGrille() {
    for (let i = 0; i < totalCases; i++) {
        const caseElement = document.getElementById(i);
        if (tableau_voisins[i] === -1) {
            caseElement.classList.add('mine'); // Affiche la mine
        } else if (tableau_voisins[i] > 0) {
            caseElement.textContent = tableau_voisins[i]; // Affiche le nombre de mines voisines
            caseElement.setAttribute('data-value', tableau_voisins[i]);
        }
        caseElement.classList.add('revealed'); // Révèle la case
    }
}