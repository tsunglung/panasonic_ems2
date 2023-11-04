""" Panasonic Smart Home Exceptions."""

class Ems2BaseException(Exception):
    """ Base exception """


class Ems2TokenNotFound(Ems2BaseException):
    """ Refresh token not found """

    def __init__(
        self, message="Refresh token not existed. You may need to open session again."
    ):
        super().__init__(message)
        self.message = message


class Ems2TokenExpired(Ems2BaseException):
    """ Token expired """


class Ems2InvalidRefreshToken(Ems2BaseException):
    """ Refresh token expired """


class Ems2TooManyRequest(Ems2BaseException):
    """ Too many request """


class Ems2LoginFailed(Ems2BaseException):
    """ Any other login exception """


class Ems2Expectation(Ems2BaseException):
    """ Any other exception """


class Ems2ExceedRateLimit(Ems2BaseException):
    """ API reaches rate limit """