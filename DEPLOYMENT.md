# 🚀 PharmaGuard Deployment Guide

This guide covers deploying PharmaGuard to production environments.

---

## 📋 Pre-Deployment Checklist

- [ ] OpenAI API key obtained
- [ ] GitHub repository created and code pushed
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] Sample VCF files validated
- [ ] Environment variables documented

---

## 🔧 Backend Deployment (Render)

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

### Step 2: Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the `pharmaguard` repository

### Step 3: Configure Service
```
Name: pharmaguard-backend
Region: Oregon (US West) or closest to your users
Branch: main
Root Directory: backend
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

### Step 4: Set Environment Variables
In Render dashboard, add:
```
OPENAI_API_KEY=your_actual_openai_api_key_here
FLASK_ENV=production
```

### Step 5: Deploy
1. Click "Create Web Service"
2. Wait for deployment (2-3 minutes)
3. Note your backend URL: `https://pharmaguard-backend.onrender.com`

### Step 6: Test Backend
```bash
curl https://pharmaguard-backend.onrender.com/health
# Should return: {"status":"ok","service":"PharmaGuard API","version":"1.0.0"}

curl https://pharmaguard-backend.onrender.com/drugs
# Should return list of supported drugs
```

---

## 🎨 Frontend Deployment (Vercel)

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy Frontend
```bash
cd frontend
vercel --prod
```

### Step 4: Configure Environment Variables
When prompted or in Vercel dashboard:
```
REACT_APP_API_URL=https://pharmaguard-backend.onrender.com
```

### Step 5: Verify Deployment
1. Vercel will provide a URL: `https://pharmaguard.vercel.app`
2. Open in browser and test file upload
3. Try analyzing a sample VCF file

---

## 🐳 Alternative: Docker Deployment

### Backend Dockerfile
Create `backend/Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Frontend Dockerfile
Create `frontend/Dockerfile`:
```dockerfile
FROM node:16-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Deploy with Docker Compose
Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_URL=http://localhost:5000
    depends_on:
      - backend
    restart: unless-stopped
```

Run:
```bash
docker-compose up -d
```

---

## ☁️ AWS Deployment

### Backend (Elastic Beanstalk)
```bash
cd backend
eb init -p python-3.9 pharmaguard-backend
eb create pharmaguard-backend-env
eb setenv OPENAI_API_KEY=your_key
eb deploy
```

### Frontend (S3 + CloudFront)
```bash
cd frontend
npm run build
aws s3 sync build/ s3://pharmaguard-frontend
aws cloudfront create-invalidation --distribution-id YOUR_ID --paths "/*"
```

---

## 🔒 Security Configuration

### Backend CORS
Update `app.py` for production:
```python
CORS(app, origins=[
    "https://pharmaguard.vercel.app",
    "https://your-custom-domain.com"
])
```

### Environment Variables
Never commit:
- `.env` files
- API keys
- Secrets

Always use:
- `.env.example` templates
- Platform environment variable managers
- Secret management services (AWS Secrets Manager, etc.)

---

## 📊 Monitoring & Logging

### Render Monitoring
- View logs in Render dashboard
- Set up alerts for errors
- Monitor response times

### Application Logging
Add to `app.py`:
```python
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    logger.info(f"Analysis request received")
    # ... rest of code
```

---

## 🧪 Post-Deployment Testing

### Automated Tests
```bash
# Test backend health
curl https://your-backend-url.com/health

# Test with sample VCF
curl -X POST https://your-backend-url.com/analyze \
  -F "vcf=@sample_vcfs/sample1.vcf" \
  -F "drugs=CODEINE"
```

### Manual Testing Checklist
- [ ] Upload sample1.vcf with CODEINE
- [ ] Upload sample2.vcf with CLOPIDOGREL
- [ ] Test multi-drug analysis
- [ ] Verify JSON download works
- [ ] Test copy-to-clipboard
- [ ] Check mobile responsiveness
- [ ] Verify error handling (invalid file, unsupported drug)

---

## 🔄 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy PharmaGuard

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## 📈 Scaling Considerations

### Backend Scaling
- **Render**: Auto-scaling available on paid plans
- **AWS**: Use Auto Scaling Groups with ALB
- **Horizontal Scaling**: Stateless design allows multiple instances

### Performance Optimization
- Enable gzip compression
- Add Redis caching for repeated analyses
- Implement rate limiting
- Use CDN for frontend assets

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: CORS errors in browser
**Solution**: Update CORS origins in `app.py`

**Issue**: OpenAI API timeout
**Solution**: Increase timeout, implement retry logic

**Issue**: VCF parsing fails
**Solution**: Check VCF format, validate INFO fields

**Issue**: Frontend can't reach backend
**Solution**: Verify REACT_APP_API_URL is set correctly

---

## 📞 Support

For deployment issues:
1. Check logs in platform dashboard
2. Review error messages
3. Consult platform documentation
4. Open GitHub issue with details

---

**Last Updated**: February 2026  
**Maintainer**: Your Name
