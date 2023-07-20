from fastapi import APIRouter, Depends
from Repositories.TableRepo import TableRepo
from model.table import Table
from auth.jwt_bearer import JWTBearer

router = APIRouter(prefix="/table", tags=['/table'])


@router.get("/")
async def get_all(token: str = Depends(JWTBearer())):
    return await TableRepo.get_all()


@router.post("/add_tabel", status_code=201)
async def add_tabel(table: Table, token: str = Depends(JWTBearer())):
    _table = await TableRepo.insert(table)
    return _table
