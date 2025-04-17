import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, decl_api
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch the database URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Set up SQLAlchemy database engine
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal will allow us to manage sessions for DB interaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base: decl_api.DeclarativeMeta = declarative_base()


# Function to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# if __name__ == "__main__":
#     # test db connection
#     conn = get_db()
#     print(type(Base))
#     print(conn, type(conn))
