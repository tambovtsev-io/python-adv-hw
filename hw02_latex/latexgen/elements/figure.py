from functools import wraps
from typing import Callable


def latex_figure_env(func: Callable) -> Callable:
    """Decorator for Latex figure environment"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return "\n".join(
            [
                "\\begin{figure}[h]",
                "\\centering",
                func(*args, **kwargs),
                "\\end{figure}",
            ]
        )

    return wrapper


@latex_figure_env
def generate_latex_figure(
    fname: str, relative_width: float = 0.8, caption: str = "Sample Image"
) -> str:
    """Generate LaTeX image inclusion code."""
    width = f"{relative_width}\\textwidth"
    lines = [
        f"\\includegraphics[width={width}]{{{fname}}}",
        f"\\caption{{{caption}}}",
    ]

    return "\n".join(lines)
