# Payment Processing

from abc import ABC, abstractmethod

class PaymentMethod(ABC):
       @abstractmethod
       def process_payment(self, amount: float) -> bool:
             pass

class CreditCardPayment(PaymentMethod):
       def __init__(self, card_number: str, expiry: str, cvv: str):
             self.card_number = card_number
             self.expiry = expiry
             self.cvv = cvv

       def process_payment(self, amount: float) -> bool:
             # Integration with payment gateway would go here
             print(f"Procesing credit card payment of ₹{amount}")
             return True

class UPI_Payment(PaymentMethod):
        def __init__(self, upi_id: str):
             self.upi_id = upi_id

        def process_payment(self, amount: float) -> bool:
             # UPI payment processing logic
             print(f"Processing UPI payment ₹{amount} to {self.upi_id}")
             return True

class PaymentProcessor:
         def __init__(self):
             self.payment_method = { }
  
        def register_payment_method(self, method_name: str, method: PaymentMethod):
             self.payment_method[method_name] = method

        def make_payment(self, method_name: str, amount: float) -> bool:
             if method_name not in self.payment_methods:
                raise ValueError(f"Payment method {method_name} not registered")

             return self.payment_methods[method_name].process_payment(amount) 
            
  