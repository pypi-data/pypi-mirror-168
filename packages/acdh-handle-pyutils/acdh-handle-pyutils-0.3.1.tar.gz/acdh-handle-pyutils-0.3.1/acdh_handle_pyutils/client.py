"""Main module."""
import json
import requests


class HandleClient():

    def __init__(
        self,
        hdl_user,
        hdl_pw,
        hdl_provider="http://pid.gwdg.de/handles/",
        hdl_prefix="21.11115",
        hdl_resolver="https://hdl.handle.net/"
    ):
        """ initializes the class

        :param hdl_user: handle-username, e.g. 'user12.12345-06'
        :type hdl_user: str

        :param hdl_user: handle-password, e.g. 'verysecret'
        :type hdl_user: str

        :param hdl_provider: the base url of your handle-provider
        :type hdl_provider: str

        :param hdl_prefix: the prefix of you institution
        :type hdl_prefix: str

        :param hdl_resolver: An URL resolving your handle-id
        :type hdl_resolver: str

        :return: A HandleClient instance
        :rtype: `client.HandleClient`

        """

        self.user = hdl_user
        self.pw = hdl_pw
        self.provider = hdl_provider
        self.prefix = hdl_prefix
        if hdl_resolver.endswith('/'):
            self.resolver = hdl_resolver
        else:
            self.resolver = f"{hdl_resolver}/"
        if f"{self.provider}{hdl_prefix}".endswith('/'):
            self.url = f"{self.provider}{self.prefix}"
        else:
            self.url = f"{self.provider}{self.prefix}/"
        self.json_header = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.auth = (self.user, self.pw)

    def register_handle(self, parsed_data, full_url=True):
        """ registers an handle-id for the passed in URL aka 'parsed_data'

        :param parsed_data: An URL to register a HANDLE-ID for
        :type parsed_data: str

        :return: The created HANDLE-ID
        :rtype: str
        """
        payload = json.dumps([{
            "type": "URL",
            "parsed_data": parsed_data
        }])
        response = requests.request(
            "POST", self.url,
            headers=self.json_header, data=payload, auth=self.auth
        )
        handle = response.json()['epic-pid']
        if full_url:
            return f"{self.resolver}{handle}"
        else:
            return handle
