from fastapi import FastAPI
from a_platform.l_interfaces.api.routes import router

app = FastAPI(title="Analytics AI Factory API", version="0.9.0")

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Analytics AI Factory API is running"}
