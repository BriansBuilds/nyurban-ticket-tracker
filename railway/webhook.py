#!/usr/bin/env python3
"""
Webhook endpoint for Railway deployment
Allows external cron services to trigger the check via HTTP
"""

from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Optional: Add a secret token for security
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', '')

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'}), 200

@app.route('/check', methods=['POST', 'GET'])
def trigger_check():
    """Trigger availability check"""
    # Optional: Verify secret token
    if WEBHOOK_SECRET:
        provided_secret = request.headers.get('X-Webhook-Secret') or request.args.get('secret')
        if provided_secret != WEBHOOK_SECRET:
            return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # Run the check script
        result = subprocess.run(
            ['python', 'check_availability.py'],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return jsonify({
            'status': 'success' if result.returncode == 0 else 'error',
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr
        }), 200 if result.returncode == 0 else 500
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Check timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
