@echo off
echo Deploying changes to GitHub...
git add app.py
git commit -m "Add database diagnostics and fix initialization"
git push origin main
echo.
echo Done! Vercel will now redeploy automatically.
echo Once deployed, visit: https://p3-cst150.vercel.app/init
echo.
pause
