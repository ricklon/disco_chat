from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

app = FastAPI()

engine = create_engine("sqlite:///mydatabase.db", dialect="aiosqlite")

@app.get("/items")
async def list_items():
    async with engine.connect() as conn:
        result = await conn.execute("SELECT * FROM items")
        rows = await result.fetchall()
        return rows
