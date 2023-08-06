import re
from typing import List


class FieldParser:
    def __init__(self, fields: List[str], table_name: str, schema_name: str = "public", table_quote: str = '"',
                 field_quote: str = '"'):
        self.fields = fields
        self.table_name = table_name
        self.schema_name = schema_name
        self.table_quote = table_quote
        self.field_quote = field_quote

    def parse(self):
        if self.fields is None or len(self.fields) == 0:
            return "*"

        in_function_parameters = ""
        f = ""

        fields = []
        for field in self.fields:
            alias = field.split(" as ")
            if alias.__len__() > 1:
                field = alias[0]
                alias = alias[-1]
            else:
                alias = ""

            f = ""
            if re.search("[a-zA-Z]+\([^\)]*\)(\.[^\)]*\))?", field):
                split = field.split("(")
                f = split[0]
                in_function_parameters = split[-1][:-1]

            field_split = in_function_parameters.split(",") if in_function_parameters.__contains__(",") else field

            # field_split = field.split(".")
            # field = field_split[-1] if field_split.__len__() in [1, 2, 3] else field
            # table_name = field_split[-2] if field_split.__len__() in [2, 3] else self.table_name
            # schema_name = field_split[-3] if field_split.__len__() == 3 else self.schema_name
            #
            # schema_name = f"{self.table_quote}{schema_name}{self.table_quote}."
            # table_name = f"{self.table_quote}{table_name}{self.table_quote}."
            # field = schema_name + table_name + f"{self.field_quote}{field}{self.field_quote}"
            # field = f"{f}({field})" if f != "" else field

            if in_function_parameters.__contains__(","):
                params = []
                for param in in_function_parameters.split(","):

                    if not param.__contains__("'"):
                        param_split = param.split(".") if param.__contains__(".") else param.strip()
                        param_split[0] = param_split[0].strip()

                        table_name = param_split[-2] if param.__contains__(".") and param_split.__len__() in [2,3] else self.table_name

                        schema_name = param.split(".")[-3] if param.__contains__(".") and param_split.__len__() in [3] else self.schema_name

                        param = param.split(".")[-1] if param.__contains__(".") else param

                        schema_name = f"{self.table_quote}{schema_name}{self.table_quote}."
                        table_name = f"{self.table_quote}{table_name}{self.table_quote}."
                        param = schema_name + table_name + f"{self.field_quote}{param}{self.field_quote}"

                    params.append(param)

                field = f"{f}({','.join(params)})" if f != "" else field
            else:
                field_split = field.split(".")

                table_name = field_split[-2] if field_split.__len__() in [2, 3] else self.table_name

                schema_name = field_split[-3] if field_split.__len__() in [3] else self.schema_name

                field = field_split[-1] if field_split.__len__() > 1 else field

                schema_name = f"{self.table_quote}{schema_name}{self.table_quote}."
                table_name = f"{self.table_quote}{table_name}{self.table_quote}."
                field = schema_name + table_name + f"{self.field_quote}{field}{self.field_quote}"


            field = f"{field} as {alias}" if alias != "" else field
            fields.append(field)

        fields = f','.join(fields)

        return fields
