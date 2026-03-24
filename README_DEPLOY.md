# 🚀 Fraud Detection System — Deployment Guide

Your fraud detection system is enterprise-ready and deployment-tested. This guide covers everything needed to go live.

---

## 📦 What's Included

### Deployment Configuration Files
- ✅ `netlify.toml` — Frontend deployment to Netlify
- ✅ `vercel.json` — Frontend deployment to Vercel
- ✅ `backend/Procfile` — Backend deployment to Railway/Heroku
- ✅ `.github/workflows/ci-cd.yml` — Automated testing on GitHub push
- ✅ `.env.example` — Environment variable template

### Documentation
- ✅ `DEPLOY.md` — Complete deployment guide (all platforms)
- ✅ `RAILWAY_DEPLOY.md` — Railway quick-start (recommended)
- ✅ `DEPLOYMENT_CHECKLIST.md` — Pre & post-deployment checklist

---

## 🎯 Quick Start (5 Minutes)

### Option A: Railway + Netlify (Easiest)

**Backend (Railway):**
```bash
# 1. Push code to GitHub
git push origin main

# 2. Visit railway.app → New Project → Deploy from GitHub
# 3. Select fraud_detection repo → Railway auto-deploys
# 4. Copy backend URL from Railway dashboard
```

**Frontend (Netlify):**
```bash
# 1. Update frontend/netlify.toml with your backend URL
# 2. Visit netlify.com → Add site → Import from GitHub
# 3. Base: frontend, Build: npm run build, Publish: dist
# 4. Add env var VITE_API_URL = <your-railway-url>
# 5. Netlify auto-deploys
```

**Time:** ~10 minutes | **Cost:** ~$5-20/month

---

### Option B: Vercel + Heroku

**Backend (Heroku):**
```bash
git subtree push --prefix backend heroku main
```

**Frontend (Vercel):**
```bash
# 1. Import repo from Vercel dashboard
# 2. Root: frontend, Add VITE_API_URL env var
# 3. Deploy
```

**Time:** ~15 minutes | **Cost:** Free → ~$7/month

---

## ✅ Pre-Deployment Checklist

Run these locally first:

```bash
# 1. Test backend
cd backend
pytest -q                    # All tests pass ✓
uvicorn main:app --port 5000 # Starts without errors ✓

# 2. Test frontend
cd ../frontend
npm run build                # Build succeeds ✓
npm run dev                  # Dev server works ✓

# 3. Verify configuration
ls netlify.toml vercel.json  # Both exist ✓
ls ../backend/Procfile       # Exists ✓
```

---

## 🌐 Supported Platforms

| Platform | Frontend | Backend | Cost | Ease |
|----------|----------|---------|------|------|
| **Netlify** | ✅ | ❌ | Free | Easy |
| **Vercel** | ✅ | ❌ | Free | Easy |
| **Railway** | ❌ | ✅ | $5-20 | Easy |
| **Heroku** | ❌ | ✅ | $7+ | Medium |
| **AWS EC2** | ✅ | ✅ | $5-50 | Hard |
| **Docker (any cloud)** | ✅ | ✅ | Varies | Varies |

**Recommended:** Railway (backend) + Netlify/Vercel (frontend)

---

## 📋 Detailed Guides

For step-by-step instructions, see:

1. **[RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)** — Railway quick-start (recommended)
2. **[DEPLOY.md](./DEPLOY.md)** — Complete multi-platform guide
3. **[DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md)** — Pre/post-deployment checks

---

## 🔑 Environment Variables

### Frontend (`frontend/.env.local`)
```
VITE_API_URL=https://your-backend-url.com
```

### Backend (`backend/.env`)
```
REDIS_URL=redis://localhost:6379
PYTHONUNBUFFERED=1
```

Use `.env.example` templates. **Never commit `.env` files.**

---

## 🧪 Post-Deployment Tests

After both frontend and backend are live:

```bash
# 1. Test backend API
curl https://your-backend-url/api/health

# 2. Test frontend
curl https://your-frontend-url | grep "Fraud Detection"

# 3. Full flow
# - Open frontend in browser
# - Upload sample CSV
# - View results
```

---

## 🔐 Security Notes

- ✅ No `.env` file committed (in `.gitignore`)
- ✅ API URLs use HTTPS only
- ✅ Backend logs don't expose secrets
- ✅ CORS configured for frontend domain
- ✅ Database credentials in environment variables

---

## 📊 Monitoring

- **Railway**: Logs visible in dashboard
- **Netlify**: Deploy logs & build status
- **Vercel**: Analytics & performance metrics
- **GitHub**: CI/CD workflow status in Actions tab

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Frontend shows blank page | Check `VITE_API_URL` env var |
| CORS errors in browser | Verify backend is running, check URL |
| Upload fails | Check backend logs on Railway/Heroku |
| Tests fail in CI/CD | Run `pytest -q` and `npm run build` locally first |
| Slow performance | Check Railway/Heroku logs for bottlenecks |

---

## 💡 Next Steps

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Deployment ready"
   git push origin main
   ```

2. **Deploy backend**
   - Follow [RAILWAY_DEPLOY.md](./RAILWAY_DEPLOY.md)

3. **Deploy frontend**
   - Update `frontend/netlify.toml` with backend URL
   - Push and Netlify auto-deploys

4. **Test**
   - Open frontend URL in browser
   - Run full flow (upload → analyze → results)

5. **Monitor**
   - Check logs regularly
   - Set up alerts for errors

---

## 🎉 You're Live!

Once deployed, your system is:
- ✅ Accessible from anywhere
- ✅ Auto-scaling with traffic
- ✅ Backed by CI/CD testing
- ✅ Monitored and secure

**Estimated time to deployment: 30-60 minutes**

---

## 📞 Support

- Railway docs: [docs.railway.app](https://docs.railway.app)
- Netlify docs: [docs.netlify.com](https://docs.netlify.com)
- Vercel docs: [vercel.com/docs](https://vercel.com/docs)
- FastAPI docs: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- React docs: [react.dev](https://react.dev)

---

**Built with ❤️ | Ready for production 🚀**
