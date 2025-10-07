#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk menghapus semua dependencies dan menginstall ulang dari requirements.txt
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Menjalankan command dan menampilkan output"""
    print(f"\n[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"[SUCCESS] {description} berhasil!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"[ERROR] {description} gagal!")
            print(f"Error: {result.stderr.strip()}")
            return False
        return True
    except Exception as e:
        print(f"[ERROR] Error saat {description}: {e}")
        return False

def main():
    print("[START] Memulai proses reinstall dependencies...")
    
    # 1. Backup requirements yang sudah terinstall
    print("\n[STEP 1] Backup packages yang sudah terinstall")
    if not run_command("pip freeze > installed_packages_backup.txt", "Backup packages"):
        return
    
    # 2. Hapus semua packages (kecuali pip, setuptools, wheel)
    print("\n[STEP 2] Menghapus semua packages")
    
    # Dapatkan list packages yang akan dihapus
    try:
        result = subprocess.run("pip freeze", shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            packages = result.stdout.strip().split('\n')
            packages_to_remove = []
            
            for package in packages:
                if package and not any(skip in package.lower() for skip in ['pip', 'setuptools', 'wheel']):
                    package_name = package.split('==')[0].split('>=')[0].split('<=')[0]
                    packages_to_remove.append(package_name)
            
            if packages_to_remove:
                print(f"[INFO] Akan menghapus {len(packages_to_remove)} packages...")
                
                # Hapus packages dalam batch
                batch_size = 10
                for i in range(0, len(packages_to_remove), batch_size):
                    batch = packages_to_remove[i:i+batch_size]
                    cmd = f"pip uninstall -y {' '.join(batch)}"
                    if not run_command(cmd, f"Menghapus batch {i//batch_size + 1}"):
                        print(f"[WARNING] Beberapa packages mungkin gagal dihapus, melanjutkan...")
            else:
                print("[INFO] Tidak ada packages yang perlu dihapus")
        else:
            print("[ERROR] Gagal mendapatkan list packages")
            return
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return
    
    # 3. Upgrade pip, setuptools, wheel
    print("\n[STEP 3] Upgrade pip, setuptools, wheel")
    run_command("python -m pip install --upgrade pip setuptools wheel", "Upgrade pip tools")
    
    # 4. Install dari requirements.txt
    print("\n[STEP 4] Install dari requirements.txt")
    if os.path.exists("requirements.txt"):
        if not run_command("pip install -r requirements.txt", "Install dari requirements.txt"):
            print("[ERROR] Gagal install dari requirements.txt")
            return
    else:
        print("[ERROR] File requirements.txt tidak ditemukan!")
        return
    
    # 5. Install dari optional-requirements.txt jika ada
    print("\n[STEP 5] Install dari optional-requirements.txt (jika ada)")
    if os.path.exists("resources/startup/optional-requirements.txt"):
        if not run_command("pip install -r resources/startup/optional-requirements.txt", "Install optional requirements"):
            print("[WARNING] Beberapa optional requirements mungkin gagal diinstall")
    else:
        print("[INFO] File optional-requirements.txt tidak ditemukan")
    
    # 6. Verifikasi install
    print("\n[STEP 6] Verifikasi install")
    run_command("pip list", "List packages yang terinstall")
    
    print("\n[SUCCESS] Proses reinstall dependencies selesai!")
    print("\n[INFO] File backup tersimpan di: installed_packages_backup.txt")
    print("[INFO] Jika ada masalah, Anda bisa restore dengan:")
    print("       pip install -r installed_packages_backup.txt")

if __name__ == "__main__":
    main()
