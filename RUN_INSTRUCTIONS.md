# 🚀 How to Run the Application

## Prerequisites

- ✅ Python 3.8+ installed
- ✅ Node.js 18+ and npm installed
- ✅ Git (optional)

## Step-by-Step Instructions

### Step 1: Open Two Terminals

You'll need two terminal windows:
- **Terminal 1**: For the backend (FastAPI)
- **Terminal 2**: For the frontend (React)

---

### Step 2: Start the Backend (Terminal 1)

```bash
# Navigate to backend directory
cd automotive-backend

# Install Python dependencies (first time only)
pip install -r requirements.txt

# Start the FastAPI server
python -m uvicorn src.web.main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify Backend:**
- Open browser: http://127.0.0.1:8000/docs
- You should see the Swagger UI documentation

---

### Step 3: Start the Frontend (Terminal 2)

```bash
# Navigate to frontend directory
cd automotive-frontend

# Install Node dependencies (first time only)
npm install

# Start the development server
npm run dev
```

**Expected Output:**
```
  VITE v7.2.4  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Verify Frontend:**
- Open browser: http://localhost:5173
- You should see the Automotive Fleet Management dashboard

---
