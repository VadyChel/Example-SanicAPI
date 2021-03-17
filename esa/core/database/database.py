import uuid
import aiosqlite
import hashlib
from esa.core.exceptions import *


class Database:
    async def prepare(self) -> None:
        database = await aiosqlite.connect("esa/database/database.db")
        cursor = await database.execute("""CREATE TABLE IF NOT EXISTS users (
			id TEXT,
			password TEXT,
			username TEXT,
			email TEXT
		)""")
        await database.commit()
        await cursor.close()

    async def get_users(self) -> list:
        database = await aiosqlite.connect("esa/database/database.db")
        cursor = await database.execute("""SELECT * FROM users""")
        data = await cursor.fetchall()
        await cursor.close()
        await database.close()

        return [{
            "id": user[0],
            "username": user[2],
            "email": user[3]
        } for user in data]

    async def get_user(self, user_id: str) -> dict:
        database = await aiosqlite.connect("esa/database/database.db")
        cursor = await database.execute(f"""SELECT * FROM users WHERE id = '{user_id}' """)
        data = await cursor.fetchone()

        if data is None:
            raise UserNotFound

        await cursor.close()
        await database.close()

        return {
            "id": data[0],
            "password": data[1],
            "username": data[2],
            "email": data[3]
        }

    async def create_user(
            self,
            password: str,
            username: str,
            email: str
    ) -> bool:
        if email in [user["email"] for user in await self.get_users()]:
            raise UserAlreadyExists

        database = await aiosqlite.connect("esa/database/database.db")
        pass_hash = hashlib.md5(password.encode()).hexdigest()
        await database.execute(f"""INSERT INTO users (id, password, username, email) VALUES (
			'{str(uuid.uuid4())}',
			'{pass_hash}',
			'{username}',
			'{email}'
		)""")
        await database.commit()
        await database.close()
        return True

    async def delete_user(
            self,
            user_id: str,
            password: str
    ) -> bool:
        pass_hash = hashlib.md5(password.encode()).hexdigest()

        database = await aiosqlite.connect("esa/database/database.db")
        cursor = await database.execute(f"""SELECT password FROM users WHERE id = '{user_id}' """)
        data = await cursor.fetchone()
        await cursor.close()

        if data is None:
            raise UserNotFound

        if pass_hash != data[0]:
            raise InvalidPassword

        await database.execute(f"""DELETE FROM users WHERE id = '{user_id}' """)
        await database.commit()
        await database.close()

        return True

    async def edit_user(
            self,
            user_id: str,
            params: dict
    ) -> bool:
        pass_hash = hashlib.md5(params.get("password").encode()).hexdigest()

        database = await aiosqlite.connect("esa/database/database.db")
        cursor = await database.execute(f"""SELECT password FROM users WHERE id = '{user_id}'""")
        data = await cursor.fetchone()

        if data is None:
            raise UserNotFound

        await cursor.close()

        if pass_hash != data[0]:
            raise InvalidPassword

        for key, value in params.items():
            if key == "username":
                await database.execute(
                    f"""UPDATE users SET username = "{params.get("username")}" WHERE id = '{user_id}'""")
            elif key == "email":
                await database.execute(
                    f"""UPDATE users SET email = '{params.get("email")}' WHERE id = '{user_id}'""")

        await database.commit()
        await database.close()

        return True
