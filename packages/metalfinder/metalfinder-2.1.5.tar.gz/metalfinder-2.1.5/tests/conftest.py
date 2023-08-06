#!/usr/bin/python3

"""Pytest fixtures to simplify tests"""

import pytest


@pytest.fixture
def cachedir(tmp_path):
    """Create temporary dir named 'cachedir'"""
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    return cache_dir


@pytest.fixture
def outdir(tmp_path):
    """Create temporary dir named 'outdir'"""
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    return out_dir


@pytest.fixture
def musicdir(tmp_path):
    """Create temporary dir named 'musicdir'"""
    music_dir = tmp_path / "music"
    music_dir.mkdir()
    return music_dir
