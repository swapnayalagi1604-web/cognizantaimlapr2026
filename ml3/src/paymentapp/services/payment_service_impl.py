
from paymentapp.services.payment_service import PaymentService
from paymentapp.dtos.payment_response import PaymentResponse
from paymentapp.dtos.payment_request import PaymentRequest
from paymentapp.repositories.payment_repo_impl import PaymentRepoImpl


class PaymentServiceImpl(PaymentService):
    def __init__(self):
        self.payment_repository = PaymentRepoImpl()

    def add_payment(self, payment_request: PaymentRequest) -> PaymentResponse:
        return self.payment_repository.add_payment(payment_request)

    def get_all_payments(self) -> list[PaymentResponse]:
        return self.payment_repository.get_all_payments()