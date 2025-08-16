import time
import os
import datetime

# --- Configuration ---
DEFAULT_FOLDER = r"Text Files"
LOG_FOLDER = r"ProgramData"
LOG_FILE = r"Log.txt"
VERSION = 2.4
PROGRAM_NAME = "File Loader"
QUIT_COMMAND = "x"
HELP_COMMAND = "?"
DIR_COMMAND = "dir"

# Ensure the log folder exists
os.makedirs(LOG_FOLDER, exist_ok=True)

# --- Logging function ---
def log_message(message):
    """Writes a message to the log file with timestamp."""
    log_filepath = os.path.join(LOG_FOLDER, LOG_FILE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    try:
        with open(log_filepath, "a", encoding="utf-8") as log_file:
            log_file.write(log_entry + "\n")
    except Exception as e:
        print(f"⚠️ Could not write to log file: {e}")

# --- Display help ---
def show_help():
    print("\n📖 Help:")
    print(f" - Type a filename to load it from the current folder")
    print(f" - Type a full path to load a file from anywhere")
    print(f" - Type a folder name or full path to change the current folder")
    print(f" - Type '{DIR_COMMAND}' to list files in the current folder")
    print(f" - Press '{QUIT_COMMAND}' to exit")
    print(f" - Press '{HELP_COMMAND}' to show this help\n")

# --- Start program ---
current_folder = DEFAULT_FOLDER
print(f"{PROGRAM_NAME} v{VERSION}")
print(f"(Press {QUIT_COMMAND} to exit, {HELP_COMMAND} for help)\n")

while True:
    user_input = input(f"[CF={current_folder}]> ").strip()

    # --- Quit program ---
    if user_input.lower() == QUIT_COMMAND:
        print("🔄 Loading, please wait...")
        time.sleep(0.5)
        print("🧹 Cleaning up temporary files...")
        time.sleep(0.8)
        print("👋 Goodbye!")
        log_message("Program exited by user.")
        break

    # --- Help command ---
    if user_input == HELP_COMMAND:
        show_help()
        continue

    # --- DIR command ---
    if user_input.lower() == DIR_COMMAND:
        try:
            files = os.listdir(current_folder)
            if not files:
                print(f"⚠️ The folder '{current_folder}' is empty.\n")
            else:
                print(f"📂 Files and folders in '{current_folder}':")
                for f in files:
                    print(f" - {f}")
                print("")
            log_message(f"Listed files in folder: '{current_folder}'")
        except Exception as e:
            error_msg = f"Could not list folder contents: {e}"
            print(f"❌ {error_msg}\n")
            log_message(error_msg)
        continue

    # --- Determine file or folder path ---
    potential_path = user_input
    # Full path
    if os.path.sep in user_input or ":" in user_input:
        potential_path = os.path.normpath(user_input)  # normalize backslashes
        if os.path.isdir(potential_path):
            current_folder = potential_path
            print(f"📂 Current folder changed to: {current_folder}\n")
            log_message(f"Changed current folder to: '{current_folder}'")
            continue
        else:
            filepath = potential_path
            current_folder = os.path.dirname(filepath) or current_folder
    else:
        # Check if it is a folder in the current folder
        # If user_input is a folder in the current folder
        folder_candidate = os.path.join(current_folder, user_input)
        if os.path.isdir(folder_candidate):
            current_folder = os.path.normpath(folder_candidate)  # <- normalize path
            print(f"📂 Current folder changed to: {current_folder}\n")
            log_message(f"Changed current folder to: '{current_folder}'")
            continue

        else:
            filepath = os.path.join(current_folder, user_input)

    # --- Try to load file ---
    try:
        if not os.path.isfile(filepath):
            raise FileNotFoundError

        with open(filepath, "r", encoding="utf-8") as file:
            lines = file.readlines()

        if not lines:
            print(f"⚠️ Warning: The file '{filepath}' is empty.\n")
            log_message(f"Warning: The file '{filepath}' was empty.")
            continue

        print("✅ File loaded")
        print("===============================================")
        for line in lines:
            print(line.strip())
            time.sleep(0.025)
        print("===============================================")
        print("🛑 End of file\n")
        log_message(f"File loaded successfully: '{filepath}'.")

    except FileNotFoundError:
        error_msg = f"Error: The file '{filepath}' was not found."
        print(f"❌ {error_msg} Please try again.\n")
        log_message(error_msg)

    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        print(f"❌ {error_msg}\n")
        log_message(error_msg)
