from functools import wraps
from typing import Any, Callable, List, Literal, Union

DATA_TYPE = List[List[Union[str, int, float]]]


def latex_table_env(func: Callable) -> Callable:
    """Decorator for Latex table environment"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return "\n".join(
            [
                "\\begin{table}[h]",
                "\\centering",
                func(*args, **kwargs),
                "\\caption{Sample Table}",
                "\\end{table}",
            ]
        )

    return wrapper


def format_row(row: List[Any]) -> str:
    """Function to format a single row"""
    return " & ".join(map(str, row)) + " \\\\"


def generate_tabular(data: DATA_TYPE, alignment: Literal["c", "l", "r"] = "c") -> str:
    """Function to generate tabular environment"""

    if not data or not data[0]:
        return ""

    n_columns = len(data[0])
    header_col_spec = f"|{'|'.join(alignment * n_columns)}|"
    header = f"\\begin{{tabular}}{{{header_col_spec}}}"
    content = "\n\\hline\n".join(map(format_row, data))
    return f"{header}\n\\hline\n{content}\n\\hline\n\\end{{tabular}}"
