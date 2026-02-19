import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://pharmaguard-api-ic59.onrender.com';

export const analyzeVCF = async (vcfFile, drugs) => {
  // Based on your API test, it seems to expect a single drug
  // For multiple drugs, you might need to make multiple calls
  const drugName = Array.isArray(drugs) ? drugs[0] : drugs;
  
  const response = await axios.post(`${API_BASE}/analyze`, {
    drug_name: drugName
  }, {
    headers: { 'Content-Type': 'application/json' }
  });
  
  // Since the response might be an array of results or a single result
  return response.data;
};
