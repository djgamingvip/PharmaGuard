import React from 'react';

const riskColors = {
  'Safe': 'bg-green-100 text-green-800 border-green-300',
  'Adjust Dosage': 'bg-yellow-100 text-yellow-800 border-yellow-300',
  'Toxic': 'bg-red-100 text-red-800 border-red-300',
  'Ineffective': 'bg-orange-100 text-orange-800 border-orange-300',
  'Unknown': 'bg-gray-100 text-gray-800 border-gray-300'
};

const severityIcons = {
  'none': '✓',
  'low': 'ℹ',
  'moderate': '⚠',
  'high': '⚠',
  'critical': '⛔',
  'unknown': '?'
};

export default function ResultsCard({ result }) {
  const riskClass = riskColors[result.risk_assessment.risk_label] || riskColors['Unknown'];
  
  const downloadJSON = () => {
    const dataStr = JSON.stringify(result, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `pharmaguard_${result.drug}_${result.patient_id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };
  
  const copyJSON = () => {
    navigator.clipboard.writeText(JSON.stringify(result, null, 2));
    alert('JSON copied to clipboard!');
  };
  
  return (
    <div className="border-2 p-6 rounded-lg shadow-lg bg-white">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div>
          <h3 className="text-2xl font-bold text-gray-800">{result.drug}</h3>
          <p className="text-sm text-gray-600">Patient: {result.patient_id}</p>
          <p className="text-xs text-gray-500">{new Date(result.timestamp).toLocaleString()}</p>
        </div>
        <div className={`px-4 py-2 rounded-lg border-2 font-bold text-lg ${riskClass}`}>
          {severityIcons[result.risk_assessment.severity]} {result.risk_assessment.risk_label}
        </div>
      </div>
      
      {/* Risk Assessment */}
      <div className="mb-4 p-4 bg-gray-50 rounded">
        <h4 className="font-semibold mb-2">Risk Assessment</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-600">Confidence:</span>{' '}
            <span className="font-medium">{(result.risk_assessment.confidence_score * 100).toFixed(0)}%</span>
          </div>
          <div>
            <span className="text-gray-600">Severity:</span>{' '}
            <span className="font-medium capitalize">{result.risk_assessment.severity}</span>
          </div>
        </div>
      </div>
      
      {/* Pharmacogenomic Profile */}
      <div className="mb-4 p-4 bg-blue-50 rounded">
        <h4 className="font-semibold mb-2">Pharmacogenomic Profile</h4>
        <div className="space-y-1 text-sm">
          <p><span className="text-gray-600">Gene:</span> <span className="font-mono font-medium">{result.pharmacogenomic_profile.primary_gene}</span></p>
          <p><span className="text-gray-600">Diplotype:</span> <span className="font-mono font-medium">{result.pharmacogenomic_profile.diplotype}</span></p>
          <p><span className="text-gray-600">Phenotype:</span> <span className="font-medium">{result.pharmacogenomic_profile.phenotype}</span></p>
        </div>
        
        {result.pharmacogenomic_profile.detected_variants.length > 0 && (
          <details className="mt-2">
            <summary className="cursor-pointer text-blue-700 font-medium">
              Detected Variants ({result.pharmacogenomic_profile.detected_variants.length})
            </summary>
            <ul className="mt-2 space-y-1 text-xs">
              {result.pharmacogenomic_profile.detected_variants.map((v, idx) => (
                <li key={idx} className="font-mono bg-white p-2 rounded">
                  {v.rsid} - {v.gene} {v.allele}
                </li>
              ))}
            </ul>
          </details>
        )}
      </div>
      
      {/* Clinical Recommendation */}
      <div className="mb-4 p-4 bg-purple-50 rounded">
        <h4 className="font-semibold mb-2">Clinical Recommendation</h4>
        <p className="text-sm mb-2">{result.clinical_recommendation.recommendation}</p>
        <p className="text-xs text-gray-600">Source: {result.clinical_recommendation.guideline_source}</p>
        
        {result.clinical_recommendation.alternative_drugs.length > 0 && (
          <div className="mt-2">
            <p className="text-xs font-medium text-gray-700">Alternative Drugs:</p>
            <p className="text-xs text-gray-600">{result.clinical_recommendation.alternative_drugs.join(', ')}</p>
          </div>
        )}
      </div>
      
      {/* LLM Explanation */}
      <details className="mb-4">
        <summary className="cursor-pointer font-semibold text-green-700 bg-green-50 p-3 rounded">
          AI-Generated Explanation
        </summary>
        <div className="mt-2 p-4 bg-green-50 rounded space-y-2 text-sm">
          <div>
            <p className="font-medium text-gray-700">Summary:</p>
            <p className="text-gray-800">{result.llm_generated_explanation.summary}</p>
          </div>
          <div>
            <p className="font-medium text-gray-700">Mechanism:</p>
            <p className="text-gray-800">{result.llm_generated_explanation.mechanism}</p>
          </div>
          <div>
            <p className="font-medium text-gray-700">Variant Impact:</p>
            <p className="text-gray-800">{result.llm_generated_explanation.variant_impact}</p>
          </div>
        </div>
      </details>
      
      {/* Quality Metrics */}
      <div className="mb-4 p-3 bg-gray-50 rounded text-xs">
        <h4 className="font-semibold mb-1">Quality Metrics</h4>
        <div className="flex gap-4">
          <span>VCF Parsing: {result.quality_metrics.vcf_parsing_success ? '✓' : '✗'}</span>
          <span>Missing Annotations: {result.quality_metrics.missing_annotations ? 'Yes' : 'No'}</span>
          <span>Confidence: {result.quality_metrics.confidence_level}</span>
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="flex gap-2">
        <button 
          onClick={copyJSON}
          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
        >
          📋 Copy JSON
        </button>
        <button 
          onClick={downloadJSON}
          className="flex-1 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition"
        >
          ⬇ Download JSON
        </button>
      </div>
    </div>
  );
}