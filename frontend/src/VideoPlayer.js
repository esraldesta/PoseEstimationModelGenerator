import { Box } from '@mui/material';
import React, { useState } from 'react'

const VideoPlayer = ({ src }) => {
    const [currentTime, setCurrentTime] = useState(0);
  
    const handleTimeUpdate = (event) => {
      setCurrentTime(event.target.currentTime);
    };
  
    return (
      <Box>
        <video id="video" src={src} onTimeUpdate={handleTimeUpdate} controls />
        <p>Current Time: {currentTime}</p>
      </Box>
    );
  };

export default VideoPlayer