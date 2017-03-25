from sanic import Sanic
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

app = Sanic(__name__)

Base = declarative_base()
Base.query = db_session.query_property()


# Models for database
class User(Base):
    user_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    subscription = relationship('Channel', secondary=subscriber, backref=backref('subscribers',
                                                                                 lazy='dynamic'))


class Channel(Base):
    channel_id = Column(Integer, primary_key=True)
    channel_name = Column(String(255), nullable=False)

# Create an intermediate table that will act as a bridge between User and Channel
subscriber = Table('subscriber',
                   Column('user_id', Integer, ForeignKey('user.user_id')),
                   Column('channel_id', Integer, ForeignKey('channel_channel_id'))
                   )

# Seed the database some fake data
async def db_init():
    user1 = User(name='Dave')
    db_session.add(user1)
    user2 = User(name='Bob')
    db_session.add(user2)

    channel1 = Channel(channel_name='Cat Videos')
    db_session.add(channel1)
    channel2 = Channel(channel_name='Puppy Videos')
    db_session.add(channel2)

    # Associate channel and user
    channel1.subscribers.append(user1)
    channel1.subscribers.append(user2)
    channel2.subscribers.append(user1)

    # Commit changes
    db_session.commit()

if __name__ == '__main__':
    db_init()
    app.run()

