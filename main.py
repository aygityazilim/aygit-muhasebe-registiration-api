from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from shared.db import Base, engine
from shared.utils import http_exception_handler, request_validation_exception_handler, internal_server_exception_handler
from routers.pre_registiration import router as pre_registiration_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    root_path="/pre-registiration",
    title="Pre Registiration Service",
    description="Pre Registiration Service",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, internal_server_exception_handler)


app.include_router(pre_registiration_router)
