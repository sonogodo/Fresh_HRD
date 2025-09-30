# Deployment Guide

## Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app:app --reload
```

3. Test the endpoints:
```bash
python test_api.py
```

4. Open browser to `http://localhost:8000` to see the web interface

## Vercel Deployment

1. Make sure all files are committed to git
2. Connect your repository to Vercel
3. Vercel will automatically detect the Python project and deploy using the `vercel.json` configuration

## Key Files for Deployment

- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies
- `app.py` - Main FastAPI application
- `index.html` - Frontend interface
- `JSONs/candidates.json` - Candidate data (required for matching)
- `Matching/` - Matching algorithm modules

## Troubleshooting

- If you get 404 errors, check that all file paths are correct
- If the API doesn't respond, check the Vercel function logs
- Make sure all dependencies are listed in requirements.txt
- Ensure the JSONs folder and candidates.json file are not ignored by .vercelignore