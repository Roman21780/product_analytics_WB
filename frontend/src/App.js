import React, { useState, useEffect, useMemo } from 'react';
import { getProducts } from './api';
import ProductTable from './components/ProductTable';
import PriceHistogram from './components/PriceHistogram';
import DiscountScatterPlot from './components/DiscountScatterPlot';
import PriceFilter from './components/PriceFilter';
import RatingFilter from './components/RatingFilter';
import './App.css';

function App() {
  const [allProducts, setAllProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    minPrice: 0,
    maxPrice: 100000,
    minRating: 3,
  });

  // Загрузка всех продуктов один раз при монтировании
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const response = await getProducts();
        setAllProducts(response.data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  // Фильтрация продуктов при изменении фильтров
  const filteredProducts = useMemo(() => {
    return allProducts.filter(product => {
      const price = parseFloat(product.price);
      const rating = parseFloat(product.rating);
      return (
        price >= filters.minPrice &&
        price <= filters.maxPrice &&
        rating >= filters.minRating
      );
    });
  }, [allProducts, filters]);

  if (loading) {
    return <div className="loading">Загрузка данных...</div>;
  }

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

      <div className="data-container">
        <ProductTable products={filteredProducts} />

        <div className="charts-container">
          <PriceHistogram products={filteredProducts} />
          <DiscountScatterPlot products={filteredProducts} />
        </div>
      </div>
    </div>
  );
}

export default App;