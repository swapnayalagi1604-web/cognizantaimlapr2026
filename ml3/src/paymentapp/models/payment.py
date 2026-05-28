import datetime

from sqlalchemy import Column, DateTime, Integer, DateTime, Boolean, Float
from paymentapp.configurations.mysql_conf import base

from datetime import datetime
class Payment(base):
    #define table name for the payment model
    __tablename__="payments"
    payment_id:int=Column(Integer,primary_key=True,autoincrement=True)     
    order_id:int=Column(Integer,default=0)
    #date of mysql datetime format
    payment_date:datetime=Column(DateTime,default=datetime.today)
    payment_status:bool=Column(Boolean,default=False)
    payment_total:float=Column(Float,default=0.0)
