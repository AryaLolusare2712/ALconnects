# Arya Lolusare Portfolio

React + Python portfolio site built from Arya's resume and GitHub profile.

## Project Structure

- `frontend/` - Vite React app
- `backend/` - FastAPI backend serving portfolio data

## Run Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Run Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://127.0.0.1:5173`.

The frontend reads from `http://127.0.0.1:8000/api/profile` and falls back to local data if the backend is offline.
