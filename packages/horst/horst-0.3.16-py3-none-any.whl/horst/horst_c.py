class HorstTable():

    sql_critical_keywords = {'group'}

    def __init__(self, table_name):
        self.table_name = table_name
        self.field_list = []
        self.temp_table = 'TEMP'

    def add_field(self, name, type):
        field = {}
        field["name"] = name
        field["type"] = 'INT64' if type == 'integer' else type
        self.field_list.append(field)

    def create_table(self) -> str:
        table_list = ''
        for field in self.field_list:
            table_list = table_list + self.wrap_keywords(field["name"]) +' '+ field["type"] + ', '
        # uups, one comma 2 much
        table_list = table_list[:-2]
        sql_create_string = f"CREATE {self.temp_table} TABLE {self.table_name} ({table_list});"
        return sql_create_string        

    def drop_table(self) -> str:
        sql_code = f"DROP TABLE {self.table_name};"
        return sql_code

    def fields(self, fields_out=[], show_type=False, table_alias='') -> str:
        first_field = True
        for field in self.field_list:
            if field["name"] in fields_out:
                pass
            else:
                if first_field:
                    select_fields = (table_alias+'.' if table_alias != '' else '') + self.wrap_keywords(field["name"]) \
                    + ((' ' + field["type"]) if show_type else '')
                    first_field = False
                else:
                    select_fields = select_fields + ', ' + (table_alias+'.' if table_alias != '' else '') \
                    + self.wrap_keywords(field["name"]) + ((' ' + field["type"]) if show_type else '')
        return select_fields

    def show(self):
        print("..............................")
        print(f"table {self.table_name} has some fields {self.field_list} ")

    def wrap_keywords(self, key) -> str:
        if key in self.sql_critical_keywords:
            return "`" + key + "`"
        else:
            return key

