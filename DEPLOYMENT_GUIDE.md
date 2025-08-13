# MMCalc Web - Deployment Guide for Render

## Quick Deployment Steps

### 1. Prepare Your Repository
1. Upload all project files to a GitHub repository
2. Include these files in your repo:
   - All Python files (`app.py`, `calculator.py`, `models.py`, etc.)
   - `templates/` folder with all HTML files
   - `static/` folder (if any)
   - `requirements_render.txt` (rename to `requirements.txt` in your repo)
   - `runtime.txt`
   - `render.yaml` (optional, for automatic configuration)

### 2. Deploy on Render
1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - **Name**: `mmcalc-web` (or any name you prefer)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - **Plan**: `Free` (for testing)

### 3. Environment Variables
In Render's dashboard, add these environment variables:
- **SESSION_SECRET**: Click "Generate" to auto-create a secure key
- **DATABASE_URL**: (Optional) Leave empty to use SQLite, or add PostgreSQL database

### 4. Optional: Add Database
For production use, add a PostgreSQL database:
1. In Render dashboard: "New +" → "PostgreSQL"
2. Name: `mmcalc-db`, Plan: `Free`
3. Copy the "External Database URL" 
4. Add it as `DATABASE_URL` environment variable in your web service

## File Structure for Export
```
your-repo/
├── app.py                 # Main Flask application
├── calculator.py          # Calculation engine
├── compound_library.py    # Library management
├── models.py             # Database models
├── main.py               # Entry point
├── requirements.txt      # Python dependencies
├── runtime.txt           # Python version
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── calculate.html
│   ├── library.html
│   ├── history.html
│   └── settings.html
└── static/              # CSS/JS files (if any)

```

## Important Notes
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
- **Python Version**: 3.11.6 (specified in runtime.txt)
- **Database**: Uses SQLite by default, PostgreSQL optional
- **Port**: Automatically provided by Render via `$PORT` variable

## Troubleshooting
- If deployment fails, check the build logs in Render dashboard
- Make sure all file names match exactly (case-sensitive)
- Verify `requirements.txt` has correct package versions
- Check that `main.py` imports the Flask app correctly

Your app will be available at: `https://your-app-name.onrender.com`