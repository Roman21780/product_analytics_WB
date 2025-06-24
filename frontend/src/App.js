import React, { useState, useEffect } from 'react';
import { getProducts } from './api';
import ProductTable from './components/ProductTable';
import PriceHistogram from './components/PriceHistogram';
import DiscountScatterPlot from './components/DiscountScatterPlot';
import PriceFilter from './components/PriceFilter';
import RatingFilter from './components/RatingFilter';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    minPrice: 0,
    maxPrice: 100000,
    minRating: 3,
  });

  useEffect(() => {
    fetchProducts();
  }, [filters]);

  const fetchProducts = async () => {
    try {
      setLoading(true);
      const params = {
        price__gte: filters.minPrice,
        price__lte: filters.maxPrice,
        rating__gte: filters.minRating,
      };
      const response = await getProducts(params);
      setProducts(response.data);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>Аналитика товаров Wildberries</h1>

      <div className="filter-container">
        <PriceFilter
          min={0}
          max={100000}
          values={[filters.minPrice, filters.maxPrice]}
          onChange={(min, max) => setFilters({...filters, minPrice: min, maxPrice: max})}
        />
        <RatingFilter
          value={filters.minRating}
          onChange={(rating) => setFilters({...filters, minRating: rating})}
        />
      </div>

      {loading ? (
        <p>Загрузка данных...</p>
      ) : (
        <>
          <ProductTable products={products} />

          <div className="charts-container">
            <PriceHistogram products={products} />
            <DiscountScatterPlot products={products} />
          </div>
        </>
      )}
    </div>
  );
}

export default App;