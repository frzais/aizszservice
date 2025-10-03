#!/usr/bin/env python3
"""
Ultroid Session Generator
Generate session string untuk Ultroid UserBot
"""

import os
import sys

def generate_telethon_session():
    """Generate Telethon session"""
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
        
        print("=" * 50)
        print("Ultroid Telethon Session Generator")
        print("=" * 50)
        
        # Get API credentials
        api_id = input("Masukkan API ID: ").strip()
        api_hash = input("Masukkan API Hash: ").strip()
        
        if not api_id or not api_hash:
            print("Error: API ID dan API Hash harus diisi!")
            return None
            
        # Create client
        client = TelegramClient(StringSession(), int(api_id), api_hash)
        
        print("\nMencoba koneksi ke Telegram...")
        client.start()
        
        # Get session string
        session_string = client.session.save()
        
        print(f"\nSession String berhasil dibuat!")
        print(f"Session: {session_string}")
        
        # Save to file
        with open("session.txt", "w") as f:
            f.write(session_string)
        
        print("\nSession telah disimpan ke file 'session.txt'")
        print("Copy session string ini ke file .env sebagai SESSION")
        
        client.disconnect()
        return session_string
        
    except ImportError:
        print("Error: Telethon tidak terinstall!")
        print("Install dengan: pip install telethon")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def generate_pyrogram_session():
    """Generate Pyrogram session"""
    try:
        from pyrogram import Client
        from pyrogram.sessions import StringSession
        
        print("=" * 50)
        print("Ultroid Pyrogram Session Generator")
        print("=" * 50)
        
        # Get API credentials
        api_id = input("Masukkan API ID: ").strip()
        api_hash = input("Masukkan API Hash: ").strip()
        
        if not api_id or not api_hash:
            print("Error: API ID dan API Hash harus diisi!")
            return None
            
        # Create client
        client = Client(StringSession(), int(api_id), api_hash)
        
        print("\nMencoba koneksi ke Telegram...")
        client.start()
        
        # Get session string
        session_string = client.export_session_string()
        
        print(f"\nSession String berhasil dibuat!")
        print(f"Session: {session_string}")
        
        # Save to file
        with open("session.txt", "w") as f:
            f.write(session_string)
        
        print("\nSession telah disimpan ke file 'session.txt'")
        print("Copy session string ini ke file .env sebagai SESSION")
        
        client.stop()
        return session_string
        
    except ImportError:
        print("Error: Pyrogram tidak terinstall!")
        print("Install dengan: pip install pyrogram")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("Ultroid Session Generator")
    print("=" * 30)
    print("1. Telethon Session")
    print("2. Pyrogram Session")
    print("3. Keluar")
    
    choice = input("\nPilih opsi (1-3): ").strip()
    
    if choice == "1":
        generate_telethon_session()
    elif choice == "2":
        generate_pyrogram_session()
    elif choice == "3":
        print("Keluar...")
        sys.exit(0)
    else:
        print("Pilihan tidak valid!")
        main()

if __name__ == "__main__":
    main()
