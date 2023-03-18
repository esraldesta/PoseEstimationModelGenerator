import React, { useState } from 'react';
import { Box, Button, TextField } from '@mui/material';

const LabeledButtons = ({ handleClick, lableError ,setLableError }) => {
  const [labels, setLabels] = useState([]);
  const [currentLabel, setCurrentLabel] = useState('');

  const handleAddLabel = () => {
    if (labels.includes(currentLabel)) {
      setLableError(currentLabel  + " Lable existes")
      console.log(lableError);
    } else {
      console.log(lableError);
      setLabels([...labels, currentLabel]);
      setCurrentLabel('');
      setLableError("")
    }
  };

  return (
    <Box display="flex" flexDirection="column">
      <Box display="flex" flexWrap="wrap" sx={{
        p:1
      }}>

        {labels.map((label) => (
          <Button  variant='outlined' key={label} onClick={() => handleClick(label)} sx={{m:0.5 ,bgcolor:"lightgrey" , color:"black"}}>
            {label}
          </Button>
        ))}
      </Box>
      <Box display="flex" justifyContent="center" sx={{
        m: 1
      }}>
        <TextField
          label="Add Label"
          value={currentLabel}
          onChange={(e) => setCurrentLabel(e.target.value)}
        />
        <Button variant='contained' sx={{
          ml: 1
        }} onClick={handleAddLabel}>Add</Button>
      </Box>
    </Box>
  );
};


export default LabeledButtons