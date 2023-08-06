class ElviaException(Exception):
    def __init__(self, message):
        self.message = message


class ElviaClientException(ElviaException):
    pass


class MissingCredentialsException(ElviaException):
    pass


class ElviaServerException(ElviaException):
    def __init__(self, message, status_code, headers, body):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def __str__(self):
        return self.message + " " + str(self.status_code) + " " + self.body


class AuthError(ElviaServerException):
    pass


class InvalidRequestBody(ElviaServerException):
    pass


class UnexpectedError(ElviaServerException):
    pass
