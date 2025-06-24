import React from 'react';
import Slider from '@mui/material/Slider';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';

const RatingFilter = ({ value, onChange }) => {
  const handleChange = (event, newValue) => {
    onChange(newValue);
  };

  return (
    <Box sx={{ width: 300 }}>
      <Typography gutterBottom>Минимальный рейтинг</Typography>
      <Slider
        value={value}
        onChange={handleChange}
        min={0}
        max={5}
        step={0.1}
        marks={[
          { value: 0, label: '0' },
          { value: 5, label: '5' }
        ]}
        valueLabelDisplay="auto"
        valueLabelFormat={(value) => value.toFixed(1)}
      />
    </Box>
  );
};

export default RatingFilter;