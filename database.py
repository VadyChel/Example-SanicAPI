import typing
import aiosqlite
import hashlib

class Database:
	async def prepare_to_start(self) -> None:
		database = await aiosqlite.connect("database.db")
		cursor = await database.execute("""CREATE TABLE IF NOT EXISTS users (
			user_id TEXT,
			pass_hash TEXT,
			name TEXT,
			e_mail TEXT
		)""")
		await database.commit()
		await cursor.close()

	async def get_users(self) -> list:
		database = await aiosqlite.connect("database.db")
		cursor = await database.execute("""SELECT * FROM users""")
		data = await cursor.fetchall()
		await cursor.close()
		await database.close()

		return [{
			"id": user[0],
			"name": user[2],
			"email": user[3]
		} for user in data]

	async def get_user(self, user_id:str) -> typing.Union[tuple, bool]:
		try:
			database = await aiosqlite.connect("database.db")
			cursor = await database.execute(f"""SELECT * FROM users WHERE user_id = "{user_id}" """)
			data = await cursor.fetchone()
			await cursor.close()
			await database.close()

			return {
				"id": data[0],
				"pass_hash": data[1],
				"name": data[2],
				"email": data[3]
			}
		except:
			return False

	async def create_user(
		self, 
		user_id:str, 
		password:str, 
		user_name:str, 
		user_email:str
	) -> typing.Union[bool, None]:
		if user_email in [user["email"] for user in await self.get_users()]:
			return False

		database = await aiosqlite.connect("database.db")
		pass_hash = hashlib.md5(password.encode()).hexdigest()
		await database.execute(f"""INSERT INTO users (user_id, pass_hash, name, e_mail) VALUES (
			"{user_id}",
			"{pass_hash}",
			"{user_name}",
			"{user_email}"
		)""")
		await database.commit()
		await database.close()
		return True

	async def delete_user(
		self, 
		user_id:str, 
		password:str
	) -> bool:
		database = await aiosqlite.connect("database.db")
		pass_hash = hashlib.md5(password.encode()).hexdigest()
		cursor = await database.execute(f"""SELECT pass_hash FROM users WHERE user_id = "{user_id}" """)
		database_pass_hash = (await cursor.fetchone())[0]
		await cursor.close()

		if pass_hash != database_pass_hash:
			return False

		await database.execute(f"""DELETE FROM users WHERE user_id = "{user_id}" """)
		await database.commit()
		await database.close()
		
		return True

	async def edit_user(
		self,
		user_id:str,
		password:str,
		params:dict
	) -> bool:
		database = await aiosqlite.connect("database.db")
		if "name" in params.keys():
			field = "name"
			value = params.get("name")
		elif "email" in params.keys():
			field = "e_mail"
			value = params.get("email")
		else:
			return True
