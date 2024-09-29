from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

# MySQL database URL
# Format: mysql://username:password@host:port/database_name
DATABASE_URL = "mysql://user:password@localhost:3306/your_database_name"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a Base class for declarative models
Base = declarative_base()

class DatabaseSession:
    def __init__(self):
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    def commit(self):
        self.session.commit()

    def refresh(self, instance):
        self.session.refresh(instance)

    def query(self, *entities, **kwargs):
        return self.session.query(*entities, **kwargs)

    def add(self, instance):
        self.session.add(instance)

    def close(self):
        self.session.close()

# Dependency to get the database session
def get_db():
    db = DatabaseSession()
    try:
        yield db
    finally:
        db.close()

# Context manager for database operations
@contextmanager
def db_session():
    db = DatabaseSession()
    try:
        yield db
        db.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.close()

# Function to initialize the database (create tables)
def init_db():
    Base.metadata.create_all(bind=engine)