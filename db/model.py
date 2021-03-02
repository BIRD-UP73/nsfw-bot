from sqlalchemy import BigInteger, DateTime, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Post(Base):
    __tablename__ = 'post'
    user_id = Column(BigInteger, primary_key=True)
    post_id = Column(BigInteger, primary_key=True)
    url = Column(String(1024), primary_key=True)
    saved_at = Column(DateTime, nullable=False)


engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
