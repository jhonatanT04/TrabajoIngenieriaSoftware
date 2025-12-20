from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from routers import auth
from db.database import init_db
import schemas, deps

app = FastAPI(title="Minimercado - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/", tags=["salud"])
def root():
    return {"status": "ok", "message": "Backend Minimercado funcionando"}


app.include_router(auth.router)  # Rutas de autenticación


@app.get("/users/me", response_model=schemas.UserRead, tags=["users"])
def read_current_user(current_user=Depends(deps.get_current_user)):
    return current_user
