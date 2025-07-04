# Core Exceptions

class UberBaseException(Exception):
      """Base exception class for all uber exceptions""""
      pass

class InvalideLocationError(UberBaseException):
      """Raised when location data is invalid"""
      pass

class PaymentFailureError(UberBaseException):
      """Raised when payment processing fails"""
      pass

class DriverUnavailableError(UberBaseException):
      """Raised when no driver are available"""
      pass

class TripAlreadyCompletedError(UberBaseException):
      """"Raised when attempting to modify a completed trip"""
      pass

