from fastapi import APIRouter, HTTPException, Depends
from typing import List
from .models import League, Season, Player, Lineup, Contest
from .schemas import LeagueSchema, SeasonSchema, PlayerSchema, LineupSchema, ContestSchema

router = APIRouter()

# Add and update league
@router.put("/leagues/{league_id}", response_model=LeagueSchema)
async def add_update_league(league_id: int, league: LeagueSchema, is_admin: bool = Depends(check_if_admin)):
    # code to update or add league using `league_id` and `league`
    # is_admin is function based dependency to check if requester is admin
    # raise HTTPException(status_code=403, detail="Operation not allowed") if requester is not admin
    pass

# Add and update season
@router.put("/leagues/{league_id}/seasons/{season_id}", response_model=SeasonSchema)
async def add_update_season(league_id: int, season_id: int, season: SeasonSchema, is_admin: bool = Depends(check_if_admin)):
    # code to update or add season in a league using `league_id` and `season_id` and `season`
    pass

# Post a contest and its lineups
@router.post("/leagues/{league_id}/seasons/{season_id}/contests", response_model=ContestSchema)
async def add_contest(league_id: int, season_id: int, contest: ContestSchema, is_admin: bool = Depends(check_if_admin)):
    # code to add contest using `league_id` `season_id` and `contest`
    pass

# Get leagues by player
@router.get("/player/{player_id}/leagues", response_model=List[LeagueSchema])
async def get_leagues_by_player(player_id: int):
    # code to get leagues of a player
    pass

# Get seasons by league
@router.get("/league/{league_id}/seasons", response_model=List[SeasonSchema])
async def get_seasons_by_league(league_id: int):
    # code to get seasons of a league
    pass

# Get season dashboard
@router.get("/league/{league_id}/seasons/{season_id}/dashboard", response_model=SeasonSchema)
async def get_season_dashboard(league_id: int, season_id: int):
    # code to get season details for dashboard
    pass