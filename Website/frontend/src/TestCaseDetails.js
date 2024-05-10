import React, { useState } from 'react';
import { Card, CardContent, Typography, Collapse, IconButton } from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui.material/ExpandLessIcon;

const TestCaseDetails = ({ testCase }) => {
  const [expanded, setExpanded] = useState(false);

  const toggleExpand = () => {
    setExpanded(!expanded);
  };

  return (
    <Card style={{ marginBottom: '10px' }}>
      <CardContent>
        <Typography variant="h6" onClick={toggleExpand} style={{ cursor: 'pointer' }}>
          {testCase.name}
          <IconButton onClick={toggleExpand}>
            {expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
          </IconButton>
        </Typography>
        <Collapse in={expanded}>
          <div>
            <Typography><strong>Input:</strong> {testCase.input}</Typography>
            <Typography><strong>Actual Output:</strong> {testCase.actualOutput}</Typography>
            <Typography><strong>Expected Output:</strong> {testCase.expectedOutput}</Typography>
            <Typography><strong>Context:</strong> {testCase.context.join(', ')}</Typography>
            <Typography variant="subtitle1">Metrics</Typography>
            <ul>
              {testCase.metricsMetadata.map((metric, index) => (
                <li key={index}>
                  <strong>{metric.metric}</strong>: 
                  {metric.success ? ' Success' : ' Failed'} - 
                  {metric.reason}
                </li>
              ))}
            </ul>
          </div>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default TestCaseDetails;
