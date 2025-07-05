# Test Exceptions 

import unittest
from core.exceptions import UberBaseException, InvalidLocationError, PaymentFailureError

class TestException(unittest.TestCase):
      def test_uber_base_exception(self):
             with self.assertRaises(UberBaseException):
                  raise UberBaseException("Test base exception")

      def test_invalid_location_error(self):
             with self.assertRaise(InvalidLocationError):
                  raise InvalidLocationError("Invalid coordinates")

      def test_payment_failure_error(self):
             with self.assertRaises(PaymentFailureError):
                  raise PaymentFailureError("Card declined")

if __name__ == '__main__':
      unittest.main()

