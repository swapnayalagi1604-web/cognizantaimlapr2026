import datetime

from pydantic import BaseModel,Field
from datetime import datetime
class PaymentRequest(BaseModel):
    
    order_id:int=Field(description="order id foreign key")
   
    
    
