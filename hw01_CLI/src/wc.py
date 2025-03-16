import sys
from dataclasses import dataclass
from typing import List, Optional, TextIO

import fire


@dataclass
class FileStats:
    lines: int
    words: int
    bytes: int
    filename: Optional[str] = None

    def __str__(self) -> str:
        """Format stats as wc output row"""
        parts = [f"{self.lines:4d}", f"{self.words:4d}", f"{self.bytes:4d}"]
        if self.filename:
            parts.append(self.filename)
        return " ".join(parts)


def count_stats(input_stream: TextIO) -> FileStats:
    """Count lines, words and bytes in input stream"""
    content = input_stream.read()
    return FileStats(
        lines=content.count("\n"),
        words=len(content.split()),
        bytes=len(content.encode()),
    )


def sum_stats(stats_list: List[FileStats]) -> FileStats:
    """Calculate total statistics for list of files"""
    return FileStats(
        lines=sum(s.lines for s in stats_list),
        words=sum(s.words for s in stats_list),
        bytes=sum(s.bytes for s in stats_list),
        filename="total",
    )


def wc(*filenames: str):
    """
    Print newline, word, and byte counts for each FILE,
    and a total line if more than one FILE is specified.

    Args:
        *filenames: Variable number of input filenames
    """
    # Read from stdin if no files provided
    if not filenames:
        stats = count_stats(sys.stdin)
        print(stats)
        return

    # Process input files
    all_stats = []
    for filename in filenames:
        with open(filename, "r") as f:
            stats = count_stats(f)
            stats.filename = filename
            all_stats.append(stats)
            print(stats)

    # Print total if multiple files
    if len(filenames) > 1:
        print(sum_stats(all_stats))


def wc_cli():
    fire.Fire(wc)


if __name__ == "__main__":
    wc_cli()
