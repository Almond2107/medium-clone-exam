from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users, article  
from app.admin.settings import admin
from app.middleware import ProcessTimeLoggerMiddleware, origins
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


# --- App instance ---
app = FastAPI(title="Medium Clone", version="1.0.0")


# Static fayllar uchun
app.mount("/static", StaticFiles(directory="static"), name="static")

# Template fayllar uchun
templates = Jinja2Templates(directory="templates")



# --- Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(article.router)


# --- Root endpoint ---
@app.get("/")
def welcome():
    return {"message": "Welcome to Medium Clone API "}



admin.mount_to(app=app)
