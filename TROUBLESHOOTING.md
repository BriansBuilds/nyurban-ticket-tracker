# Troubleshooting GitHub Actions Scheduled Workflows

## Workflow Runs Manually But Not Automatically

If your workflow runs successfully when you click "Run workflow" but doesn't run automatically on schedule, here are the most common causes and solutions:

### 1. Workflow File Must Be in Default Branch

**Problem**: GitHub Actions only reads workflow files from the default branch (usually `main` or `master`).

**Solution**:
- Make sure `.github/workflows/check-availability.yml` is committed and pushed to your default branch
- Check which branch is your default: Go to Settings → General → Default branch
- If you're on a different branch, merge it to the default branch

### 2. Actions Must Be Enabled

**Problem**: GitHub Actions might be disabled for your repository.

**Solution**:
1. Go to Settings → Actions → General
2. Under "Actions permissions", select "Allow all actions and reusable workflows"
3. Under "Workflow permissions", select "Read and write permissions"
4. Click "Save"

### 3. Repository Activity

**Problem**: GitHub may skip scheduled workflows if the repository has been inactive.

**Solution**:
- Make a small commit (even just updating the README)
- Or manually trigger the workflow once to "wake it up"
- After activity, scheduled workflows should resume

### 4. Check Scheduled Run History

**How to check**:
1. Go to the Actions tab in your repository
2. Click on "Check NY Urban Availability" workflow
3. Look for runs with a clock icon (⏰) - these are scheduled runs
4. Scheduled runs can be delayed up to 15 minutes, so check back later

### 5. Cron Schedule Limitations

**Problem**: GitHub Actions may throttle very frequent schedules.

**Current setup**:
- The workflow cron runs every 5 minutes (`*/5 * * * *`)
- The actual check interval is controlled by `CHECK_INTERVAL_MINUTES` secret
- This avoids throttling while still allowing flexible intervals

### 6. Verify Secrets Are Set

**Problem**: Missing secrets might cause the workflow to fail silently.

**Solution**:
1. Go to Settings → Secrets and variables → Actions
2. Verify these secrets are set:
   - `CHECK_INTERVAL_MINUTES` (optional, defaults to 3)
   - `EMAIL_ENABLED`
   - `EMAIL_SMTP_SERVER`
   - `EMAIL_SMTP_PORT`
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECIPIENT`

### 7. Check GitHub Status

Sometimes GitHub Actions has service issues:
- Visit [GitHub Status](https://www.githubstatus.com/)
- Check if there are any ongoing incidents

### 8. Force a Scheduled Run

To test if scheduled runs work:
1. Wait for the next scheduled time (check cron: `*/5 * * * *` means every 5 minutes)
2. Or temporarily change the cron to run in 1 minute:
   ```yaml
   schedule:
     - cron: '*/1 * * * *'  # Every minute for testing
   ```
3. Commit and push, then wait to see if it runs
4. Change it back to `*/5 * * * *` after testing

### 9. Check Workflow Logs

If scheduled runs appear but fail:
1. Go to Actions tab
2. Click on a failed scheduled run
3. Check the logs to see what went wrong
4. Common issues:
   - Missing secrets
   - Python errors
   - Network timeouts

## Still Not Working?

If none of the above helps:
1. Try creating a new workflow file with a simple test
2. Check if you're on a free GitHub account (some limitations apply)
3. Consider using a different scheduling service or running locally
