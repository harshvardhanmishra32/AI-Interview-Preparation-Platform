# Frontend on Vercel + Backend on Render

This project now includes a Vercel-compatible frontend in `frontend-next/`.

## Architecture

```text
Browser
  -> Vercel Next.js frontend
  -> Render FastAPI backend
  -> Gemini / GitHub API / database
```

The original `frontend/` folder is the Streamlit app. Keep it for local demos or Streamlit-friendly hosting. Use `frontend-next/` for Vercel.

## 1. Deploy Backend on Render

Create a Render Web Service from the GitHub repository.

Recommended settings:

```text
Language: Python
Branch: main
Root Directory: leave empty
Build Command: pip install -r requirements.txt
Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
Health Check Path: /health
```

Environment variables:

```env
SECRET_KEY=your-long-random-secret
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
FRONTEND_ORIGINS=https://your-vercel-frontend.vercel.app
```

After deployment, confirm:

```text
https://your-render-backend.onrender.com/health
https://your-render-backend.onrender.com/docs
```

## 2. Deploy Frontend on Vercel

Import the same GitHub repository into Vercel.

Use these Vercel settings:

```text
Framework Preset: Next.js
Root Directory: frontend-next
Build Command: npm run build
Install Command: npm install
Output Directory: leave default
```

Environment variable:

```env
NEXT_PUBLIC_API_URL=https://your-render-backend.onrender.com
```

Deploy the project.

## 3. Connect CORS

After Vercel gives you the frontend URL, update Render:

```env
FRONTEND_ORIGINS=https://your-vercel-frontend.vercel.app
```

Redeploy the Render backend.

## 4. Test

From the Vercel frontend:

1. Register a new account.
2. Log in.
3. Open Dashboard.
4. Upload a resume.
5. Generate mock interview questions.
6. Analyze a GitHub profile.
7. Generate a career roadmap.

