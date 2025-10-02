from bson import ObjectId

def todo_helper(todo) -> dict:
    return {
        "id": str(todo["_id"]),   # convert ObjectId to string
        "title": todo["title"],
        "description": todo.get("description"),
        "completed": todo.get("completed", False),
        "owner": todo["owner"]
    }
