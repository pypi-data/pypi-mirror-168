import click

from ppcmd import ppc
from ppcmd.ppc.ppc_processor import PpcProcessor

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

processor = PpcProcessor()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(ppc.__version__)
def cli():
    """Pico Python Command"""


@cli.command()
def update():
    """Update ppc command."""
    processor.update()


@cli.command()
def test():
    """Run unit test."""
    processor.test()


@cli.command()
def cov():
    """Run coverage report."""
    processor.coverage()


@cli.command()
def lint():
    """Run lint report."""
    processor.lint()
