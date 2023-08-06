import copy
import sys
from sly import Parser

from horst.horst_l import HorstLexer
from horst.horst_c import HorstTable

class HorstParser(Parser):
    tokens = HorstLexer.tokens
    tables = {}
    wrap_keywords = HorstTable('tool').wrap_keywords

    def error(self, token):
        print(f".......... ERROR - during parsing: Type '{token.type}' with value '{token.value}'")

# ++++++++++++++++++++++++++++++++++++++++++
# +++ statement
# ++++++++++++++++++++++++++++++++++++++++++

    @_('table_declaration')
    def statement(self, p) -> str:
        return p.table_declaration

    @_('clone_table')
    def statement(self, p) -> str:
        return p.clone_table

    @_('DROP TABLES')
    def statement(self, p):
        sql_code = ''
        first_table = True
        for table_name in self.tables:
            if first_table:
                first_table = False
            else:
                sql_code = sql_code + '\n'
            sql_code = sql_code + self.tables[table_name].drop_table()
        return sql_code

    @_('list_fields')
    def statement(self, p) -> str:
        return p.list_fields

    @_('join_fields')
    def statement(self, p) -> str:
        return p.join_fields

    @_('COMMENT')
    def statement(self, p) -> str:
        return ''

# ++++++++++++++++++++++++++++++++++++++++++
# +++ table_declaration
# ++++++++++++++++++++++++++++++++++++++++++

    @_('error CREATE ')
    def table_declaration(self, p):
        sys.exit(f".......... ERROR - a table declaration begins with 'CREATE' ")

    @_('CREATE TABLE ID table_instance field_list')
    def table_declaration(self, p) -> str:
        return self.tables[self.table_name].create_table()

    @_('')
    def table_instance(self, p):
        self.table_name = p[-1]
        self.tables[self.table_name] = HorstTable(self.table_name)

    @_('SHOW_ALL')
    def table_declaration(self, p):
        for table_instance in self.tables.values():
            table_instance.show()

# ++++++++++++++++++++++++++++++++++++++++++
# +++ clone_table
# ++++++++++++++++++++++++++++++++++++++++++

    @_('clone_this_table add_field_list')
    def clone_table(self, p):
        return self.tables[self.table_name].create_table()

    @_('clone_this_table WITHOUT field_names')
    def clone_table(self, p):
        without_list = []
        for field in self.tables[self.table_name].field_list:
            if field["name"] not in p.field_names:
                without_list.append(field)
        self.tables[self.table_name].field_list = without_list
        return self.tables[self.table_name].create_table()

    @_('')
    def add_field_list(self, p):
        pass

    @_('ADD field_list')
    def add_field_list(self, p):
        pass

    @_('CLONE TABLE ID AS ID table_id')
    def clone_this_table(self, p):
        self.tables[self.table_name] = copy.deepcopy(self.tables[p.ID0])
        self.tables[self.table_name].table_name = self.table_name

    @_('')
    def table_id(self, p):
        self.table_name = p[-1]

# ++++++++++++++++++++++++++++++++++++++++++
# +++ list_fields
# ++++++++++++++++++++++++++++++++++++++++++

    @_('table_fields fields_with')
    def list_fields(self, p) -> str:
        return self.tables[p.table_fields['name']].fields(table_alias=p.table_fields['alias']
        , fields_out=p.fields_with['fields_out'], show_type=p.fields_with['show_type'])

    @_('table_fields')
    def list_fields(self, p) -> str:
        return self.tables[p.table_fields['name']].fields(table_alias=p.table_fields['alias'])

    @_('WITH TYPE')
    def fields_with(self, p) -> str:
        return {'show_type':True, 'fields_out':[]}
        # return self.tables[p.ID].fields(show_type=True)

    @_('WITH TYPE WITHOUT field_names')
    def fields_with(self, p) -> str:
        return {'show_type':True, 'fields_out':p.field_names}

    @_('WITHOUT field_names')
    def fields_with(self, p) -> str:
        return {'show_type':False, 'fields_out':p.field_names}

    @_('ID FIELDS')
    def table_fields(self, p) -> str:
        return {'name':p.ID, 'alias':''}

    @_('ID table_alias FIELDS')
    def table_fields(self, p) -> str:
        return {'name':p.ID, 'alias':p.table_alias}

