
from datetime import datetime

from orderapp.repositories.order_repo import OrderRepository
from orderapp.dtos.order_request import OrderRequest
from orderapp.dtos.order_response import OrderResponse
from orderapp.configurations.mysql_conf import session_local
from orderapp.models.order import Order
from orderapp.exceptions.order_exception import OrderException
class OrderRepoImpl(OrderRepository):

    def __init__(self):
        self.session = session_local()

    def add_order(self, order_request:OrderRequest)->OrderResponse:
        #convert order_request to order model
        order = Order(
            customer_id=order_request.customer_id,
            #convert string to datetime
            order_date = datetime.strptime(
            order_request.order_date,
                "%Y-%m-%d"
            ),
            order_status=order_request.order_status,
            order_total=order_request.order_total
        )
        try:
            self.session.add(order)
            self.session.commit()
            #convert order model to order response
            order_response = OrderResponse( 
                order_id=order.order_id,
                customer_id=order.customer_id,
                order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                order_status=order.order_status,
                order_total=order.order_total
            )
            return order_response
        except OrderException as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()
        

    def get_all_orders(self) -> list[OrderResponse]:
        try:
            orders = self.session.query(Order).all()
            order_responses = [
                OrderResponse(
                    order_id=order.order_id,
                    customer_id=order.customer_id,
                    order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                    order_status=order.order_status,
                    order_total=order.order_total
                )
                for order in orders
            ]
            return order_responses
        except OrderException as e:
            raise e
        finally:
            self.session.close()

    def get_order_by_id(self, order_id: int) -> OrderResponse:
        try:
            order = self.session.query(Order).filter(Order.order_id == order_id).first()
            if not order:
                raise OrderException(f"Order with id {order_id} not found")
            order_response = OrderResponse(
                order_id=order.order_id,
                customer_id=order.customer_id,
                order_date=order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                order_status=order.order_status,
                order_total=order.order_total
            )
            return order_response
        except OrderException as e:
            raise e
        finally:
            self.session.close()