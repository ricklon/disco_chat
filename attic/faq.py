from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import scoped_session
from sqlalchemy.ext.declarative import declarative_base

#from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class FAQ(Base):
    __tablename__ = 'faq'

    id = Column(Integer, primary_key=True)
    message_id = Column(String)
    channel_id = Column(String)
    question = Column(String)
    answer = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

engine = create_engine('sqlite+aiosqlite:///faqs.db')
Session = scoped_session(session_factory=AsyncSession, bind=engine)


# engine = create_async_engine('sqlite+aiosqlite:///faqs.db')
# Base.metadata.begin(engine)
# #Base.metadata.create_all(engine)
# #Session = sessionmaker(bind=engine)
# Session = sessionmaker(bind=engine, class_=AsyncSession)

async def add_faq(session, channel_id, question, answer):
    # Create a new FAQ entry
    faq = FAQ(channel_id=channel_id, question=question, answer=answer, created_at=datetime.utcnow())

    # Add the entry to the session and commit the changes
    session.add(faq)
    await session.commit()

async def list_faqs(session, channel_id):
    # Retrieve a list of all the FAQ entries for the specified channel
    return await session.query(FAQ).filter(FAQ.channel_id == channel_id).all()

def update_faq(session, faq_id, question, answer):
    # Update the question and answer for the specified FAQ entry
    session.query(FAQ).filter(FAQ.id == faq_id).update({FAQ.question: question, FAQ.answer: answer, FAQ.updated_at: datetime.utcnow()})
    session.commit()

def delete_faq(session, faq_id):
    # Delete the specified FAQ entry
    session.query(FAQ).filter(FAQ.id == faq_id).delete()
    session.commit()

def get_faq(session, faq_id):
    # Retrieve the specified FAQ entry
    return session.query(FAQ).filter(FAQ.id == faq_id).first()


    
def like_faq(session, message_id):
    session.query(FAQ).filter(FAQ.message_id == message_id).update({FAQ.likes: FAQ.likes + 1})
    session.commit()

def dislike_faq(session, message_id):
    session.query(FAQ).filter(FAQ.message_id == message_id).update({FAQ.likes: FAQ.likes - 1})
    session.commit()
