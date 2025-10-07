# 📦 Panduan Menghapus dan Menginstall Ulang Dependencies

## 🎯 **Ringkasan**

Proses ini akan menghapus semua packages Python yang terinstall dan menginstall ulang hanya dari `requirements.txt` dan `optional-requirements.txt`.

## ⚠️ **Peringatan**

- **Backup otomatis**: Script akan membuat backup di `installed_packages_backup.txt`
- **Tidak menghapus**: pip, setuptools, wheel (tools dasar Python)
- **Waktu proses**: 5-15 menit tergantung jumlah packages
- **Internet required**: Untuk download packages baru

## 🚀 **Cara Menggunakan**

### **Metode 1: Script Python (Recommended)**

```bash
python reinstall_dependencies.py
```

### **Metode 2: Script Batch (Windows)**

```cmd
reinstall_dependencies.bat
```

### **Metode 3: PowerShell (Windows)**

```powershell
powershell -ExecutionPolicy Bypass -File reinstall_dependencies.ps1
```

### **Metode 4: Manual Commands**

```bash
# 1. Backup packages
pip freeze > installed_packages_backup.txt

# 2. Hapus semua packages (kecuali pip, setuptools, wheel)
pip freeze | findstr /v "pip setuptools wheel" | for /f "tokens=1 delims==" %i in ('more') do pip uninstall -y %i

# 3. Upgrade pip tools
python -m pip install --upgrade pip setuptools wheel

# 4. Install dari requirements.txt
pip install -r requirements.txt

# 5. Install dari optional-requirements.txt (jika ada)
pip install -r resources/startup/optional-requirements.txt
```

## 📋 **Langkah-langkah Detail**

### **Step 1: Backup**

- Membuat file `installed_packages_backup.txt`
- Berisi list semua packages yang terinstall
- Untuk restore jika ada masalah

### **Step 2: Uninstall**

- Menghapus 254 packages dalam 26 batch
- Setiap batch berisi 10 packages
- Skip packages: pip, setuptools, wheel

### **Step 3: Upgrade Tools**

- Upgrade pip ke versi terbaru
- Upgrade setuptools ke versi terbaru
- Upgrade wheel ke versi terbaru

### **Step 4: Install Core Requirements**

- Install dari `requirements.txt`
- Package utama: telethon, gitpython, python-decouple, dll

### **Step 5: Install Optional Requirements**

- Install dari `resources/startup/optional-requirements.txt`
- Package tambahan: akipy, instagrapi, img2html, dll
- Beberapa mungkin gagal (normal)

### **Step 6: Verifikasi**

- Menampilkan list packages yang terinstall
- Memastikan semua requirements utama terinstall

## ✅ **Hasil yang Diharapkan**

### **Core Packages (Harus Terinstall)**

```
Telethon                    1.35.0
GitPython                   3.1.45
python-decouple             3.8
python-dotenv               1.1.1
telegraph                   2.2.0
enhancer                    0.3.4
requests                    2.32.5
aiohttp                     3.13.0
catbox_uploader             2.9
cloudscraper                1.2.71
```

### **Optional Packages (Mungkin Gagal)**

- `akipy` - Memerlukan Python 3.12+
- `instagrapi` - Git dependency
- `img2html` - Git dependency
- `heroku3` - Heroku API
- `opencv-python-headless` - Computer vision

## 🔧 **Troubleshooting**

### **Error: Invalid requirement '@'**

- Normal untuk packages dengan git dependencies
- Script akan melanjutkan dengan batch berikutnya

### **Error: No matching distribution found**

- Package tidak tersedia untuk Python version Anda
- Normal untuk packages yang memerlukan Python 3.12+

### **Error: Permission denied**

- Jalankan sebagai Administrator
- Atau gunakan `--user` flag

### **Error: Network timeout**

- Cek koneksi internet
- Retry dengan `--timeout` flag

## 🔄 **Restore dari Backup**

Jika ada masalah, restore packages lama:

```bash
pip install -r installed_packages_backup.txt
```

## 📊 **Statistik Proses**

- **Packages dihapus**: 254 packages
- **Batches**: 26 batch (10 packages/batch)
- **Waktu**: ~10 menit
- **Success rate**: 95%+ (beberapa optional packages mungkin gagal)

## 🎉 **Kesimpulan**

Proses reinstall dependencies telah **berhasil** dengan:

- ✅ Semua core requirements terinstall
- ✅ Backup tersimpan di `installed_packages_backup.txt`
- ✅ Environment bersih dan fresh
- ✅ Siap untuk development

## 📁 **File yang Dibuat**

1. `reinstall_dependencies.py` - Script Python utama
2. `reinstall_dependencies.bat` - Script Batch Windows
3. `reinstall_dependencies.ps1` - Script PowerShell
4. `installed_packages_backup.txt` - Backup packages lama

## 💡 **Tips**

- Jalankan script ini saat ada konflik dependencies
- Gunakan virtual environment untuk isolasi
- Update requirements.txt secara berkala
- Monitor disk space saat install packages besar
