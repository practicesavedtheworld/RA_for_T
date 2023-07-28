from fastapi import FastAPI
from app.backend.targets.router import router as targets_router
from app.backend.users.router import router as users_router

app = FastAPI(title="RA")

app.include_router(targets_router)
app.include_router(users_router)
