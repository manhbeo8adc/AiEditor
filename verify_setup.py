import subprocess
import sys
import os

def check_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

print("=== Environment Verification ===")
print("✓ Python:", sys.version.split()[0] if sys.version_info >= (3, 8) else "❌ Version too old")
print("✓ FFmpeg:", "OK" if check_command("ffmpeg -version") else "❌ Not installed")
print("✓ Node.js:", "OK" if check_command("node --version") else "❌ Not installed")
print("✓ Git:", "OK" if check_command("git --version") else "❌ Not installed")

# Check directories
dirs = ['temp', 'uploads', 'output', 'backend', 'frontend']
for d in dirs:
    print(f"✓ Directory {d}:", "OK" if os.path.exists(d) else "❌ Missing")

print("\nSetup complete! Ready for development.") 