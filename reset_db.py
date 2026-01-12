import os
import sqlite3

db_path = 'mindzen_erp.db'

def force_delete_db():
    print(f"Attempting to force delete {db_path}...")
    if os.path.exists(db_path):
        try:
            # Try to connect and close to ensure no local handles
            conn = sqlite3.connect(db_path)
            conn.close()
            
            os.remove(db_path)
            print(f"[OK] Successfully deleted {db_path}")
        except Exception as e:
            print(f"[ERROR] Failed to delete {db_path}: {e}")
            # Try renaming if delete fails
            try:
                os.rename(db_path, db_path + ".bak")
                print(f"[OK] Renamed {db_path} to {db_path}.bak")
            except Exception as e2:
                print(f"[ERROR] Final fail: {e2}")
    else:
        print("[INFO] Database file does not exist.")

if __name__ == "__main__":
    force_delete_db()
