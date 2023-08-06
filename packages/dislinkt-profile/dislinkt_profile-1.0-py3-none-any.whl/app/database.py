from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import app.models as models

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker()
local_session = Session(bind=engine)

models.Base.metadata.create_all(bind=engine)