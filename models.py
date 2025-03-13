from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import List, Optional
from pydantic import BaseModel

# Modelo Pydantic para validação
class Team(BaseModel):
    id: int
    name: str
    city: str
    championships: int
    founded: int
    market_value: float
    conference_titles: int
    conference: str