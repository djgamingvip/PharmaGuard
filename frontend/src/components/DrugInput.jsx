import React, { useState } from 'react';

const SUPPORTED_DRUGS = ['CODEINE', 'WARFARIN', 'CLOPIDOGREL', 'SIMVASTATIN', 'AZATHIOPRINE', 'FLUOROURACIL'];

export default function DrugInput({ onDrugsChange }) {
  const [input, setInput] = useState('');
  const [suggestions, setShowSuggestions] = useState(false);
  
  const handleChange = (e) => {
    const value = e.target.value;
    setInput(value);
    onDrugsChange(value.split(',').map(d => d.trim()).filter(d => d));
  };
  
  const addDrug = (drug) => {
    const current = input ? input.split(',').map(d => d.trim()) : [];
    if (!current.includes(drug)) {
      const newInput = [...current, drug].join(', ');
      setInput(newInput);
      onDrugsChange(newInput.split(',').map(d => d.trim()).filter(d => d));
    }
  };
  
  return (
    <div>
      <label className="block mb-2 font-semibold text-gray-700">
        Drug(s) to Analyze
      </label>
      <input
        type="text"
        value={input}
        onChange={handleChange}
        onFocus={() => setShowSuggestions(true)}
        onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
        placeholder="e.g., CODEINE, WARFARIN"
        className="border-2 border-gray-300 p-3 w-full rounded-lg focus:border-blue-500 focus:outline-none"
      />
      <p className="text-xs text-gray-500 mt-1">
        Enter one or more drugs (comma-separated)
      </p>
      
      {suggestions && (
        <div className="mt-2 p-3 bg-gray-50 rounded-lg border">
          <p className="text-xs font-semibold text-gray-600 mb-2">Supported Drugs:</p>
          <div className="flex flex-wrap gap-2">
            {SUPPORTED_DRUGS.map(drug => (
              <button
                key={drug}
                type="button"
                onMouseDown={() => addDrug(drug)}
                className="px-3 py-1 bg-blue-100 text-blue-800 rounded text-xs hover:bg-blue-200 transition"
              >
                + {drug}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}