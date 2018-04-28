import sly

from termcolor import cprint


class MetaCommandLexer(sly.Lexer):
    tokens = {
        SHOW,
        TABLES,
        DATASETS,
        DESCRIBE,
        IN,
        DOT,
        ID,
    }

    ignore = ' \t'

    ID = r'[A-Za-z_][A-Za-z_0-9-]*'
    ID['datasets'] = DATASETS
    ID['describe'] = DESCRIBE
    ID['tables'] = TABLES
    ID['show'] = SHOW
    ID['in'] = IN

    DOT = '\.'


class MetaCommandParser(sly.Parser):
    tokens = MetaCommandLexer.tokens

    def __init__(self, con):
        self.con = con

    @_('SHOW TABLES IN ID DOT ID')
    def stmt(self, p):
        cprint('\n'.join(self.con.list_tables(database=f'{p.ID0}.{p.ID1}')), attrs=['bold'])

    @_('SHOW TABLES IN ID')
    def stmt(self, p):
        cprint('\n'.join(self.con.list_tables(database=p.ID)), attrs=['bold'])

    @_('SHOW DATASETS')
    def stmt(self, p):
        cprint('\n'.join(self.con.list_databases()), attrs=['bold'])

    @_('SHOW TABLES')
    def stmt(self, p):
        cprint('\n'.join(self.con.list_tables()), attrs=['bold'])

    @_('DESCRIBE ID DOT ID DOT ID')
    def stmt(self, p):
        cprint(
            self.con.table(
                p.ID2, database=f'{p.ID0}.{p.ID1}'
            ).schema(), attrs=['bold']
        )

    @_('DESCRIBE ID DOT ID')
    def stmt(self, p):
        cprint(self.con.table(p.ID1, database=p.ID0).schema(), attrs=['bold'])

    @_('DESCRIBE ID')
    def stmt(self, p):
        cprint(self.con.table(p.ID).schema(), attrs=['bold'])

    def error(self, p):
        if not p:
            self.errok()


lexer = MetaCommandLexer()


def meta(con, text):
    parser = MetaCommandParser(con)
    parser.parse(lexer.tokenize(text))
