# 🚀 Deployment Checklist

## Pre-Deployment (Local)

- [ ] Run tests: `cd backend && pytest -q` (all pass)
- [ ] Build frontend: `cd frontend && npm run build` (succeeds)
- [ ] Run backend locally: `cd backend && uvicorn main:app --port 5000` (no errors)
- [ ] Test API: `curl http://localhost:5000/api/health` (returns 200)
- [ ] No sensitive data in `.env` files (use .env.example template instead)
- [ ] All dependencies listed in `requirements.txt` and `package.json`
- [ ] Git history clean: `git log --oneline` shows clear commits

---

## Backend Deployment (Railway / Heroku)

### Step 1: Prepare
- [ ] Copy backend `.env.example` → `.env` and fill values
- [ ] Ensure `Procfile` exists in backend folder
- [ ] `requirements.txt` is updated: `pip freeze > requirements.txt`

### Step 2: Railway (Recommended)
- [ ] Create Railway account at [railway.app](https://railway.app)
- [ ] Connect GitHub repository
- [ ] Create service from `backend` directory
- [ ] Set environment variables in Railway dashboard
- [ ] Deploy — Railway auto-builds and starts service
- [ ] Copy service URL (e.g., `https://fraud-api-prod-xxx.railway.app`)

### Step 3: Test Backend
- [ ] `curl https://your-backend-url/api/health` returns `{"status":"healthy"}`
- [ ] `POST /api/upload` accepts CSV file
- [ ] `/api/results` returns JSON data
- [ ] Logs visible in Railway dashboard (no errors)

---

## Frontend Deployment (Netlify / Vercel)

### Step 1: Prepare Frontend
- [ ] Backend URL confirmed (from Railway/Heroku)
- [ ] Create `.env.local` in frontend with `VITE_API_URL=https://your-backend-url`
- [ ] Test locally: `npm run dev` connects to backend
- [ ] Commit changes and push to GitHub

### Step 2: Netlify
- [ ] Connect GitHub to Netlify
- [ ] Select `fraud_detection` repository
- [ ] Base directory: `frontend`
- [ ] Build command: `npm run build`
- [ ] Publish directory: `dist`
- [ ] Add environment variable: `VITE_API_URL=https://your-backend-url`
- [ ] Deploy — Netlify auto-builds
- [ ] Copy site URL (e.g., `https://fraud-detection-app.netlify.app`)

### Step 3: Vercel
- [ ] Sign in to Vercel
- [ ] Import GitHub repository
- [ ] Root directory: `frontend`
- [ ] Framework preset: Vite
- [ ] Add environment variable: `VITE_API_URL=https://your-backend-url`
- [ ] Deploy — Vercel auto-builds
- [ ] Copy site URL (e.g., `https://fraud-detection-app.vercel.app`)

---

## Post-Deployment Testing

### From Browser
- [ ] Frontend loads at `https://your-frontend-url`
- [ ] Dashboard displays with blue background
- [ ] No console errors (DevTools → Console)
- [ ] No CORS errors in Network tab
- [ ] File upload works (drop zone visible)
- [ ] Risk Analysis tab loads
- [ ] Export button calls backend

### From Terminal
```bash
# Test backend
curl https://your-backend-url/api/health

# Test frontend
curl https://your-frontend-url | grep -q "Fraud Detection" && echo "✓ Frontend OK"

# Test full flow (if backend has demo data)
curl -L https://your-frontend-url/api/transactions
```

---

## Monitoring & Logs

### Railway
- [ ] Dashboard shows green "Running" status
- [ ] Logs show startup messages (clean startup)
- [ ] No recurring error patterns in logs

### Netlify
- [ ] Build logs show success
- [ ] Deploy preview tests passing
- [ ] Site loads from CDN edge (fast response)

### Vercel
- [ ] Deployment status shows success
- [ ] Analytics dashboard functional
- [ ] Performance metrics visible

---

## Rollback Plan

If deployment fails:
1. **Frontend**: Netlify/Vercel auto-reverts to previous build on failed deploy
   - Or manually select previous deployment in dashboard
2. **Backend**: Railway/Heroku keeps previous version running
   - Redeploy from main branch or select previous release

---

## Security Sign-Off

- [ ] No `.env` file committed to Git
- [ ] Backend API requires HTTPS (default on Railway/Heroku)
- [ ] Frontend uses secure cookies for sessions (if added)
- [ ] API rate-limiting enabled (optional: add to FastAPI)
- [ ] CORS policy set correctly (frontend + backend domains)

---

## Final Verification

- [ ] Frontend URL accessible from anywhere
- [ ] Backend API responds within 2 seconds
- [ ] File upload → analyze → results completes in < 30 seconds
- [ ] No 5xx errors in backend logs
- [ ] All environmental variables correctly set in production

---

## 🎉 Deployment Complete!

Your fraud detection system is now live at:
- **Frontend**: `https://your-frontend-url`
- **Backend API**: `https://your-backend-url`
- **Health check**: `https://your-backend-url/api/health`

Share the frontend URL with users. Keep backend URL private or use API keys for production.

