"""
==========================================================
 Stackpay Payment Configuration
----------------------------------------------------------
 This file contains the configuration settings for the
 Stackpay payment system, including CORS and logging settings.

 Project: Stackpay
 Developed with: FastAPI, Redis, React
 Author: idarbandi
 Contact: darbandidr99@gmail.com
 GitHub: https://github.com/idarbandi
==========================================================
"""

import logging

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("StackpayPaymentConfig")

# Create the FastAPI application instance
app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
