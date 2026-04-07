from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

#1 On dit à SQLAlchemy de créer un fichier "whatsapp.db"
SQLALCHEMY_DATABASE_URL = "sqlite:///./whatsapp.db"

#2 Le "moteur" qui fait le lien entre Python et le fichier SQLite
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#3 Le générateur de "sessions" (les sessions permettent de parler à la base)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#4 La classe de base pour créer nos tables
Base = declarative_base()

#5 On définit le "moule" de notre table de messages
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    room = Column(String, index=True)      # Le salon de discussion
    username = Column(String)              # L'expéditeur
    content = Column(String)               # Le texte du message

#6 On ordonne la création de la table dans le fichier
Base.metadata.create_all(bind=engine)

#7 Petite fonction utilitaire pour fournir une session à FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()