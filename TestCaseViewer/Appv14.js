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

// Function to extract metric details
const extractMetricDetails = (metric) => {
    const details = [];
    for (const key in metric) {
        if (key !== 'metric' && key !== 'score') {
            details.push({ key, value: metric[key] });
        }
    }
    return details;
};

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
            <div className="columns">
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
                </section>
                <section className="column">
                    <h2>Metrics</h2>
                    {metrics.length > 0 && (
                        <table className="table-container">
                            <thead>
                                <tr>
                                    <th>Metric</th>
                                    <th>Details</th>
                                </tr>
                            </thead>
                            <tbody>
                                {metrics.map((metric, index) => (
                                    <tr key={index}>
                                        <td>{metric.metric}</td>
                                        <td>
                                            <ul>
                                                {extractMetricDetails(metric).map((detail, i) => (
                                                    <li key={i}><strong>{detail.key}:</strong> {detail.value}</li>
                                                ))}
                                            </ul>
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </section>
            </div>
        </main>
    </div>
);