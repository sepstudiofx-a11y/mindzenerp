import os
import sys
import uvicorn
import multiprocessing
import traceback

def get_resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def main():
    # PyInstaller multiprocessing fix for Windows
    multiprocessing.freeze_support()
    
    print("Starting MindZen ERP...")
    
    try:
        # Set current directory to where the EXE/script is
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        os.chdir(base_dir)
        print(f"Working directory: {base_dir}")
        
        # Add src to sys.path if running in dev mode
        src_path = os.path.join(base_dir, 'src')
        if os.path.exists(src_path):
            sys.path.insert(0, src_path)
            print(f"Added {src_path} to sys.path")

        # Import the app (this will trigger engine initialization)
        print("Loading application modules...")
        from mindzen_erp.web import app
        
        print("MindZen ERP is starting on http://localhost:8000")
        print("Press Ctrl+C to stop the server.")
        
        # Run uvicorn Programmatically
        # use_colors=False is CRITICAL for PyInstaller windowed/noconsole mode
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info", reload=False, use_colors=False)
        
    except Exception as e:
        print("\n" + "!"*50)
        print("CRITICAL ERROR DURING STARTUP")
        print("!"*50)
        traceback.print_exc()
        print("\n" + "!"*50)
        input("\nPress Enter to close this window...")
        sys.exit(1)

if __name__ == "__main__":
    main()
