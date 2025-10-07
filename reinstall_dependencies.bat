@echo off
echo 🚀 Memulai proses reinstall dependencies...
echo.

echo 📋 Langkah 1: Backup packages yang sudah terinstall
pip freeze > installed_packages_backup.txt
if %errorlevel% neq 0 (
    echo ❌ Gagal backup packages
    pause
    exit /b 1
)
echo ✅ Backup berhasil!

echo.
echo 🗑️ Langkah 2: Menghapus semua packages
echo ⚠️ Ini akan menghapus semua packages kecuali pip, setuptools, wheel
pause

for /f "tokens=1 delims==" %%i in ('pip freeze') do (
    set package=%%i
    set package=!package:>= =!
    set package=!package:<= =!
    set package=!package:== =!
    
    echo !package! | findstr /i "pip setuptools wheel" >nul
    if !errorlevel! neq 0 (
        echo Menghapus: !package!
        pip uninstall -y !package!
    )
)

echo.
echo ⬆️ Langkah 3: Upgrade pip, setuptools, wheel
python -m pip install --upgrade pip setuptools wheel
if %errorlevel% neq 0 (
    echo ❌ Gagal upgrade pip tools
    pause
    exit /b 1
)

echo.
echo 📥 Langkah 4: Install dari requirements.txt
if exist requirements.txt (
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Gagal install dari requirements.txt
        pause
        exit /b 1
    )
) else (
    echo ❌ File requirements.txt tidak ditemukan!
    pause
    exit /b 1
)

echo.
echo 📥 Langkah 5: Install dari optional-requirements.txt (jika ada)
if exist resources\startup\optional-requirements.txt (
    pip install -r resources\startup\optional-requirements.txt
    if %errorlevel% neq 0 (
        echo ⚠️ Beberapa optional requirements mungkin gagal diinstall
    )
) else (
    echo ℹ️ File optional-requirements.txt tidak ditemukan
)

echo.
echo ✅ Langkah 6: Verifikasi install
pip list

echo.
echo 🎉 Proses reinstall dependencies selesai!
echo 📁 File backup tersimpan di: installed_packages_backup.txt
echo 💡 Jika ada masalah, Anda bisa restore dengan:
echo    pip install -r installed_packages_backup.txt
echo.
pause
