from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from database import user_collection
from schemas.user import UserCreate, UserUpdate
from serializers import user as serializer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCrud:
    @staticmethod
    def create_user(user_data: UserCreate):
        user_data = jsonable_encoder(user_data)
        user_data["password"] = pwd_context.hash(user_data["password"])
        user_document_data = user_collection.insert_one(user_data)
        user_id = user_document_data.inserted_id
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        return serializer.user_serializer(user)

    @staticmethod
    def get_user(user_id: str):
        user = user_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return serializer.user_serializer(user)
        return None

    @staticmethod
    def get_user_by_email(email: str):
        user = user_collection.find_one({"email": email})
        if user:
            return serializer.user_serializer(user)
        return None

    @staticmethod
    def update_user(user_id: str, user_data: UserUpdate):
        user_data = {k: v for k, v in user_data.dict().items() if v is not None}
        if "password" in user_data:
            user_data["password"] = pwd_context.hash(user_data["password"])
        if len(user_data) >= 1:
            update_result = user_collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_data}
            )
            if update_result.modified_count == 1:
                updated_user = user_collection.find_one({"_id": ObjectId(user_id)})
                if updated_user:
                    return serializer.user_serializer(updated_user)
        existing_user = user_collection.find_one({"_id": ObjectId(user_id)})
        if existing_user:
            return serializer.user_serializer(existing_user)
        return None

    @staticmethod
    def delete_user(user_id: str):
        delete_result = user_collection.delete_one({"_id": ObjectId(user_id)})
        return delete_result.deleted_count == 1

user_crud = UserCrud()



