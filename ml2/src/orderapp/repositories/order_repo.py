
from abc import ABC, abstractmethod

from orderapp.dtos.order_request import OrderRequest
from orderapp.dtos.order_response import OrderResponse

class OrderRepository(ABC):
   
    @abstractmethod  
    def add_order(self, order_request:OrderRequest)->OrderResponse:
        pass
   
    @abstractmethod
    def get_all_orders(self) -> list[OrderResponse]:
        pass

    @abstractmethod
    def get_order_by_id(self, order_id: int) -> OrderResponse:
        pass