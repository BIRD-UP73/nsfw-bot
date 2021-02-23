from sqlalchemy import Column, String, create_engine, ForeignKey, BigInteger
from sqlalchemy import Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('user_id', BigInteger, ForeignKey('user.id')),
                          Column('post_id', String(512), ForeignKey('post.id'))
                          )


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    posts = relationship('Post', secondary=association_table)


class Post(Base):
    __tablename__ = 'post'
    id = Column(BigInteger, primary_key=True)
    url = Column(String(1024), primary_key=True)
    users = relationship('User', secondary=association_table)


engine = create_engine('sqlite:///sqlalchemy_example.db')
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()
