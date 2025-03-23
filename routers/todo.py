from fastapi import APIRouter, HTTPException
from crud.todo import todo_crud
from schemas import todo as todo_schema

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.post("/", response_model=todo_schema.Todo)
def create_todo_endpoint(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)

@router.get("/{todo_id}", response_model=todo_schema.Todo)
def get_todo_endpoint(todo_id: str):
    todo = todo_crud.get_todo(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@router.get("/user/{user_id}", response_model=list[todo_schema.Todo])
def get_user_todos_endpoint(user_id: str):
    return todo_crud.get_todos(user_id)

@router.put("/{todo_id}", response_model=todo_schema.Todo)
def update_todo_endpoint(todo_id: str, todo: todo_schema.TodoUpdate):
    updated_todo = todo_crud.update_todo(todo_id, todo)
    if not updated_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated_todo

@router.delete("/{todo_id}")
def delete_todo_endpoint(todo_id: str):
    deleted = todo_crud.delete_todo(todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo deleted successfully"}