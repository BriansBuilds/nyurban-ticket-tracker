# NY Urban Ticket Tracker

A monitoring tool that checks the NY Urban website every 3 minutes for slot availability changes. Notifies you when sold-out slots become available.

## Features

- ✅ Monitors NY Urban open play slots every 3 minutes
- ✅ Detects when "Sold Out" slots become available
- ✅ Tracks state between runs to identify changes
- ✅ Console and email notifications for newly available slots
- ✅ Runs on GitHub Actions (no PC needed!)

## Setup Options

### Option 1: GitHub Actions (Recommended - No PC Required!)

This is the easiest way to run the tracker 24/7 without keeping your computer on.

#### 1. Fork/Clone this repository

#### 2. Set up GitHub Secrets

Go to your repository → Settings → Secrets and variables → Actions → New repository secret

Add these secrets:

- `CHECK_INTERVAL_MINUTES`: How often to check (in minutes). Default is `3` if not set. Example: `3` for every 3 minutes, `5` for every 5 minutes
- `EMAIL_ENABLED`: `true`
- `EMAIL_SMTP_SERVER`: Your SMTP server (e.g., `smtp.gmail.com` for Gmail)
- `EMAIL_SMTP_PORT`: SMTP port (e.g., `587` for Gmail)
- `EMAIL_SENDER`: Your email address (e.g., `yourname@gmail.com`)
- `EMAIL_PASSWORD`: Your email password or app-specific password (for Gmail, use an [App Password](https://support.google.com/accounts/answer/185833))
- `EMAIL_RECIPIENT`: Email address(es) to receive notifications. For multiple recipients, separate with commas: `email1@gmail.com,email2@gmail.com`

**Gmail Setup:**
1. Enable 2-Factor Authentication on your Google account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. Generate an app password for "Mail"
4. Use that password as `EMAIL_PASSWORD`

#### 3. Enable GitHub Actions

The workflow is already set up in `.github/workflows/check-availability.yml`. It will:
- Run every minute, but only actually check based on `CHECK_INTERVAL_MINUTES` secret (default: 3 minutes)
- Check for availability changes across all 5 locations
- Send email notifications when slots become available
- Persist state between runs
- **You can change the check interval anytime by updating the `CHECK_INTERVAL_MINUTES` secret - no code changes needed!**

The workflow will start running automatically once you push to the repository!

#### 4. Test the Workflow

You can manually trigger a test run:
- Go to Actions tab in your repository
- Select "Check NY Urban Availability"
- Click "Run workflow"

### Option 2: Local Setup (PC Required)

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Configure Email (Optional)

Set environment variables for email notifications:

**Windows (PowerShell):**
```powershell
$env:EMAIL_ENABLED="true"
$env:EMAIL_SMTP_SERVER="smtp.gmail.com"
$env:EMAIL_SMTP_PORT="587"
$env:EMAIL_SENDER="yourname@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"
$env:EMAIL_RECIPIENT="yourname@gmail.com"
```

**Linux/Mac:**
```bash
export EMAIL_ENABLED=true
export EMAIL_SMTP_SERVER=smtp.gmail.com
export EMAIL_SMTP_PORT=587
export EMAIL_SENDER=yourname@gmail.com
export EMAIL_PASSWORD=your-app-password
export EMAIL_RECIPIENT=yourname@gmail.com
```

Or create a `.env` file (not recommended for production, but useful for testing).

#### 3. Test the Script

Run the script manually to ensure it works:

```bash
python check_availability.py
```

The script will:
- Scrape the NY Urban website
- Save the current state to `availability_state.json`
- Print any newly available slots to the console
- Send email notifications if configured

#### 4. Set Up Cron Job

#### Linux/Mac

1. Open your crontab:
   ```bash
   crontab -e
   ```

2. Add this line (adjust the path to your project):
   ```bash
   * * * * * cd /path/to/nyurban-ticket-tracker && /usr/bin/python3 check_availability.py >> availability.log 2>&1
   ```

   Or if using a virtual environment:
   ```bash
   * * * * * cd /path/to/nyurban-ticket-tracker && /path/to/venv/bin/python check_availability.py >> availability.log 2>&1
   ```

#### Windows

Windows doesn't use cron. Use Task Scheduler instead:

1. Open Task Scheduler
2. Create Basic Task
3. Name it "NY Urban Ticket Tracker"
4. Trigger: Daily → Repeat task every 3 minutes
5. Action: Start a program
   - Program: `python` (or full path to python.exe)
   - Arguments: `check_availability.py`
   - Start in: `C:\Users\Brian Kim\Documents\GitHub\nyurban-ticket-tracker`
6. Check "Open the Properties dialog" and click Finish
7. In Properties:
   - Check "Run whether user is logged on or not"
   - Check "Run with highest privileges" (if needed)
   - In Settings: Check "Allow task to be run on demand" and "Run task as soon as possible after a scheduled start is missed"

Alternatively, use a PowerShell script (see `run_scheduler.ps1`).

## Files

- `check_availability.py` - Main monitoring script
- `availability_state.json` - Tracks previous slot states (auto-generated)
- `requirements.txt` - Python dependencies
- `.cronjob` - Cron configuration example

## How It Works

1. The script fetches the NY Urban open play page
2. Parses the table to extract slot information
3. Compares current availability with the previous state
4. If a slot changes from "Sold Out" to available, it prints a notification
5. Saves the current state for the next run

## Email Configuration

Email notifications are configured via environment variables:

- `EMAIL_ENABLED`: Set to `true` to enable email notifications
- `EMAIL_SMTP_SERVER`: SMTP server (e.g., `smtp.gmail.com`)
- `EMAIL_SMTP_PORT`: SMTP port (usually `587` for TLS)
- `EMAIL_SENDER`: Your email address
- `EMAIL_PASSWORD`: Your email password or app-specific password
- `EMAIL_RECIPIENT`: Email address(es) to receive notifications. **For multiple recipients, separate with commas**: `email1@gmail.com,email2@gmail.com,email3@example.com`

### Gmail Setup

1. Enable 2-Factor Authentication
2. Create an [App Password](https://myaccount.google.com/apppasswords)
3. Use the app password (not your regular password) as `EMAIL_PASSWORD`

### Other Email Providers

- **Outlook/Hotmail**: `smtp-mail.outlook.com`, port `587`
- **Yahoo**: `smtp.mail.yahoo.com`, port `587`
- **Custom SMTP**: Use your provider's SMTP settings

## Customization

### Different Check Intervals (GitHub Actions)

Simply update the `CHECK_INTERVAL_MINUTES` secret in your repository settings:
- Go to Settings → Secrets and variables → Actions
- Edit `CHECK_INTERVAL_MINUTES` and set it to your desired interval (e.g., `3`, `5`, `10`)
- The change takes effect on the next workflow run

**Note:** The workflow runs every minute, but the script will only perform the actual check if enough time has passed based on `CHECK_INTERVAL_MINUTES`. This allows you to change the interval without modifying code!

### Different Check Intervals (Local)

- **Every 3 minutes**: Change cron to `*/3 * * * *` (current)
- **Every 5 minutes**: Change cron to `*/5 * * * *`
- **Every 10 minutes**: Change cron to `*/10 * * * *`

## Troubleshooting

- **Script not running**: Check that Python path in cron is correct
- **No output**: Check `availability.log` for errors
- **Website changes**: If the website structure changes, update the parsing logic in `scrape_availability()`

## License

MIT
