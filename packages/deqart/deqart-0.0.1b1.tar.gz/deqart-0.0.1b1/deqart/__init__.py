import logging

import packaging.version
import requests

from .api import API as _API
from .version import __version__

from .db.jobs import search_jobs


formatter = logging.Formatter(fmt="DEQART-PYTHON-SDK - %(levelname)s - %(message)s")
# formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger("deqart-python-sdk")
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def _check_version():
    local_version = packaging.version.parse(__version__)
    if local_version.is_prerelease:
        logger.warning(
            "Development version %s of Deqart Python SDK is being used", __version__
        )
    req = requests.get("https://pypi.python.org/pypi/deqart/json")
    if not req.ok:
        return

    # find max version on PyPI
    releases = req.json().get("releases", [])
    pip_version = packaging.version.parse("0")
    for release in releases:
        ver = packaging.version.parse(release)
        if not ver.is_prerelease or local_version.is_prerelease:
            pip_version = max(pip_version, ver)

    if pip_version.major > local_version.major:
        logger.warning(
            "There is a major upgrade of Deqart Python SDK available on PyPI. We recommend upgrading. Run 'pip install --upgrade deqart' to upgrade from your version %s to %s.",
            local_version,
            pip_version,
        )
    elif pip_version > local_version:
        logger.info(
            "There is a newer version of Deqart Python SDK available on PyPI. Run 'pip install --upgrade deqart' to upgrade from your version %s to %s.",
            local_version,
            pip_version,
        )


_api = _API.get_instance()


def init(path_to_config_json):
    """Initializes and authenticates to Deqart platform using the config file.
    If not initialized then $HOME/.deqart/config.json
    will be used.

    :param path_to_config_json: Location to config JSON file
    :type path_to_config_json: str or Path
    """
    _api.init(path_to_config_json)


_check_version()
init(None)
