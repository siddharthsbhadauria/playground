import React from 'react';
import FileList from './FileList';
import { Typography } from '@mui/material';

const App = () => {
  return (
    <div className="App" style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <Typography variant="h4" align="center" style={{ marginBottom: '20px' }}>Test Case Viewer</Typography>
      <FileList />
    </div>
  );
};

export default App;
