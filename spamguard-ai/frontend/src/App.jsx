import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import OverviewPage from './pages/OverviewPage';
import MessageDetectorPage from './pages/MessageDetectorPage';
import BatchAnalysisPage from './pages/BatchAnalysisPage';
import ModelIntelligencePage from './pages/ModelIntelligencePage';
import DatasetExplorerPage from './pages/DatasetExplorerPage';
import ValidationLabPage from './pages/ValidationLabPage';
import DocumentationPage from './pages/DocumentationPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<OverviewPage />} />
          <Route path="detector" element={<MessageDetectorPage />} />
          <Route path="analyzer" element={<MessageDetectorPage />} />
          <Route path="batch" element={<BatchAnalysisPage />} />
          <Route path="models" element={<ModelIntelligencePage />} />
          <Route path="dataset" element={<DatasetExplorerPage />} />
          <Route path="validation" element={<ValidationLabPage />} />
          <Route path="documentation" element={<DocumentationPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
