#cerate router for order service
from fastapi import APIRouter, FastAPI
from orderapp.dtos.order_request import OrderRequest    
from orderapp.dtos.order_response import OrderResponse
from orderapp.services.order_service_impl import OrderServiceImpl


order_router = APIRouter(prefix="/orders", tags=["orders"])
order_service = OrderServiceImpl()
@order_router.post("/", response_model=OrderResponse)
def add_order(order_request:OrderRequest):
    return order_service.add_order(order_request)
@order_router.get("/", response_model=list[OrderResponse])
def get_all_orders():
    return order_service.get_all_orders()
@order_router.get("/{order_id}", response_model=OrderResponse)
def get_order_by_id(order_id: int):
    return order_service.get_order_by_id(order_id)
