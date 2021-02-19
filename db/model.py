from sqlalchemy import Column, Integer, String, create_engine, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import Table

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('user_id', BigInteger, ForeignKey('user.id')),
                          Column('post_file_url', String(512), ForeignKey('post.file_url'))
                          )


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    posts = relationship('Post', secondary=association_table)


class Post(Base):
    __tablename__ = 'post'
    file_url = Column(String(512), primary_key=True)
    file_ext = Column(String(8))
    score = Column(Integer)
    source = Column(String(512))
    users = relationship('User', secondary=association_table)


engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
