import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Select, MenuItem, FormControl, InputLabel, Card, CardContent, Typography } from '@mui/material';
import TestCaseDetails from './TestCaseDetails';

const FileList = () => {
  const [files, setFiles] = useState([]); // Holds the list of available files
  const [selectedFile, setSelectedFile] = useState(null); // State for the selected file

  useEffect(() => {
    // Fetch the list of files
    const fetchFiles = async () => {
      const response = await axios.get('http://localhost:3001/files');
      setFiles(response.data);
    };
    fetchFiles();
  }, []);

  const handleFileSelect = async (e) => {
    // Fetch the selected file's content
    const file = e.target.value;
    const response = await axios.get(`http://localhost:3001/file/${file}`);
    setSelectedFile(response.data);
  };

  return (
    <div style={{ padding: '20px' }}>
      <FormControl fullWidth>
        <InputLabel>Select a File</InputLabel>
        <Select value={selectedFile ? selectedFile.name : ''} onChange={handleFileSelect}>
          {files.map((file) => (
            <MenuItem key={file} value={file}>
              {file}
            </MenuItem>
          ))}
        </Select>
      </FormControl>

      {selectedFile && (
        <Card style={{ marginTop: '20px' }}>
          <CardContent>
            <Typography variant="h5">Test Cases in {selectedFile.name}</Typography>
            {selectedFile.testCases.map((testCase) => (
              <TestCaseDetails key={testCase.name} testCase={testCase} />
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default FileList;
