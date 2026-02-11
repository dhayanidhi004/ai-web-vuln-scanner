import os
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ================= DATABASE CONFIG =================
# We use os.path to ensure scanner.db is created in the backend folder
# even when running the app from different terminal locations.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "scanner.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Essential for SQLite + Flask
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ================= USER TABLE =================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)  # Note: Plain text for now, hash in production

    def __repr__(self):
        return f"<User username={self.username}>"

# ================= SCAN HISTORY TABLE =================
class ScanHistory(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, index=True, nullable=False)
    
    # Severity: Critical / High / Medium / Low
    severity = Column(String, nullable=False)
    
    # Optional future use for specific vulnerability names
    vulnerability = Column(String, nullable=True)

    scanned_at = Column(
        DateTime,
        default=datetime.datetime.utcnow
    )

    def __repr__(self):
        return f"<ScanHistory url={self.url} severity={self.severity} at={self.scanned_at}>"

# ================= CREATE ALL TABLES =================
def init_db():
    # This creates the scanner.db file and tables if they don't exist
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at: {DATABASE_PATH}")