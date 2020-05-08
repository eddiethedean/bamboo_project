import unittest
import pandas as pd

from first_table_maker import make_filled_data_base
from make_db_delete_column import make_db_delete_column
from make_db_add_column import make_db_add_column

import sys
project_home = u'/home/EddieDean/bamboo/'
if project_home not in sys.path:
     sys.path = [project_home] + sys.path

from bamboo.migration import add_column, delete_column
from bamboo.bamboo_utils import get_table, get_type
from bamboo.generate_code import generate_code


class Test(unittest.TestCase):

    def test_metadata_add_column(self):
        """table, name, type"""
        engine = make_filled_data_base()
        table_name = 'test_table'
        df = pd.read_sql(table_name, engine)
        col_name = 'age'
        df[col_name] = [22, 33]
        add_column(get_table(table_name, engine), col_name, get_type(df, col_name))
        engine2 = make_db_add_column()
        code1 = generate_code(engine)
        code2 = generate_code(engine2)
        self.assertEqual(code1, code2)

    def test_metadata_delete_column(self):
        """table, name, engine"""
        engine = make_filled_data_base()
        table_name = 'test_table'
        df = pd.read_sql(table_name, engine)
        df.drop(['val'], axis=1, inplace=True)
        delete_column(get_table(table_name, engine), 'val', engine)
        engine3 = make_db_delete_column()
        code1 = generate_code(engine)
        code3 = generate_code(engine3)
        self.assertEqual(code1, code3)

    def test_data_add_column(self):
        """table, name, type"""
        engine = make_filled_data_base()
        table_name = 'test_table'
        df = pd.read_sql(table_name, engine)
        col_name = 'age'
        df[col_name] = [22, 33]
        add_column(get_table(table_name, engine), col_name, get_type(df, col_name))
        engine2 = make_db_add_column()
        df2 = pd.read_sql(table_name, engine2)
        self.assertTrue(df.equals(df2))

    def test_data_delete_column(self):
        """table, name, engine"""
        engine = make_filled_data_base()
        table_name = 'test_table'
        df = pd.read_sql(table_name, engine)
        df.drop(['val'], axis=1, inplace=True)
        delete_column(get_table(table_name, engine), 'val', engine)
        engine3 = make_db_delete_column()
        df2 = pd.read_sql(table_name, engine3)
        self.assertTrue(df.equals(df2))


