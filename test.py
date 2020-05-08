import sqlalchemy as sa
from datetime import datetime
from bamboo.generate_code import generate_code
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from bamboo.bamboo_base import DataBase


def main():
    print('starting main')
    engine = sa.create_engine('sqlite:///', echo=False)
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

    print('creating tables')
    # create tables
    Base.metadata.create_all(bind=engine)

    print(generate_code(engine))

    # Setup session
    Session = sessionmaker(bind=engine)
    session = Session()

    print('adding items')
    # Add items
    session.add(TestTable(key='21', val='Thing'))
    session.add(TestTable(key='25', val='Person'))
    session.add(SecondTable(key='21', val='Chair'))
    session.commit()

    print('creating DataBase object')
    # create DataBase object
    db = DataBase(engine)
    print('printing DataBase object before changes')
    print(db)
    tbl = db['test_table']

    print('adding column to table')
    tbl['age'] = [18, 19]
    print('pushing changes')
    db.push()
    print('printing DataBase object')
    print(db)
    print('printing data types')
    print(tbl.types)

    print('printing new DataBase')
    new_db = DataBase(engine)
    print(new_db)
    print('printing new data types')
    print(new_db['test_table'].types)

    #add_foreign_key('second_table', 'key', engine, 'test_table', 'key')

    print(generate_code(engine))

    print('deleting a column')
    tbl2 = db['second_table']
    tbl2.drop(['date'], axis=1, inplace=True)

    db.push()

    print(db)
    print(generate_code(engine))

if __name__ == '__main__':
    main()