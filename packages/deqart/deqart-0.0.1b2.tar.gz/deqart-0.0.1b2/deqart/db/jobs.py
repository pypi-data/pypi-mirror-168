import logging

from ..api import API
from ..exceptions import DeqartBaseException

logger = logging.getLogger("deqart-python-sdk")

_api = API.get_instance()


def search_jobs():
    SINGLE_REQUEST_LIMIT = 10
    params = {"limit": SINGLE_REQUEST_LIMIT}
    result_list = []
    while True:
        response = _api.send_request(req_type="GET", path="/jobs", params=params)
        if not response.ok:
            raise DeqartBaseException(
                response.status_code, "Couldn't search jobs " + response.text
            )
        response = response.json()

        results = response["data"]
        result_list += results

        if len(results) < SINGLE_REQUEST_LIMIT:
            break

        params["startAfterSubmitTime"] = results[-1]["submitTime"]
    return result_list

def submit_job():
    pass
