from fastapi import APIRouter, HTTPException
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_schema.User)
def create_user_endpoint(user: user_schema.UserCreate):
    db_user = user_crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(user)

@router.get("/{user_id}", response_model=user_schema.User)
def get_user_endpoint(user_id: str):
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=user_schema.User)
def update_user_endpoint(user_id: str, user: user_schema.UserUpdate):
    updated_user = user_crud.update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/{user_id}")
def delete_user_endpoint(user_id: str):
    deleted = user_crud.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}