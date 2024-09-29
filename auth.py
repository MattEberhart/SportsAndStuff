from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session, declarative_base
from .database import get_db
from .models import User, League  # Assuming you have User and League models
from typing import Optional
from sqlalchemy import Integer, String, Boolean, Column

# These would typically be stored in a secure configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

async def check_if_admin(current_user: User = Depends(get_current_user)) -> bool:
    return current_user.is_admin

async def check_if_league_admin(league_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> bool:
    league = db.query(League).filter(League.id == league_id).first()
    if not league:
        raise HTTPException(status_code=404, detail="League not found")
    
    # This assumes you have a many-to-many relationship between User and League
    # with an additional 'is_admin' field in the association table
    admin_association = db.query(LeagueAdmin).filter(
        LeagueAdmin.user_id == current_user.id,
        LeagueAdmin.league_id == league.id,
        LeagueAdmin.is_admin == True
    ).first()

    return admin_association is not None

# You might want to add this to your models.py
from sqlalchemy import Table, Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

Base = declarative_base()

LeagueAdmin = Table('league_admins', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('league_id', Integer, ForeignKey('leagues.id')),
    Column('is_admin', Boolean, default=False)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    is_admin = Column(Boolean, default=False)
    # other fields...
    leagues = relationship("League", secondary=LeagueAdmin, back_populates="users")

class League(Base):
    __tablename__ = 'leagues'
    id = Column(Integer, primary_key=True, index=True)
    # other fields...
    users = relationship("User", secondary=LeagueAdmin, back_populates="leagues")