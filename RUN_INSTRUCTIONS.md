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

### Step 4: Test the Application

1. **View Empty State**
   - You should see "No hay vehículos registrados"

2. **Create a Vehicle**
   - Click "Registrar Vehículo"
   - Fill in the form:
     - ID: `V-001`
     - Placa: `ABC-123`
     - Modelo: `Toyota Corolla 2020`
     - Kilometraje: `5000`
   - Click "Registrar"
   - You should see a success toast notification

3. **View Vehicle**
   - The vehicle card should appear in the grid
   - Stats should update (1 vehicle, 0 alerts)

4. **Update Mileage**
   - Click "Actualizar KM" on the vehicle card
   - Enter new mileage: `15000`
   - Click "Actualizar"
   - Mileage should update and you might see alerts

5. **View Alerts**
   - Click on the badge showing alerts
   - Modal should open showing maintenance alerts

6. **View Details**
   - Click "Ver Detalles"
   - Modal should show vehicle information

7. **Delete Vehicle**
   - Click "Eliminar"
   - Confirm deletion
   - Vehicle should be removed

---

## Troubleshooting

### Backend Issues

#### Error: "ModuleNotFoundError: No module named 'fastapi'"
```bash
# Install dependencies
cd automotive-backend
pip install -r requirements.txt
```

#### Error: "Address already in use"
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port
python -m uvicorn src.web.main:app --reload --port 8001
```

#### Error: "Database not found"
```bash
# The database will be created automatically on first run
# If issues persist, delete maintenance.db and restart
```

---

### Frontend Issues

#### Error: "npm: command not found"
```bash
# Install Node.js from https://nodejs.org/
# Verify installation:
node --version
npm --version
```

#### Error: "Failed to fetch"
```bash
# 1. Verify backend is running: http://127.0.0.1:8000/docs
# 2. Check API URL in src/services/api.ts
# 3. Check browser console for CORS errors
```

#### Error: "Port 5173 already in use"
```bash
# Kill process on port 5173 (Windows)
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Or edit vite.config.js to use different port:
export default defineConfig({
  plugins: [react()],
  server: { port: 3000 }
})
```

#### Error: TypeScript compilation errors
```bash
# Clean and reinstall
cd automotive-frontend
rm -rf node_modules package-lock.json
npm install
```

---

## Quick Commands Reference

### Backend Commands
```bash
# Start backend
cd automotive-backend
python -m uvicorn src.web.main:app --reload

# Run tests
pytest

# View API docs
# Open: http://127.0.0.1:8000/docs
```

### Frontend Commands
```bash
# Start frontend
cd automotive-frontend
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linter
npm run lint
```

---

## Environment URLs

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://127.0.0.1:8000 | FastAPI server |
| API Docs | http://127.0.0.1:8000/docs | Swagger UI |
| Frontend | http://localhost:5173 | React app |

---

## Development Workflow

### Making Changes

1. **Backend Changes**
   - Edit files in `automotive-backend/src/`
   - Server auto-reloads (--reload flag)
   - Test at http://127.0.0.1:8000/docs

2. **Frontend Changes**
   - Edit files in `automotive-frontend/src/`
   - Browser auto-refreshes (HMR)
   - Changes appear instantly

### Adding New Features

1. **Backend**: Add endpoint in `src/web/main.py`
2. **Frontend**: 
   - Add type in `src/types/`
   - Add API call in `src/services/api.ts`
   - Create component in `src/components/`
   - Use in `App.tsx`

---

## Production Deployment

### Backend
```bash
cd automotive-backend
pip install -r requirements.txt
uvicorn src.web.main:app --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd automotive-frontend
npm run build
# Deploy the 'dist' folder to your hosting service
```

---

## Need Help?

### Documentation
- Frontend README: `automotive-frontend/README.md`
- Quick Start: `automotive-frontend/QUICKSTART.md`
- Migration Notes: `automotive-frontend/MIGRATION_NOTES.md`
- Comparison: `automotive-frontend/COMPARISON.md`

### API Documentation
- Swagger UI: http://127.0.0.1:8000/docs
- Postman Collection: `automotive-backend/docs/postman/`

### Design System
- Design Specs: `automotive-backend/docs/design/DESIGN.md`

---

## Success Checklist

- [ ] Backend running on http://127.0.0.1:8000
- [ ] Backend docs accessible at http://127.0.0.1:8000/docs
- [ ] Frontend running on http://localhost:5173
- [ ] Can create a vehicle
- [ ] Can update mileage
- [ ] Can view alerts
- [ ] Can delete vehicle
- [ ] Toast notifications work
- [ ] No console errors

---

**Happy Coding! 🚗✨**

If everything is working, you're ready to start developing!
