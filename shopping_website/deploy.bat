@echo off
echo ================================
echo Vercel Deployment Helper Script
echo ================================
echo.

echo Step 1: Checking Git status...
git status
echo.

echo Step 2: Removing old vercel_models.py file...
del vercel_models.py
echo.

echo Step 3: Adding all files to Git...
git add .
echo.

echo Step 4: Committing changes...
git commit -m "Fix Vercel deployment - updated app.py, requirements.txt, and vercel.json"
echo.

echo Step 5: Pushing to GitHub...
git push origin main
echo.

echo ================================
echo Done! Check Vercel for new deployment
echo ================================
pause
