import time
import os
from googletrans import Translator
import configparser

translator = Translator()
config = configparser.ConfigParser()
config.read('config/config.ini')

# === CONFIGURATION ===
CHAT_FILE = config.get('General', 'chat_file')       # File to read from (created by your other script)
TRANSLATED_FILE = config.get('General', 'translated_file')  # File where translated lines will be saved
TARGET_LANG = config.get('General', 'target_language')                 # <--- Change this to your preferred language code

def clean_files():
    files_to_clean = [
        "textfiles/parsed_chat.txt",
        "textfiles/translated_chat.txt"
    ]
    for file in files_to_clean:
        try:
            open(file, "w").close()  # overwrite with empty content
            print(f"🛑 Cleared: {file}")
        except FileNotFoundError:
            print(f"🛑 File not found, skipping: {file}")



def follow(file_path):
    """Generator that yields new lines as they appear."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()


def translate_line(line, target_lang):
    """Extract message and translate it."""
    # Try to separate the message (after the first ':')
    try:
        prefix, message = line.split(":", 1)
        message = message.strip()
        translated = translator.translate(message, dest=target_lang).text
        language_detected = translator.detect(message).lang.upper()
        if translated != message:
            return f"{prefix}: {translated}  ( {language_detected} )"
        else:
            return "=="
    except Exception as e:
        print(f"⚠️ Error translating line: {e}")
        return line


def main():
    print(f"📖 Reading from: {CHAT_FILE}")
    print(f"🌍 Translating into: {TARGET_LANG}")
    print(f"💾 Saving translated chat to: {TRANSLATED_FILE}")

    with open(TRANSLATED_FILE, "a", encoding="utf-8") as out_file:
        for line in follow(CHAT_FILE):
            if not line.strip():
                continue

            translated_line = translate_line(line, TARGET_LANG)
            print(f"🌍 TRANSLATED: " + translated_line)
            out_file.write(translated_line + "\n")
            out_file.flush()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Translation stopped.")
        clean_files()
