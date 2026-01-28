#!/usr/bin/env python3
"""
NY Urban Ticket Tracker
Monitors the NY Urban website for slot availability changes.
Sends notifications when sold-out slots become available.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from pathlib import Path
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
BASE_URL = "https://www.nyurban.com/?page_id=400&gametypeid=1"
# All available locations/filters
LOCATIONS = {
    1: "LaGuardia / Fri.",
    2: "Beacon / Fri.",
    3: "Brandeis / Fri.",
    4: "Brandeis / Sunday",
    5: "Clinics"
}
STATE_FILE = Path(__file__).parent / "availability_state.json"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# Load .env file if it exists (for local development)
ENV_FILE = Path(__file__).parent / ".env"
if ENV_FILE.exists():
    try:
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    except Exception as e:
        print(f"Warning: Could not load .env file: {e}", file=sys.stderr)

# Check interval configuration from environment variables
CHECK_INTERVAL_MINUTES = int(os.getenv('CHECK_INTERVAL_MINUTES', '3'))

# Email configuration from environment variables
EMAIL_ENABLED = os.getenv('EMAIL_ENABLED', 'false').lower() == 'true'
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.gmail.com')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', '587'))
EMAIL_SENDER = os.getenv('EMAIL_SENDER', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', '')


def load_previous_state():
    """Load the previous state of slot availability."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                # Ensure it has the expected structure
                if isinstance(data, dict):
                    return data
                return {}
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def get_last_check_time():
    """Get the timestamp of the last check from state file."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and '_metadata' in data:
                    return data['_metadata'].get('last_check_time', 0)
        except (json.JSONDecodeError, IOError):
            pass
    return 0


def save_last_check_time():
    """Save the current timestamp to the state file metadata."""
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {}
    else:
        data = {}
    
    if '_metadata' not in data:
        data['_metadata'] = {}
    data['_metadata']['last_check_time'] = datetime.now().timestamp()
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        print(f"Error saving last check time: {e}", file=sys.stderr)


def save_state(state):
    """Save the current state of slot availability."""
    # Preserve metadata if it exists
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                old_data = json.load(f)
                if isinstance(old_data, dict) and '_metadata' in old_data:
                    state['_metadata'] = old_data['_metadata']
        except (json.JSONDecodeError, IOError):
            pass
    
    # Add/update last check time
    if '_metadata' not in state:
        state['_metadata'] = {}
    state['_metadata']['last_check_time'] = datetime.now().timestamp()
    
    try:
        with open(STATE_FILE, 'w') as f:
            json.dump(state, f, indent=2)
    except IOError as e:
        print(f"Error saving state: {e}", file=sys.stderr)


def get_slot_key(row, location_name=""):
    """Generate a unique key for a slot based on its attributes."""
    cells = row.find_all('td')
    if len(cells) < 6:
        return None
    
    date = cells[1].get_text(strip=True) if len(cells) > 1 else ""
    gym = cells[2].get_text(strip=True) if len(cells) > 2 else ""
    level = cells[3].get_text(strip=True) if len(cells) > 3 else ""
    time = cells[4].get_text(strip=True) if len(cells) > 4 else ""
    
    # Include location in key to avoid conflicts between different locations
    return f"{location_name}|{date}|{gym}|{level}|{time}"


def scrape_availability_for_location(filter_id, location_name):
    """Scrape a specific location's availability."""
    try:
        url = f"{BASE_URL}&filter_id={filter_id}"
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with availability data
        tables = soup.find_all('table')
        table = None
        
        for t in tables:
            header_text = t.get_text().lower()
            if 'available' in header_text and 'date' in header_text:
                table = t
                break
        
        # Fallback to first table if no match found
        if not table and tables:
            table = tables[0]
        
        if not table:
            print(f"[{datetime.now()}] Warning: Could not find table for {location_name}", file=sys.stderr)
            return {}
        
        slots = {}
        rows = table.find_all('tr')
        
        # Skip header row(s) - look for row with actual data
        data_rows = []
        for row in rows:
            cells = row.find_all(['td', 'th'])
            # Skip header rows (usually have 'th' tags or contain "Date", "Gym", etc. in first row)
            if len(cells) >= 6 and cells[0].name == 'td':
                data_rows.append(row)
        
        for row in data_rows:
            cells = row.find_all('td')
            if len(cells) < 7:  # Need at least 7 columns: Select, Date, Gym, Level, Time, Fee, Available
                continue
            
            date = cells[1].get_text(strip=True) if len(cells) > 1 else ""
            gym = cells[2].get_text(strip=True) if len(cells) > 2 else ""
            level = cells[3].get_text(strip=True) if len(cells) > 3 else ""
            time = cells[4].get_text(strip=True) if len(cells) > 4 else ""
            fee = cells[5].get_text(strip=True) if len(cells) > 5 else ""
            available = cells[6].get_text(strip=True) if len(cells) > 6 else ""
            
            # Skip empty rows
            if not date or not gym:
                continue
            
            slot_key = get_slot_key(row, location_name)
            if slot_key:
                slots[slot_key] = {
                    'location': location_name,
                    'date': date,
                    'gym': gym,
                    'level': level,
                    'time': time,
                    'fee': fee,
                    'available': available,
                    'is_available': available.lower() != 'sold out' and available.lower() != ''
                }
        
        return slots
    
    except requests.RequestException as e:
        print(f"[{datetime.now()}] Error fetching {location_name}: {e}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"[{datetime.now()}] Unexpected error for {location_name}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return {}


def scrape_availability():
    """Scrape all locations and extract slot availability."""
    all_slots = {}
    
    for filter_id, location_name in LOCATIONS.items():
        print(f"[{datetime.now()}] Checking {location_name}...")
        location_slots = scrape_availability_for_location(filter_id, location_name)
        all_slots.update(location_slots)
        if location_slots:
            print(f"[{datetime.now()}] Found {len(location_slots)} slots for {location_name}")
    
    return all_slots


def send_email_notification(slots):
    """Send email notification when slots become available."""
    if not EMAIL_ENABLED:
        return
    
    if not EMAIL_SENDER or not EMAIL_RECIPIENT:
        print(f"[{datetime.now()}] Warning: Email enabled but sender/recipient not configured", file=sys.stderr)
        return
    
    # Parse recipients - support comma-separated list
    recipients = [email.strip() for email in EMAIL_RECIPIENT.split(',') if email.strip()]
    
    if not recipients:
        print(f"[{datetime.now()}] Warning: No valid email recipients found", file=sys.stderr)
        return
    
    try:
        # Create email body
        body = f"Great news! {len(slots)} slot(s) have become available on NY Urban:\n\n"
        body += "=" * 60 + "\n\n"
        
        for i, slot in enumerate(slots, 1):
            body += f"Slot {i}:\n"
            if 'location' in slot:
                body += f"  Location: {slot['location']}\n"
            body += f"  Date: {slot['date']}\n"
            body += f"  Gym: {slot['gym']}\n"
            body += f"  Level: {slot['level']}\n"
            body += f"  Time: {slot['time']}\n"
            body += f"  Fee: {slot['fee']}\n"
            body += f"  Status: {slot['available']}\n"
            body += "\n"
        
        body += "=" * 60 + "\n\n"
        body += f"Book now: {BASE_URL}\n"
        body += f"\nChecked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        # Connect to SMTP server once
        server = smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Send to all recipients
        success_count = 0
        for recipient in recipients:
            try:
                # Create message for each recipient
                msg = MIMEMultipart()
                msg['From'] = EMAIL_SENDER
                msg['To'] = recipient
                msg['Subject'] = f"🎉 NY Urban: {len(slots)} Slot(s) Available!"
                msg.attach(MIMEText(body, 'plain'))
                
                server.send_message(msg)
                success_count += 1
            except Exception as e:
                print(f"[{datetime.now()}] Error sending email to {recipient}: {e}", file=sys.stderr)
        
        server.quit()
        
        if success_count > 0:
            print(f"[{datetime.now()}] Email notification sent successfully to {success_count}/{len(recipients)} recipient(s)")
    
    except Exception as e:
        print(f"[{datetime.now()}] Error sending email: {e}", file=sys.stderr)


def check_availability_changes():
    """Check for availability changes and notify if slots become available."""
    # Check if enough time has passed since last check
    last_check_time = get_last_check_time()
    current_time = datetime.now().timestamp()
    time_since_last_check = (current_time - last_check_time) / 60  # Convert to minutes
    
    if last_check_time > 0 and time_since_last_check < CHECK_INTERVAL_MINUTES:
        minutes_remaining = CHECK_INTERVAL_MINUTES - time_since_last_check
        print(f"[{datetime.now()}] Skipping check - only {time_since_last_check:.1f} minutes since last check. Next check in {minutes_remaining:.1f} minutes.")
        return
    
    print(f"[{datetime.now()}] Running availability check (interval: {CHECK_INTERVAL_MINUTES} minutes)")
    
    previous_state = load_previous_state()
    # Remove metadata from previous state for comparison
    previous_slots = {k: v for k, v in previous_state.items() if k != '_metadata'}
    
    current_slots = scrape_availability()
    
    if not current_slots:
        print(f"[{datetime.now()}] Warning: No slots found or error occurred")
        return
    
    # Check for newly available slots
    newly_available = []
    
    for slot_key, slot_info in current_slots.items():
        previous_slot = previous_slots.get(slot_key, {})
        previous_available = previous_slot.get('is_available', False)
        current_available = slot_info.get('is_available', False)
        
        # If it was sold out before and is now available
        if not previous_available and current_available:
            newly_available.append(slot_info)
    
    # Save current state
    save_state(current_slots)
    
    # Notify about newly available slots
    if newly_available:
        print(f"\n[{datetime.now()}] 🎉 SLOTS BECAME AVAILABLE! 🎉\n")
        for slot in newly_available:
            if 'location' in slot:
                print(f"  Location: {slot['location']}")
            print(f"  Date: {slot['date']}")
            print(f"  Gym: {slot['gym']}")
            print(f"  Level: {slot['level']}")
            print(f"  Time: {slot['time']}")
            print(f"  Fee: {slot['fee']}")
            print(f"  Status: {slot['available']}")
            print()
        
        # Send email notification
        send_email_notification(newly_available)
    else:
        print(f"[{datetime.now()}] Checked - No new availability. Total slots: {len(current_slots)}")


if __name__ == "__main__":
    check_availability_changes()
