from bson import ObjectId

def user_serializer(user) -> dict:
    return {
        "id": str(user["_id"]),
        "email": user["email"],
        "username": user["username"],
        "created_at": user["created_at"].isoformat() if "created_at" in user and user["created_at"] else None
    }

def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]
