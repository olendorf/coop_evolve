#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `coop_evolve` package."""

import os
import pytest

from app_settings import AppSettings

from click.testing import CliRunner

from coop_evolve import coop_evolve
from coop_evolve import cli


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'coop_evolve.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output
    
def test_reporter_cli():
    runner = CliRunner()
    result = runner.invoke(cli.main, ['report'])
    assert result.exit_code == 0
    assert "reporting" in result.output
    cfg = AppSettings()
    try:
        os.system('rm -rf ' + cfg.report_directory)
    except:
        pass
