#!/usr/bin/python3

"""Unit tests for metalfinder.scan"""

import os
import pickle
import logging
import shutil

import pytest

import metalfinder.scan as mfs


NO_ARTIST_ERROR = "<class 'KeyError'>: 'artist'"
NO_HEADER_ERROR = "<class 'mutagen.flac.FLACNoHeaderError'>"


def move_testfile(filename, musicdir):
    """Move a test file from our local test_files dir to a temporary dir
       musicdir', so that the path is reproducible"""
    origfile = os.path.join('tests/test_files', filename)
    destfile = os.path.join(str(musicdir), filename)
    shutil.copyfile(origfile, destfile)
    return destfile


def change_mtime(artist, filename, musicdir):
    """Change the mtime of a test file, so that it's reproducible"""
    destfile = move_testfile(filename, musicdir)
    mtime = int('1111111111')
    os.utime(destfile, (mtime, mtime))
    good_song_cache = {os.path.join(str(musicdir), filename):
            [1111111111.0, artist]}
    return destfile, good_song_cache


@pytest.mark.parametrize("artist, filename",
    [('Arch Enemy', 'arch_enemy.flac'),
     ('Napalm Death', 'napalm_death.flac')])
def test_has_changed_new(artist, filename, musicdir):
    """Test if has_changed() picks up a new song"""
    new_song_cache = {}
    song_cache = {'/home/foo/NOFX/a.flac': [1449768136.0, 'NOFX'],
                  '/home/foo/NOFX/b.flac': [1449768136.0, 'NOFX']}
    destfile, good_song_cache = change_mtime(artist, filename, musicdir)
    new_song_cache, file_changed = mfs.has_changed(song_cache, new_song_cache, destfile)
    assert new_song_cache == good_song_cache
    assert file_changed is True


@pytest.mark.parametrize("artist, filename",
    [('Arch Enemy', 'arch_enemy.flac'),
     ('Napalm Death', 'napalm_death.flac')])
def test_has_changed_old(artist, filename, musicdir):
    """Test if has_changed() skips over a previously cached file"""
    new_song_cache = {}
    destfile, song_cache = change_mtime(artist, filename, musicdir)
    new_song_cache, file_changed = mfs.has_changed(song_cache, new_song_cache, destfile)
    assert new_song_cache == song_cache
    assert file_changed is False


@pytest.mark.parametrize("artist, filepath",
    [('Arch Enemy', 'tests/test_files/arch_enemy.flac'),
     ('Napalm Death', 'tests/test_files/napalm_death.flac')])
def test_get_artist_ok(artist, filepath):
    """Test get_artist() extracts the tag properly"""
    assert artist == mfs.get_artist(None, filepath)


@pytest.mark.parametrize("filepath, error",
    [('tests/test_files/no_artist.flac', NO_ARTIST_ERROR),
     ('tests/test_files/no_header.flac', NO_HEADER_ERROR)])
def test_get_artist_common_errors(filepath, error, caplog):
    """Test get_artist() returns nothing when there is no artist tag"""
    caplog.set_level(logging.WARNING)
    assert mfs.get_artist(None, filepath) is None
    for record in caplog.records:
        assert error in record.args[1]


def test_write_song_cache(cachedir):
    """Test function write_song_cache()"""
    data = ['1', '2']
    mfs.write_song_cache(data, str(cachedir))
    song_cache_file = os.path.join(str(cachedir), 'song_cache')
    with open(song_cache_file, 'rb') as _cache:
        song_cache = pickle.load(_cache)
        assert song_cache == data


def test_get_song_cache(cachedir):
    """Test function get_song_cache()"""
    data = ['1', '2']
    song_cache_file = os.path.join(str(cachedir), 'song_cache')
    with open(song_cache_file, 'wb') as _cache:
        pickle.dump(data, _cache)
    assert data == mfs.get_song_cache(str(cachedir))


def test_write_artist_cache(cachedir):
    """Test function write_artist_cache()"""
    data = ['1', '2']
    mfs.write_artist_cache(data, str(cachedir))
    artist_cache_file = os.path.join(str(cachedir), 'artist_cache')
    with open(artist_cache_file, 'r', encoding='utf-8') as _cache:
        artist_cache = _cache.read()
        assert artist_cache == '1\n2'


def test_get_artist_cache(cachedir):
    """Test function get_artist_cache()"""
    data = '1\n2'
    artist_cache_file = os.path.join(str(cachedir), 'artist_cache')
    with open(artist_cache_file, 'w', encoding='utf-8') as _cache:
        _cache.write(data)
    assert ['1', '2'] == mfs.get_artist_cache(str(cachedir))


@pytest.mark.parametrize("artist, filename",
    [('Arch Enemy', 'arch_enemy.flac'),
     ('Napalm Death', 'napalm_death.flac')])
def test_scan_dir(artist, filename, musicdir):
    """Test function scan_dir()"""
    _, good_song_cache = change_mtime(artist, filename, musicdir)
    artist_list, new_song_cache = mfs.scan_dir(musicdir, '', [])
    assert artist_list == {artist}
    assert new_song_cache == good_song_cache


@pytest.mark.parametrize("artist, filename",
    [('Arch Enemy', 'arch_enemy.flac'),
     ('Napalm Death', 'napalm_death.flac')])
def test_scan_wrapper(artist, filename, cachedir, musicdir):
    """Test wrapper function scan_wrapper()"""
    _ = move_testfile(filename, musicdir)
    artist_list = mfs.scan_wrapper(str(musicdir), str(cachedir))
    assert artist_list == {artist}


def test_issue21(cachedir, tmpdir):
    """Test that we don't crash on broken symlinks"""
    musicdir = tmpdir.join("music")
    musicdir.mkdir()
    musicdir.join("brokensymlink.mp3").mksymlinkto("nonexistent")
    # we don't actually need the result here
    _ = mfs.scan_wrapper(musicdir, cachedir)


def test_issue22(cachedir, musicdir):
    """Test artists are removed from the cache when their files are removed"""
    for filename in ['arch_enemy.flac', 'napalm_death.flac']:
        destfile = move_testfile(filename, musicdir)
    artist_list = mfs.scan_wrapper(str(musicdir), str(cachedir))
    assert artist_list == {'Arch Enemy', 'Napalm Death'}
    os.remove(destfile)
    artist_list = mfs.scan_wrapper(str(musicdir), str(cachedir))
    assert artist_list == {'Arch Enemy'}


def test_issue28(cachedir, musicdir, caplog):
    """Test metalfinder continues running if a file passed through get_artist()
       raises an exception"""
    caplog.set_level(logging.WARNING)
    for filename in ['no_header.flac', 'no_artist.flac', 'arch_enemy.flac']:
        _ = move_testfile(filename, musicdir)
    artist_list = mfs.scan_wrapper(str(musicdir), str(cachedir))
    assert artist_list == {'Arch Enemy'}
    assert NO_ARTIST_ERROR in caplog.records[0].args[1]
    assert NO_HEADER_ERROR in caplog.records[1].args[1]