# ++++++++++++++++++++++++++++++++++++++++++
# +++ join_fields
# +++ join table_name {as table_alias} on table_name {as table_alias} {(with | without) field_names}
# ++++++++++++++++++++++++++++++++++++++++++

    @_('ID table_alias ON ID')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias if len(p.table_alias) >0 else p.ID0
        join_on_fields = ''
        first_field = True
        for field in self.tables[p.ID0].field_list:
            if not first_field:
                join_on_fields = join_on_fields + ' AND ' 
            join_on_fields = join_on_fields + p.ID1 + '.' + self.wrap_keywords(field["name"]) + ' = ' + tab1 \
            + '.' + self.wrap_keywords(field["name"]) 
            first_field = False
        return join_on_fields

    @_('ID table_alias ON ID table_alias')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias0 if len(p.table_alias0) >0 else p.ID0
        tab2 = p.table_alias1 if len(p.table_alias1) >0 else p.ID1
        join_on_fields = ''
        first_field = True
        for field in self.tables[p.ID0].field_list:
            if not first_field:
                join_on_fields = join_on_fields + ' AND ' 
            join_on_fields = join_on_fields + tab2 + '.' + self.wrap_keywords(field["name"]) + ' = ' + tab1 \
            + '.' + self.wrap_keywords(field["name"]) 
            first_field = False
        return join_on_fields

    @_('ID table_alias ON ID WITH field_names')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias if len(p.table_alias) >0 else p.ID0
        join_on_fields = ''
        first_field = True
        for field in p.field_names:
            if not first_field:
                join_on_fields = join_on_fields + ' AND ' 
            join_on_fields = join_on_fields + p.ID1 + '.' + self.wrap_keywords(field) + ' = ' \
            + tab1 + '.' + self.wrap_keywords(field)
            first_field = False
        return join_on_fields

    @_('ID table_alias ON ID table_alias WITH field_names')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias0 if len(p.table_alias0) >0 else p.ID0
        tab2 = p.table_alias1 if len(p.table_alias1) >0 else p.ID1
        join_on_fields = ''
        first_field = True
        for field in p.field_names:
            if not first_field:
                join_on_fields = join_on_fields + ' AND ' 
            join_on_fields = join_on_fields + tab2 + '.' + self.wrap_keywords(field) + ' = ' \
            + tab1 + '.' + self.wrap_keywords(field)
            first_field = False
        return join_on_fields

    @_('ID table_alias ON ID WITHOUT field_names')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias if len(p.table_alias) >0 else p.ID0
        join_on_fields = ''
        first_field = True
        for field in self.tables[p.ID0].field_list:
            if field["name"] not in p.field_names:
                if not first_field:
                    join_on_fields = join_on_fields + ' AND ' 
                join_on_fields = join_on_fields + p.ID1 + '.' + self.wrap_keywords(field["name"]) + ' = ' \
                + tab1 + '.' + self.wrap_keywords(field["name"]) 
                first_field = False
        return join_on_fields

    @_('ID table_alias ON ID table_alias WITHOUT field_names')
    def join_fields(self, p) -> str:
        tab1 = p.table_alias0 if len(p.table_alias0) >0 else p.ID0
        tab2 = p.table_alias1 if len(p.table_alias1) >0 else p.ID1
        join_on_fields = ''
        first_field = True
        for field in self.tables[p.ID0].field_list:
            if field["name"] not in p.field_names:
                if not first_field:
                    join_on_fields = join_on_fields + ' AND ' 
                join_on_fields = join_on_fields + tab2 + '.' + self.wrap_keywords(field["name"]) + ' = ' \
                + tab1 + '.' + self.wrap_keywords(field["name"]) 
                first_field = False
        return join_on_fields

# ++++++++++++++++++++++++++++++++++++++++++
# +++ common methods
# ++++++++++++++++++++++++++++++++++++++++++

    @_('ID')
    def field_names(self, p) -> str:
        element = [p.ID,]
        return element

    @_('ID "," field_names')
    def field_names(self, p) -> str:
        element = [p.ID,]
        field_names = p.field_names
        field_names.append(element[0])
        return field_names

    @_('AS ID')
    def table_alias(self, p) -> str:
        return f"{p.ID}"

    @_('field_definition')
    def field_list(self, p):
        pass

    @_('field_definition "," field_list')
    def field_list(self, p):
        pass

    @_('ID FIELD_TYPE')
    def field_definition(self, p):
        self.tables[self.table_name].add_field(name=p.ID, type=p.FIELD_TYPE)
