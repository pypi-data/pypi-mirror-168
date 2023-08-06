import json

class NotYetSupported(Exception):

    def __init__(self, message="This is not yet supported", *args, **kwargs):
        self.message = message
        super().__init__(message, *args, **kwargs)

class APIError(Exception):
    def __init__(self, r):
        self.status = r.status_code
        self.data = None
        try:
            self.data = r.json()
        except json.decoder.JSONDecodeError:
            self.data = r.content

class NoContentError(APIError):
    pass


class LoginError(APIError):
    pass


class NotLoggedInError(Exception):
    pass


class NoResultsError(Exception):
    pass
