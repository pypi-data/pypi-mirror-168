#!/usr/bin/python3

"""Test the functions in metalfinder.cli"""

import logging
import os

from unittest import mock
from datetime import date, timedelta
from pathlib import Path

import pytest

from metalfinder.cli import output_choices, date_lint, dir_lint, parse_args
from metalfinder import __version__


def test_output_choices_ok(outdir):
    """Test output_choices() when path is valid"""
    choices = { 'text': str(outdir) + '/test.txt',
                'json': str(outdir) + '/test.json',
                'atom': str(outdir) + '/test.atom' }
    for _, value in choices.items():
        assert output_choices(value) == value


def test_output_choices_invalid_extension():
    """Test output_choices() errors when file extension is invalid"""
    with pytest.raises(SystemExit):
        assert output_choices('foo.notvalid')


def test_output_choices_invalid_path():
    """Test output_choices() errors when path is invalid"""
    with pytest.raises(SystemExit):
        assert output_choices('/asdkaskdm/kmasdkmD/foo.txt')


# date_lint()
def test_date_lint_ok():
    """Test date_lint() for valid ISO 8601 input"""
    assert date_lint('2100-01-01') == '2100-01-01'


def test_date_lint_not_iso_8601():
    """Test date_lint() errors when input is not ISO 8601"""
    with pytest.raises(SystemExit):
        date_lint('21000101')


def test_date_lint_maxdate_too_early():
    """Test date_lint() errors when max_date earlier than today"""
    with pytest.raises(SystemExit):
        yesterday = date.today() - timedelta(days = 1)
        date_lint(str(yesterday))


def test_dir_not_path():
    """Test dir_lint() errors when dir is not a valid"""
    with pytest.raises(SystemExit):
        dir_lint('')


# parse_args()
def test_parser_no_dir(cachedir):
    """Test argparse without --directory"""
    args = parse_args(['-o', 'foo.txt', '-l', 'Montreal', '-b', 'FooBar',
                       '-c', str(cachedir)])
    assert args.directory is None
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'FooBar'
    assert args.cache_dir == str(cachedir)


def test_parser_no_output(cachedir, outdir):
    """Test argparse without --output"""
    with pytest.raises(SystemExit):
        _args = parse_args(['-d', str(outdir), '-l', 'Montreal', '-b', 'FooBar',
                            '-c', str(cachedir)])


def test_parser_no_location(cachedir, outdir):
    """Test argparse without --location"""
    with pytest.raises(SystemExit):
        _args = parse_args(['-d', str(outdir), '-l', 'Montreal', '-b', 'FooBar',
                            '-c', str(cachedir)])


@mock.patch.dict(os.environ, {'METALFINDER_BIT_APPID': 'FooBar'})
def test_parser_api_with_env(cachedir, outdir):
    """Test argparse with --bit_appid and METALFINDER_BIT_APPID"""
    args = parse_args(['-d', str(outdir), '-o', 'foo.txt', '-l', 'Montreal',
                       '-b', 'NonDefault', '-c', str(cachedir)])
    assert args.directory == str(outdir)
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'NonDefault'
    assert args.cache_dir == str(cachedir)


def test_parser_api_no_env(cachedir, outdir):
    """Test argparse with --bit_appid, without METALFINDER_BIT_APPID"""
    args = parse_args(['-d', str(outdir), '-o', 'foo.txt', '-l', 'Montreal',
                       '-b', 'FooBar', '-c', str(cachedir)])
    assert args.directory == str(outdir)
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'FooBar'
    assert args.cache_dir == str(cachedir)


@mock.patch.dict(os.environ, {'METALFINDER_BIT_APPID': 'FooBar'})
def test_parser_no_api_with_env(cachedir, outdir):
    """Test argparse without --bit_appid, with METALFINDER_BIT_APPID"""
    args = parse_args(['-d', str(outdir), '-o', 'foo.txt', '-l', 'Montreal',
                       '-c', str(cachedir)])
    assert args.directory == str(outdir)
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'FooBar'
    assert args.cache_dir == str(cachedir)


def test_parser_no_api_no_env(cachedir, outdir):
    """Test argparse without --bit_appid and METALFINDER_BIT_APPID"""
    with pytest.raises(SystemExit):
        _args = parse_args(['-d', str(outdir), '-l', 'Montreal', '-b', 'FooBar',
                            '-c', str(cachedir)])


def test_parse_cache_default(cachedir, outdir, monkeypatch):
    """Test argparse with default cache"""
    def mockreturn():
        return cachedir
    monkeypatch.setattr(Path, "home", mockreturn)
    args = parse_args(['-d', str(outdir), '-o', 'foo.txt', '-l', 'Montreal',
                       '-b', 'FooBar'])
    assert args.directory == str(outdir)
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'FooBar'
    assert args.cache_dir == str(cachedir) + '/.cache/metalfinder'


def test_parser_cache_non_default(cachedir, outdir):
    """Test argparse with cli non-default cache"""
    args = parse_args(['-d', str(outdir), '-o', 'foo.txt', '-l', 'Montreal',
                       '-b', 'FooBar', '-c', str(cachedir)])
    assert args.directory == str(outdir)
    assert args.output == 'foo.txt'
    assert args.location == 'Montreal'
    assert args.bit_appid == 'FooBar'
    assert args.cache_dir == str(cachedir)


def test_parser_verbose_default():
    """Test argpase with default log level"""
    _args = parse_args(['-o', 'foo.txt', '-l', 'Montreal', '-b', 'FooBar'])
    assert logging.getLogger().getEffectiveLevel() == logging.WARNING


def test_parser_verbose_debug():
    """Test argpase with info log level"""
    _args = parse_args(['-o', 'foo.txt', '-l', 'Montreal', '-b', 'FooBar',
                        '--verbose'])
    assert logging.root.getEffectiveLevel() == logging.INFO


# This test cannot be done using pytest.raises(Foo), as it will exit after
# catching the exception, thus not letting us test the captured stdout.
def test_parser_version(capsys):
    """Test argparse --version outputs the right version number"""
    try:
        _args = parse_args(['--version'])
    except SystemExit:
        out, _err = capsys.readouterr()
        assert out.rstrip() == "metalfinder " + __version__
