class RequestFailedException(Exception):
    def __init__(self, status_code):
        message = f'request failed with status code {status_code}.'
        super(RequestFailedException, self).__init__(message)
