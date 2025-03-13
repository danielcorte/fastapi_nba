from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import List, Optional
from pydantic import BaseModel

from models import Team
from database import TeamDB, get_db

app = FastAPI(description="")

# Habilitando CORS para acesso aberto
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Rota para adicionar um time
@app.post("/teams", response_model=Team)
def create_team(team: Team, db: Session = Depends(get_db)):
    db_team = TeamDB(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

# Rota para listar todos os times com filtros avançados
@app.get("/teams", response_model=List[Team])
def get_teams(
    min_championships: Optional[int] = None,
    min_conference_titles: Optional[int] = None,
    min_market_value: Optional[float] = None,
    conference: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(TeamDB)

    if min_championships is not None:
        query = query.filter(TeamDB.championships >= min_championships)
    if min_conference_titles is not None:
        query = query.filter(TeamDB.conference_titles >= min_conference_titles)
    if min_market_value is not None:
        query = query.filter(TeamDB.market_value >= min_market_value)
    if conference:
        query = query.filter(TeamDB.conference == conference)

    return query.all()

# Rota para obter um time específico pelo ID
@app.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")
    return team

# Rota para atualizar um time completamente (Put)
@app.put("/teams/{team_id}", response_model=Team)
def update_team(team_id: int, updated_team: Team, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")

    for key, value in updated_team.dict().items():
        setattr(team, key, value)

    db.commit()
    db.refresh(team)
    return team

# Rota para atualização parcial (PATCH)
@app.patch("/teams/{team_id}", response_model=Team)
def partial_update_team(
    team_id: int,
    championships: Optional[int] = None,
    market_value: Optional[float] = None,
    db: Session = Depends(get_db)
):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")

    if championships is not None:
        team.championships = championships
    if market_value is not None:
        team.market_value = market_value

    db.commit()
    db.refresh(team)
    return team

# Rota para deletar um time
@app.delete("/teams/{team_id}")
def delete_team(team_id: int, db: Session = Depends(get_db)):
    team = db.query(TeamDB).filter(TeamDB.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Time não encontrado")

    db.delete(team)
    db.commit()
    return {"message": "Time removido com sucesso"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1",  # host="10.234.91.223"
                port=8080, log_level="info", 
                reload=True)