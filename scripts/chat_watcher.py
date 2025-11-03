import re
import time
import os
import configparser

config = configparser.ConfigParser()
config.read('config/config.ini')

# === CONFIGURATION ===
# Path to your CS2 console.log file
LOG_PATH = config.get('General', 'log_file')

# Path to the parsed chat output file
PARSED_FILE = config.get('General', 'parsed_file')

# Regex to capture timestamp, chat type, username, and message
CHAT_REGEX = re.compile(
    r'^(\d{2}\/\d{2}\s+\d{2}:\d{2}:\d{2})\s+\[(T|CT|ALL)\]\s+([^\[]+?)(?:\s+\[DEAD\])?:\s+(.+)$'
)

def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access values from the configuration file
    debug_mode = config.getboolean('General', 'debug')
    log_level = config.get('General', 'log_level')

    # Return a dictionary with the retrieved values
    config_values = {
        'debug_mode': debug_mode,
        'log_level': log_level
    }

    return config_values


def follow(file_path):
    """Generator that yields new lines as they appear in the file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, os.SEEK_END)  # Go to the end of the file
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line.strip()


def parse_chat(line):
    """Apply regex and return dict if the line is a chat message."""
    match = CHAT_REGEX.match(line)
    if match:
        return {
            "time": match.group(1),
            "chat": match.group(2),
            "user": match.group(3).strip(),
            "message": match.group(4).strip(),
        }
    return None


def main():
    print(f"📡 Watching log file: {LOG_PATH}")
    print(f"💾 Saving parsed chats to: {PARSED_FILE}")

    # Open output file for appending
    with open(PARSED_FILE, "a", encoding="utf-8") as out_file:
        for line in follow(LOG_PATH):
            data = parse_chat(line)
            if data:
                # Format line for saving
                formatted_for_file = f"[{data['time']}] ({data['chat']}) {data['user']}: {data['message']}"
                formatted = f"[{data['user']}: {data['message']}"
                print(f"🛑 ORIGINAL: " + formatted)  # Print to console
                out_file.write(formatted + "\n")  # Save to file
                out_file.flush()  # Immediately write to disk


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n🛑 Stopped watching log.")

