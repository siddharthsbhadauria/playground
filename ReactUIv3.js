import React, { useState } from 'react';
import { Container, Row, Col, Form, Table, Dropdown } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  const [jsonData, setJsonData] = useState(null);
  const [selectedTestCase, setSelectedTestCase] = useState(null);

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.onload = (e) => {
      try {
        const data = JSON.parse(e.target.result);
        setJsonData(data);
        setSelectedTestCase(data.testCases[0]);
      } catch (error) {
        console.error('Error parsing JSON', error);
      }
    };
    reader.readAsText(file);
  };

  const handleTestCaseSelect = (testCaseName) => {
    const testCase = jsonData.testCases.find(tc => tc.name === testCaseName);
    setSelectedTestCase(testCase);
  };

  return (
    <Container>
      <Row className="my-4">
        <Col>
          <Form.Group>
            <Form.File
              label="Upload JSON File"
              accept=".json"
              onChange={handleFileUpload}
            />
          </Form.Group>
        </Col>
      </Row>
      {jsonData && (
        <Row className="my-4">
          <Col>
            <Dropdown onSelect={handleTestCaseSelect}>
              <Dropdown.Toggle variant="primary">
                {selectedTestCase ? selectedTestCase.name : 'Select Test Case'}
              </Dropdown.Toggle>
              <Dropdown.Menu>
                {jsonData.testCases.map(testCase => (
                  <Dropdown.Item
                    key={testCase.name}
                    eventKey={testCase.name}
                  >
                    {testCase.name}
                  </Dropdown.Item>
                ))}
              </Dropdown.Menu>
            </Dropdown>
          </Col>
        </Row>
      )}
      {selectedTestCase && (
        <>
          <Row className="my-4">
            <Col>
              <h4>Test Case Information</h4>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>Key</th>
                    <th>Value</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.keys(selectedTestCase).map((key) => {
                    if (key !== 'metricsMetadata') {
                      return (
                        <tr key={key}>
                          <td>{key}</td>
                          <td>{Array.isArray(selectedTestCase[key]) ? selectedTestCase[key].join(', ') : selectedTestCase[key]}</td>
                        </tr>
                      );
                    }
                    return null;
                  })}
                </tbody>
              </Table>
            </Col>
          </Row>
          {selectedTestCase.metricsMetadata.map((metric, index) => (
            <Row className="my-4" key={index}>
              <Col>
                <h4>Metric {index + 1}: {metric.metric}</h4>
                <Table striped bordered hover>
                  <thead>
                    <tr>
                      <th>Key</th>
                      <th>Value</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Object.keys(metric).map((key) => (
                      <tr key={key}>
                        <td>{key}</td>
                        <td>{Array.isArray(metric[key]) ? metric[key].join(', ') : metric[key]}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              </Col>
            </Row>
          ))}
        </>
      )}
    </Container>
  );
};

export default App;