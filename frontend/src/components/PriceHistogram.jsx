import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const PriceHistogram = ({ products }) => {
  // Группировка цен по диапазонам
  const priceRanges = [
    { name: '0-10k', min: 0, max: 10000, count: 0 },
    { name: '10k-20k', min: 10000, max: 20000, count: 0 },
    { name: '20k-30k', min: 20000, max: 30000, count: 0 },
    { name: '30k+', min: 30000, max: Infinity, count: 0 },
  ];

  products.forEach((product) => {
    const price = parseFloat(product.price);
    for (const range of priceRanges) {
      if (price >= range.min && price < range.max) {
        range.count++;
        break;
      }
    }
  });

  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>Распределение цен</h3>
      <ResponsiveContainer width="100%" height="80%">
        <BarChart data={priceRanges}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="count" fill="#8884d8" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PriceHistogram;