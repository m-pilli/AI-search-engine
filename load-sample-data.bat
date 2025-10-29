@echo off
echo ========================================
echo Loading Sample Data
echo ========================================
echo.

docker-compose exec backend python load_sample_data.py

echo.
echo ========================================
echo Sample data loaded successfully!
echo ========================================
echo.
echo You can now search at: http://localhost:3000
echo.
pause

