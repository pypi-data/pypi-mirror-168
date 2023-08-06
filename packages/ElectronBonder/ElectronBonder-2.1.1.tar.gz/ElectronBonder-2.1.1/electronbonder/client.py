import json
from urllib.parse import urlparse

from oauthlib.oauth2 import BackendApplicationClient
from requests import Session
from requests.adapters import HTTPAdapter
from requests_oauthlib import OAuth2Session
from six import add_metaclass
from urllib3.util.retry import Retry


class ElectronBondAuthError(Exception):
    pass


class ElectronBondReturnError(Exception):
    pass


def http_meth_factory(meth):
    """Utility method for producing HTTP proxy methods for ElectronBondProxyMethods mixin class.

    Urls are prefixed with the baseurl defined
    """

    def http_method(self, url, *args, **kwargs):
        url = urlparse(url)
        full_url = "/".join([self.config["baseurl"].rstrip("/"),
                             url.path.lstrip("/")])
        result = getattr(self.session, meth)(full_url, *args, **kwargs)
        return result
    return http_method


def retry_session(retries, session=None, backoff_factor=0.3,
                  status_forcelist=(500, 502, 503, 504)):
    session = session or Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


class ElectronBondProxyMethods(type):
    """Metaclass to set up proxy methods for all requests-supported HTTP methods"""
    def __init__(cls, name, parents, dct):

        for meth in ("get", "post", "head", "patch",
                     "put", "delete", "options",):
            fn = http_meth_factory(meth)
            fn.__name__ = meth
            fn.__doc__ = """Proxied :meth:`requests.Session.{}` method from :class:`requests.Session`""".format(
                meth)

            setattr(cls, meth, fn)


@add_metaclass(ElectronBondProxyMethods)
class ElectronBond(object):
    """ElectronBonder Web Client"""

    def __init__(self, **config):
        self.config = {}
        self.config.update(config)

        if not hasattr(self, "session"):
            self.session = retry_session(retries=5)
        self.session.headers.update({"Accept": "application/json",
                                     "User-Agent": "ElectronBond/0.1"})

    def authorize(self):
        """Authorizes the client against the configured microservice instance."""

        resp = self.session.post(
            "/".join([self.config["baseurl"].rstrip("/"), "get-token/"]),
            data={"password": self.config["password"], "username": self.config["username"]})

        if resp.status_code not in [200, 201]:
            raise ElectronBondAuthError(
                "Failed to authorize with status: {}".format(
                    resp.status_code))
        else:
            session_token = json.loads(resp.text)["token"]
            self.session.headers["Authorization"] = "Bearer {}".format(
                session_token)
            return session_token

    def authorize_oauth(self):
        """Authorizes the client using a configured OAuth provider."""
        try:
            client = BackendApplicationClient(
                client_id=self.config["oauth_client_id"])
            oauth = OAuth2Session(client=client)
            token = oauth.fetch_token(
                token_url=f"{self.config['oauth_client_baseurl']}/oauth2/token",
                client_id=self.config["oauth_client_id"],
                client_secret=self.config["oauth_client_secret"])
        except Exception as e:
            raise ElectronBondAuthError(
                f"Failed to authorize OAuth with message: {str(e)}")
        self.session.headers["Authorization"] = f"Bearer {token['access_token']}"

    def get_paged(self, url, *args, **kwargs):
        """get list of json objects from urls of paged items"""
        params = {"page": 1}
        if "params" in kwargs:
            params.update(**kwargs["params"])
            del kwargs["params"]

        current_page = self.get(url, params=params, **kwargs)
        current_json = current_page.json()
        try:
            while len(current_json["results"]) > 0:
                for obj in current_json["results"]:
                    yield obj
                if not current_json.get("next"):
                    break
                params["page"] += 1
                current_page = self.get(url, params=params)
                current_json = current_page.json()
        except Exception:
            raise ElectronBondReturnError(
                "get_paged doesn't know how to handle {}".format(current_json))
