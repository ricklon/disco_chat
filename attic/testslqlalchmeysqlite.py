# import asyncio
# from sqlalchemy.ext.asyncio import create_async_engine



# async def main():
#     engine = create_async_engine("sqlite:///mydatabase.db+aiosqlite", dialect="aiosqlite")
#     async with engine.connect() as conn:
#         result = await conn.execute("SELECT * FROM items")
#         rows = await result.fetchall()
#         print(rows)

# asyncio.run(main())
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///mydatabase.db")
    async with engine.connect() as conn:
        # Create a statement object using the text method
        stmt = text("SELECT * FROM items")
        # Execute the statement and fetch the results
        result = await conn.execute(stmt)
        rows = result.fetchall()
        print(rows)

asyncio.run(main())
