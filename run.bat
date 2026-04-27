@echo off
title K-TomasGest - Inicio automático

echo ================================
echo   Iniciando Backend (FastAPI)
echo ================================
start "Backend" cmd /k "cd backend && uvicorn backend.main:app --reload"

echo Esperando 3 segundos...
timeout /t 3 >nul

echo ================================
echo   Iniciando Frontend (Vite)
echo ================================
start "Frontend" cmd /k "cd frontend && npm run dev"

echo ================================
echo   Todo listo
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ================================
