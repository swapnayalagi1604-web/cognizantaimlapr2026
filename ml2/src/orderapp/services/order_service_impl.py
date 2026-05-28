
from orderapp.services.order_service import OrderService
from orderapp.dtos.order_response import OrderResponse
from orderapp.dtos.order_request import OrderRequest
from orderapp.repositories.order_repo_impl import OrderRepoImpl


class OrderServiceImpl(OrderService):
    def __init__(self):
        self.order_repository = OrderRepoImpl()

    def add_order(self, order_request: OrderRequest) -> OrderResponse:
        return self.order_repository.add_order(order_request)

    def get_all_orders(self) -> list[OrderResponse]:
        return self.order_repository.get_all_orders()
    def get_order_by_id(self, order_id: int) -> OrderResponse:
        return self.order_repository.get_order_by_id(order_id)