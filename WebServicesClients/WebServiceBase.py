import json
import logging
from enum import Enum

import httplib2
import oauth2

from WebServicesClients.WebServiceResponse import WebServiceResponse


class HttpMethod(Enum):
    GET = 1
    PUT = 2
    POST = 3
    DELETE = 4


class WebServiceBase:

    consumer_key = None
    consumer_secret = None
    access_token = None
    access_token_secret = None

    logger = None

    def __init__(self, base_url, consumer_key, consumer_secret, access_token, access_token_secret, logger_id):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.logger = logging.getLogger(logger_id)
        # lets do some funky python stuff to add the base url to all our urls
        url_vars = [attr for attr in dir(self) if not callable(attr) and attr.endswith("_URL")]
        for var in url_vars:
            self.__dict__[var] = base_url + eval('self.'+var)

    def _get(self, url, headers=None):
        self.logger.debug("GET: {}".format(url))
        return self._service_call_impl(url, HttpMethod.GET, "", headers)

    def _put(self, url, payload, headers=None):
        self.logger.debug("PUT: {}".format(url))
        return self._service_call_impl(url, HttpMethod.PUT, payload, headers)

    def _post(self, url, payload, headers=None):
        self.logger.debug("POST: {}".format(url))
        return self._service_call_impl(url, HttpMethod.POST, payload, headers)

    def _delete(self, url, headers=None):
        self.logger.debug("DELETE: {}".format(url))
        return self._service_call_impl(url, HttpMethod.DELETE, "", headers)

    def _service_call_impl(self, url, http_method, payload, headers=None):
        try:
            if payload:
                self.logger.debug("Payload: {}".format(payload))
            consumer = oauth2.Consumer(key=self.consumer_key, secret=self.consumer_secret)
            token = oauth2.Token(key=self.access_token, secret=self.access_token_secret)
            client = oauth2.Client(consumer, token)
            resp, content = client.request( url, method=http_method.name, body=payload, headers=headers)
        except httplib2.HttpLib2Error as e:
            service_response = WebServiceResponse(0, "", str(e))
            return service_response
        service_response = WebServiceResponse(resp['status'], self.loads_json(content), content)
        self.logger.debug("Response Code: {}".format(service_response.response_code))
        self.logger.debug("Response json: {}".format(content))
        return service_response

    def loads_json(self, myjson):
        try:
            return json.loads(myjson.decode("utf-8"))
        except ValueError:
            return None
