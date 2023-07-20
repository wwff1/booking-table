from fastapi import APIRouter, HTTPException, Depends
from Repositories.BookingRepo import BookingRepo
from model.booking import Booking
from auth.jwt_bearer import JWTBearer


router = APIRouter(prefix="/booking", tags=['/booking'])


@router.get("/")
async def get_all(token: str = Depends(JWTBearer())):
    return await BookingRepo.get_all()


@router.post("/add_booking", status_code=201)
async def add_booking(booking: Booking, token: str = Depends(JWTBearer())):
    try:
        _booking = await BookingRepo.insert(booking)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))
    return _booking


@router.delete("/delete", status_code=200)
async def delete_booking(id: str, token: str = Depends(JWTBearer())):
    await BookingRepo.delete_one(id)


@router.get("/find_booking_user", status_code=200)
async def find_booking_user(id: str, token: str = Depends(JWTBearer())):
    user = await BookingRepo.find_booking_user(id)
    return user


@router.delete("/cancel_booking", status_code=200)
async def cancel_booking(id: str, token: str = Depends(JWTBearer())):
    try:
        await BookingRepo.cancel_booking(id)
    except ValueError as ex:
        raise HTTPException(status_code=400, detail=str(ex))


@router.patch("/update_booking", status_code=201)
async def update_booking(booking: Booking, token: str = Depends(JWTBearer())):
    _booking = await BookingRepo.update(booking)
    return _booking
