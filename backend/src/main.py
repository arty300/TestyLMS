from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import users, courses

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Для фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users")
app.include_router(courses.router, prefix="/courses")
app.include_router(courses.images_router)

