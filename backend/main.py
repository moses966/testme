
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from testingapp import router
 


app = FastAPI()

# https://fastapi.tiangolo.com/tutorial/cors/
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "https://localhost.networkbet.com",
    "http://localhost",
    "http://localhost:8080",
    "http://0.0.0.0:8083"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the router
app.include_router(router.router)


