from  dotenv import load_dotenv
import os
load_dotenv()
from sqlmodel import create_engine ,Session

DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_NAME=os.getenv("DB_NAME")

DATABASE_URL=f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine=create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
