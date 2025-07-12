"""database configuration and connection handling"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./movies.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

""" if __name__ == "__main__":
    # This block is for testing the database connection
    try:
        with SessionLocal() as session:
            print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}") """