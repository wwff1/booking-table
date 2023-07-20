import uuid
from db.db_connect import db
from model.table import Table


class TableRepo():

    @staticmethod
    async def get_all():
        _items = db.get_collection('table').find()
        _list_items = []
        async for book in _items:
            _list_items.append(book)
        return _list_items

    @staticmethod
    async def insert(table: Table):
        id = str(uuid.uuid4())
        table.id = id
        _table = table.dict(exclude={})
        _table['_id'] = id
        _table.pop('id')
        await db.get_collection('table').insert_one(_table)
