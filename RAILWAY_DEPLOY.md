# Railway Deployment Quick Start

Railway is the simplest way to deploy both frontend and backend. Follow these exact steps.

## Step 1: Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (recommended)
3. Authorize Railway to access your repos

## Step 2: Deploy Backend

1. In Railway dashboard, click **New Project**
2. Select **Deploy from GitHub repo**
3. Choose your `fraud_detection` repository
4. Railway auto-detects `Procfile` in `backend/`
5. Go to **Variables** tab → Add:
   ```
   PYTHONUNBUFFERED=1
   ```
6. Railway auto-deploys! ✅
7. In **Settings** tab, copy your service URL:
   ```
   https://fraud-api-prod-xxxxxxxx.railway.app
   ```

## Step 3: Update Frontend Config

Before deploying frontend, set the backend URL:

1. In your local `fraud_detection` folder, edit `frontend/netlify.toml`:
   ```toml
   [context.production.environment]
     VITE_API_URL = "https://fraud-api-prod-xxxxxxxx.railway.app"
   ```
   (Replace with your Railway backend URL)

2. Commit and push:
   ```bash
   git add frontend/netlify.toml
   git commit -m "Update backend URL for production"
   git push origin main
   ```

## Step 4: Deploy Frontend to Netlify

1. Go to [netlify.com](https://netlify.com)
2. Click **Add new site** → **Import an existing project**
3. Authorize GitHub
4. Select `fraud_detection` repository
5. **Configure**:
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Environment variable `VITE_API_URL`: (your Railway URL)
6. **Deploy site**
7. Netlify assigns you a URL like `https://fraud-detection-xxx.netlify.app`

## Step 5: Test It Works

1. Open your Netlify frontend URL in browser
2. You should see the fraud detection dashboard
3. Try uploading a CSV file
4. If it works, you're done! 🎉

---

## Troubleshooting

### Backend not responding
- Check Railway dashboard for errors in Logs
- Verify `Procfile` exists in `backend/`
- Ensure Python version is 3.9+

### Frontend shows CORS error
- Check browser DevTools → Network tab
- The `VITE_API_URL` must match your Railway backend URL exactly
- Update `netlify.toml` and redeploy

### Uploads fail
- Verify backend is running (`/api/health` returns 200)
- Check backend logs for errors
- Ensure CSV has required columns: `transaction_id`, `transaction_amount`

---

## Production URLs

Once deployed, share this:
```
Frontend: https://fraud-detection-xxx.netlify.app
```

**Keep backend URL private** (only used by frontend).

---

## Cost

- **Railway**: Free tier (limited) → ~$5-20/month for backend
- **Netlify**: Free tier sufficient for frontend
- **Total**: ~$5-20/month for production

To monitor costs on Railway:
- Dashboard → **Usage** tab
- Set budget alerts in **Settings**

