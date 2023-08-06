import os

import click


def run__(cmd):
    print_cmd_step__(cmd)
    os.system(cmd)


def is_git_root__():
    """Is git root directory?"""
    return os.path.exists('.git')


def print_cmd_step__(cmd):
    print_step__(cmd, 'blue')


def print_step__(step, color):
    click.echo(click.style('>> ' + step, fg=color))
