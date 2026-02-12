import ast
import os
import shutil
import subprocess
import sys

def get_imports_from_file(filepath):
    """Extract top-level package imports from a Python file"""
    packages = set()
    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    pkg = alias.name.split('.')[0]
                    if pkg not in ['os', 'sys', 'argparse', 'pathlib']:  # Exclude stdlib
                        packages.add(pkg)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    pkg = node.module.split('.')[0]
                    if pkg not in ['os', 'sys', 'argparse', 'pathlib']:
                        packages.add(pkg)
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return packages

file_paths = [
    'gui.bin',
    'main.bin',
    'CLI-app.dmg'
]

for file_path in file_paths:
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File '{file_path}' has been deleted.")  
    except FileNotFoundError:
        pass

# Scan main.py for imports
packages = get_imports_from_file('main.py')

# Only include packages that exist as directories
local_packages = [p for p in packages if os.path.isdir(p)]

cmd_main = [
    'nuitka',
    'main.py',
    '--static-libpython=no',
]

cmd_args = []

for pkg in local_packages:
    cmd_args.append(f'--include-package={pkg}')

print(f"Auto-detected packages main.py: {local_packages}")
subprocess.run(cmd_main + cmd_args)

try:
    shutil.copy('main.bin', 'Installer/CLI-app.app/Contents/MacOS/main.bin')
except FileNotFoundError:
    print("main.bin not found in current directory")
    sys.exit(1)

packages = get_imports_from_file('gui.py')

cmd_gui = [
    'nuitka',
    'gui.py',
    '--static-libpython=no',
]

local_packages = [p for p in packages if os.path.isdir(p)]

cmd_args = []

for pkg in local_packages:
    cmd_args.append(f'--include-package={pkg}')

print(f"Auto-detected packages gui.py: {local_packages}")
subprocess.run(cmd_gui + cmd_args)

try:
    shutil.copy('gui.bin', 'Installer/CLI-app.app/Contents/MacOS/gui.bin')
except FileNotFoundError:
    print("gui.bin not found in current directory")
    sys.exit(1)


cmd_build_dmg = [
    'create-dmg',
    '--volname', 'CLI app',
    '--app-drop-link', '600', '300',
    'CLI-app.dmg',
    'Installer/CLI-app.app'
]
print("--------------------------------------------")
print("Building DMG...")
subprocess.run(cmd_build_dmg)

os.makedirs('build', exist_ok=True)

shutil.copy('CLI-app.dmg', 'build/CLI-app.dmg')

print("DMG created at: build/CLI-app.dmg")