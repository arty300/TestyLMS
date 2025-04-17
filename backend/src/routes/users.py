from fastapi import APIRouter, Depends, HTTPException, Header
from pymongo import MongoClient
from src.database import db
from src.models.user import User, UserCreate, UserUpdate, Group
from src.utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

async def get_db():
    return db

async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.users.find_one({"username": payload["sub"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {**user, "id": str(user["_id"])}

@router.post("/login")
async def login(request: LoginRequest, db=Depends(get_db)):
    db_user = db.users.find_one({"username": request.username})
    if not db_user or not verify_password(request.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def get_current_user_data(current_user=Depends(get_current_user)):
    return current_user

@router.post("", response_model=User)
async def create_user(user: UserCreate, db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create users")
    db_user = db.users.find_one({"username": user.username})
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    new_user = {
        "username": user.username,
        "password": hashed_password,
        "points": 0,
        "role": user.role,
        "groups": user.groups
    }
    result = db.users.insert_one(new_user)
    return {**new_user, "id": str(result.inserted_id), "password": None}

@router.get("", response_model=list[User])
async def get_users(db=Depends(get_db), current_user=Depends(get_current_user), group: str = None):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view users")
    query = {"groups": group} if group else {}
    users = list(db.users.find(query))
    return [{**user, "id": str(user["_id"]), "password": None} for user in users]

@router.delete("/{user_id}")
async def delete_user(user_id: str, db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users")
    try:
        result = db.users.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid user ID")

@router.put("/by-username/{username}")
async def update_user_by_username(
    username: str,
    user: UserUpdate,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update users")
    db_user = db.users.find_one({"username": username})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.users.update_one(
        {"username": username},
        {"$set": {"groups": user.groups}}
    )
    return {"message": "User updated successfully"}

@router.post("/groups")
async def create_group(group: Group, db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can create groups")
    db_group = db.groups.find_one({"name": group.name})
    if db_group:
        raise HTTPException(status_code=400, detail="Group already exists")
    result = db.groups.insert_one(group.dict())
    return {**group.dict(), "id": str(result.inserted_id)}

@router.get("/groups", response_model=list[Group])
async def get_groups(db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can view groups")
    groups = list(db.groups.find())
    return [{**group, "id": str(group["_id"])} for group in groups]

@router.put("/groups/{group_id}")
async def update_group(group_id: str, group: Group, db=Depends(get_db), current_user=Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can update groups")
    try:
        result = db.groups.update_one(
            {"_id": ObjectId(group_id)},
            {"$set": group.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Group not found")
        return {**group.dict(), "id": group_id}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid group ID")