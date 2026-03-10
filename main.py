from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from shared.db import Base, engine
from shared.utils import http_exception_handler, request_validation_exception_handler, internal_server_exception_handler
from routers.registiration import router as registiration_router
from routers.contract_verification import router as contract_verification_router
from routers.document import router as document_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    root_path="/registiration",
    title="Registiration Service",
    description="Registiration Service",
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


app.include_router(registiration_router)
app.include_router(contract_verification_router)
app.include_router(document_router)
