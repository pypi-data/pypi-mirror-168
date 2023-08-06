# coding: utf-8

import click
import os
import sys
import shutil
from itertools import chain
from pathlib import Path


ALL_FILES_GLOBS = ('*',)


@click.command()
@click.argument('src')
@click.argument('dst')
@click.option('globs', '--glob', '-g', default=ALL_FILES_GLOBS, help='File pattern(s) to include', multiple=True)
def lner(src, dst, globs):
    """Recursively create hard links to files in another directory."""
    src = Path(src).resolve()
    dst = Path(dst).resolve()
    dst = dst.joinpath(dst, src.name)
    if dst.exists():
        click.echo("Error: destination folder already exists!")
        sys.exit(1)
    dst.mkdir(parents=True, exist_ok=True)
    for file in recursively_iterdir(src, globs=globs):
        dst.joinpath(file.relative_to(src)).parent.mkdir(parents=True, exist_ok=True)
        os.link(
            file,
            dst.joinpath(file.relative_to(src))
        )


@click.command()
@click.argument('src')
def unlner(src):
    """Remove hardlinks from a directory."""
    src = Path(src).resolve()
    for entry in recursively_iterdir(src, globs=ALL_FILES_GLOBS):
        if entry.stat().st_nlink > 1:
            os.unlink(entry)
    for directory in (d for d in src.iterdir() if d.is_dir()):
        shutil.rmtree(directory)
    shutil.rmtree(src)


def recursively_iterdir(path, globs):
    """Iterate over files, exclusively, in path and its sub directories."""
    path = Path(path)
    if tuple(globs) == ALL_FILES_GLOBS:
        files_iter = path.iterdir()
    else:
        files_iter = chain(*[
            path.rglob(g)
            for g in globs
        ])
    for item in files_iter:
        if item.name.startswith("."):
            continue
        elif item.is_dir():
            yield from recursively_iterdir(item, globs)
        else:
            yield item

