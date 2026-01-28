# Setting Up External Cron Service for Reliable Scheduling

GitHub Actions scheduled workflows (`schedule` trigger) are **not guaranteed** to run on time. Delays of 3-10 minutes (or even hours) are common, and runs may be skipped entirely.

For more reliable scheduling, you can use an external cron service to trigger the workflow via the GitHub API.

## How It Works

Instead of relying on GitHub's `schedule` trigger, an external service makes HTTP requests to GitHub's API to trigger the workflow using `workflow_dispatch`. This is much more reliable.

## Option 1: Cronhub (Free Tier Available)

1. Go to [Cronhub.io](https://cronhub.io/)
2. Sign up for a free account
3. Create a new monitor:
   - **URL**: `https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/check-availability.yml/dispatches`
   - **Method**: POST
   - **Headers**:
     - `Authorization`: `Bearer YOUR_GITHUB_TOKEN`
     - `Accept`: `application/vnd.github+json`
     - `X-GitHub-Api-Version`: `2022-11-28`
   - **Body** (JSON): `{"ref":"main"}` (replace `main` with your default branch)
   - **Schedule**: Every 3 minutes (`*/3 * * * *`)

### Creating a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Name it "Cronhub Workflow Trigger"
4. Select scopes: `repo` (full control of private repositories)
5. Generate and copy the token
6. Use this token in Cronhub's Authorization header

## Option 2: EasyCron (Free Tier Available)

1. Go to [EasyCron.com](https://www.easycron.com/)
2. Sign up for free account
3. Create a new cron job:
   - **URL**: `https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/check-availability.yml/dispatches`
   - **Method**: POST
   - **Headers**: Same as Cronhub above
   - **Body**: `{"ref":"main"}`
   - **Schedule**: Every 3 minutes

## Option 3: Google Cloud Scheduler (Free Tier: 3 Jobs)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to Cloud Scheduler
3. Create a new job:
   - **Target**: HTTP
   - **URL**: `https://api.github.com/repos/YOUR_USERNAME/YOUR_REPO/actions/workflows/check-availability.yml/dispatches`
   - **HTTP method**: POST
   - **Headers**: Same as above
   - **Body**: `{"ref":"main"}`
   - **Frequency**: `*/3 * * * *` (every 3 minutes)

## Option 4: GitHub Actions (Current - Less Reliable)

The current setup uses GitHub's `schedule` trigger, which works but has delays:
- Delays of 3-10 minutes are common
- Sometimes runs are skipped entirely
- No guarantee of execution

This is fine if you don't need precise timing, but for production use, an external cron service is recommended.

## API Endpoint Details

**Endpoint**: 
```
POST https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches
```

**Headers**:
```
Authorization: Bearer YOUR_GITHUB_TOKEN
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
Content-Type: application/json
```

**Body**:
```json
{
  "ref": "main"
}
```

Replace:
- `{owner}`: Your GitHub username
- `{repo}`: Your repository name
- `{workflow_id}`: The filename of your workflow (e.g., `check-availability.yml`)
- `main`: Your default branch name

## Testing

After setting up, you can test by:
1. Manually triggering from the external service
2. Checking the Actions tab to see if the workflow runs
3. Verifying it runs at the scheduled times

## Security Note

- Keep your GitHub token secure
- Use a token with minimal required permissions
- Consider using a GitHub App instead of a personal access token for better security
