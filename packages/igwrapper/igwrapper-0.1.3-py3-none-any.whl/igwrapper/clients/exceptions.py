class IGException(Exception):
    pass

class ApiExceededException(Exception):
    """Raised when our code hits the IG endpoint too often"""
    pass