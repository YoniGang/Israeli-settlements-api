import requests
from sqlalchemy import delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError


class InitManager:
    def __init__(self, db, table_to_change, data_manipulation_function):
        self._db = db
        self._table_to_change = table_to_change
        self._data_manipulation_function = data_manipulation_function

    async def delete_all_data(self):
        delete_stmt = delete(self._table_to_change)

        await self._db.execute(statement=delete_stmt)
        await self._db.commit()

    async def get_data(self, url, extra_data_for_manipulation_function=None):
        try:
            res = requests.get(url)
            json_res = res.json()
            records = json_res["result"]["records"]
            data_to_add = []
            for record in records:
                self._data_manipulation_function(record, data_to_add, extra_data_for_manipulation_function)
            insert_stmt = insert(self._table_to_change).values(data_to_add)

            await self._db.execute(statement=insert_stmt)
            await self._db.commit()
        except IntegrityError:
            print(f"integrity error in {self._table_to_change.__tablename__} table")
            raise IntegrityError
        except Exception as e:
            print(repr(e))
