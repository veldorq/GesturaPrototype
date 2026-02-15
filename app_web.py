"""
Gestura Web - Production Deployment
====================================
Serves product page and demo interface.

NOTE: Full gesture control requires local installation due to camera access.
This deployed version showcases the interface and provides download instructions.
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import os

# Import download handler
from download_handler import register_download_routes

# Configuration from environment variables
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gestura-default-secret-2026')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'

# CORS configuration
ALLOWED_ORIGINS = os.environ.get('ALLOWED_ORIGINS', '*')
socketio = SocketIO(app, cors_allowed_origins=ALLOWED_ORIGINS, async_mode='gevent')

# Deployment info
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE', 'demo')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'https://github.com/veldorq/GesturaPrototype')


@app.route('/')
def home():
    """Redirect to product page"""
    return render_template('product.html')


@app.route('/product')
def product():
    """Render product landing page"""
    return render_template('product.html')


@app.route('/dashboard')
def dashboard():
    """Render demo dashboard (info only - requires local install for full functionality)"""
    return render_template('dashboard.html')


@app.route('/api/status')
def get_status():
    """Get deployment status"""
    return jsonify({
        'deployment': 'production',
        'mode': DEPLOYMENT_MODE,
        'environment': app.config['ENV'],
        'message': 'Download for full gesture control functionality',
        'github_repo': GITHUB_REPO,
        'gestures_available': 11,
        'features': {
            'real_time_tracking': True,
            'privacy_first': True,
            'zero_setup': True,
            'accuracy': '95%+'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint for hosting platform"""
    return jsonify({'status': 'healthy'}), 200


# Register download routes
register_download_routes(app)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
