# Test helpers contains basic methods that are useful for test assertions, and data creation.
# the methods here are generally static.
import random
import string


def verify_http_response(response, expected_return_code, message, expect_empty_json=False):
    assert response.response_code == str(expected_return_code), \
        "Expected {}, got {} : {}".format(expected_return_code, response.response_code, message)
    if not expect_empty_json:
        assert response.response_json is not None, "Expected response payload.  Got none. :{}".format(message)


def make_random_string(num_chars):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(num_chars))
