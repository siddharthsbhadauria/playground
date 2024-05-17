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

    useEffect(() => {
        axios.get('/api/files').then(response => {
            setFiles(response.data);
        });
    }, []);

    useEffect(() => {
        if (selectedFile) {
            axios.get(`/api/file/${selectedFile}`).then(response => {
                setTestCases(response.data.testCases.map(tc => tc.name));
                setSelectedTestCase(response.data.testCases[0].name);
                setTestCaseData(response.data.testCases[0]);
                setMetrics(response.data.testCases[0].metricsMetadata || []);
            });
        }
    }, [selectedFile]);

    useEffect(() => {
        if (selectedTestCase && selectedFile) {
            axios.get(`/api/file/${selectedFile}`).then(response => {
                const testCase = response.data.testCases.find(tc => tc.name === selectedTestCase);
                setTestCaseData(testCase);
                setMetrics(testCase.metricsMetadata || []);
            });
        }
    }, [selectedTestCase]);

    return (
        <div className="App">
            <header className="App-header">
                <h1>JSON Viewer</h1>
                <div>
                    <label>Select a JSON file:</label>
                    <select onChange={e => setSelectedFile(e.target.value)} value={selectedFile}>
                        <option value="">Select File...</option>
                        {files.map(file => (
                            <option key={file} value={file}>{file}</option>
                        ))}
                    </select>
                </div>
                <div>
                    <label>Select a test case:</label>
                    <select onChange={e => setSelectedTestCase(e.target.value)} value={selectedTestCase}>
                        {testCases.map(testCase => (
                            <option key={testCase} value={testCase}>{testCase}</option>
                        ))}
                    </select>
                </div>
            </header>
            <main>
                <section>
                    <h2>Test Case Information</h2>
                    {testCaseData && (
                        <table>
                            <thead>
                                <tr>
                                    <th>Key</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                {Object.entries(testCaseData).map(([key, value]) => (
                                    key !== 'metricsMetadata' && (
                                        <tr key={key}>
                                            <td>{key}</td>
                                            <td>{Array.isArray(value) ? value.join(', ') : value.toString()}</td>
                                        </tr>
                                    )
                                ))}
                            </tbody>
                        </table>
                    )}
                </section>
                <section>
                    <h2>Metrics</h2>
                    {metrics.map((metric, index) => (
                        <div key={index}>
                            <h3>Metric {index + 1}: {metric.metric}</h3>
                            <table>
                                <thead>
                                    <tr>
                                        <th>Key</th>
                                        <th>Value</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {Object.entries(metric).map(([key, value]) => (
                                        <tr key={key}>
                                            <td>{key}</td>
                                            <td>{Array.isArray(value) ? value.join(', ') : value.toString()}</td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    ))}
                </section>
            </main>
        </div>
    );
};

export default App;