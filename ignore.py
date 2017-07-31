import os
import sys
import traceback

from jasily.cli import EngineBuilder

builder = EngineBuilder()

@builder.command
def equals(value: str):
    for line in sys.stdin.read().splitlines():
        if line != value:
            print(line)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        if sys.stdin.isatty():
            print('you must call this script use pipe.')
        else:
            builder.build().execute(argv)
    except Exception:
        traceback.print_exc()
        input()

if __name__ == '__main__':
    main()
