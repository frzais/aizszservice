# PowerShell Script untuk Reinstall Dependencies
# Jalankan dengan: powershell -ExecutionPolicy Bypass -File reinstall_dependencies.ps1

Write-Host "🚀 Memulai proses reinstall dependencies..." -ForegroundColor Green
Write-Host ""

# Langkah 1: Backup packages
Write-Host "📋 Langkah 1: Backup packages yang sudah terinstall" -ForegroundColor Yellow
try {
    pip freeze | Out-File -FilePath "installed_packages_backup.txt" -Encoding UTF8
    Write-Host "✅ Backup berhasil!" -ForegroundColor Green
} catch {
    Write-Host "❌ Gagal backup packages: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Langkah 2: Hapus semua packages
Write-Host ""
Write-Host "🗑️ Langkah 2: Menghapus semua packages" -ForegroundColor Yellow
Write-Host "⚠️ Ini akan menghapus semua packages kecuali pip, setuptools, wheel" -ForegroundColor Red

$confirm = Read-Host "Lanjutkan? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "❌ Dibatalkan oleh user" -ForegroundColor Red
    exit 0
}

try {
    $packages = pip freeze | Where-Object { $_ -notmatch "^(pip|setuptools|wheel)" -and $_ -ne "" }
    
    foreach ($package in $packages) {
        $packageName = $package.Split("==")[0].Split(">=")[0].Split("<=")[0]
        Write-Host "Menghapus: $packageName" -ForegroundColor Cyan
        pip uninstall -y $packageName 2>$null
    }
    Write-Host "✅ Semua packages berhasil dihapus!" -ForegroundColor Green
} catch {
    Write-Host "⚠️ Beberapa packages mungkin gagal dihapus: $($_.Exception.Message)" -ForegroundColor Yellow
}

# Langkah 3: Upgrade pip tools
Write-Host ""
Write-Host "⬆️ Langkah 3: Upgrade pip, setuptools, wheel" -ForegroundColor Yellow
try {
    python -m pip install --upgrade pip setuptools wheel
    Write-Host "✅ Upgrade pip tools berhasil!" -ForegroundColor Green
} catch {
    Write-Host "❌ Gagal upgrade pip tools: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Langkah 4: Install dari requirements.txt
Write-Host ""
Write-Host "📥 Langkah 4: Install dari requirements.txt" -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    try {
        pip install -r requirements.txt
        Write-Host "✅ Install dari requirements.txt berhasil!" -ForegroundColor Green
    } catch {
        Write-Host "❌ Gagal install dari requirements.txt: $($_.Exception.Message)" -ForegroundColor Red
        Read-Host "Tekan Enter untuk keluar"
        exit 1
    }
} else {
    Write-Host "❌ File requirements.txt tidak ditemukan!" -ForegroundColor Red
    Read-Host "Tekan Enter untuk keluar"
    exit 1
}

# Langkah 5: Install dari optional-requirements.txt
Write-Host ""
Write-Host "📥 Langkah 5: Install dari optional-requirements.txt (jika ada)" -ForegroundColor Yellow
if (Test-Path "resources\startup\optional-requirements.txt") {
    try {
        pip install -r resources\startup\optional-requirements.txt
        Write-Host "✅ Install optional requirements berhasil!" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Beberapa optional requirements mungkin gagal diinstall: $($_.Exception.Message)" -ForegroundColor Yellow
    }
} else {
    Write-Host "ℹ️ File optional-requirements.txt tidak ditemukan" -ForegroundColor Blue
}

# Langkah 6: Verifikasi
Write-Host ""
Write-Host "✅ Langkah 6: Verifikasi install" -ForegroundColor Yellow
try {
    pip list
    Write-Host ""
    Write-Host "🎉 Proses reinstall dependencies selesai!" -ForegroundColor Green
    Write-Host "📁 File backup tersimpan di: installed_packages_backup.txt" -ForegroundColor Blue
    Write-Host "💡 Jika ada masalah, Anda bisa restore dengan:" -ForegroundColor Blue
    Write-Host "   pip install -r installed_packages_backup.txt" -ForegroundColor Blue
} catch {
    Write-Host "⚠️ Gagal verifikasi: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host ""
Read-Host "Tekan Enter untuk keluar"
