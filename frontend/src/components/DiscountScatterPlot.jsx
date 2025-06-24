import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function DiscountScatterPlot({ products }) {
  const data = products.map(product => ({
    discount: ((product.price - product.sale_price) / product.price) * 100,
    rating: product.rating,
  }));

  return (
    <div className="chart">
      <h2>Зависимость скидки от рейтинга</h2>
      <ScatterChart width={500} height={300}>
        <CartesianGrid />
        <XAxis type="number" dataKey="discount" name="Скидка %" />
        <YAxis type="number" dataKey="rating" name="Рейтинг" domain={[0, 5]} />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        <Legend />
        <Scatter data={data} fill="#82ca9d" />
      </ScatterChart>
    </div>
  );
}