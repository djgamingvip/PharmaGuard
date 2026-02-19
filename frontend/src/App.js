import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import DrugInput from './components/DrugInput';
import ResultsCard from './components/ResultsCard';
import { analyzeVCF } from './api';

function App() {
  const [vcfFile, setVcfFile] = useState(null);
  const [drug, setDrug] = useState(''); // Changed from drugs array to single drug
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!vcfFile || !drug) {
      setError('Please select a VCF file and enter a drug name.');
      return;
    }
    setLoading(true);
    setError('');
    setResults(null);
    try {
      const data = await analyzeVCF(vcfFile, [drug]); // Pass as array or single value
      setResults(data);
    } catch (err) {
      setError(err.response?.data?.error || err.message || 'Analysis failed');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setVcfFile(null);
    setDrug('');
    setResults(null);
    setError('');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      <div className="container mx-auto p-4 max-w-5xl">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🧬 PharmaGuard
          </h1>
          <p className="text-lg text-gray-600">
            Pharmacogenomic Risk Prediction System
          </p>
          <p className="text-sm text-gray-500 mt-1">
            AI-powered drug safety analysis using genetic data
          </p>
        </div>

        {/* Input Form */}
        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <FileUpload onFileSelect={setVcfFile} />
            {vcfFile && (
              <div className="text-sm text-green-700 bg-green-50 p-2 rounded">
                ✓ Selected: {vcfFile.name} ({(vcfFile.size / 1024).toFixed(1)} KB)
              </div>
            )}
            
            {/* Updated DrugInput to handle single drug */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-700">
                Drug Name
              </label>
              <input
                type="text"
                value={drug}
                onChange={(e) => setDrug(e.target.value)}
                placeholder="Enter drug name (e.g., warfarin)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <p className="text-xs text-gray-500">
                Enter a single drug name for analysis
              </p>
            </div>

            <div className="flex gap-2">
              <button 
                type="submit" 
                disabled={loading || !vcfFile || !drug}
                className="flex-1 bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {loading ? '🔄 Analyzing...' : '🔬 Analyze Risk'}
              </button>
              {(vcfFile || results) && (
                <button 
                  type="button"
                  onClick={handleReset}
                  className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg font-semibold hover:bg-gray-300 transition"
                >
                  Reset
                </button>
              )}
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-100 border-2 border-red-300 text-red-800 p-4 rounded-lg mb-6">
            <p className="font-semibold">⚠ Error</p>
            <p>{error}</p>
          </div>
        )}

        {/* Results Display */}
        {results && (
          <div className="space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-800">Analysis Results</h2>
              <p className="text-sm text-gray-600">
                Drug: {drug}
              </p>
            </div>
            <ResultsCard result={results} />
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 pb-8 text-sm text-gray-500">
          <p>PharmaGuard v1.0 | RIFT 2026 Hackathon</p>
          <p className="mt-1">
            Powered by CPIC Guidelines & AI | For research purposes only
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
