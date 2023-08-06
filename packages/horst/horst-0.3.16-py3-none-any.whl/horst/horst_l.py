import sys
from sly import Lexer

class HorstLexer(Lexer):
    tokens = { ADD, AS, COMMENT, CLONE, CREATE, DROP, FIELDS, FIELD_TYPE, ID, ON
        , SHOW_ALL, TABLE, TABLES, TYPE
        , WITH, WITHOUT }
    ignore = ' \t'
    literals = { ',', }

    # Identifiers
    # general
    ID = r'[a-z_][a-z0-9_.]*'
    COMMENT = r'--.*'
    
    # keywords aka terminal identifiers
    ID['add'] = ADD
    ID['as'] = AS
    ID['bool'] = FIELD_TYPE
    ID['create'] = CREATE
    ID['clone'] = CLONE
    ID['drop'] = DROP
    ID['fields'] = FIELDS
    ID['integer'] = FIELD_TYPE
    ID['string'] = FIELD_TYPE
    ID['timestamp'] = FIELD_TYPE
    ID['on'] = ON
    ID['show_all'] = SHOW_ALL
    ID['table'] = TABLE
    ID['tables'] = TABLES
    ID['type'] = TYPE
    ID['with'] = WITH
    ID['without'] = WITHOUT

    # Line number tracking
    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, token):
        sys.exit(f"ERROR during lexical analysis: Bad character '{token.value[0]}'")