import argparse
import inspect
import io
from importlib import metadata
from sys import stderr
from typing import TextIO

import markovify


try:
    VERSION = metadata.version(inspect.getmodulename(__file__))
except:
    VERSION = 'unknown'


class MarkovChatter():

    def __init__(self, text: str, state_size=2, word_divider=' ', new_line=False) -> None:

        if new_line:
            self._model = markovify.NewlineText(text, state_size=state_size)
        else:
            self._model = markovify.Text(text, state_size=state_size)
        self._model = self._model.compile()
        self._word_divider = word_divider

    def make_sentence(self, *, max_chars: int = 0, tries: int = 10) -> str:

        sentence = ''

        for _ in range(tries):
            raw_sentense = self._model.make_sentence()
            if raw_sentense:
                sample_sentense = self._word_divider.join(raw_sentense.split())
                if max_chars and max_chars < len(sample_sentense):
                    continue
                sentence = sample_sentense
                break

        if not sentence:
            print(f'{__class__.__name__}.{inspect.currentframe().f_code.co_name}:',
                'failed to generate sentence', file=stderr)

        return sentence


def chatter_from_args(args: argparse.Namespace) -> MarkovChatter:

    text = ''
    files: list[TextIO] = args.file
    sio = io.StringIO()
    for file_ in files:
        sio.write(file_.read())
    word_divider = '' if args.no_divider else ' '
    new_line = bool(args.new_line)
    return MarkovChatter(sio.getvalue(), word_divider=word_divider, new_line=new_line)


def _run(args: argparse.Namespace) -> None:

    chatter = chatter_from_args(args)
    max_chars: int = args.max_chars
    tries: int = args.tries
    print(chatter.make_sentence(max_chars=max_chars, tries=tries))


def _server(args: argparse.Namespace) -> None:

    from flask import Flask, request

    chatter = chatter_from_args(args)

    app = Flask(__name__)

    @app.route('/text')
    def text() -> str:

        max_chars = int(request.args.get('max_chars', 0))
        tries = int(request.args.get('tries', 10))
        sentense = chatter.make_sentence(max_chars=max_chars, tries=tries)
        status = 204 if not sentense else 200
        headers = {'Content-Type': 'text/plain'}
        return sentense, status, headers

    app.run(args.host, args.port)


def _version(args: argparse.Namespace) -> None:

    print(VERSION)


def main() -> None:

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='sub-command')

    def add_common_sub_command_arguments(_parser: argparse.ArgumentParser):
        _parser.add_argument('-d', '--no-divider',  action='store_true',
                             help='join words without spaces')
        _parser.add_argument('-l', '--new-line', action='store_true',
                             help='files are in new-line text format')
        _parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), nargs='+',
                             help='text file(s) to learn')

    _parser =  subparsers.add_parser('run', help='output one sentense')
    _parser.set_defaults(func=_run)
    add_common_sub_command_arguments(_parser)
    _parser.add_argument('-m', '--max-chars', type=int, default=0,
                        help='Maximum number of characters [%(default)s]')
    _parser.add_argument('-t', '--tries', type=int, default=10,
                        help='Maximum times to make a sentence [%(default)s]')

    _parser = subparsers.add_parser('server', help='run as a Web API server')
    _parser.set_defaults(func=_server)
    add_common_sub_command_arguments(_parser)
    _parser.add_argument('-o', '--host', default='0.0.0.0',
                         help='server host [%(default)s]')
    _parser.add_argument('-p', '--port', type=int, default=8080,
                         help='listen port number [%(default)d]')

    _parser = subparsers.add_parser('version', help='show version and exit')
    _parser.set_defaults(func=_version)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
