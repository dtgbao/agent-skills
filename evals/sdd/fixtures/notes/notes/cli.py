import argparse
from pathlib import Path

from notes.repo import NoteRepo


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="notes")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("title")
    add.add_argument("body")
    sub.add_parser("list")
    args = parser.parse_args(argv)

    repo = NoteRepo(Path("notes.json"))
    if args.cmd == "add":
        print(repo.add(args.title, args.body).id)
    elif args.cmd == "list":
        for n in repo.all():
            print(f"{n.id}\t{n.title}")
    return 0
