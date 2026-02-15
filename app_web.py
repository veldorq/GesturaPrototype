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

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gestura-secret-key-2026')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')


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
        'mode': 'demo',
        'message': 'Download for full gesture control functionality',
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


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
