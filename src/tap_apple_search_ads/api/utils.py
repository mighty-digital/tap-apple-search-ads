import requests
import singer

logger = singer.get_logger()


def check_response(response: requests.Response) -> bool:
    if response.status_code != 200:
        message = "Received non-200 response code ([%s]) for URL %s"
        logger.error(message, response.status_code, response.url)
        logger.error("Response content: [%s]", response.text)

        raise RuntimeError(message % response.status_code)

    return True
