import requests


API_URL = "https://graph.facebook.com/{0}/{1}/{2}?access_token={3}"

CONNECT_TIMEOUT = 3.5
READ_TIMEOUT = 9999


class FacebookClient():

    def __init__(self, access_token, version):
        self.access_token = access_token
        self.version = version

    def _check_result(self, result):
        """
        Checks whether `result` is a valid API response.
        A result is considered invalid if:
            - The server returned an HTTP response code other than 200
            - The content of the result is invalid JSON.

        :raises FacebookApiException: if one of the above listed
        cases is applicable
        :param result: The returned result of the method request
        :return: The result parsed to a JSON dictionary.
        """
        print(result)
        if result.status_code != 200:
            msg = 'The server returned HTTP {0} {1}. Response body:\n[{2}]' \
                .format(result.status_code, result.reason,
                        result.text.encode('utf8'))
            raise FacebookApiException(msg, result)

        try:
            result_json = result.json()
        except Exception:
            msg = 'The server returned an invalid JSON response.' \
                'Response body:\n[{0}]' \
                .format(result.text.encode('utf8'))
            raise FacebookApiException(msg, result)
        return result_json

    def _make_request(self, node_id, field, access_token,
                      params=None, base_url=API_URL):
        connect_timeout = CONNECT_TIMEOUT
        read_timeout = READ_TIMEOUT
        if params:
            if 'connect-timeout' in params:
                connect_timeout = params['connect-timeout'] + 10
            if 'timeout' in params:
                read_timeout = params['timeout'] + 10
        request_url = base_url.format(
            self.version, node_id, field, access_token)
        print('request_url: ', request_url)
        result = requests.get(request_url, timeout=(
            connect_timeout, read_timeout))
        result_checked = self._check_result(result)
        return result_checked

    def fetch_obj(self, node_id, field=''):
        response = self._make_request(
            node_id, field, self.access_token)
        return response


class FacebookApiException(Exception):
    """
    This class represents an Exception thrown when a call
        to the FacebookClient API fails.
    It has a `result` attribute, which contain the returned
        result that made the function to be considered  as
    failed.
    """

    def __init__(self, msg, result):
        super(FacebookApiException, self).__init__(
            "A request to the FacebookClient API was"
            "unsuccessful. {0}".format(msg))
        self.result = result
