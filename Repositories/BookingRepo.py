import uuid
from db.db_connect import db
from model.booking import Booking
from datetime import timedelta, datetime


class BookingRepo():

    @staticmethod
    async def get_all():
        _items = db.get_collection('booking').find()
        _list_items = []
        async for booking in _items:
            _list_items.append(booking)
        return _list_items

    @staticmethod
    async def insert(booking: Booking):
        id = str(uuid.uuid4())
        booking.id = id
        _booking = booking.dict(exclude={})
        _items = db.get_collection('booking').find()
        async for book in _items:
            if book['table_id'] == _booking['table_id']:
                if book['booking_start_time'].replace(tzinfo=None) - timedelta(hours=2) <= \
                        _booking['booking_start_time'].replace(tzinfo=None) <= \
                        book['booking_start_time'].replace(tzinfo=None) + timedelta(hours=2):
                    raise ValueError("The table is already booked")
        _booking['_id'] = id
        _booking.pop('id')
        await db.get_collection('booking').insert_one(_booking)

    @staticmethod
    async def delete_one(id: str):
        return await db.get_collection('booking').delete_one({'_id': id})

    @staticmethod
    async def find_booking_user(id) -> Booking | None:
        _items = db.get_collection('booking').find({"user_id": id})
        _list_items = []
        async for book in _items:
            _list_items.append(book)
        return _list_items

    @staticmethod
    async def cancel_booking(id: str):
        _items = db.get_collection('booking').find()
        async for book in _items:
            duration = book['booking_start_time'].replace(tzinfo=None) - datetime.now()
            duration_in_min = duration.total_seconds() / 60
            if duration_in_min <= 60:
                raise ValueError("Can't cancel booking")
        return await db.get_collection('booking').delete_one({'_id': id})

    @staticmethod
    async def update(booking: Booking):
        _booking = await db.get_collection('booking').find_one({"_id": booking.id})
        _booking['table_id'] = booking.table_id
        _booking['user_id'] = booking.user_id
        _booking['booking_start_time'] = booking.booking_start_time
        await db.get_collection("booking").update_one({"_id": booking.id}, {"$set": _booking})
