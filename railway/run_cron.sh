#!/bin/bash
# Railway cron wrapper script
# Runs check_availability.py every 3 minutes

echo "Starting NY Urban Ticket Tracker on Railway..."
echo "Check interval: ${CHECK_INTERVAL_MINUTES:-3} minutes"

while true; do
  echo "[$(date)] Running availability check..."
  python check_availability.py
  sleep $((CHECK_INTERVAL_MINUTES * 60))
done
