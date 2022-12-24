import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text

async def main():
    # Connect to the database
    engine = create_async_engine("sqlite+aiosqlite:///mydatabase.db")
    async with engine.connect() as conn:
        # Create the faqs table if it doesn't exist
        await conn.execute(text("CREATE TABLE IF NOT EXISTS faqs (question text, answer text)"))

        # Insert some test data into the table
        await conn.execute(text("INSERT INTO faqs (question, answer) VALUES ('What is the capital of France?', 'Paris')"))
        await conn.execute(text("INSERT INTO faqs (question, answer) VALUES ('What is the capital of Germany?', 'Berlin')"))
        await conn.execute(text("INSERT INTO faqs (question, answer) VALUES ('What is the capital of Italy?', 'Rome')"))
       
        # Save the changes to the database
        await conn.commit()

        # Fetch the rows from the table
        result = await conn.execute(text("SELECT * FROM faqs"))
        rows = result.fetchall()

        # Create the faqs object
        faqs = {}
        for row in rows:
            question = row['question']
            answer = row['answer']
            faqs[question] = answer

        # Print the faqs object
        print(faqs)

asyncio.run(main())
