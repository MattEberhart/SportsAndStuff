from pydantic import BaseModel
from typing import List, Optional


class LeagueBase(BaseModel):
    name: str
    admin_id: str


class LeagueCreate(LeagueBase):
    pass


class LeagueSchema(LeagueBase):
    id: int

    class Config:
        orm_mode = True


class SeasonBase(BaseModel):
    league_id: int
    year: int
    point_scale: str


class SeasonCreate(SeasonBase):
    pass


class SeasonSchema(SeasonBase):
    id: int

    class Config:
        orm_mode = True


class PlayerBase(BaseModel):
    user_name: str
    league_ids: List[int]


class PlayerCreate(PlayerBase):
    pass


class PlayerSchema(PlayerBase):
    id: int

    class Config:
        orm_mode = True


class LineupBase(BaseModel):
    player_id: int
    contest_id: int
    fantasy_points: float


class LineupCreate(LineupBase):
    pass


class LineupSchema(LineupBase):
    id: int

    class Config:
        orm_mode = True


class ContestBase(BaseModel):
    league_id: int
    season_id: int
    start_date: str
    point_scale: Optional[List[int]] = []


class ContestCreate(ContestBase):
    pass


class ContestSchema(ContestBase):
    id: int

    class Config:
        orm_mode = True