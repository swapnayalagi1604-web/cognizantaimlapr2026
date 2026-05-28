#cerate router for order service
from fastapi import APIRouter
from paymentapp.dtos.payment_request import PaymentRequest   
from paymentapp.dtos.payment_response import PaymentResponse
from paymentapp.services.payment_service_impl import PaymentServiceImpl
payment_router = APIRouter()
payment_service = PaymentServiceImpl()
@payment_router.post("/payments", response_model=PaymentResponse)
def add_payment(payment_request:PaymentRequest):
    return payment_service.add_payment(payment_request)
@payment_router.get("/payments", response_model=list[PaymentResponse])
def get_all_payments():
    return payment_service.get_all_payments()
