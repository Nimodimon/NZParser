from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from connection import scrap_week

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/user-data")
def read_item(username: str, password: str, start_date: str):
    return scrap_week(username=username, password=password, start_date=start_date)
