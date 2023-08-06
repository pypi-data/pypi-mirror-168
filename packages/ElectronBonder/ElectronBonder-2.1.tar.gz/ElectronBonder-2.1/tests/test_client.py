import json
import unittest
from unittest.mock import Mock, patch

from electronbonder.client import ElectronBond, ElectronBondAuthError

BASEURL = "http://localhost:8007"
OAUTH_BASEURL = "https://awscognito.com"
OAUTH_CLIENT_ID = "123456789"
OAUTH_CLIENT_SECRET = "987654321"
PATH = "custom/path"


class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = ElectronBond(
            baseurl=BASEURL,
            username="username",
            password="password",
            oauth_client_baseurl=OAUTH_BASEURL,
            oauth_client_id=OAUTH_CLIENT_ID,
            oauth_client_secret=OAUTH_CLIENT_SECRET)

    @patch("requests.Session.post")
    def test_authorize(self, mock_post):
        token = "token_value"
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = json.dumps({"token": token})
        resp = self.client.authorize()
        mock_post.return_value.status_code = 201
        resp = self.client.authorize()
        self.assertEqual(token, resp)
        with self.assertRaises(ElectronBondAuthError):
            mock_post.return_value.status_code = 404
            self.client.authorize()

    @patch("requests_oauthlib.OAuth2Session.fetch_token")
    def test_authorize_oauth(self, mock_token):
        token = "12345"
        mock_token.return_value = {"access_token": token}
        self.client.authorize_oauth()
        self.assertEqual(
            self.client.session.headers["Authorization"],
            f"Bearer {token}")
        mock_token.assert_called_with(
            token_url=f"{OAUTH_BASEURL}/oauth2/token",
            client_id=OAUTH_CLIENT_ID,
            client_secret=OAUTH_CLIENT_SECRET)

    @patch("requests.Session.get")
    def test_get_paged(self, mock_get):
        list(self.client.get_paged(PATH))
        mock_get.assert_called_once()
        mock_get.assert_called_with(
            '{}/{}'.format(BASEURL, PATH), params={'page': 1})
        mock_get.reset_mock()

        list(self.client.get_paged(PATH, params={"page": 4}))
        mock_get.assert_called_once()
        mock_get.assert_called_with(
            '{}/{}'.format(BASEURL, PATH), params={'page': 4})

        expected_results = {"foo": "bar"}
        results_mock = Mock()
        results_mock.side_effect = [
            {"results": [expected_results], "next": True},
            {"results": [expected_results], "next": False}]
        mock_get.return_value.json = results_mock
        results = list(self.client.get_paged(PATH))
        self.assertEqual(results, [expected_results, expected_results])
        mock_get.reset_mock()
