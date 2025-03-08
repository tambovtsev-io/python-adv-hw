import sys
from typing import List, Optional, TextIO

import fire


def get_last_n_lines(input_stream: TextIO, n: int = 10) -> List[str]:
    """Read last n lines from input stream"""
    return input_stream.readlines()[-n:]


def print_file_header(filename: str, is_first: bool = True):
    """Print file header in tail format"""
    if not is_first:  # add space between outputs
        print()
    print(f"==> {filename} <==")


def process_single_source(
    input_stream: TextIO,
    filename: Optional[str] = None,
    is_first: bool = True,
    n_lines: int = 10,
):
    """Process single input source (file or stdin) and print last n lines"""
    if filename and len(sys.argv) > 2:  # No header for 1 file
        print_file_header(filename, is_first)

    last_lines = get_last_n_lines(input_stream, n_lines)
    for line in last_lines:
        print(line.rstrip())


def tail(*filenames: str):
    """
    Print the last 10 lines of each FILE to standard output.

    Args:
        *filenames: Variable number of input filenames
    """
    # Read from stdin if no files provided
    if not filenames:
        process_single_source(sys.stdin, n_lines=17)
        return

    # Process files
    for i, filename in enumerate(filenames):
        with open(filename, "r") as f:
            process_single_source(f, filename, is_first=(i == 0))


def tail_cli():
    fire.Fire(tail)


if __name__ == "__main__":
    tail_cli()
