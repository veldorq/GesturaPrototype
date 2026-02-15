"""
Download Request Handler for Gestura
Captures leads before providing download link
"""

from flask import render_template, request, jsonify, redirect, url_for
import os
import json
from datetime import datetime

# Simple JSON-based storage (for demo - use database in production)
LEADS_FILE = 'leads.json'

def load_leads():
    """Load existing leads from file"""
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_lead(lead_data):
    """Save new lead to file"""
    leads = load_leads()
    leads.append(lead_data)
    with open(LEADS_FILE, 'w') as f:
        json.dump(leads, f, indent=2)

def register_download_routes(app):
    """Register download-related routes"""
    
    @app.route('/download')
    def download_page():
        """Show download form"""
        return render_template('download.html')
    
    @app.route('/api/request-download', methods=['POST'])
    def request_download():
        """Process download request and capture email"""
        data = request.json
        
        # Validate input
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        use_case = data.get('use_case', '').strip()
        
        if not email or '@' not in email:
            return jsonify({'error': 'Valid email required'}), 400
        
        # Save lead
        lead_data = {
            'email': email,
            'name': name,
            'use_case': use_case,
            'timestamp': datetime.now().isoformat(),
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        save_lead(lead_data)
        
        # Generate unique download token (simple version)
        download_token = f"{email.split('@')[0]}_{datetime.now().timestamp()}"
        
        return jsonify({
            'success': True,
            'message': 'Check your email for download instructions',
            'download_token': download_token
        })
    
    @app.route('/get-download/<token>')
    def get_download(token):
        """Provide download after email verification"""
        # In production: verify token, check database
        # For now: redirect to GitHub releases
        return redirect('https://github.com/veldorq/GesturaPrototype/releases/latest')
