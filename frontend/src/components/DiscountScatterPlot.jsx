import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const DiscountScatterPlot = ({ products }) => {
  const data = products.map(product => ({
    discount: ((parseFloat(product.price) - parseFloat(product.sale_price)) / parseFloat(product.price)) * 100,
    rating: parseFloat(product.rating),
    price: parseFloat(product.price),
  }));

  return (
    <div className="chart">
      <h3>Зависимость скидки от рейтинга</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid />
          <XAxis type="number" dataKey="discount" name="Скидка %" />
          <YAxis type="number" dataKey="rating" name="Рейтинг" domain={[0, 5]} />
          <ZAxis type="number" dataKey="price" name="Цена" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }}
            formatter={(value, name) => name === 'price' ? [`${value} ₽`, 'Цена'] : [value, name]} />
          <Scatter name="Товары" data={data} fill="#82ca9d" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DiscountScatterPlot;