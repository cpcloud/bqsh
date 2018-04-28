import os
import click

from prompt_toolkit import prompt
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory


from pygments.lexers.sql import PostgresLexer


@click.command()
@click.argument('project')
@click.argument('dataset')
@click.option(
    '--history-file',
    type=click.Path(),
    default=os.path.join(os.path.expanduser('~'), '.bqsh-history'),
)
def main(project, dataset, history_file):
    import ibis

    history = FileHistory(history_file)
    lexer = PygmentsLexer(PostgresLexer)
    con = ibis.bigquery.connect(project, dataset)
    while True:
        query = prompt('bqsh> ', lexer=lexer, history=history)
        try:
            cursor = con.raw_sql(query)
            result = cursor._fetch()
        except Exception as e:
            print(e)
        else:
            print(result)


if __name__ == '__main__':
    main()
