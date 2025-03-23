from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from database import todo_collection
from schemas.todo import TodoCreate, TodoUpdate
from serializers import todo as serializer

class TodoCrud:
    @staticmethod
    def create_todo(todo_data: TodoCreate):
        todo_data = jsonable_encoder(todo_data)
        todo_document_data = todo_collection.insert_one(todo_data)
        todo_id = todo_document_data.inserted_id
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        return serializer.todo_serializer(todo)

    @staticmethod
    def get_todo(todo_id: str):
        todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if todo:
            return serializer.todo_serializer(todo)
        return None

    @staticmethod
    def get_todos(user_id: str):
        todos = todo_collection.find({"user_id": user_id})
        return serializer.todos_serializer(todos)

    @staticmethod
    def update_todo(todo_id: str, todo_data: TodoUpdate):
        todo_data = {k: v for k, v in todo_data.dict().items() if v is not None}
        if len(todo_data) >= 1:
            update_result = todo_collection.update_one(
                {"_id": ObjectId(todo_id)}, {"$set": todo_data}
            )
            if update_result.modified_count == 1:
                updated_todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
                if updated_todo:
                    return serializer.todo_serializer(updated_todo)
        existing_todo = todo_collection.find_one({"_id": ObjectId(todo_id)})
        if existing_todo:
            return serializer.todo_serializer(existing_todo)
        return None

    @staticmethod
    def delete_todo(todo_id: str):
        delete_result = todo_collection.delete_one({"_id": ObjectId(todo_id)})
        return delete_result.deleted_count == 1

todo_crud = TodoCrud()