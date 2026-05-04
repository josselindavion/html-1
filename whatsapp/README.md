# Mini WhatsApp

Application de chat en temps réel inspirée de WhatsApp, construite avec FastAPI, WebSockets et SQLite.

## Stack technique

| Couche | Technologie |
|--------|-------------|
| Backend | FastAPI + SQLModel |
| Base de données | SQLite (via SQLModel/SQLAlchemy) |
| Temps réel | WebSockets |
| Frontend | Jinja2 + Vanilla JavaScript |
| Style | CSS maison (thème vert WhatsApp) |

## Installation

```bash
pip install "fastapi[standard]" sqlmodel jinja2
```

## Lancer le serveur

```bash
# (optionnel) repartir d'une BDD vierge
rm whatsapp.db

# démarrer en mode développement
fastapi dev main.py
```

## Créer des utilisateurs et des salons

Dans un second terminal (utilise [httpie](https://httpie.io/)) :

```bash
# Créer des utilisateurs
http POST http://localhost:8000/users name=alice
http POST http://localhost:8000/users name=bob
http POST http://localhost:8000/users name=charlie

# Créer des salons
http POST http://localhost:8000/rooms name=general
http POST http://localhost:8000/rooms name=sports
http POST http://localhost:8000/rooms name=bde
```

## Utiliser l'interface

1. Ouvrir **http://localhost:8000** dans le navigateur
2. Choisir son nom d'utilisateur dans la liste
3. Sur la page des salons : s'abonner / se désabonner librement
4. Cliquer **Entrer** pour rejoindre un salon et échanger des messages en temps réel

## Référence API

| Méthode | URL | Description |
|---------|-----|-------------|
| `GET` | `/users` | Lister tous les utilisateurs |
| `POST` | `/users` | Créer un utilisateur `{"name": "..."}` |
| `GET` | `/rooms` | Lister tous les salons |
| `POST` | `/rooms` | Créer un salon `{"name": "..."}` |
| `POST` | `/rooms/{id}/subscribe?user_id=X` | S'abonner à un salon |
| `DELETE` | `/rooms/{id}/subscribe?user_id=X` | Se désabonner d'un salon |
| `GET` | `/rooms/{id}/messages` | Historique des messages d'un salon |
| `WS` | `/ws/{room_id}/{user_id}` | Connexion WebSocket temps réel |

La documentation interactive Swagger est disponible sur **http://localhost:8000/docs**.
