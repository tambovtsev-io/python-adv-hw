import sys
from typing import Optional, TextIO

import fire


def print_number_lines(input_stream: TextIO):
    """Read lines from input stream and print them numbered"""
    for i, line in enumerate(input_stream):
        print(f"{i+1:6d}\t{line.rstrip()}")


def nl(filename: Optional[str] = None):
    """
    Write each FILE to standard output, with line numbers added.

    Args:
        filename: Optional path to input file. If None, reads from stdin
    """
    if filename:
        with open(filename, "r") as f:
            print_number_lines(f)
    else:
        print_number_lines(sys.stdin)


def nl_cli():
    fire.Fire(nl)


if __name__ == "__main__":
    nl_cli()
