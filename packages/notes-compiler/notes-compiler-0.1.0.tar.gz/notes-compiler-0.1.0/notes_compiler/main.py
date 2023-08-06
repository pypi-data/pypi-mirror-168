import argparse
from typing import Dict, List
from pathlib import Path
import markdown
import importlib.resources
from functools import reduce
from markdown_katex import KatexExtension
import os
import os.path


def compile_dir(input_dir: str) -> Dict:
    result = dict()
    for entry in os.scandir(input_dir):
        stem = Path(entry.path).stem
        if entry.is_dir():
            result[stem] = compile_dir(entry.path)
        elif entry.is_file() and entry.name.endswith(".md"):
            with open(entry.path, "r") as file:
                result[stem] = file.read()
    return result


def build_output(compiled: Dict, output_path: str):
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    with open(f"{output_path}/index.html", "w") as f:
        f.write(
            make_html_file(body=toc(compiled, []), name="table_of_contents", prefix=[])
        )
    make_output_dir(compiled, output_path, prefix=[])


def make_output_dir(compiled: Dict, output_path: str, prefix: List[str]):
    full_path = f"{output_path}/{get_path_from_prefix(prefix)}"
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    for name, item in compiled.items():
        if isinstance(item, dict):
            make_output_dir(
                compiled=item, output_path=output_path, prefix=prefix + [name]
            )
        elif isinstance(item, str):
            with open(
                f"{output_path}/{get_path_from_prefix(prefix)}/{name}.html", "w"
            ) as f:
                f.write(
                    make_html_file(
                        body=compile_markdown(item), name=name, prefix=prefix
                    )
                )


def get_path_from_prefix(prefix: List[str]):
    if len(prefix) == 0:
        return ""
    return reduce(lambda a, b: f"{a}/{b}", prefix)


def make_html_file(
    body: str,
    name: str,
    prefix: List[str],
) -> str:
    def key(name: str) -> str:
        return f"<!--###{name}###-->"

    outer = importlib.resources.read_text("notes_compiler", "outer.html")
    return outer.replace(key("body"), body)


def compile_markdown(md: str) -> str:
    return markdown.markdown(md, tab_length=2, extensions=[KatexExtension()])


def toc(compiled: Dict, prefix: List[str]) -> str:
    def make_toc(compiled: Dict, prefix: List[str]) -> str:
        if len(prefix) == 0:
            toc_str = ""
        else:
            toc_str = "<ul>\n"
        for name, item in compiled.items():
            if isinstance(item, dict):
                if len(prefix) == 0:
                    toc_str += f"<h2>{snake_case_to_title_case(name)}</h2>\n{make_toc(item, prefix=prefix + [name])}"
                else:
                    toc_str += f"<li>{snake_case_to_title_case(name)}\n{make_toc(item, prefix=prefix + [name])}</li>"
            elif isinstance(item, str):
                toc_str += f'<li><a href="{get_path_from_prefix(prefix)}/{name}.html">{snake_case_to_title_case(name)}</a></li>\n'
        if len(prefix) == 0:
            toc_str += ""
        else:
            toc_str += "</ul>"
        return toc_str

    toc_str = "<h1>Table of Contents</h1>\n" + make_toc(compiled, prefix)

    return toc_str


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", type=str, default="./src")
    parser.add_argument("output_path", type=str, default="./public")
    args = parser.parse_args()
    build_output(compile_dir(args.input_path), args.output_path)


def snake_case_to_title_case(snake_case: str) -> str:
    return snake_case.replace("_", " ").capitalize()


def get_output_name(input_name: str) -> str:
    return input_name.removesuffix(".md") + ".html"
