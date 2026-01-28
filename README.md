# NY Urban Ticket Tracker

A monitoring tool that checks the NY Urban website every 3 minutes for slot availability changes. Notifies you when sold-out slots become available.

## Features

- ✅ Monitors NY Urban open play slots every 3 minutes
- ✅ Detects when "Sold Out" slots become available
- ✅ Tracks state between runs to identify changes
- ✅ Console and email notifications for newly available slots
- ✅ Runs on GitHub Actions (no PC needed!)

## Setup Options

### Option 1: Fly.io (🏆 BEST FREE OPTION - 100% Free!)

Fly.io offers a **completely free tier** with no credit card required. Perfect for this use case!

See [fly.io/README.md](fly.io/README.md) for detailed setup instructions.

**Pros:**
- ✅ **100% free** - No credit card needed
- ✅ **Runs Python directly** - No code changes
- ✅ **Very reliable** - No delays
- ✅ **Persistent storage** - State files persist
- ✅ **No spin-down** - Always running

**Setup time**: ~10 minutes

### Option 2: Render (⭐ EASIEST FREE OPTION - Recommended!)

Render has built-in cron job support and a free tier. **This is the easiest option to get started!**

See [render/README.md](render/README.md) for detailed setup instructions.

**Pros:**
- ✅ **Free tier** - No credit card required
- ✅ **Built-in cron** - Native cron job support
- ✅ **Runs Python directly** - No code changes needed
- ✅ **Easiest setup** - ~5 minutes total
- ✅ **Automatic deployments** - Updates on git push

**Setup time**: ~5 minutes

**Quick Start:**
1. Go to [render.com](https://render.com) and sign up
2. Click "New +" → "Cron Job"
3. Connect your GitHub repo
4. Set schedule: `*/3 * * * *`
5. Set command: `python check_availability.py`
6. Add environment variables
7. Deploy! 🎉

### Option 3: Railway (⭐ Easiest Paid Option - $5/month)

Railway is the easiest option but uses a $5/month credit (may charge if exceeded).

See [railway/README.md](railway/README.md) for detailed setup instructions.

**Pros:**
- ✅ **Runs Python directly** - No code conversion needed
- ✅ **Very reliable** - Much better than GitHub Actions
- ✅ **Easiest setup** - Just connect GitHub and deploy
- ✅ **$5 credit/month** - Usually free, may charge if exceeded

**Setup time**: ~5 minutes

### Option 4: GitHub Actions (Free but Unreliable)

Railway is the **best option** for running your Python script reliably. It requires no code changes and is very simple to set up.

See [railway/README.md](railway/README.md) for detailed setup instructions.

**Pros:**
- ✅ **Runs Python directly** - No code conversion needed
- ✅ **Very reliable** - Much better than GitHub Actions
- ✅ **Easiest setup** - Just connect GitHub and deploy
- ✅ **Free tier** - $5 credit/month (plenty for this)
- ✅ **Automatic deployments** - Updates on git push

**Setup time**: ~5 minutes

### Option 2: Render (Good Alternative)

Render has built-in cron job support and can run Python directly.

See [render/README.md](render/README.md) for setup instructions.

**Pros:**
- ✅ Built-in cron jobs
- ✅ Runs Python directly
- ✅ Free tier available

**Cons:**
- ⚠️ Free tier may have some delays

### Option 3: GitHub Actions (Free but Unreliable)

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
- Run every 3 minutes automatically (via GitHub's schedule trigger)
- Check for availability changes across all 5 locations
- Send email notifications when slots become available
- Persist state between runs
- **You can change the check interval anytime by updating the `CHECK_INTERVAL_MINUTES` secret - no code changes needed!**

**⚠️ Important Note about Scheduled Workflows:**
GitHub Actions scheduled workflows (`schedule` trigger) are **not guaranteed** to run on time. Delays of 3-10 minutes (or even hours) are common, and runs may be skipped entirely. This is a known limitation of GitHub Actions.

**For more reliable scheduling**, consider using an external cron service to trigger the workflow via API. See [EXTERNAL_CRON_SETUP.md](EXTERNAL_CRON_SETUP.md) for detailed instructions.

**Note:** The cron schedule runs every 3 minutes. The script will only perform the actual check if enough time has passed based on your `CHECK_INTERVAL_MINUTES` secret (default: 3 minutes). If you set `CHECK_INTERVAL_MINUTES` to a value greater than 3, the script will skip runs until enough time has passed.

The workflow will start running automatically once you push to the repository!

#### 4. Test the Workflow

You can manually trigger a test run:
- Go to Actions tab in your repository
- Select "Check NY Urban Availability"
- Click "Run workflow"

**Important**: Make sure the workflow file is in your **default branch** (usually `main` or `master`) for scheduled runs to work!

#### 5. Troubleshooting Scheduled Runs

If the workflow runs manually but not automatically, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions.

### Option 3: Other Services

See [ALTERNATIVES.md](ALTERNATIVES.md) for other options like:
- Vercel Cron Jobs
- Railway
- Render
- Fly.io
- AWS Lambda

### Option 4: Local Setup (PC Required)

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

### GitHub Actions Scheduled Workflows Not Running

If your workflow runs manually but not automatically, try these steps:

1. **Check if Actions are enabled**:
   - Go to Settings → Actions → General
   - Ensure "Allow all actions and reusable workflows" is selected
   - Ensure "Workflow permissions" allows read and write permissions

2. **Verify the workflow file is in the default branch**:
   - The workflow must be in your default branch (usually `main` or `master`)
   - Make sure you've committed and pushed the `.github/workflows/check-availability.yml` file

3. **Check workflow run history**:
   - Go to Actions tab → Check NY Urban Availability
   - Look for scheduled runs (they may show as "Scheduled" or have a clock icon)
   - Scheduled runs can be delayed up to 15 minutes

4. **Repository activity requirement**:
   - GitHub may skip scheduled workflows if the repository has been inactive
   - Try making a small commit or manually triggering the workflow to "wake it up"

5. **Cron schedule limitations**:
   - GitHub Actions may throttle very frequent schedules (like every minute)
   - Consider using a longer cron interval (e.g., `*/5 * * * *` for every 5 minutes) since the script respects `CHECK_INTERVAL_MINUTES` anyway

6. **Check GitHub Actions status page**:
   - Visit [GitHub Status](https://www.githubstatus.com/) to see if there are any service issues

### Local Setup Issues

- **Script not running**: Check that Python path in cron is correct
- **No output**: Check `availability.log` for errors
- **Website changes**: If the website structure changes, update the parsing logic in `scrape_availability()`

## License

MIT
