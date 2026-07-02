from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Format: mysql+pymysql://<username>:<password>@<host>:<port>/<database_name>
# Update 'root' and 'your_password' with your actual MySQL credentials
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Root%40123@localhost:3306/expense_tracker"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()