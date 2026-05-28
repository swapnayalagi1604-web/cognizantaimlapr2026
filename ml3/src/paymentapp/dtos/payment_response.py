
from pydantic import BaseModel, Field

class PaymentResponse(BaseModel):
    order_id:int
    payment_id:int
    #date of mysql datetime format
    payment_date:str
    payment_status:bool
    payment_total:float