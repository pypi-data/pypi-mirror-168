#!/usr/bin/python3

"""Test the functions in metalfinder.concerts"""

import logging
import os
import pickle

from collections import namedtuple

import pytest

import metalfinder.concerts as mfc


def test_has_changed_false():
    """Test has_changed() is False for existing concert"""
    concert = {'id': '102459446', 'title': 'Placeholder'}
    concert_cache = [{'artist_id': '862',
                      'id': '102459446'}]
    concert_is_new = mfc.has_changed(concert_cache, concert)
    assert concert_is_new is False


def test_has_changed_true(caplog):
    """Test has_changed() is True for new concert"""
    concert = {'id': '12345', 'title': 'Placeholder'}
    concert_cache = [{'artist_id': '862',
                      'id': '102459446'}]
    caplog.set_level(logging.INFO)
    concert_is_new = mfc.has_changed(concert_cache, concert)
    assert concert_is_new is True
    for record in caplog.records:
        assert record.levelname == 'INFO'
        assert record.message == 'Concert 12345 is new'


def test_write_concert_cache(cachedir):
    """Test function write_concert_cache()"""
    data = ['1', '2']
    mfc.write_concert_cache(data, str(cachedir))
    concert_cache_file = os.path.join(str(cachedir), 'concert_cache')
    with open(concert_cache_file, 'rb') as _cache:
        concert_cache = pickle.load(_cache)
        assert concert_cache == data


def test_get_concert_cache(cachedir):
    """Test function get_concert_cache()"""
    data = ['1', '2']
    concert_cache_file = os.path.join(str(cachedir), 'concert_cache')
    with open(concert_cache_file, 'wb') as _cache:
        pickle.dump(data, _cache)
    assert data == mfc.get_concert_cache(str(cachedir))


@pytest.mark.parametrize("artist_list, split_artist_list",
    [(['Mark+Spencer', 'Terry/ Berry', 'John &James'],
      ['Mark', 'Spencer', 'Terry', 'Berry', 'John', 'James']),
     (['Napalm Death', 'Arch Enemy'], ['Napalm Death', 'Arch Enemy'])])
def test_query_bit(artist_list, split_artist_list, monkeypatch):
    """Test function query_bit(). We mostly want to test that artists are split properly."""
    def mocked_client(bit_appid):
        return bit_appid
    def mocked_bit_request(artist, concert_list, *args): # pylint: disable=W0613
        concert_list.append(artist)
        return concert_list
    monkeypatch.setattr('metalfinder.api.bandsintown.Client', mocked_client)
    monkeypatch.setattr('metalfinder.concerts.bit_request', mocked_bit_request)
    Args = namedtuple('Args', ['bit_appid', 'max_date'])
    mocked_args = Args('placeholder', 'placeholder')
    assert split_artist_list == mfc.query_bit(artist_list, mocked_args)


def test_filter_location():
    """Test function filter_location()"""
    concert_list = [{'artist_id': '862',
                     'id': '102459446',
                     'venue': {'city': 'Montreal',
                               'other': 'Foobar'}},
                    {'artist_id': '1',
                     'id': '12345',
                     'venue': {'city': 'Oslo',
                               'other': 'Foobar'}}]
    filtered_list = [{'artist_id': '1',
                      'id': '12345',
                      'venue': {'city': 'Oslo',
                                'other': 'Foobar'}}]
    assert filtered_list == mfc.filter_location(concert_list, 'Oslo')
