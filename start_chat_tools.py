import subprocess
import sys
import os

# Paths to your scripts (adjust if needed)
CHAT_WATCHER = "scripts/chat_watcher.py"
TRANSLATOR = "scripts/translator.py"

def clear():
    os.system('cls||clear')

def main():
    # Get the full path to the Python executable currently running this script
    python_exe = sys.executable

    print("🚀 Starting CS2 chat watcher and translator...")

    # Start the chat watcher
    watcher_process = subprocess.Popen([python_exe, CHAT_WATCHER])

    # Start the translator
    translator_process = subprocess.Popen([python_exe, TRANSLATOR])

    try:
        # Wait for both processes to finish (will run indefinitely until you Ctrl+C)
        watcher_process.wait()
        translator_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping both scripts...")
        watcher_process.terminate()
        translator_process.terminate()
        watcher_process.wait()
        translator_process.wait()
        print("✅ Both scripts stopped.")

if __name__ == "__main__":
    clear()
    main()
