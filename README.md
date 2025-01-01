# StackPay

![StackPay Logo](https://github.com/idarbandi/StackPay/blob/main/frontend/public/StackPay%20logo.png)
idarbandi - [idarbandi](https://github.com/idarbandi)
Email: darbandidr99@gmail.com

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

StackPay is a comprehensive React application designed to streamline order creation and product management. Developed with FastAPI, Redis, and React, StackPay provides a seamless experience for users to browse and purchase their favorite products.

## Features

- **Order Creation**: Users can create orders with ease, specifying the product and quantity.
- **Product Fetching**: Retrieve product details and prices dynamically.
- **Error Handling**: Robust error handling for better user experience.
- **Responsive Design**: Optimized for both desktop and mobile devices.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/idarbandi/StackPay.git
   cd StackPay
Install frontend dependencies:

sh
cd frontend
npm install
Install backend dependencies:

sh
cd backend
pip install -r requirements.txt
Start the development servers:

Frontend:

sh
npm start
Backend:

sh
uvicorn main:app --reload
Usage
Navigate to the frontend at http://localhost:3000 to interact with the application.

Use the input fields to specify the product ID and quantity.

Submit the order and view the response message.

API Endpoints
GET /products/{product_id}: Fetch product details.

POST /orders/: Create a new order.

Technologies Used

Frontend: React

Backend: FastAPI

Database: Redis

Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

Fork the Project

Create your Feature Branch (git checkout -b feature/AmazingFeature)

Commit your Changes (git commit -m 'Add some AmazingFeature')

Push to the Branch (git push origin feature/AmazingFeature)

Open a Pull Request

License
Distributed under the MIT License. See LICENSE for more information.

Contact
idarbandi - idarbandi Email: darbandidr99@gmail.com

Project Link: https://github.com/idarbandi/StackPay
