import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const analyzeVCF = async (vcfFile, drugs) => {
  const formData = new FormData();
  formData.append('vcf', vcfFile);
  formData.append('drugs', drugs.join(','));
  const response = await axios.post(`${API_BASE}/analyze`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
};