from fastapi import APIRouter, HTTPException, Depends
from Repositories.UserRepo import UserRepo
from model.user import User
from auth.jwt_handler import signJWT
from auth.jwt_bearer import JWTBearer


router = APIRouter(prefix="/user", tags=['/user'])


@router.get("/")
async def get_all(token: str = Depends(JWTBearer())):
    return await UserRepo.get_all()


@router.get("/login")
async def login(email: str, password: str):
    _user = await UserRepo.auth(email, password)
    if _user is None:
        raise HTTPException(status_code=403, detail="Неправильный логин или пароль")
    _user['token'] = signJWT(_user['id']).get("access_token")
    return _user


@router.post("/registration", status_code=201)
async def registration(user: User):
    _user = await UserRepo.insert(user)
    _user['token'] = signJWT(_user['id']).get("access_token")
    return _user


@router.delete("/delete", status_code=200)
async def delete_user(id: str, token: str = Depends(JWTBearer())):
    await UserRepo.delete_one(id)