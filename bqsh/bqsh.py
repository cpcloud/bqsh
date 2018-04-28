import os
import sys

from google.api_core.exceptions import BadRequest

from prompt_toolkit import prompt
from prompt_toolkit.token import Token
from prompt_toolkit.layout.lexers import PygmentsLexer
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import style_from_pygments

from pygments.styles.default import DefaultStyle
from pygments.lexers.sql import PostgresLexer

import ngrid.grid

from bqsh.meta import meta

style = style_from_pygments(DefaultStyle, {
    # Prompt tokens.
    Token.Project: 'bold',
    Token.Dataset: 'bold',
})


def loop(
    project, dataset, history_file, completion, multiline, verbose, true_color
):
    import ibis

    history = FileHistory(history_file)
    lexer = PygmentsLexer(PostgresLexer)
    con = ibis.bigquery.connect(project, dataset)

    while True:
        def get_prompt_tokens(cli):
            return [
                (Token.Project, con.data_project),
                (Token.ProjectDatasetDot, '.'),
                (Token.Dataset, con.dataset_id),
                (Token.RightAngle, ' > '),
            ]
        try:
            query = prompt(
                get_prompt_tokens=get_prompt_tokens,
                style=style,
                lexer=lexer,
                history=history,
                multiline=multiline,
                true_color=true_color,
            )
            if not query:
                continue

            if verbose:
                print(query)

            lower_query = query.lower()
            if lower_query.startswith(('show', 'describe')):
                meta(con, lower_query)
                continue
        except KeyboardInterrupt:
            pass
        except EOFError:
            return 0
        else:
            try:
                cursor = con.raw_sql(query)
                result = cursor.query.to_dataframe()
            except KeyboardInterrupt:
                pass
            except BadRequest as e:
                error, = e.errors
                if error['reason'] == 'invalidQuery':
                    print(e.message)
                else:
                    raise
            else:
                ngrid.grid.show_dataframe(result)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    parser.add_argument('dataset')
    parser.add_argument(
        '-H', '--history-file',
        default=os.path.join(os.path.expanduser('~'), '.bqsh-history')
    )
    parser.add_argument('-C', '--completion', action='store_true')
    parser.add_argument('-m', '--multiline', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-c', '--true-color', action='store_true')
    return parser.parse_args()


def main():
    args = parse_args()
    result = loop(**dict(args._get_kwargs()))
    sys.exit(result)


if __name__ == '__main__':
    main()
