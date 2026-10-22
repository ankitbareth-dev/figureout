
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.exception_handlers import (
    http_exception_handler,
    validation_exception_handler,
)
from app.routes.auth import router as auth_router

app = FastAPI()

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    HTTPException,
    http_exception_handler,
)

app.include_router(auth_router)


@app.get("/")
def home():
    return {"message": "Welcome to Figureout API"}
