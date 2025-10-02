# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from routes.todos import router as todo_router


app = FastAPI(
    title="To-Do App Backend",
    description="FastAPI backend for To-Do app with MongoDB",
    version="1.0.0"
)

# Allow frontend (React) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tasks-todo-18.netlify.app/",
        "http://localhost:5173",
    ],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include users routes
app.include_router(user_router)
app.include_router(todo_router)
# Root endpoint
@app.get("/")
def root():
    return {"message": "Backend is up and running!"}
