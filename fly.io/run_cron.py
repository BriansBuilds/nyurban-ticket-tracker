#!/usr/bin/env python3
"""
Fly.io cron runner script
Runs check_availability.py every CHECK_INTERVAL_MINUTES
"""
import time
import subprocess
import os
import sys
from pathlib import Path

# Add parent directory to path so we can import check_availability
sys.path.insert(0, str(Path(__file__).parent.parent))

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_MINUTES', '3')) * 60

print(f"Starting NY Urban Ticket Tracker on Fly.io...")
print(f"Check interval: {CHECK_INTERVAL / 60} minutes")

while True:
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] Running availability check...")
    
    try:
        result = subprocess.run(
            ['python', 'check_availability.py'],
            cwd=Path(__file__).parent.parent,
            check=False
        )
        if result.returncode != 0:
            print(f"[{timestamp}] Check failed with return code {result.returncode}")
    except Exception as e:
        print(f"[{timestamp}] Error running check: {e}")
    
    time.sleep(CHECK_INTERVAL)
