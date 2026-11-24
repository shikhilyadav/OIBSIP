import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/layout/Layout';
import OverviewPage from './pages/OverviewPage';
import MessageAnalyzerPage from './pages/MessageAnalyzerPage';
import ModelIntelligencePage from './pages/ModelIntelligencePage';
import PerformanceAnalyticsPage from './pages/PerformanceAnalyticsPage';
import ThreatIntelligencePage from './pages/ThreatIntelligencePage';
import ScanHistoryPage from './pages/ScanHistoryPage';
import SettingsPage from './pages/SettingsPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<OverviewPage />} />
          <Route path="analyzer" element={<MessageAnalyzerPage />} />
          <Route path="models" element={<ModelIntelligencePage />} />
          <Route path="analytics" element={<PerformanceAnalyticsPage />} />
          <Route path="threat-intel" element={<ThreatIntelligencePage />} />
          <Route path="history" element={<ScanHistoryPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
