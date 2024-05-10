const express = require('express');
const fs = require('fs');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors()); // Allow CORS for frontend-backend communication
app.use(express.json());

const PORT = 3001; // Port for the backend server

// Get the list of available files
app.get('/files', (req, res) => {
  const files = fs.readdirSync(path.join(__dirname, 'data')); // Read the files in the 'data' folder
  res.json(files);
});

// Get the content of a specific file
app.get('/file/:name', (req, res) => {
  const { name } = req.params;
  const filePath = path.join(__dirname, 'data', name);
  if (fs.existsSync(filePath)) {
    const content = fs.readFileSync(filePath, 'utf-8');
    res.json(JSON.parse(content));
  } else {
    res.status(404).send('File not found');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
