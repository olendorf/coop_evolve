#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Console script for coop_evolve."""
import sys
import click
from coop_evolve.reporter import Reporter

@click.group(invoke_without_command=True)
@click.option('-o', '--output-directory')
def main(output_directory):
    """Console script for coop_evolve."""
    click.echo("Replace this message by putting your code into "
               "coop_evolve.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    click.echo(output_directory)
    return 0


if __name__ == '__main__':  # pragma: no cover
    main()

@main.command()
def report():
    click.echo("I'm reporting")
    reporter = Reporter()
    reporter.generate()
    return 0