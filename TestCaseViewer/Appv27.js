import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [files, setFiles] = useState([]);
  const [selectedFile, setSelectedFile] = useState("");
  const [testCases, setTestCases] = useState([]);
  const [selectedTestCase, setSelectedTestCase] = useState("");
  const [testCaseData, setTestCaseData] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const threshold = 0.5; // Threshold value for score comparison

  useEffect(() => {
    axios.get('/api/files').then(response => {
      setFiles(response.data);
    }).catch(error => {
      console.error("Error fetching files:", error);
    });
  }, []);

  useEffect(() => {
    if (selectedFile) {
      axios.get(`/api/file/${selectedFile}`).then(response => {
        const testCasesData = response.data.testCases || [];
        setTestCases(testCasesData.map(tc => tc.name));
        if (testCasesData.length > 0) {
          setSelectedTestCase(testCasesData[0].name);
          setTestCaseData(testCasesData[0]);
          setMetrics(testCasesData[0].metricsMetadata || []);
        } else {
          setSelectedTestCase("");
          setTestCaseData(null);
          setMetrics([]);
        }
      }).catch(error => {
        console.error("Error fetching file data:", error);
      });
    }
  }, [selectedFile]);

  useEffect(() => {
    if (selectedTestCase && selectedFile) {
      axios.get(`/api/file/${selectedFile}`).then(response => {
        const testCase = response.data.testCases.find(tc => tc.name === selectedTestCase);
        if (testCase) {
          setTestCaseData(testCase);
          setMetrics(testCase.metricsMetadata || []);
        }
      }).catch(error => {
        console.error("Error fetching test case data:", error);
      });
    }
  }, [selectedTestCase, selectedFile]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>JSON Viewer</h1>
        <div className="selectors middle-section">
          <label>Select a JSON file:</label>
          <select onChange={e => setSelectedFile(e.target.value)} value={selectedFile}>
            <option value="">Select File...</option>
            {files.map(file => (
              <option key={file} value={file}>{file}</option>
            ))}
          </select>
        </div>
        <div className="selectors middle-section">
          <label>Select a test case:</label>
          <select onChange={e => setSelectedTestCase(e.target.value)} value={selectedTestCase} disabled={!selectedFile}>
            <option value="">Select Test Case...</option>
            {testCases.map(testCase => (
              <option key={testCase} value={testCase}>{testCase}</option>
            ))}
          </select>
        </div>
      </header>
      <main>
        {selectedFile && selectedTestCase && (
          <section className="column">
            <h2>Test Case Information</h2>
            {testCaseData && (
              <table className="table-container">
                <tbody>
                  {Object.entries(testCaseData).map(([key, value]) => (
                    key !== 'metricsMetadata' && (
                      <tr key={key}>
                        <th>{key}</th>
                        <td>{Array.isArray(value) ? value.join(', ') : value.toString()}</td>
                      </tr>
                    )
                  ))}
                </tbody>
              </table>
            )}
            <h2>Metrics</h2>
            {metrics.length > 0 && (
              <table className="table-container">
                <tbody>
                  {metrics.map((metric, index) => (
                    <tr key={index}>
                      <th>{metric.metric}</th>
                      <td>{Object.entries(metric).map(([key, value]) => (key !== 'metric' && <div key={key}>{Array.isArray(value) ? value.join(', ') : value.toString()}</div>))}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            <h2>Metrics Bar Graph</h2>
            <div className="bar-graph-container">
              {metrics.length > 0 && metrics.map((metric, index) => (
                <div key={index} className="bar-graph">
                  <div className="y-label">{metric.metric}</div>
                  <div className="bar" style={{ width: `${metric.score * 100}%`, backgroundColor: metric.threshold && metric.score >= metric.threshold ? '#9fdf9f' : '#f99f9f' }}>
                    <span>{metric.score}</span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>
    </div>
  );
};

export default App;