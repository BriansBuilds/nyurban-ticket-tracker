# Fly.io Setup (⭐ Best Free Option)

Fly.io offers a **completely free tier** that's perfect for this cron job. No credit card required!

## Why Fly.io?

✅ **100% free** - No credit card needed for free tier  
✅ **Runs Python directly** - No code changes  
✅ **Reliable scheduling** - Built-in cron support  
✅ **Persistent storage** - State files persist  
✅ **No spin-down** - Always running  

## Free Tier Details

- 3 shared-cpu-1x VMs (256MB RAM each)
- 160GB outbound data transfer/month
- Perfect for a simple cron job like this

## Setup Steps

### 1. Install Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Mac/Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Sign Up

```bash
fly auth signup
```

Or sign up at [fly.io](https://fly.io) and then login:
```bash
fly auth login
```

### 3. Initialize Your App

In your project directory:
```bash
fly launch
```

This will:
- Create a `fly.toml` configuration file
- Ask you to name your app
- Detect Python and set it up

### 4. Configure for Cron Job

Edit `fly.toml` (already created in this directory) or create it:

```toml
app = "nyurban-tracker"
primary_region = "iad"  # Choose closest region

[build]

[env]
  CHECK_INTERVAL_MINUTES = "3"
  EMAIL_ENABLED = "true"
  EMAIL_SMTP_SERVER = "smtp.gmail.com"
  EMAIL_SMTP_PORT = "587"
  EMAIL_SENDER = "yourname@gmail.com"
  EMAIL_PASSWORD = "your-app-password"
  EMAIL_RECIPIENT = "yourname@gmail.com"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

# Cron job configuration
[[processes]]
  name = "cron"
  command = "python fly.io/run_cron.py"
```

### 5. Create Cron Runner Script

Create `fly.io/run_cron.py`:

```python
#!/usr/bin/env python3
import time
import subprocess
import os

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_MINUTES', '3')) * 60

print(f"Starting NY Urban Ticket Tracker on Fly.io...")
print(f"Check interval: {CHECK_INTERVAL / 60} minutes")

while True:
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Running availability check...")
    subprocess.run(['python', 'check_availability.py'])
    time.sleep(CHECK_INTERVAL)
```

### 6. Set Secrets (Environment Variables)

```bash
fly secrets set CHECK_INTERVAL_MINUTES=3
fly secrets set EMAIL_ENABLED=true
fly secrets set EMAIL_SMTP_SERVER=smtp.gmail.com
fly secrets set EMAIL_SMTP_PORT=587
fly secrets set EMAIL_SENDER=yourname@gmail.com
fly secrets set EMAIL_PASSWORD=your-app-password
fly secrets set EMAIL_RECIPIENT=yourname@gmail.com,friend@gmail.com
```

### 7. Deploy

```bash
fly deploy
```

### 8. Set Up Persistent Storage (for state file)

```bash
# Create a volume for persistent storage
fly volumes create data --size 1 --region iad

# Update fly.toml to mount the volume
```

Add to `fly.toml`:
```toml
[mounts]
  source = "data"
  destination = "/data"
```

Then update `check_availability.py` to use `/data/availability_state.json`:
```python
STATE_FILE = Path("/data/availability_state.json")
```

Or use Fly.io's built-in storage (simpler):
- State files persist in the VM's filesystem
- They'll persist across deployments

### 9. Monitor

```bash
# View logs
fly logs

# Check status
fly status

# SSH into the VM
fly ssh console
```

## Alternative: Use Fly.io Timers (More Reliable)

Fly.io supports scheduled tasks via timers. Create `fly.io/timer.toml`:

```toml
[[timers]]
  schedule = "*/3 * * * *"  # Every 3 minutes
  command = "python check_availability.py"
```

Then deploy with:
```bash
fly deploy --config fly.toml --timer-config fly.io/timer.toml
```

## Cost

**Free tier covers this completely:**
- Your cron job uses minimal resources
- Well within the 3 free VMs limit
- Data transfer is minimal

**If you exceed free tier:**
- $1.94/month per VM (but you won't need to pay)

## Pros vs Cons

**Pros:**
- ✅ Completely free
- ✅ Reliable
- ✅ Runs Python directly
- ✅ Persistent storage
- ✅ No spin-down

**Cons:**
- ⚠️ Need to learn Fly.io (but it's simple)
- ⚠️ Need to set up volumes for persistent storage

## Troubleshooting

**State file not persisting?**
- Use a Fly.io volume (see step 8)
- Or use Fly.io's KV store (more advanced)

**Cron not running?**
- Check logs: `fly logs`
- Verify the process is running: `fly status`
- Check the timer configuration

## Next Steps

1. Install Fly CLI
2. Run `fly launch`
3. Set secrets
4. Deploy
5. Done! 🎉
