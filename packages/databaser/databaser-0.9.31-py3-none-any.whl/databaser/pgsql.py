from typing import List

from databaser.db_parser.table_data.finder import Finder
from databaser.db_parser.table_data.insert import Insert
from databaser.db_parser.table_data.insert_from_select import InsertFromSelect
from databaser.db_parser.table_data.update import Update
from databaser.db_parser.table_data.delete import Delete
from databaser.db_parser.table_structure.add_column import AddColumn
from databaser.db_parser.table_structure.create_table import CreateTable, TableField
from databaser.db_parser.table_structure.drop_table import DropTable

from databaser.db_parser.database.create_database import CreateDatabase
from databaser.db_parser.database.drop_database import DropDatabase
from databaser.db_parser.database.create_schema import CreateSchema
from databaser.db_parser.database.drop_schema import DropSchema


class Query:
    TABLE_QUOTE = ""
    FIELD_QUOTE = ""

    def __init__(self, server_name: str):
        self.server_name = server_name
        if server_name == "pgsql" or server_name == "sqlsrv":
            self.FIELD_QUOTE = '"'
            self.TABLE_QUOTE = '"'

    def count(self, table_name: str, schema_name: str = "public"):
        return f"""SELECT count(*) FROM {f"{self.TABLE_QUOTE}{schema_name}{self.TABLE_QUOTE}." if self.server_name == "pgsql" else ""}{self.TABLE_QUOTE}{table_name}{self.TABLE_QUOTE}"""

    def find(self, table_name: str, fields: List[str] = None, condition: dict = {}, joins: dict = {},
             group_by: list = [], order_by: dict = {}, limit: int = 0, skip: int = 0, schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return Finder(table_name, fields, condition, joins, group_by, order_by, limit, skip, self.FIELD_QUOTE,
                      self.FIELD_QUOTE, schema_name, self.server_name)

    def insert(self, table_name: str, data: dict, value_quote: bool = False, schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return Insert(table_name, data, self.TABLE_QUOTE, self.FIELD_QUOTE, value_quote, schema_name)

    def insert_select(self, table_name: str, select: Finder, value_quote: bool = False, schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return InsertFromSelect(table_name, select.fields, select)  # TODO: Assign

    def insert_many(self, table_name: str, data: dict, value_quote: bool = False, schema_name: str = "public"):
        # TODO: Not functioning yet
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return Insert(table_name, data, self.TABLE_QUOTE, self.FIELD_QUOTE, value_quote, schema_name)

    def update(self, table_name: str, data: dict, conditions: dict, value_quote: bool = False,
               schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return Update(table_name, data, conditions, self.TABLE_QUOTE, self.FIELD_QUOTE, value_quote, schema_name)

    def delete(self, table_name: str, conditions: dict, value_quote: bool = False, schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return Delete(table_name, conditions, self.TABLE_QUOTE, self.FIELD_QUOTE, value_quote, schema_name)


class TableStructure:
    TABLE_QUOTE = ""
    FIELD_QUOTE = ""

    def __init__(self, server_name: str):
        self.server_name = server_name
        if server_name in ["pgsql", "sqlsrv"]:
            self.FIELD_QUOTE = '"'
            self.TABLE_QUOTE = '"'

    def create_table(self, table_name: str, table_fields: List[TableField], schema_name: str = "public"):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return CreateTable(table_name, table_fields, schema_name, self.TABLE_QUOTE, self.FIELD_QUOTE)

    def add_column(self, table_name: str, column_name: str, data_type: str, not_null: bool, schema_name: str = "public"):
        return AddColumn(table_name, column_name, data_type, not_null, self.TABLE_QUOTE, self.FIELD_QUOTE, schema_name)

    def drop_table(self, table_name: str, if_exists: bool = False):
        return DropTable(table_name, self.TABLE_QUOTE, if_exists)


class DatabaseStructure:
    TABLE_QUOTE = ""
    FIELD_QUOTE = ""

    def __init__(self, server_name: str):
        self.server_name = server_name
        if server_name in ["pgsql", "sqlsrv"]:
            self.FIELD_QUOTE = '"'
            self.TABLE_QUOTE = '"'

    def create_database(self, database_name: str):
        return CreateDatabase(database_name, self.TABLE_QUOTE)

    def drop_database(self, database_name: str):
        return DropDatabase(database_name, self.TABLE_QUOTE)

    def create_schema(self, schema_name):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return CreateSchema(schema_name, self.TABLE_QUOTE)

    def drop_schema(self, schema_name, cascade: bool = False):
        schema_name = schema_name if self.server_name in ['pgsql'] else ''
        return DropSchema(schema_name, self.TABLE_QUOTE, cascade=cascade)
