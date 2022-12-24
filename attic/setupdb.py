from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

engine = create_engine('sqlite:///faqs.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

