/**
 * ==========================================================
 *  Stackpay App Component
 * ----------------------------------------------------------
 *  This file contains the main App component for the Stackpay
 *  React application, handling routing between different
 *  components.
 *
 *  Project: Stackpay
 *  Developed with: FastAPI, Redis, React
 *  Author: idarbandi
 *  Contact: darbandidr99@gmail.com
 *  GitHub: https://github.com/idarbandi
 * ==========================================================
 */

import { Products } from './components/Products';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ProductsCreate } from './components/ProductsCreate';
import { Orders } from './components/Orders';

/**
 * App Component
 *
 * This component handles the routing for different pages of
 * the Stackpay application, including Products, ProductsCreate,
 * and Orders.
 */
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Products />} />
        <Route path="/create" element={<ProductsCreate />} />
        <Route path="/orders" element={<Orders />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
