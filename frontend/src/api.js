import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'https://pharmaguard-api-ic59.onrender.com';

export const analyzeVCF = async (vcfFile, drugs) => {
  // If API supports multiple drugs
  const response = await axios.post(`${API_BASE}/analyze`, {
    drugs: drugs
  }, {
    headers: { 'Content-Type': 'application/json' }
  });
  return response.data;
};

// Or if you need to make separate calls for each drug:
export const analyzeVCFMulti = async (vcfFile, drugs) => {
  try {
    const results = await Promise.all(
      drugs.map(drug => 
        axios.post(`${API_BASE}/analyze`, {
          drug_name: drug
        }, {
          headers: { 'Content-Type': 'application/json' }
        }).then(res => res.data)
      )
    );
    return results;
  } catch (error) {
    throw error;
  }
};
