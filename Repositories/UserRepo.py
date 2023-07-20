import uuid
from db.db_connect import db
from model.user import User


class UserRepo():

    @staticmethod
    async def get_all():
        _items = db.get_collection('user').find()
        _list_items = []
        async for user in _items:
            _list_items.append(user)
        return _list_items

    @staticmethod
    async def auth(email: str, password: str) -> dict:
        user = await db.get_collection('user').find_one({"email": email, "password": password})
        if user:
            user['id'] = user['_id']
            user.pop('_id')
            user.pop('password')
        return user

    @staticmethod
    async def insert(user: User):
        id = str(uuid.uuid4())
        user.id = id
        _user = user.dict(exclude={})
        _user['_id'] = id
        _user.pop('id')
        await db.get_collection('user').insert_one(_user)
        # _user.pop('password')
        return user.dict(exclude={'password'})

    @staticmethod
    async def delete_one(id: str):
        return await db.get_collection('user').delete_one({'_id': id})