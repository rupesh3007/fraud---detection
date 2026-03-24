# Fraud Detection System — Deployment Guide

## 📋 Overview

This is a full-stack fraud detection system:
- **Frontend**: React + Vite (deploys to Netlify/Vercel)
- **Backend**: FastAPI + scikit-learn (deploys to Railway, Heroku, AWS, DigitalOcean, etc.)

---

## 🚀 Frontend Deployment (Netlify / Vercel)

### Deploy to Netlify

1. **Connect repository** to Netlify (GitHub/GitLab)
2. **Select site settings**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
3. **Set environment variables** under `Site settings → Build & deploy → Environment`:
   - `VITE_API_URL`: Your backend URL (e.g., `https://fraud-api.railway.app`)
4. **Deploy** — Netlify auto-builds on push

### Deploy to Vercel

1. **Import project** from GitHub to Vercel dashboard
2. **Configure root path**: `frontend` directory
3. **Build settings** (auto-detected):
   - Framework: Vite
   - Build command: `npm run build`
   - Output directory: `dist`
4. **Environment variables**:
   - `VITE_API_URL`: Your backend URL
5. **Deploy** — auto-deployment on main branch push

---

## 🐍 Backend Deployment

### Prerequisites
- Python 3.9+
- Backend code: `backend/` folder
- Requirements: `backend/requirements.txt`

### Option 1: Deploy to Railway (Recommended — Easy)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Create new project** from repo
4. **Select `backend` directory** as root
5. **Add `Procfile`** in backend folder:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
   ```
6. **Environment variables** (Railway dashboard):
   - `PYTHONUNBUFFERED=1`
   - Any `.env` vars from template
7. **Deploy** — Railway auto-detects and runs

**Result**: API URL like `https://fraud-api-prod-xxxx.railway.app`

---

### Option 2: Deploy to Heroku

1. **Install Heroku CLI**
2. **Login**: `heroku login`
3. **Create app**: `heroku create your-fraud-api`
4. **Add Procfile** in backend:
   ```
   web: gunicorn -w 4 -b 0.0.0.0:$PORT main:app
   ```
5. **Deploy**:
   ```bash
   git push heroku main
   ```
6. Set vars: `heroku config:set PYTHONUNBUFFERED=1`

**Result**: API URL like `https://your-fraud-api.herokuapp.com`

---

### Option 3: Deploy to AWS Lambda + API Gateway

1. **Use Serverless Framework**:
   ```bash
   npm install -g serverless
   ```
2. **Create `serverless.yml`** in backend with FastAPI handler
3. **Deploy**:
   ```bash
   serverless deploy
   ```

---

### Option 4: Docker + Any Cloud (AWS ECS, GCP Cloud Run, etc.)

1. **Backend `Dockerfile`** already exists
2. **Build image**:
   ```bash
   docker build -t fraud-api:latest backend/
   ```
3. **Push to Docker Registry** (Docker Hub, ECR, GCR, etc.)
4. **Deploy to container cloud** (AWS ECS, GCP Cloud Run, DigitalOcean App Platform, etc.)

---

## 🔗 Connect Frontend → Backend

After deploying backend:

1. **Copy backend URL** (e.g., `https://fraud-api-prod.railway.app`)
2. **Frontend environment variable**:
   - **Netlify**: Site settings → `VITE_API_URL=https://fraud-api-prod.railway.app`
   - **Vercel**: Project settings → `VITE_API_URL=https://fraud-api-prod.railway.app`
3. **Redeploy frontend** to apply new API URL

---

## 🧪 Post-Deploy Verification

After both frontend and backend are live:

```bash
# Test backend health
curl https://your-fraud-api.com/api/health

# Test frontend load
# Visit: https://your-frontend.netlify.app or https://your-frontend.vercel.app
```

Check browser console for any CORS or connection errors.

---

## 🔐 Security Checklist

- [ ] Backend `.env` file not committed (`.gitignore` has it)
- [ ] Database credentials in environment variables, not code
- [ ] Frontend API URL points to production backend
- [ ] CORS configured in FastAPI for frontend domain
- [ ] No debug logs in production (`DEBUG=False`)
- [ ] Use HTTPS for all URLs
- [ ] Keep dependencies updated

---

## 📊 Monitoring

- **Netlify**: Deployment logs, function logs
- **Vercel**: Analytics, error tracking integration
- **Backend**: Use platform logging (Railway/Heroku dashboard)

---

## 🛠️ Troubleshooting

| Issue | Solution |
|---|---|
| Frontend gets 404 on API calls | Check `VITE_API_URL` env var, verify backend is running |
| CORS errors | Add `Access-Control-Allow-Origin: *` in FastAPI |
| Backend crashes on small upload | Tested; should handle edge cases now |
| Tests fail in CI/CD | Run `pytest` locally first: `cd backend && pytest -q` |

---

## 📝 Next Steps

1. Deploy backend to Railway/Heroku
2. Get backend domain URL
3. Deploy frontend with correct `VITE_API_URL`
4. Test full flow end-to-end
5. Monitor logs for errors

**Questions?** Refer to platform docs or reach out! 🚀
