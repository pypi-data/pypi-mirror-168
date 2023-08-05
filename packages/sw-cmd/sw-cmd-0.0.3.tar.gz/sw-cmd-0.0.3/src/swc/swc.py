import click

from swc.swc_processor import SwcProcessor

__version__ = '0.0.3'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

processor = SwcProcessor()


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__)
def cli():
    """stopwatch command"""


@cli.command()
def start():
    processor.start(2)
