
from abc import ABC, abstractmethod

from paymentapp.dtos.payment_response import  PaymentResponse
from paymentapp.dtos.payment_request import PaymentRequest


class PaymentService(ABC):
    @abstractmethod
    def add_payment(self, payment_request:PaymentRequest) -> PaymentResponse:
        pass

    @abstractmethod
    def get_all_payments(self) -> list[PaymentResponse]:
        pass

   