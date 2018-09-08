import requests


API_URL = "https://graph.facebook.com/{0}/{1}/{2}?access_token={3}"

CONNECT_TIMEOUT = 3.5
READ_TIMEOUT = 9999


class FacebookClient():

    def __init__(self, access_token):
        self.access_token = access_token

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

    def _make_request(self, version, node_id, field, access_token,
                      params=None, base_url=API_URL):
        connect_timeout = CONNECT_TIMEOUT
        read_timeout = READ_TIMEOUT
        if params:
            if 'connect-timeout' in params:
                connect_timeout = params['connect-timeout'] + 10
            if 'timeout' in params:
                read_timeout = params['timeout'] + 10
        request_url = base_url.format(
            version, node_id, field, access_token)
        result = requests.get(request_url, timeout=(
            connect_timeout, read_timeout))
        return self._check_result(result)['data']

    def gen_posts(self, node_id):
        version = 'v1.0'
        response = self._make_request(
            version, node_id, 'posts', self.access_token)
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


if __name__ == '__main__':
    valid_access_token = 'EAAAAUaZA8jlABAMhIgavkNdr984f3HhzP9M4xCrvwivBGqGnt'\
        'ER7rYGQjStSPo9foYMuMkhMGN6ZC5wKZB9xFaJex7x0d5vaFF0tyg72jut3C0z'\
        'dPPxuCEyUXiYPVzIb0ybfC3kFv6F8xQzSYjS14RXYFUyyp8ZD'
    # invalid_access_token = 'EAACYqFZAXAzABAEbjgdEmnYgR0hiVlPv'\
    #     'XGCFNhvS6qVnZBxmx6b3ZBvcVGqZBWLkvsaxJCGTnXPPlg78XwdH3BSNDE9o4'\
    #     'xtl9ZCTT6cZATSmT057IXc4EfcypGRY1TL8Kpvlod4RvOo81lUVCFxt4KbD13qG'\
    #     'nWo464JERHVO6xTW2TqFtlTVF8UEJbNsVtPWIDUtnQiLZAhcgZDZD'
    page_id = '1007443141'
    obj = FacebookClient(valid_access_token)
    # obj = FacebookClient(invalid_access_token)
    res = obj.gen_posts(page_id)
    print(res)
