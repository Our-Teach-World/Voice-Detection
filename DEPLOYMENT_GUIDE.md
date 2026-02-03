# 🚀 Free Hosting Deployment Guide

## Option 1: **Railway** (RECOMMENDED - Easiest) ⭐

Railway is the **easiest free option** with generous free tier (5 GB storage, good for our project).

### Steps:

#### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/voice-detection.git
git push -u origin main
```

#### 2. Deploy on Railway
1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repository
5. Railway auto-detects Python and reads Procfile
6. Wait for deployment (~5-10 minutes)

#### 3. Get Your Public URL
- Railway provides: `https://your-app-name.railway.app`
- Your API endpoint: `https://your-app-name.railway.app/api/voice-detection`

#### 4. Test API
```bash
curl -X POST https://your-app-name.railway.app/api/voice-detection \
  -H "x-api-key: sk_test_123456789" \
  -H "Content-Type: application/json" \
  -d '{"language":"Hindi","audioFormat":"mp3","audioBase64":"..."}'
```

**Pros:**
- ✅ Free tier: 5GB memory + good CPU
- ✅ Auto-deploys from GitHub
- ✅ Custom domain support
- ✅ Environment variables support

**Cons:**
- ❌ Limited free tier (may not support heavy PyTorch model)

---

## Option 2: **Render** (Good Alternative)

Render offers good free tier with Python support.

### Steps:

1. Go to https://render.com
2. Sign up with GitHub
3. Create "New Web Service"
4. Connect your GitHub repo
5. Fill details:
   - Build command: `pip install -r requirements_deploy.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

**Pros:**
- ✅ Free tier with good performance
- ✅ Auto-deploys from GitHub
- ✅ Custom domain

**Cons:**
- ❌ Spins down after inactivity (slow first request)

---

## Option 3: **Replit** (Fastest Setup)

Perfect for quick deployment without GitHub.

### Steps:

1. Go to https://replit.com
2. Sign up
3. Click "Create Repl" → "Import from GitHub" OR upload files
4. Create `.replit` file:
```
run = "uvicorn main:app --host 0.0.0.0 --port 8000"
```
5. Click "Run"
6. Share link: `https://your-replit-name.replit.dev`

**Pros:**
- ✅ Instant setup
- ✅ No GitHub required
- ✅ Web IDE included

**Cons:**
- ❌ Spins down after inactivity
- ❌ Limited resources

---

## Option 4: **Google Cloud Run** (Serverless)

Free tier: 2 million requests/month.

### Steps:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements_deploy.txt .
RUN pip install -r requirements_deploy.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

2. Push to GitHub
3. Connect to Google Cloud Run
4. Deploy (free tier: 2M requests/month)

**Pros:**
- ✅ Generous free tier
- ✅ Serverless (always on)
- ✅ Scalable

**Cons:**
- ❌ Complex setup
- ❌ Needs Google Cloud account

---

## Option 5: **PythonAnywhere** (Python-Specific)

Specialized Python hosting.

### Steps:

1. Go to https://www.pythonanywhere.com
2. Create free account
3. Upload your files
4. Configure WSGI: `from main import app`
5. Set web app to use FastAPI
6. Get URL: `https://yourusername.pythonanywhere.com`

---

## 🎯 RECOMMENDATION

For your project, I recommend **Railway** because:
- ✅ Best free tier (5GB)
- ✅ Handles PyTorch/Transformers model (378MB)
- ✅ Easiest setup
- ✅ Auto-deploys from GitHub
- ✅ Good uptime

---

## 📋 Files You Need for Deployment

✅ Already created:
- `Procfile` - Deployment command
- `runtime.txt` - Python version
- `requirements_deploy.txt` - All dependencies

---

## 🔐 Environment Variables Setup

For Railway/Render, set these environment variables:
```
API_KEY=sk_test_123456789
PYTHONUNBUFFERED=1
```

---

## ✅ Final Checklist Before Deployment

- [ ] `Procfile` created ✓
- [ ] `runtime.txt` created ✓
- [ ] `requirements_deploy.txt` created ✓
- [ ] Code pushed to GitHub
- [ ] Free hosting account created (Railway/Render)
- [ ] Repository connected
- [ ] Deploy button clicked
- [ ] Public URL received
- [ ] API tested with base64 audio

---

## 📊 Comparison Table

| Platform | Free Tier | Setup Time | Performance | Best For |
|----------|-----------|-----------|-------------|----------|
| **Railway** ⭐ | 5GB | 5 min | Excellent | Production |
| Render | Limited | 5 min | Good | Development |
| Replit | Limited | 2 min | Poor | Testing |
| Google Cloud | 2M req/mo | 15 min | Excellent | Scaling |
| PythonAnywhere | Limited | 10 min | Good | Python |

---

## 🎉 After Deployment

Your API will be live at:
```
https://your-app-name.railway.app/api/voice-detection
```

**Access endpoints:**
- 📍 API: `https://your-app-name.railway.app/api/voice-detection`
- 📖 Swagger UI: `https://your-app-name.railway.app/docs`
- 📚 ReDoc: `https://your-app-name.railway.app/redoc`

---

## 💡 Tips

1. **Monitor logs**: Check deployment logs if issues occur
2. **Test immediately**: Send test request after deployment
3. **Scale if needed**: Upgrade plan if traffic increases
4. **Custom domain**: Most platforms allow custom domains (paid)

---

## ⚠️ Note on Large Model

The Wav2Vec2 model (378MB) might exceed free tier limits on some platforms. If issues occur:
- Reduce model size (use smaller model)
- Use Railway (recommended for large models)
- Consider paid tier ($5-10/month)

---

**Ready to deploy? Choose Railway and follow the steps above!** 🚀
