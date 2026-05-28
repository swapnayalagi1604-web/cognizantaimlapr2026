# Create app FIRST
from fastapi import FastAPI
import consul
from contextlib import asynccontextmanager
from paymentapp.configurations.config import CONSUL_HOST, CONSUL_PORT, SERVICE_NAME_1, SERVICE_ID_1, SERVICE_HOST_1, SERVICE_NAME_1, SERVICE_PORT_1, SERVICE_NAME_2, SERVICE_ID_2, SERVICE_HOST_2, SERVICE_PORT_2
# --------------------------------
# Lifespan (startup + shutdown)
# --------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):

    # startup
    c = consul.Consul(
        host=CONSUL_HOST,
        port=CONSUL_PORT
    )

    c.agent.service.register(
        name=SERVICE_NAME_1,
        service_id=SERVICE_ID_1,
        address=SERVICE_HOST_1,
        port=SERVICE_PORT_1,
        check={
            "http": f"http://{SERVICE_HOST_1}:{SERVICE_PORT_1}/health",
            "interval": "10s",
            "timeout": "5s"
        }
    )
    c.agent.service.register(   
        name=SERVICE_NAME_2,
        service_id=SERVICE_ID_2,
        address=SERVICE_HOST_2,
        port=SERVICE_PORT_2,
        check={
            "http": f"http://{SERVICE_HOST_2}:{SERVICE_PORT_2}/health",
            "interval": "10s",
            "timeout": "5s"
        }
    )

    print("✅ Both Payment services registered with Consul")

    yield

    # shutdown
    c.agent.service.deregister(SERVICE_ID_1)
    c.agent.service.deregister(SERVICE_ID_2)

    print("❌ Both Payment services deregistered")
app = FastAPI(
    title="🛒 E-commerce API",
    description="API for managing e-commerce operations",
    version="1.0.0",
    lifespan=lifespan
)
@app.get("/health")
def health():
    return {
        "status": "UP"
    }

from paymentapp.configurations.mysql_conf import engine, base

#  IMPORT MODELS FIRST (VERY IMPORTANT)
from paymentapp.models.payment import Payment
#create all the tables in the database
base.metadata.create_all(bind=engine)
#make api call to the customer controller

from paymentapp.controllers import payment_controller


app.include_router(payment_controller.payment_router)




