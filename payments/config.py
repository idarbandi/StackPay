"""
==========================================================
 Stackpay Configuration
----------------------------------------------------------
 This file contains the configuration settings for the
 Stackpay project, including CORS and logging settings.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import logging
# settings.py
import os
from os.path import dirname, join

from dotenv import load_dotenv
# fastAPI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StackpayPaymentConfig")

load_dotenv()


dotenv_path = join(dirname('/'), '.env')
load_dotenv(dotenv_path)


# Create the FastAPI application instance
app = FastAPI()

stack_origins = os.environ.get('FRONTEND_ALLOWED_ROUTE')

# CORS configuration

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
