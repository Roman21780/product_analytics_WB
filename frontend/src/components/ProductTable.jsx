import React, { useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import { Box } from '@mui/material';

const ProductTable = ({ products }) => {
  const [sortModel, setSortModel] = useState([
    { field: 'price', sort: 'asc' },
  ]);

  const columns = [
    { field: 'name', headerName: 'Название', width: 300 },
    { field: 'price', headerName: 'Цена', width: 120 },
    { field: 'sale_price', headerName: 'Цена со скидкой', width: 150 },
    { field: 'rating', headerName: 'Рейтинг', width: 120 },
    { field: 'review_count', headerName: 'Отзывы', width: 120 },
  ];

  const rows = products.map((product) => ({
    id: product.id,
    name: product.name,
    price: product.price,
    sale_price: product.sale_price,
    rating: product.rating,
    review_count: product.review_count,
  }));

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <DataGrid
        rows={rows}
        columns={columns}
        sortModel={sortModel}
        onSortModelChange={(model) => setSortModel(model)}
        pageSize={5}
        rowsPerPageOptions={[5, 10, 20]}
        localeText={{
          noRowsLabel: 'Нет данных',
          footerRowSelected: (count) =>
            `${count.toLocaleString()} строк выбрано`,
        }}
      />
    </Box>
  );
};

export default ProductTable;