import sly

from termcolor import cprint


class MetaCommandLexer(sly.Lexer):
    tokens = {
        SHOW,  # noqa: F821
        TABLES,  # noqa: F821
        DATASETS,  # noqa: F821
        DESCRIBE,  # noqa: F821
        IN,  # noqa: F821
        DOT,  # noqa: F821
        ID,  # noqa: F821
    }

    ignore = ' \t'

    ID = r'[A-Za-z_][A-Za-z_0-9-]*'
    ID['datasets'] = DATASETS  # noqa: F821
    ID['describe'] = DESCRIBE  # noqa: F821
    ID['tables'] = TABLES  # noqa: F821
    ID['show'] = SHOW  # noqa: F821
    ID['in'] = IN  # noqa: F821

    DOT = '\.'


class MetaCommandParser(sly.Parser):
    tokens = MetaCommandLexer.tokens

    def __init__(self, con):
        self.con = con

    @_('SHOW TABLES IN ID DOT ID')  # noqa: F821
    def stmt(self, p):
        cprint('\n'.join(
            self.con.list_tables(database=f'{p.ID0}.{p.ID1}')), attrs=['bold'])

    @_('SHOW TABLES IN ID')  # noqa: F811,F821
    def stmt(self, p):
        cprint('\n'.join(self.con.list_tables(database=p.ID)), attrs=['bold'])

    @_('SHOW DATASETS')  # noqa: F811,F821
    def stmt(self, p):
        cprint('\n'.join(self.con.list_databases()), attrs=['bold'])

    @_('SHOW TABLES')  # noqa: F811,F821
    def stmt(self, p):
        cprint('\n'.join(self.con.list_tables()), attrs=['bold'])

    @_('DESCRIBE ID DOT ID DOT ID')  # noqa: F811,F821
    def stmt(self, p):
        cprint(
            self.con.table(
                p.ID2, database=f'{p.ID0}.{p.ID1}'
            ).schema(), attrs=['bold']
        )

    @_('DESCRIBE ID DOT ID')  # noqa: F811,F821
    def stmt(self, p):
        cprint(self.con.table(p.ID1, database=p.ID0).schema(), attrs=['bold'])

    @_('DESCRIBE ID')  # noqa: F811,F821
    def stmt(self, p):
        cprint(self.con.table(p.ID).schema(), attrs=['bold'])

    def error(self, p):
        if not p:
            self.errok()


lexer = MetaCommandLexer()


def meta(con, text):
    parser = MetaCommandParser(con)
    parser.parse(lexer.tokenize(text))
