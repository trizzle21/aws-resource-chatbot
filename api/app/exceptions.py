"""
API & HTTP Clients exceptions.
"""


class AWSMonitorException(Exception):
    """
    Base class for exceptions.
    """
    def __init__(self):
        self.message = 'Sorry, did not understand that'