
from abc import ABC, abstractmethod

from paymentapp.dtos.payment_request import PaymentRequest
from paymentapp.dtos.payment_response import PaymentResponse

class PaymentRepository(ABC):
   
    @abstractmethod  
    def add_payment(self, payment_request:PaymentRequest)->PaymentResponse:
        pass
   
    @abstractmethod
    def get_all_payments(self) -> list[PaymentResponse]:
        pass