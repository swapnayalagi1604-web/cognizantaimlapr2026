
from datetime import datetime
import requests
from paymentapp.repositories.payment_repo import PaymentRepository
from paymentapp.dtos.payment_request import PaymentRequest
from paymentapp.dtos.payment_response import PaymentResponse
from paymentapp.configurations.mysql_conf import session_local
from paymentapp.models.payment import Payment
from paymentapp.exceptions.payment_exception import PaymentException
import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Load environment variables from .env file
load_dotenv(env_path)
order_service_url = os.getenv("order_service_url")

class PaymentRepoImpl(PaymentRepository):

    def __init__(self):
        self.session = session_local()

    def add_payment(self, payment_request:PaymentRequest)->PaymentResponse:
        #get order details from order service
        
        try:
            response = requests.get(order_service_url+str(payment_request.order_id))
            response.raise_for_status()
            order = response.json()
            if not order:
             raise PaymentException(
                f"Order with id {payment_request.order_id} not found"
            )

        except requests.exceptions.RequestException as e:
           raise PaymentException(f"Error while fetching order details: {str(e)}")
        #convert payment_request to payment model
        payment = Payment(          
            #convert string to datetime
            order_id=payment_request.order_id,
            payment_date = datetime.today(),
            payment_status=True,
            payment_total=order["order_total"]
        )
        try:
            self.session.add(payment)
            self.session.commit()
            #convert payment model to payment response
            payment_response = PaymentResponse( 
                payment_id=payment.payment_id,
                order_id=payment.order_id,
                payment_date=payment.payment_date.strftime("%Y-%m-%d %H:%M:%S"),
                payment_status=payment.payment_status,
                payment_total=payment.payment_total
            )
            return payment_response
        except PaymentException as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
        

    def get_all_payments(self) -> list[PaymentResponse]:
        try:
            payments = self.session.query(Payment).all()
            payment_responses = [
                PaymentResponse(
                    payment_id=payment.payment_id,
                    order_id=payment.order_id,
                    payment_date=payment.payment_date.strftime("%Y-%m-%d %H:%M:%S"),
                    payment_status=payment.payment_status,
                    payment_total=payment.payment_total
                )
                for payment in payments
            ]
            return payment_responses
        except PaymentException as e:
            raise e
        finally:
            self.session.close()