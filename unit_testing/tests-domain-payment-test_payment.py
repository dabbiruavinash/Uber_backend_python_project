# Test Payment

import unittest
from domain.payment_processor import PaymentProcessor, CreditCardPayment, UPI_Payment

class TestPayment(unittest.TestCase):
      def setUp(self):
        self.processor = PaymentProcessor()
        self.credit_card = CreditCardPayment("4111111111111111", "12/25", "123")
        self.upi = UPI_Payment("user@upi")
        self.processor.register_payment_method("credit_card", self.credit_card)
        self.processor.register_payment_method("upi", self.upi)

    def test_credit_card_payment(self):
        result = self.credit_card.process_payment(100.0)
        self.assertTrue(result)

    def test_upi_payment(self):
        result = self.upi.process_payment(100.0)
        self.assertTrue(result)

    def test_payment_processor(self):
        result = self.processor.make_payment("credit_card", 150.0)
        self.assertTrue(result)
        
        result = self.processor.make_payment("upi", 200.0)
        self.assertTrue(result)

    def test_unregistered_payment_method(self):
        with self.assertRaises(ValueError):
            self.processor.make_payment("paytm", 100.0)

if __name__ == '__main__':
    unittest.main()