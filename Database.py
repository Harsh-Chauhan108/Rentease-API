from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
DB_URL ="sql+pymysql://root:9713@localhost:3306/rentease"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
