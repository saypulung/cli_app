import logging
import os
import platform
import sys
import shlex
import threading
import queue
import subprocess
import tkinter as tk
import ttkbootstrap as ttk
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from ttkbootstrap.constants import *

def get_self_dir():
    # When compiled with Nuitka or frozen
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)

    # When running as normal Python script
    return os.path.dirname(os.path.abspath(__file__))


BASE_DIR = os.getcwd()


def get_executable_dir():
    # 1. Try sys.argv[0] first - this points to the actual executable that was invoked
    # This is crucial for macOS .app bundles where sys.executable points to the Python interpreter
    try:
        executable_path = Path(sys.argv[0]).resolve()
    except (IndexError, ValueError):
        # Fallback to sys.executable if sys.argv[0] is not available
        executable_path = Path(sys.executable).resolve()
    
    # If sys.argv[0] points to a Python script in development, use __file__ instead
    if executable_path.suffix == ".py" and not (".app/Contents/MacOS" in str(executable_path)):
        executable_path = Path(__file__).resolve()

    # 2. Handle the macOS .app bundle structure
    # If the path contains 'YourApp.app/Contents/MacOS', we need to go up 3 levels
    # to get to the directory containing the .app
    if ".app/Contents/MacOS" in str(executable_path):
        return executable_path.parents[3]
    
    # 3. Otherwise, just return the directory containing the binary
    return executable_path.parent

app_dir = get_executable_dir()

def get_log_path(app_name):
    if platform.system() == "Darwin":  # macOS
        # Points to ~/Library/Logs/YourAppName
        log_path = Path.home() / "Library" / "Logs" / app_name
    elif platform.system() == "Windows":
        # Points to AppData/Local/YourAppName/Logs
        log_path = Path(os.getenv('LOCALAPPDATA')) / app_name / "Logs"
    else:
        # Linux/Fallback: .config/YourAppName/logs
        log_path = Path.home() / ".config" / app_name / "logs"
    
    log_path.mkdir(parents=True, exist_ok=True)
    return log_path / "app.log"

# 2. Configure the logger
LOG_FILE = get_log_path("TestApp")

print(f"Logging to: {LOG_FILE}")

# 2. Create the Handler separately
# This is where interval and backupCount belong!
rotation_handler = TimedRotatingFileHandler(
    LOG_FILE, 
    when="midnight", 
    interval=1, 
    backupCount=7,
    encoding='utf-8'
)

# 3. Pass the handler into basicConfig
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        rotation_handler,      # Our daily rotating file handler
        logging.StreamHandler() # Also prints to your terminal
    ]
)

logger = logging.getLogger(__name__)

logger.info(f"Application started. App directory: {app_dir}")
logger.info(f"Python executable: {BASE_DIR}")

def detect_base_command():

	script_dir = get_executable_dir()
	logger.info(f"Detecting base command in script directory: {script_dir}")
	# Prefer a packaged executable if present next to this file
	candidates = [
		os.path.join(script_dir, "main"),
		os.path.join(script_dir, "main.bin"),
		os.path.join(script_dir, "main.exe"),
		os.path.join(script_dir, "main.py"),
	]
	for c in candidates:
		if os.path.exists(c):
			logger.info(f"Found executable candidate: {c}")
			# Use the file directly (may be an executable or python script)
			return c

	# Fallback to invoking with the current Python interpreter
	main_py = os.path.join(script_dir, "main.py")
	if os.path.exists(main_py):
		logger.info(f"Falling back to running main.py with Python: {main_py}")
		return f"{sys.executable} {shlex.quote(main_py)}"

	# Last resort: rely on PATH
	return "main"


root = tk.Tk()
root.title("CLI Runner")

# Top: existing demo buttons
top_frame = ttk.Frame(root)
top_frame.pack(fill="x", padx=8, pady=6)

# Middle: command entry and Run button
cmd_frame = ttk.Frame(root)
cmd_frame.pack(fill="x", padx=8, pady=6)

detected = detect_base_command()
logger.info(f"Detected base command: {detected}")
cmd_var = tk.StringVar(value=detected)

cmd_label = ttk.Label(cmd_frame, text="Command:")
cmd_label.pack(side=LEFT, padx=(0, 6))

cmd_entry = ttk.Entry(cmd_frame, textvariable=cmd_var, width=60)
cmd_entry.pack(side=LEFT, fill="x", expand=True)

run_btn = ttk.Button(cmd_frame, text="Run", bootstyle=PRIMARY)
run_btn.pack(side=LEFT, padx=6)

# Bottom: output text area
out_frame = ttk.Frame(root)
out_frame.pack(fill="both", expand=True, padx=8, pady=(0, 8))

out_text = tk.Text(out_frame, wrap="none", height=16)
out_text.pack(fill="both", expand=True)

out_q = queue.Queue()


def poll_queue():
	try:
		while True:
			line = out_q.get_nowait()
			out_text.insert("end", line)
			out_text.see("end")
	except queue.Empty:
		pass
	root.after(100, poll_queue)


def run_command():
	cmd_text = cmd_var.get().strip()
	if not cmd_text:
		return

	try:
		args = shlex.split(cmd_text)
	except Exception:
		args = cmd_text

	try:
		bundle_dir = os.path.dirname(sys.argv[0])
		env_path = os.path.abspath(os.path.join(bundle_dir, "..", "Resources", "python_env"))

		my_env = os.environ.copy()
		my_env["PYTHONPATH"] = os.path.join(env_path, "lib/python3.11/site-packages")
		my_env["PATH"] = os.path.join(env_path, "bin") + os.pathsep + my_env["PATH"]
		proc = subprocess.Popen(
			args,
			env=my_env,
			stdout=subprocess.PIPE,
			stderr=subprocess.STDOUT,
			text=True,
			bufsize=1,
		)
	except Exception as e:
		out_q.put(f"Failed to start process: {e}\n")
		return

	def reader():
		for line in proc.stdout:
			out_q.put(line)
		proc.wait()
		out_q.put(f"\n[Process exited with code {proc.returncode}]\n")

	t = threading.Thread(target=reader, daemon=True)
	t.start()


run_btn.config(command=run_command)

poll_queue()

root.mainloop()
