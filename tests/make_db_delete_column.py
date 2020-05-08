import sqlalchemy as sa

from datetime import date
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class TestTable(Base):
    __tablename__ = 'test_table'
    id   = Column(Integer, primary_key=True)
    key  = Column(Integer, nullable=False)
    date = Column(DateTime)

class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True)
    val = Column(Integer, nullable=False)
    date = Column(DateTime)
    key = Column(ForeignKey('test_table.key'))

def make_db_delete_column():
    engine = sa.create_engine('sqlite:///', echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(TestTable(key='21', date=date.fromisoformat('2019-12-04')))
    session.add(TestTable(key='25', date=date.fromisoformat('2019-12-04')))
    session.add(SecondTable(key='21', val='Chair', date=date.fromisoformat('2019-12-04')))
    session.commit()
    return engine