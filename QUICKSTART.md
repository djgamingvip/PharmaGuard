# ⚡ PharmaGuard Quick Start Guide

Get PharmaGuard running in 5 minutes!

---

## 🎯 Prerequisites

- Python 3.9+ installed
- Node.js 16+ installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

---

## 🚀 Quick Setup

### 1️⃣ Clone & Navigate
```bash
git clone https://github.com/yourusername/pharmaguard.git
cd pharmaguard
```

### 2️⃣ Backend Setup (2 minutes)
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Edit .env and add your OpenAI API key
# Windows: notepad .env
# Mac/Linux: nano .env
# Add: OPENAI_API_KEY=your_actual_key_here

# Start backend server
python app.py
```

Backend will run on `http://localhost:5000` ✅

### 3️⃣ Frontend Setup (2 minutes)
Open a NEW terminal window:

```bash
# Navigate to frontend
cd pharmaguard/frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will open automatically at `http://localhost:3000` ✅

---

## 🧪 Test the System

### Option 1: Web Interface
1. Open `http://localhost:3000` in your browser
2. Drag and drop `sample_vcfs/sample1.vcf`
3. Enter drug name: `CODEINE`
4. Click "Analyze Risk"
5. View results!

### Option 2: API Test
```bash
# In a new terminal
cd pharmaguard

# Test with curl
curl -X POST http://localhost:5000/analyze \
  -F "vcf=@sample_vcfs/sample1.vcf" \
  -F "drugs=CODEINE"
```

### Option 3: Automated Test Script
```bash
cd pharmaguard
python test_system.py
```

---

## 📊 Sample Test Cases

### Test Case 1: Single Drug
- **File**: `sample_vcfs/sample1.vcf`
- **Drug**: `CODEINE`
- **Expected**: Risk assessment with CYP2D6 variants

### Test Case 2: Multiple Drugs
- **File**: `sample_vcfs/sample2.vcf`
- **Drugs**: `CLOPIDOGREL,AZATHIOPRINE,FLUOROURACIL`
- **Expected**: Array of 3 risk assessments

### Test Case 3: All Supported Drugs
- **File**: `sample_vcfs/sample1.vcf`
- **Drugs**: `CODEINE,WARFARIN,CLOPIDOGREL,SIMVASTATIN,AZATHIOPRINE,FLUOROURACIL`
- **Expected**: 6 risk assessments

---

## 🎨 What You Should See

### Successful Analysis
```
✓ VCF file uploaded
✓ Variants detected: CYP2D6 *4/*10
✓ Risk: Ineffective (Poor Metabolizer)
✓ Recommendation: Avoid codeine, use alternative
✓ AI Explanation generated
```

### Color-Coded Results
- 🟢 **Green**: Safe
- 🟡 **Yellow**: Adjust Dosage
- 🔴 **Red**: Toxic / Ineffective
- ⚪ **Gray**: Unknown

---

## 🔧 Troubleshooting

### Backend won't start
**Error**: `ModuleNotFoundError: No module named 'flask'`  
**Fix**: Make sure virtual environment is activated and dependencies installed
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Frontend won't start
**Error**: `npm ERR! missing script: start`  
**Fix**: Make sure you're in the `frontend` directory
```bash
cd frontend
npm install
npm start
```

### OpenAI API Error
**Error**: `AuthenticationError: Invalid API key`  
**Fix**: Check your `.env` file has correct API key
```bash
cat backend/.env  # Should show: OPENAI_API_KEY=sk-...
```

### CORS Error in Browser
**Error**: `Access-Control-Allow-Origin`  
**Fix**: Make sure backend is running on port 5000
```bash
# Check if backend is running
curl http://localhost:5000/health
```

---

## 📚 Next Steps

1. ✅ **Read Full Documentation**: See [README.md](README.md)
2. 🚀 **Deploy to Production**: See [DEPLOYMENT.md](DEPLOYMENT.md)
3. 🧪 **Run Full Tests**: `python test_system.py`
4. 📊 **Explore API**: Try different VCF files and drug combinations
5. 🎥 **Create Demo Video**: Record your analysis for LinkedIn

---

## 💡 Pro Tips

- Use the drug suggestion buttons in the UI for quick input
- Download JSON results for documentation
- Test with both sample VCF files to see different variants
- Check the AI explanation section for detailed insights
- Monitor backend logs for debugging: `tail -f backend/logs/app.log`

---

## 🆘 Need Help?

- **Documentation**: [README.md](README.md)
- **API Reference**: [README.md#api-documentation](README.md#api-documentation)
- **Issues**: [GitHub Issues](https://github.com/yourusername/pharmaguard/issues)
- **Email**: your.email@example.com

---

## ✅ Checklist

Before submitting to RIFT 2026:

- [ ] Backend running without errors
- [ ] Frontend displays correctly
- [ ] Sample VCF files analyzed successfully
- [ ] JSON output matches required schema
- [ ] AI explanations generated
- [ ] Deployed to production (Vercel + Render)
- [ ] README updated with live URLs
- [ ] Demo video recorded and posted on LinkedIn
- [ ] GitHub repository public

---

**Ready to deploy?** See [DEPLOYMENT.md](DEPLOYMENT.md)

**Questions?** Open an issue or reach out!

---

Made with ❤️ for RIFT 2026 Hackathon
