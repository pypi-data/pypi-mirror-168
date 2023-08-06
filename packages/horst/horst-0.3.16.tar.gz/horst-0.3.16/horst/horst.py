""" 
    Extended BNF of horst

    statement = table_declaration 
        | clone_table
        | drop tables 
        | list_fields
        | join_fields
        | comment

    table_declaration = create table table_name field_list
    clone_table = clone table ID as ID {add field_list | without field_names}
    list_fields = table_name {as table_alias} fields {with type} {without field_names}
    join_fields = table_name {as table_alias} on table_name {as table_alias} {(with | without) field_names}
    comment = -- * 

    field_list = field_definition {, field_definition}
    field_definition = field_name field_type
    field_type = INTEGER | STRING | TIMESTAMP
    field_names = field_name {, field_name} 
    field_name = ID
    table_name = ID
    table_alias = ID
    ID = RegEx([a-zA-Z_][a-zA-Z0-9_]*) 

    code example 
    $ python horst.py this_horst_script
    << horst.this_horst_script.sql
    >> this_horst_script.sql

"""
import argparse
from sly import Parser

from horst.horst_l import HorstLexer
from horst.horst_p import HorstParser

def new_line_on(string, length=90):

    def nl_position(string2search):
        position = string2search[:length].rfind(',')
        position_and = string2search[:length].lower().rfind('and') 
        position = position if position > position_and else position_and
        return position

    if len(string) > length:
        comma_position = nl_position(string)
        line = string[:comma_position]
        string = string[comma_position:]
        while len(string) > length:
            comma_position = nl_position(string)
            line = line + '\n' + string[:comma_position]
            string = string[comma_position:]
        if len(string) > 0:
            line = line + '\n' + string
    else:
        line = string
    return line

def horst():

    command_line_parser = argparse.ArgumentParser(description='Horst supports SQL.')
    command_line_parser.add_argument("file", help='SQL-file with horst code to process.')
    command_line_args = command_line_parser.parse_args()

    lexer = HorstLexer()
    parser = HorstParser()
    
    horst_path_file = command_line_args.file
    horst_path =  horst_path_file[:horst_path_file[::-1].find("/")+1]
    horst_file = horst_path_file[horst_path_file[::-1].find("/")+1:]

    EOF = ''
    read_horst = False

    with open(horst_path + 'horst.' + horst_file + '.sql', 'r') as hsql_file \
    , open(horst_path_file + '.sql', 'w') as sql_file:
        hsql_file_line = hsql_file.readline()

        while hsql_file_line != EOF:

            horst_start = hsql_file_line.find('{{')
            horst_end = hsql_file_line.find('}}')

            # start symbol detected
            if horst_start >= 0:
                read_horst = True
                horst_code = ''

            if read_horst:
                horst_code = horst_code + hsql_file_line[
                    horst_start +2 if horst_start >= 0 else None 
                    : horst_end  if horst_end >= 0 else None
                    ]

            # end symbol detected
            if horst_end >= 0:
                read_horst = False
                sql_code = parser.parse(lexer.tokenize(horst_code))
                sql_code = new_line_on(sql_code)
                hsql_file_line = hsql_file_line[:horst_end +2] +sql_code+ hsql_file_line[horst_end +2:]

            if horst_start > 0:
                sql_file_line = hsql_file_line[:horst_start if horst_start >= 0 else None]
                if horst_end >= 0:
                    sql_file_line = sql_file_line + hsql_file_line[horst_end +2 if horst_end >= 0 else None:]
                else:
                    sql_file_line = sql_file_line + '\n\r'
            else:
                sql_file_line = hsql_file_line[horst_end +2 if horst_end >= 0 else None:]

            if (horst_start > 0 or horst_end >= 0) and len(sql_file_line.strip(' \n\r')) > 0:
                sql_file.write(sql_file_line)
            elif not read_horst and horst_end < 0:
                sql_file.write(sql_file_line)

            hsql_file_line = hsql_file.readline()

if __name__ == '__main__':
    horst()