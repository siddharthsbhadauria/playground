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
                <h1>JSON Viewer</h