# Render Setup (⭐ Recommended - Easiest Free Option!)

Render is the **easiest free option** that can run Python directly and has built-in cron job support. Perfect for getting started quickly!

## Why Render?

✅ **Runs Python directly** - No code conversion needed  
✅ **Built-in cron jobs** - Native cron support  
✅ **Free tier available** - Free tier with some limitations  
✅ **Simple setup** - Easy deployment from GitHub  
✅ **Persistent storage** - State files persist automatically  

## Setup Steps

### 1. Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Create a new account

### 2. Create a Cron Job

1. Click "New +" → "Cron Job"
2. Connect your GitHub repository (`nyurban-ticket-tracker`)
3. Configure the cron job:
   - **Name**: `nyurban-tracker`
   - **Schedule**: `*/3 * * * *` (every 3 minutes)
   - **Command**: `python check_availability.py`
   - **Branch**: `main` (or your default branch)
   - **Root Directory**: `/` (or leave empty)
   - **Plan**: Free (or Starter for $7/month if you want more reliability)

### 3. Set Environment Variables

In the Render dashboard → Environment tab, add:

```
CHECK_INTERVAL_MINUTES=3
EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=yourname@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=yourname@gmail.com,friend@gmail.com
```

### 4. Deploy

Render will automatically deploy and run your cron job on schedule.

### 5. Monitor

- View logs in the Render dashboard
- Check the "Events" tab to see when cron jobs run
- Set up email notifications for failures (in Settings)

## Quick Setup Checklist

- [ ] Sign up at render.com
- [ ] Create new Cron Job
- [ ] Connect GitHub repository
- [ ] Set schedule to `*/3 * * * *`
- [ ] Set command to `python check_availability.py`
- [ ] Add all environment variables
- [ ] Deploy!

That's it! Your tracker will now run every 3 minutes automatically.

## Free Tier Limitations

- Cron jobs may spin down after inactivity
- May take a moment to wake up
- Still more reliable than GitHub Actions

## Cost

- **Free tier**: $0/month - Available with some limitations (may spin down)
- **Starter plan**: $7/month flat rate - More reliable, no spin-down delays

**Note**: The $0.00016/minute pricing you may see is for on-demand services. Cron jobs on the Starter plan are included in the $7/month flat rate, not charged per-minute.

See [COST_ANALYSIS.md](COST_ANALYSIS.md) for detailed cost breakdown.

## Pros vs Cons

**Pros:**
- ✅ Built-in cron support
- ✅ Runs Python directly
- ✅ Simple setup
- ✅ Free tier available

**Cons:**
- ⚠️ Free tier may have delays
- ⚠️ Cron jobs may spin down
