import ast
import sys
import argparse
from typing import Set, List

from singlue import __version__
from pathlib import Path
from typing import Optional


def resolve_fn_or_cls(name: str, src_ast: ast.Module) -> Optional[ast.stmt]:
    found_fn_or_cls = next(
        filter(lambda x: getattr(x, "name", None) == name, src_ast.body), None
    )
    return found_fn_or_cls


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="file to glue")
    parser.add_argument(
        "-s",
        "--show_before",
        default=False,
        action="store_true",
        help="output source (before integrating) to standard error",
    )

    parser.add_argument(
        "-v",
        "--version",
        version=__version__,
        action="version",
        help="display singlue version",
    )
    return parser.parse_args()


def run(res: ast.Module, source: str):
    import_sentences_in_library: Set[str] = set()
    found_fn_or_cls_list: List[str] = []
    non_import_sentences_in_main: List[str] = []
    for stmt in res.body:
        if isinstance(stmt, ast.ImportFrom):
            if not Path(source).parent.joinpath(f"{stmt.module}.py").exists():
                non_import_sentences_in_main.append(ast.unparse(stmt))
                # expects standard or third-party library (Example:`from math import sin`)
                continue
            # TODO replace import part to resolved code
            for func_or_cls in stmt.names:
                with open(Path(source).parent / f"{stmt.module}.py") as f:
                    res = ast.parse(source=f.read())
                    import_sentences_in_library |= set(
                        map(
                            ast.unparse,
                            filter(
                                lambda x: isinstance(x, (ast.ImportFrom, ast.Import)),
                                res.body,
                            ),
                        )
                    )
                    found_fn_or_cls = resolve_fn_or_cls(func_or_cls.name, res)
                    if found_fn_or_cls:
                        found_fn_or_cls_list.append(ast.unparse(found_fn_or_cls))
                    else:
                        raise RuntimeError(f"cannot find {func_or_cls.name}")
        else:
            non_import_sentences_in_main.append(ast.unparse(stmt))
    # TODO resolve,duplicate import
    for s in import_sentences_in_library:
        print(s)  # contains unused imports
    for s in found_fn_or_cls_list:
        print(s)
    for s in non_import_sentences_in_main:
        print(s)


def main():
    args = parse_args()
    assert Path(args.source).exists()
    with open(Path(args.source)) as f:
        res = ast.parse(source=f.read())

    if args.show_before:
        print("====================================", file=sys.stderr)
        for stmt in res.body:
            print(ast.unparse(stmt), file=sys.stderr)
        print("====================================", file=sys.stderr)

    run(res, args.source)


if __name__ == "__main__":
    main()
