import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import OverviewPage from './pages/OverviewPage';
import PricePredictorPage from './pages/PricePredictorPage';
import DataExplorerPage from './pages/DataExplorerPage';
import ModelIntelligencePage from './pages/ModelIntelligencePage';
import EvaluationPage from './pages/EvaluationPage';
import DocumentationPage from './pages/DocumentationPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<OverviewPage />} />
          <Route path="predictor" element={<PricePredictorPage />} />
          <Route path="dataset" element={<DataExplorerPage />} />
          <Route path="models" element={<ModelIntelligencePage />} />
          <Route path="evaluation" element={<EvaluationPage />} />
          <Route path="documentation" element={<DocumentationPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
