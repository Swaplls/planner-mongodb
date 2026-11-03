from fastapi import APIRouter, HTTPException
from database.connection import Database
from models.users import User, UserSignIn

user_router = APIRouter(tags=["User"])
user_database = Database(User)

@user_router.post("/signup")
async def sign_user_up(user: User) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if user_exist:
        raise HTTPException(status_code=409, detail="User exists already.")
    await user_database.save(user)
    return {"message": "User created successfully"}

@user_router.post("/signin")
async def sign_user_in(user: UserSignIn) -> dict:
    user_exist = await User.find_one(User.email == user.email)
    if not user_exist:
        raise HTTPException(status_code=404, detail="User does not exist.")
    if user_exist.password == user.password:
        return {"message": "User signed in successfully."}
    raise HTTPException(status_code=401, detail="Invalid details passed.")