#!/usr/bin/python3

# Copyright 2015-2018 by Chris Forrette
# Copyright 2022 by Louis-Philippe Véronneau
#
# This file was originally part of python-bandsintown.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Test the functions in metalfinder.api.bandsintown"""

from unittest import TestCase, mock

import metalfinder.api.bandsintown as mab


def test_init_stores_properties():
    """Test properties are stored properly"""
    app_id = 1234
    client = mab.Client(app_id)

    assert client.api_base_url == 'https://rest.bandsintown.com'
    assert client.app_id == app_id
    assert client.default_params == {'app_id': app_id}


@mock.patch('requests.get')
class RequestTestCase(TestCase):
    """Series of tests for Client.request()"""
    def test_builds_and_executes_request(self, mock_requests_get):
        """Test request() returns expected values"""
        mock_result = {'name': 'Bad Religion'}
        mock_response = mock.MagicMock()
        mock_response.json.return_value = mock_result
        mock_requests_get.return_value = mock_response

        app_id = 5678
        client = mab.Client(app_id)
        result = client.request('things')
        url = client.api_base_url + '/things'
        mock_requests_get.assert_called_with(
            url,
            headers={'Accept': 'application/json'},
            params=client.default_params
        )
        self.assertEqual(mock_result, result)

    def test_merges_passed_in_params(self, mock_requests_get): #pylint: disable=R0201
        """Test request() accepts extra parameters"""
        app_id = 5678
        date = '2018-01-01'
        client = mab.Client(app_id)
        client.request('more/things', {'date': date})
        url = client.api_base_url + '/more/things'
        mock_requests_get.assert_called_with(
            url,
            headers={'Accept': 'application/json'},
            params={
                'app_id': app_id,
                'date': date
            }
        )

    def test_raises_error_for_bad_api_key(self, mock_requests_get):
        """Test request() raises error when app ID is invalid"""
        invalid_appid_message = ('User is not authorized to access this '
                                 'resource with an explicit deny')
        mock_result = {'Message': invalid_appid_message}
        mock_response = mock.MagicMock()
        mock_response.json.return_value = mock_result
        mock_requests_get.return_value = mock_response

        client = mab.Client('')

        with self.assertRaises(mab.BandsintownInvalidAppIdError):
            client.request('stuff')


@mock.patch.object(mab.Client, 'request')
class EventsTestCase(TestCase):
    """Series of tests for Client.artist_events()"""
    def test_requests_artist_events(self, mock_requests_get):
        """Test artist_events() returns expected values"""
        data = [
            {
                'id': '20590797',
                'datetime': '2018-05-04T13:00:00'
            },
            {
                'id': '21752009',
                'datetime': '2018-05-05T19:00:00'
            }
        ]
        mock_requests_get.return_value = data

        client = mab.Client('my-app-id')
        artist = 'Every Time I Die'
        result = client.artists_events(artist)

        mock_requests_get.assert_called_with('artists/Every%20Time%20I%20Die/events', {})
        self.assertEqual(result, data)

    def test_takes_date_param(self, mock_requests_get):
        """Test artist_events() can accept a date range"""
        data = [{'id': '1234'}]
        mock_requests_get.return_value = data

        client = mab.Client('my-app-id')
        artist = 'Every Time I Die'
        date = '2018-01-15,2018-02-15'
        result = client.artists_events(artist, date)

        mock_requests_get.assert_called_with(
            'artists/Every%20Time%20I%20Die/events',
            {'date': date}
        )
        self.assertEqual(result, data)

    def test_returns_none_when_artist_not_found(self, mock_requests_get):
        """Test artist_events() returns None when no artist is found"""
        mock_requests_get.return_value = {'errorMessage': '[NotFound] The artist was not found'}
        client = mab.Client('my-app-id')
        self.assertIsNone(client.artists_events('foo'))

    def test_returns_none_when_no_events_found(self, mock_requests_get):
        """Test artist_events() returns None when no event is found"""
        mock_requests_get.return_value = []
        client = mab.Client('my-app-id')
        self.assertEqual(client.artists_events('bar'), [])
