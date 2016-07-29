# This is just a container class for response information from a web_service call.
class WebServiceResponse:
    response_code = None
    response_json = None
    response_message = None
    http_request_url = None
    http_method = None
    http_payload = None

    def __init__(self, response_code, response_json, response_message):
        self.response_code = response_code
        self.response_json = response_json
        self.response_message = response_message
