import json
import logging
import os
from pathlib import Path

import requests
import requests_toolbelt
import urllib3

from .exceptions import DeqartBaseException
from .version import __version__

logger = logging.getLogger("deqart-python-sdk")


class API:
    __instance = None

    def __init__(self):
        self._api_config = None
        self._token = None
        self._verify = None
        self._session = None
        self._default_headers = None
        self._main_endpoint = None
        if API.__instance is not None:
            raise DeqartBaseException(0, "API class is a singleton!")
        API.__instance = self
        self._authenticated = False

    def init(self, config_location=None):
        if config_location is None:
            config_location = Path.home() / ".deqart" / "config.json"
            from_none = True
        else:
            config_location = Path(config_location)
            from_none = False

        try:
            if not config_location.is_file():
                raise DeqartBaseException(
                    0,
                    "Deqart config file "
                    + str(config_location)
                    + " not found. Please provide correct config file location to sa.init(<path>) or use CLI's deqart init to generate default location config file.",
                )
            self._api_config = json.load(open(config_location))

            try:
                self._token = self._api_config["token"]
            except KeyError:
                raise DeqartBaseException(
                    0,
                    "Incorrect config file: 'token' key is not present in the config file "
                    + str(config_location),
                )

            self._default_headers = {"Authorization": self._token}
            self._default_headers["authtype"] = "sdk"
            if "authtype" in self._api_config:
                self._default_headers["authtype"] = self._api_config["authtype"]
            self._default_headers["User-Agent"] = requests_toolbelt.user_agent(
                "deqart", __version__
            )

            self._main_endpoint = "https://us-central1-dequ001.cloudfunctions.net"
            if "main_endpoint" in self._api_config:
                self._main_endpoint = self._api_config["main_endpoint"]
            self._verify = True
            if "ssl_verify" in self._api_config:
                self._verify = self._api_config["ssl_verify"]
            self._session = None
            self._authenticated = True
            response = self.send_request(
                req_type="GET",
                path="/jobs",
                params={"limit": 1},
            )
            if not self._verify:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            if not response.ok:
                self._authenticated = False
                self._session = None
                if "Not authorized" in response.text:
                    raise DeqartBaseException(0, "Couldn't authorize " + response.text)
                raise DeqartBaseException(0, "Couldn't reach deqart " + response.text)
        except DeqartBaseException:
            self._authenticated = False
            self._session = None
            if not from_none:
                raise DeqartBaseException(0, "Couldn't authenticate")

    @staticmethod
    def get_instance():
        if API.__instance is None:
            API()
        return API.__instance

    def send_request(self, req_type, path, params=None, json_req=None):
        if not self._authenticated:
            raise DeqartBaseException(
                0,
                "Deqart was not initialized. Please provide correct config file location to deqart.init(<path>) or use CLI's deqart init to generate default location config file.",
            )
        url = self._main_endpoint + path

        if params is not None:
            for key, value in params.items():
                if isinstance(value, str):
                    params[key] = value.replace("\\", "\\\\")

        req = requests.Request(method=req_type, url=url, json=json_req, params=params)
        if self._session is None:
            self._session = self._create_session()
        prepared = self._session.prepare_request(req)
        resp = self._session.send(request=prepared, verify=self._verify)
        return resp

    def _create_session(self):
        session = requests.Session()
        retry = urllib3.Retry(
            total=5,
            read=5,
            connect=5,
            backoff_factor=0.3,
            # use on any request type
            method_whitelist=False,
            # force retry on those status responses
            status_forcelist=(501, 502, 503, 504, 505, 506, 507, 508, 510, 511),
            raise_on_status=False,
        )
        adapter = requests.adapters.HTTPAdapter(
            max_retries=retry, pool_maxsize=16, pool_connections=16
        )
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers = self._default_headers

        if "DEQART_DEBUG" in os.environ:
            session.hooks["response"].append(_log_requests)

        return session


if "DEQART_DEBUG" in os.environ:
    from requests_toolbelt.utils import dump

    def _log_requests(response, *args, **kwargs):
        data = dump.dump_all(response)
        _log_requests.response_len += len(data)
        logger.info("HTTP %s %s ", response.request.url, _log_requests.response_len)

    _log_requests.response_len = 0
