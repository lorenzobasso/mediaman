from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from mediaman_api.routes import channel as channel_router
from mediaman_api.database import create_db_and_tables

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(channel_router.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
