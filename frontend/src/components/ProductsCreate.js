/**
 * ==========================================================
 *  Stackpay ProductsCreate Component
 * ----------------------------------------------------------
 *  This file contains the ProductsCreate component for the
 *  Stackpay React application, handling the creation of
 *  products.
 *
 *  Project: Stackpay
 *  Developed with: FastAPI, Redis, React
 *  Author: idarbandi
 *  Contact: darbandidr99@gmail.com
 *  GitHub: https://github.com/idarbandi
 * ==========================================================
 */

import { Wrapper } from './Wrapper';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

/**
 * ProductsCreate Component
 *
 * This component handles the creation of new products, including
 * capturing input data and submitting it to the backend.
 */
export const ProductsCreate = () => {
  const [productName, setProductName] = useState('');
  const [productPrice, setProductPrice] = useState('');
  const [productQuantity, setProductQuantity] = useState('');
  const navigate = useNavigate();

  const submitProduct = async (e) => {
    e.preventDefault();

    await fetch('http://localhost:8000/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: productName,
        price: productPrice,
        quantity: productQuantity,
      }),
    });

    await navigate(-1);
  };

  return (
    <Wrapper>
      <form className="mt-3 stack-form" onSubmit={submitProduct}>
        <div className="form-floating pb-3">
          <input
            className="form-control stack-input-field"
            placeholder="Name"
            onChange={(e) => setProductName(e.target.value)}
          />
          <label>Name</label>
        </div>

        <div className="form-floating pb-3">
          <input
            type="number"
            className="form-control stack-input-field"
            placeholder="Price"
            onChange={(e) => setProductPrice(e.target.value)}
          />
          <label>Price</label>
        </div>

        <div className="form-floating pb-3">
          <input
            type="number"
            className="form-control stack-input-field"
            placeholder="Quantity"
            onChange={(e) => setProductQuantity(e.target.value)}
          />
          <label>Quantity</label>
        </div>

        <button className="w-100 btn btn-lg btn-primary stack-button" type="submit">
          Submit
        </button>
      </form>
    </Wrapper>
  );
};
