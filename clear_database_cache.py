#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script untuk membersihkan database dan cache
"""

import os
import sys
import json
from pathlib import Path

def clear_database_files():
    """Hapus file database lokal"""
    db_files = [
        "database.json",
        "ultroid.db", 
        "ultroid.sqlite",
        "localdb.json",
        "ultroid_cache.json",
        "userbot.db"
    ]
    
    print("[INFO] Menghapus file database lokal...")
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                os.remove(db_file)
                print(f"[SUCCESS] Dihapus: {db_file}")
            except Exception as e:
                print(f"[ERROR] Gagal hapus {db_file}: {e}")

def clear_cache_directories():
    """Hapus direktori cache"""
    cache_dirs = [
        "__pycache__",
        "pyUltroid/__pycache__",
        "plugins/__pycache__", 
        "assistant/__pycache__",
        "assistant/manager/__pycache__",
        "pyUltroid/dB/__pycache__",
        "pyUltroid/fns/__pycache__",
        "pyUltroid/startup/__pycache__",
        "pyUltroid/_misc/__pycache__",
        "strings/__pycache__"
    ]
    
    print("[INFO] Menghapus direktori cache...")
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                import shutil
                shutil.rmtree(cache_dir)
                print(f"[SUCCESS] Dihapus: {cache_dir}")
            except Exception as e:
                print(f"[ERROR] Gagal hapus {cache_dir}: {e}")

def clear_temp_files():
    """Hapus file temporary"""
    temp_files = [
        "*.log",
        "ultroid.log", 
        "profile.jpg",
        "asst.session",
        "asst.session-journal",
        "resources/downloads/*",
        "resources/auth/*"
    ]
    
    print("[INFO] Menghapus file temporary...")
    for pattern in temp_files:
        try:
            if "*" in pattern:
                # Handle wildcard patterns
                import glob
                files = glob.glob(pattern)
                for file in files:
                    if os.path.exists(file):
                        if os.path.isfile(file):
                            os.remove(file)
                        else:
                            import shutil
                            shutil.rmtree(file)
                        print(f"[SUCCESS] Dihapus: {file}")
            else:
                if os.path.exists(pattern):
                    if os.path.isfile(pattern):
                        os.remove(pattern)
                    else:
                        import shutil
                        shutil.rmtree(pattern)
                    print(f"[SUCCESS] Dihapus: {pattern}")
        except Exception as e:
            print(f"[ERROR] Gagal hapus {pattern}: {e}")

def reset_environment():
    """Reset environment variables"""
    print("[INFO] Reset environment...")
    
    # Hapus file .env jika ada
    if os.path.exists(".env"):
        try:
            os.remove(".env")
            print("[SUCCESS] Dihapus: .env")
        except Exception as e:
            print(f"[ERROR] Gagal hapus .env: {e}")
    
    # Hapus file config jika ada
    config_files = ["config.json", "settings.json", "ultroid.json"]
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                os.remove(config_file)
                print(f"[SUCCESS] Dihapus: {config_file}")
            except Exception as e:
                print(f"[ERROR] Gagal hapus {config_file}: {e}")

def create_clean_directories():
    """Buat direktori yang diperlukan"""
    print("[INFO] Membuat direktori yang diperlukan...")
    
    directories = [
        "resources/downloads",
        "resources/auth", 
        "resources/session",
        "addons"
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"[SUCCESS] Dibuat: {directory}")
        except Exception as e:
            print(f"[ERROR] Gagal buat {directory}: {e}")

def main():
    print("[START] Memulai proses pembersihan database dan cache...")
    
    clear_database_files()
    clear_cache_directories() 
    clear_temp_files()
    reset_environment()
    create_clean_directories()
    
    print("\n[SUCCESS] Proses pembersihan selesai!")
    print("[INFO] Database dan cache telah dibersihkan")
    print("[INFO] Environment telah direset")
    print("[INFO] Direktori yang diperlukan telah dibuat")

if __name__ == "__main__":
    main()
