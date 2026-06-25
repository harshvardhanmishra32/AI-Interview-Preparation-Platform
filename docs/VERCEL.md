# Vercel Deployment

This repository includes a Vercel adapter for deploying the FastAPI backend.

## What Vercel Runs

Vercel deploys:

- FastAPI backend through `api/index.py`
- API routes such as `/api/auth/login`, `/api/resume/upload-resume`, `/health`, and `/docs`

The current Streamlit frontend is not deployed by this Vercel configuration. Streamlit needs a persistent Python web server and websocket runtime, which is not a good fit for Vercel serverless functions. For the full Streamlit UI, use Streamlit Community Cloud, Render, Railway, or rebuild the frontend as Next.js for Vercel.

## Required Vercel Settings

Import the GitHub repository in Vercel:

```text
https://github.com/harshvardhanmishra32/AI-Interview-Preparation-Platform
```

Use these project settings:

- Framework Preset: Other
- Build Command: leave empty
- Output Directory: leave empty
- Install Command: `pip install -r requirements.txt`

## Environment Variables

Set these in Vercel Project Settings:

```env
SECRET_KEY=replace-with-a-long-random-production-secret
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash
FRONTEND_ORIGINS=https://your-frontend-domain.com,http://localhost:8501
```

Optional:

```env
GITHUB_TOKEN=your-github-token
```

## Database Note

By default, the Vercel deployment uses SQLite in `/tmp` so the API can boot in a serverless environment. This is suitable for demos only. Data may disappear between deployments or function instances.

For production, replace SQLite with a hosted database such as Neon Postgres, Supabase Postgres, or Vercel Postgres-compatible storage, then set:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:PORT/DB_NAME
```

## Local Verification

Run backend tests:

```bash
venv/bin/python -m pytest -q
```

Run the API locally:

```bash
venv/bin/python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## Deploy From CLI

If you install and log in to the Vercel CLI:

```bash
npm i -g vercel
vercel login
vercel --prod
```

