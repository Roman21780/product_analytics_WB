import React from 'react';
import { Slider, Typography, Box } from '@mui/material';

const PriceFilter = ({ min, max, values, onChange }) => {
  const handleChange = (event, newValue) => {
    onChange(newValue[0], newValue[1]);
  };

  return (
    <Box sx={{ width: 300 }}>
      <Typography gutterBottom>Диапазон цен</Typography>
      <Slider
        min={min}
        max={max}
        value={values}
        onChange={handleChange}
        valueLabelDisplay="auto"
        valueLabelFormat={(value) => `${value}₽`}
      />
    </Box>
  );
};

export default PriceFilter;