/**
 * ==========================================================
 *  Stackpay Orders Component
 * ----------------------------------------------------------
 *  This file contains the Orders component for the Stackpay
 *  React application, handling order creation and product
 *  fetching.
 *
 *  Project: Stackpay
 *  Developed with: FastAPI, Redis, React
 *  Author: idarbandi
 *  Contact: darbandidr99@gmail.com
 *  GitHub: https://github.com/idarbandi
 * ==========================================================
 */

import { useEffect, useState } from 'react';

/**
 * Orders Component
 *
 * This component handles the order creation process, including fetching product details and submitting orders.
 */
export const Orders = () => {
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [message, setMessage] = useState('Buy your favorite product');

  useEffect(() => {
    (async () => {
      try {
        if (productId) {
          const response = await fetch(`http://localhost:8000/products/${productId}`);
          const content = await response.json();
          const price = parseFloat(content.price) * 1.2;
          setMessage(`Your product price is $${price}`);
        }
      } catch (e) {
        setMessage('Buy your favorite product');
      }
    })();
  }, [productId]);

  const submitOrder = async (e) => {
    e.preventDefault();

    await fetch('http://localhost:8001/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        productId,
        quantity,
      }),
    });

    setMessage('Thank you for your order!');
  };

  return (
    <div className="stack-container">
      <main>
        <div className="py-5 text-center stack-header">
          <h2 className="stack-header-title">Checkout form</h2>
          <p className="lead">{message}</p>
        </div>

        <form onSubmit={submitOrder}>
          <div className="row g-3">
            <div className="col-sm-6">
              <label className="form-label">Product</label>
              <input className="form-control stack-input-field" onChange={(e) => setProductId(e.target.value)} />
            </div>

            <div className="col-sm-6">
              <label className="form-label">Quantity</label>
              <input
                type="number"
                className="form-control stack-input-field"
                onChange={(e) => setQuantity(e.target.value)}
              />
            </div>
          </div>
          <hr className="my-4" />
          <button className="w-100 btn btn-primary btn-lg stack-button" type="submit">
            Buy
          </button>
        </form>
      </main>
    </div>
  );
};
