import os
from functools import wraps
from pathlib import Path
from typing import Callable, List, Union

from .elements.figure import generate_latex_figure
from .elements.table import generate_tabular, latex_table_env

DATA_TYPE = List[List[Union[str, int, float]]]
PROJECT_ROOT = Path(os.getcwd())


def latex_document(func: Callable) -> Callable:
    """Decorator for Latex document structure"""

    images_path = (PROJECT_ROOT / "images").resolve()
    @wraps(func)
    def wrapper(*args, **kwargs) -> str:
        return "\n".join(
            [
                "\\documentclass{article}",
                "\\usepackage{graphicx}",
                f"\\graphicspath{{ {{{images_path}}} }}",
                "\\begin{document}",
                func(*args, **kwargs),
                "\\end{document}\n",
            ]
        )

    return wrapper


@latex_document
@latex_table_env
def generate_latex_table(data: DATA_TYPE) -> str:
    """Generate Latex table code from a 2D list"""
    return generate_tabular(data)


@latex_document
def generate_document_with_content(*contents: str) -> str:
    """Generate a complete Latex document with multiple content elements."""
    return "\n\n".join(contents)


def write_file(fpath: Path, content: str) -> None:
    with open(fpath, "w") as f:
        f.write(content)


def latex2pdf(fpath: Path, out_dir: Path) -> None:
    options = " ".join(
        [f"-output-directory={out_dir.resolve()}", "-interaction=nonstopmode"]
    )
    command = f"pdflatex {options} {fpath.resolve()} "
    print(command)
    os.system(command)


def main():
    data = [
        ["Name", "Age", "City"],
        ["Andrew", 21, "Moscow"],
        ["Alex", 20, "Saint-Petersburg"],
        ["Jane", 22, "Ufa"],
    ]

    # Setup artifacts dirs
    artifacts_dir = PROJECT_ROOT / "artifacts"
    tex_dir = artifacts_dir / "tex"
    tex_dir.mkdir(parents=True, exist_ok=True)

    pdf_dir = artifacts_dir / "pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Generate latex for table
    latex_code_table_document = generate_latex_table(data)
    print(f"Latex for table only:\n\n{latex_code_table_document}\n=============\n")

    write_file(tex_dir / "sample_table.tex", latex_code_table_document)

    # Generate latex for figure and table
    latex_code_table = generate_tabular(data)
    latex_code_figure = generate_latex_figure("cat_ballet.png", caption="Cat Ballet")

    # Generate latex for table and figure
    latex_code_table_figure = generate_document_with_content(
        "\\section{Table}",
        latex_code_table,
        "\\section{Image}",
        latex_code_figure,
    )

    print(f"Latex for table and figure:\n\n{latex_code_table_figure}\n=============\n")
    write_file(tex_dir / "sample_table_figure.tex", latex_code_table_figure)

    # Convert to pdfs
    for fpath in tex_dir.glob("*.tex"):
        print(fpath)
        latex2pdf(fpath, pdf_dir)


if __name__ == "__main__":
    main()
