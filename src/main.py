from src.database import db_init
from src.router import router
from fastapi import FastAPI
import time


db_init()

app = FastAPI()
app.include_router(router=router)
