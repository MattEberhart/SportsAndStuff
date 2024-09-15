from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Table
from CommaSeparatedInteger import CommaSeparatedInteger
from database import Base


class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    admin_ids = Column(String)  # Assuming admin_ids are stored as comma-separated strings


class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    year = Column(Integer)
    point_scale = Column(
        CommaSeparatedInteger)  # If your SQL version does not support this, you might have to use String and handle conversion to list in your application logic
    contest_ids = Column(String)  # Assuming contest_ids would be stored as comma-separated strings


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(100))
    league_ids = Column(String)  # Assuming league_ids would be stored as comma-separated strings


class Lineup(Base):
    __tablename__ = "lineups"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    contest_id = Column(Integer, ForeignKey("contests.id"))
    fantasy_points = Column(Float)


class Contest(Base):
    __tablename__ = "contests"

    id = Column(Integer, primary_key=True, index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"))
    season_id = Column(Integer, ForeignKey("seasons.id"))
    start_date = Column(Date)
    point_scale = Column(
        CommaSeparatedInteger)  # If your SQL version does not support this, you might have to use String and handle conversion to list in your application logic