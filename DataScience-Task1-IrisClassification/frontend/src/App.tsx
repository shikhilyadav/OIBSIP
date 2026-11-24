import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import OverviewPage from './pages/OverviewPage';
import ClassifierPage from './pages/ClassifierPage';
import DatasetExplorerPage from './pages/DatasetExplorerPage';
import SpeciesInsightsPage from './pages/SpeciesInsightsPage';
import PerformancePage from './pages/PerformancePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<OverviewPage />} />
          <Route path="classifier" element={<ClassifierPage />} />
          <Route path="dataset" element={<DatasetExplorerPage />} />
          <Route path="insights" element={<SpeciesInsightsPage />} />
          <Route path="performance" element={<PerformancePage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
