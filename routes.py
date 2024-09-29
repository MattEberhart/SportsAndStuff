from fastapi import APIRouter, HTTPException, Depends
from .database import get_db, DatabaseSession
from typing import List
from .models import League, Season, Player, Lineup, Contest
from .schemas import LeagueSchema, SeasonSchema, PlayerSchema, LineupSchema, ContestSchema
from .auth import check_if_admin

router = APIRouter()

# Add and update league
@router.put("/leagues/{league_id}", response_model=LeagueSchema)
async def add_update_league(league_id: int, league: LeagueSchema, db: DatabaseSession = Depends(get_db), is_admin: bool = Depends(check_if_admin)):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Operation not allowed")
    
    db_league = db.query(League).filter(League.id == league_id).first()
    if db_league:
        for key, value in league.dict().items():
            setattr(db_league, key, value)
    else:
        db_league = League(**league.dict(), id=league_id)
        db.add(db_league)
    
    db.commit()
    db.refresh(db_league)
    return db_league

# Add and update season
@router.put("/leagues/{league_id}/seasons/{season_id}", response_model=SeasonSchema)
async def add_update_season(league_id: int, season_id: int, season: SeasonSchema, db: Session = Depends(get_db), is_admin: bool = Depends(check_if_admin)):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Operation not allowed")
    
    db_season = db.query(Season).filter(Season.id == season_id, Season.league_id == league_id).first()
    if db_season:
        for key, value in season.dict().items():
            setattr(db_season, key, value)
    else:
        db_season = Season(**season.dict(), id=season_id, league_id=league_id)
        db.add(db_season)
    
    db.commit()
    db.refresh(db_season)
    return db_season

# Post a contest and its lineups
@router.post("/leagues/{league_id}/seasons/{season_id}/contests", response_model=ContestSchema)
async def add_contest(league_id: int, season_id: int, contest: ContestSchema, db: Session = Depends(get_db), is_admin: bool = Depends(check_if_admin)):
    if not is_admin:
        raise HTTPException(status_code=403, detail="Operation not allowed")
    
    db_contest = Contest(**contest.dict(), season_id=season_id)
    db.add(db_contest)
    db.commit()
    db.refresh(db_contest)
    return db_contest

# Get leagues by player
@router.get("/player/{player_id}/leagues", response_model=List[LeagueSchema])
async def get_leagues_by_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    
    leagues = db.query(League).join(Season).join(Contest).join(Lineup).filter(Lineup.player_id == player_id).distinct().all()
    return leagues

# Get seasons by league
@router.get("/league/{league_id}/seasons", response_model=List[SeasonSchema])
async def get_seasons_by_league(league_id: int, db: Session = Depends(get_db)):
    seasons = db.query(Season).filter(Season.league_id == league_id).all()
    if not seasons:
        raise HTTPException(status_code=404, detail="No seasons found for this league")
    return seasons

# Get season dashboard
@router.get("/league/{league_id}/seasons/{season_id}/dashboard", response_model=SeasonSchema)
async def get_season_dashboard(league_id: int, season_id: int, db: Session = Depends(get_db)):
    season = db.query(Season).filter(Season.id == season_id, Season.league_id == league_id).first()
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    
    # Here you can add additional logic to fetch and include more details for the dashboard
    # For example, you might want to include contests, top players, etc.
    
    return season