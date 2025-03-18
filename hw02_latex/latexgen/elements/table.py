from functools import reduce, wraps
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


def escape_latex(text: str) -> str:
    """Function to escape Latex special characters"""
    replacements = [
        ("_", "\\_"),
        ("%", "\\%"),
        ("&", "\\&"),
        ("#", "\\#"),
    ]
    return reduce(lambda s, kv: s.replace(kv[0], kv[1]), replacements, str(text))


def format_row(row: List[Any]) -> str:
    """Pure function to format a single row"""
    return " & ".join(map(escape_latex, row)) + " \\\\"


def generate_tabular(data: DATA_TYPE, alignment: Literal["c", "l", "r"] = "c") -> str:
    """Pure function to generate tabular environment"""

    if not data or not data[0]:
        return ""

    n_columns = len(data[0])
    header_col_spec = f"|{'|'.join(alignment * n_columns)}|"
    header = f"\\begin{{tabular}}{{{header_col_spec}}}"
    content = "\n\\hline\n".join(map(format_row, data))
    return f"{header}\n\\hline\n{content}\n\\hline\n\\end{{tabular}}"
