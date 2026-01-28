# Railway Setup (Recommended)

Railway is the **easiest and most reliable** option for running your Python script. It can run Python directly, has built-in cron support, and is very simple to set up.

## Why Railway?

✅ **Runs Python directly** - No code conversion needed  
✅ **Reliable scheduling** - Much more reliable than GitHub Actions  
✅ **Simple setup** - Just connect your repo and deploy  
✅ **Free tier available** - $5 free credit monthly  
✅ **Easy environment variables** - Set secrets in the dashboard  

## Setup Steps

### 1. Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Create a new project

### 2. Deploy from GitHub

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `nyurban-ticket-tracker` repository
4. Railway will auto-detect it's a Python project

### 3. Set Up Cron Job

Railway doesn't have built-in cron, but we'll use a simple approach:

**Option A: Use Railway's Cron Service (Recommended)**
1. In your Railway project, add a new service
2. Select "Cron Job"
3. Set the schedule: `*/3 * * * *` (every 3 minutes)
4. Set the command: `python check_availability.py`
5. Set working directory to `/`

**Option B: Use a Cron Wrapper Script**

Create `railway/run_cron.sh`:
```bash
#!/bin/bash
while true; do
  python check_availability.py
  sleep 180  # 3 minutes
done
```

Then set the start command to: `bash railway/run_cron.sh`

### 4. Set Environment Variables

In Railway dashboard → Variables tab, add:

```
CHECK_INTERVAL_MINUTES=3
EMAIL_ENABLED=true
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=yourname@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_RECIPIENT=yourname@gmail.com,friend@gmail.com
```

### 5. Configure State Storage

Railway provides persistent storage. The `availability_state.json` file will persist between runs automatically.

### 6. Deploy

Railway will automatically deploy when you push to your repository, or you can trigger a manual deploy.

## Alternative: Use External Cron Service

If Railway's cron setup is complex, you can:
1. Deploy the script as a web service on Railway
2. Use an external cron service (Cronhub, EasyCron) to hit a webhook endpoint
3. The webhook triggers the check

See `railway/webhook.py` for this approach.

## Cost

- **Free tier**: $5 credit/month (plenty for this use case)
- **Hobby plan**: $5/month if you exceed free tier
- Very affordable for a simple cron job

## Monitoring

- Check logs in Railway dashboard
- Set up alerts for failures
- Monitor resource usage

## Pros vs Cons

**Pros:**
- ✅ Easiest setup
- ✅ Runs Python directly
- ✅ Reliable
- ✅ Good free tier
- ✅ Automatic deployments

**Cons:**
- ⚠️ Need to set up cron (but it's simple)
- ⚠️ Free tier has limits (but sufficient for this)
