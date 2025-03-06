import os
import time
from chatbot import *

def get_python_files(directory):
    """Returns Python files with their last modified timestamps."""
    return {f: os.path.getmtime(os.path.join(directory, f)) for f in os.listdir(directory) if f.endswith(".py")}

def monitor_directory():
    """Monitors a directory for changes in Python files."""
    WATCH_DIRECTORY = r"C:\Users\ayush\Documents\ChatBot python file"
    print(f"👀 Watching directory: {WATCH_DIRECTORY}")

    last_modified_times = get_python_files(WATCH_DIRECTORY)

    try:
        while True:
            time.sleep(5)  # Poll every 5 seconds
            current_files = get_python_files(WATCH_DIRECTORY)

            for file, mod_time in current_files.items():
                if file not in last_modified_times or mod_time > last_modified_times[file]:
                    print(f"\n📝 Detected changes in: {file}")

                    file_path = os.path.join(WATCH_DIRECTORY, file)
                    with open(file_path, "r") as f:
                        last_analyzed_code = f.read()

                    # **Stop execution if file is empty**
                    if not last_analyzed_code.strip():
                        print(f"No code detected in {file}, stopping execution.")
                        return  # **Return instead of continue**

                    # **Analyze the new original code first**
                    suggestions = analyze_code(last_analyzed_code)
                    print(f"\n🤖 AI: {suggestions}")

                    # **Start chat mode**
                    start_chat_mode()

                    last_modified_times[file] = mod_time

    except KeyboardInterrupt:
        print("\n🛑 Stopping file monitoring...")


if __name__ == "__main__":
    monitor_directory()
