# app/routes/todos.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List
from config import db
from utils.auth import get_current_user
from helpers import todo_helper
from bson import ObjectId

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

# MongoDB collection
todos_collection = db["todos"]

# Pydantic models
class TodoCreate(BaseModel):
    title: str
    description: str = None
    completed: bool = False

class TodoResponse(BaseModel):
    id: str
    title: str
    description: str = None
    completed: bool

# Create a new todo
@router.post("/", response_model=TodoResponse)
async def create_todo(todo: TodoCreate, current_user: dict = Depends(get_current_user)):
    todo_dict = todo.dict()
    todo_dict["owner"] = current_user["email"]
    result = await todos_collection.insert_one(todo_dict)
    new_todo = await todos_collection.find_one({"_id": result.inserted_id})
    return todo_helper(new_todo)   # ✅ safe JSON response


# Get all todos for the logged-in user
@router.get("/", response_model=list[TodoResponse])
async def get_todos(current_user: dict = Depends(get_current_user)):
    todos = []
    async for todo in todos_collection.find({"owner": current_user["email"]}):
        todos.append(todo_helper(todo))
    return todos

# Update a todo by id
@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(todo_id: str, todo: TodoCreate, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in todo.dict().items() if v is not None}

    updated = await todos_collection.find_one_and_update(
        {"_id": ObjectId(todo_id), "owner": current_user["email"]},
        {"$set": update_data},
        return_document=True
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")

    return todo_helper(updated)

# Delete a todo by id
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str, current_user: dict = Depends(get_current_user)):
    # Ensure todo_id is a valid ObjectId
    try:
        obj_id = ObjectId(todo_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid todo ID format")

    result = await todos_collection.delete_one({"_id": obj_id, "owner": current_user["email"]})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Todo not found")

    return {"message": "Todo deleted successfully"}