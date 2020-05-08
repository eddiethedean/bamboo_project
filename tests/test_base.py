import unittest
import sqlalchemy as sa

import sys
project_home = u'/home/EddieDean/bamboo/'
if project_home not in sys.path:
     sys.path = [project_home] + sys.path

from bamboo.bamboo_base import DataBase

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class TestTable(Base):
    __tablename__ = 'test_table'
    id   = Column(Integer, primary_key=True)
    key  = Column(String, nullable=False)
    val  = Column(String)
    date = Column(DateTime, default=datetime.utcnow)

class SecondTable(Base):
    __tablename__ = 'second_table'
    id = Column(Integer, primary_key=True)
    val = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    key = Column(ForeignKey('test_table.key'))

def make_filled_data_base():
    engine = sa.create_engine('sqlite:///', echo=False)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(TestTable(key='21', val='Thing'))
    session.add(TestTable(key='25', val='Person'))
    session.add(SecondTable(key='21', val='Chair'))
    session.commit()
    return engine

class Test(unittest.TestCase):
    #def setUp(self):

    def test_empty_db(self):
        engine = sa.create_engine('sqlite:///', echo=False)
        db = DataBase(engine)
        expected = "DataBase()"
        self.assertEqual(expected, repr(db))

    def test_fill_db(self):
        engine = make_filled_data_base()
        db = DataBase(engine)
        self.assertEqual(2, len(db))
        self.assertEqual(2, len(db['test_table']))
        self.assertEqual(1, len(db['second_table']))

    def test_new_col(self):
        engine = make_filled_data_base()
        db = DataBase(engine)
        df = db['test_table']
        df['age'] = [11, 22]
        db.push()
        db = DataBase(engine)
        # check if new column exists
        self.assertTrue('age' in db['test_table'].column_names)
        self.assertEqual(11, db['test_table'][0]['age'])
        self.assertEqual(22, db['test_table'][1]['age'])



