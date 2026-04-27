from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.clients import router as clients_router
from app.routers.service_history import router as service_history_router

app = FastAPI(title="K-Tomás API")

# Routers
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(service_history_router)

@app.get("/")
def root():
    return {"message": "Bienvenido a K-Tomás API"}
