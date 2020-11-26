import typing
import aiosqlite
import hashlib

class Database:
	async def prepare_to_start(self) -> None:
		database = await aiosqlite.connect("core/database.db")
		cursor = await database.execute("""CREATE TABLE IF NOT EXISTS users (
			user_id TEXT,
			pass_hash TEXT,
			name TEXT,
			e_mail TEXT
		)""")
		await database.commit()
		await cursor.close()

	async def get_users(self) -> list:
		database = await aiosqlite.connect("core/database.db")
		cursor = await database.execute("""SELECT * FROM users""")
		data = await cursor.fetchall()
		await cursor.close()
		await database.close()

		return [{
			"id": user[0],
			"name": user[2],
			"email": user[3]
		} for user in data]

	async def get_user(self, user_id:str) -> typing.Union[dict, int]:
		database = await aiosqlite.connect("core/database.db")
		cursor = await database.execute(f"""SELECT * FROM users WHERE user_id = "{user_id}" """)
		data = await cursor.fetchone()

		if data is None:
			return 1

		await cursor.close()
		await database.close()

		return {
			"id": data[0],
			"pass_hash": data[1],
			"name": data[2],
			"email": data[3]
		}

	async def create_user(
		self, 
		user_id:str, 
		password:str, 
		user_name:str, 
		user_email:str
	) -> int:
		if user_email in [user["email"] for user in await self.get_users()]:
			return 1

		database = await aiosqlite.connect("core/database.db")
		pass_hash = hashlib.md5(password.encode()).hexdigest()
		await database.execute(f"""INSERT INTO users (user_id, pass_hash, name, e_mail) VALUES (
			"{user_id}",
			"{pass_hash}",
			"{user_name}",
			"{user_email}"
		)""")
		await database.commit()
		await database.close()
		return 0

	async def delete_user(
		self, 
		user_id:str, 
		password:str
	) -> int:
		pass_hash = hashlib.md5(password.encode()).hexdigest()

		database = await aiosqlite.connect("core/database.db")
		cursor = await database.execute(f"""SELECT pass_hash FROM users WHERE user_id = "{user_id}" """)
		data = await cursor.fetchone()

		if data is None:
			return 1

		database_pass_hash = data[0]
		await cursor.close()

		if pass_hash != database_pass_hash:
			return 2

		await database.execute(f"""DELETE FROM users WHERE user_id = "{user_id}" """)
		await database.commit()
		await database.close()
		
		return 0

	async def edit_user(
		self,
		user_id:str,
		params:dict
	) -> int:
		if "email" not in params.keys() and "name" not in params.keys():
			return 0

		pass_hash = hashlib.md5(params.get("password").encode()).hexdigest()

		database = await aiosqlite.connect("core/database.db")
		cursor = await database.execute(f"""SELECT pass_hash FROM users WHERE user_id = "{user_id}" """)
		data = await cursor.fetchone()

		if data is None:
			return 2

		database_pass_hash = data[0]
		await cursor.close()

		if pass_hash != database_pass_hash:
			return 1

		for key, value in params.items():
			if key == "name":
				await database.execute(f"""UPDATE users SET name = "{params.get("name")}" WHERE user_id = "{user_id}" """)
			elif key == "email":
				await database.execute(f"""UPDATE users SET e_mail = "{params.get("email")}" WHERE user_id = "{user_id}" """)

		await database.commit()
		await database.close()

		return 0