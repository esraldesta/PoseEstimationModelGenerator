import { useState } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import VideoPlayer from './VideoPlayer';
import LabeledButtons from './LabeledButtons';
import VideoFile from '@mui/icons-material/VideoFile';
import { Alert, Typography } from '@mui/material';
import { Container } from '@mui/system';
import Link from '@mui/material/Link';
import { FormControl } from '@mui/material';
import { Input } from '@mui/material';
function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [exerciseName, setExerciseName] = useState('');
  const [myData, setMyData] = useState({});
  const [lableError,setLableError] = useState("")
  const handleFileInputChange = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      const src = e.target.result;
      setSelectedFile(src);
    };
    console.log(file);
    reader.readAsDataURL(file);
  };

  const handleExerciseNameChange = (event) => {
    setExerciseName(event.target.value);
  };

  const handleButtonClick = (id) => {
    const video = document.getElementById('video');
    const minutes = Math.floor(video.currentTime / 60);
    const seconds = Math.floor(video.currentTime - minutes * 60);
    const minutesDisplay = minutes < 10 ? `0${minutes}` : minutes;
    const secondsDisplay = seconds < 10 ? `0${seconds}` : seconds;
    setMyData((prevData) => ({
      ...prevData,
      [id]: [...(prevData[id] || []), [seconds, minutes]],
    }));
    console.log(myData);
  };

  const handleFormSubmit = (event) => {
    event.preventDefault();
    console.log(myData);
    const formData = new FormData(event.target);
    const url = 'http://127.0.0.1:8000/home/';
    fetch(url, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.text())
      .then((data) => {
        console.log('file uploaded successfully');
        document.body.innerHTML = data;
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (

    <Container>
      <Typography variant="h3" color="primary.main" sx={{
        m: 2
      }} >
        <Link underline="none" href="/">PoseEstimationModelGenerator</Link>
      </Typography>
      <Box sx={
        {
          display:"flex",
          flexDirection:"column",
          alignItems:"center"
        }
      }>{
        lableError &&


            <Alert severity="info">{lableError}</Alert>

          
      }
        {selectedFile && <VideoPlayer src={selectedFile} />}
        <FormControl onSubmit={handleFormSubmit} sx={{
          display: 'flex',
          flexDirection: "column",

          maxWidth: 500
        }}>

          <Button variant="contained" component="label">
            <VideoFile />File
            <input hidden type="file" name="file" accept="mp4/*" onChange={handleFileInputChange} />
          </Button>
          <input type="hidden" name="mydata" value={JSON.stringify(myData)} />
          <TextField
            id="exercise-name"
            name="exercise_name"
            label="Exercise Name"
            value={exerciseName}
            onChange={handleExerciseNameChange}
            sx={{ margin: '12px' }}
          />

          <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <LabeledButtons handleClick={handleButtonClick} lableError={lableError} setLableError={setLableError} />
        </Box>
          <Button variant="contained" type="submit">
            Submit
          </Button>
        </FormControl>



      </Box>
    </Container>
  )
}

export default App;


// <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
// </Box>
