import asyncio

from utils.db_api.postgresql import Database


async def test():
    db = Database()
    await db.create()

    print("Users jadvalini yaratamiz ")
    await db.create_table_users()
    print("Yaratildi")

    print("Foydalanuvchilarni bazaga qo'shamiz...")

    await db.add_user("muzaffar","nitc",11921179)
    await db.add_user("shohmirzo","azamat050",12365489)
    await db.add_user("sotaquzi","topponchat",11)
    await db.add_user("Yusuf","qirol",1)
    await db.add_user("Kozim","forward",79)
    print("Qo'shildi")

    users=await db.select_all_user()
    print(f"Barcha foydalanuvchilar: {users}")

    user = await db.select_user(id=1)
    print(f"Bitta user: {user}")

asyncio.run(test())
