"""
Gestura Web - Production Deployment
====================================
Serves product page and demo interface.

NOTE: Full gesture control requires local installation due to camera access.
This deployed version showcases the interface and provides download instructions.
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_compress import Compress
import os
import logging
import sys
from datetime import timedelta

# Import download handler
from download_handler import register_download_routes

# Configuration from environment variables
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'gestura-default-secret-2026')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False').lower() == 'true'
app.config['PRODUCTION'] = app.config['ENV'] == 'production'

# Performance optimizations
app.config['COMPRESS_MIMETYPES'] = [
    'text/html', 'text/css', 'text/xml', 'text/plain',
    'application/json', 'application/javascript',
    'application/x-javascript', 'image/svg+xml'
]
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(days=365)  # Cache static files

# Initialize compression
Compress(app)

# Setup structured logging
def setup_logging():
    """Configure production-grade logging."""
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(
        '[%(asctime)s] %(levelname)-5s | %(name)-15s | %(message)s'
    ))
    
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info("="*60)
    app.logger.info("🚀 Gestura Web Dashboard Starting")
    app.logger.info(f"Environment: {app.config['ENV']}")
    app.logger.info(f"Debug Mode: {app.config['DEBUG']}")
    app.logger.info("="*60)

setup_logging()

# CORS configuration - Parse allowed origins
allowed_origins_str = os.environ.get('ALLOWED_ORIGINS', '')
if allowed_origins_str:
    allowed_origins = [origin.strip() for origin in allowed_origins_str.split(',') if origin.strip()]
else:
    # Development fallback
    allowed_origins = ['http://localhost:3000', 'http://localhost:3001', 'https://gestura-web.onrender.com']
    app.logger.warning("⚠️  No ALLOWED_ORIGINS set, using development defaults")

app.logger.info(f"📡 CORS Origins: {', '.join(allowed_origins)}")

# Apply CORS to API routes
CORS(app, resources={
    r"/api/*": {
        "origins": allowed_origins,
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

socketio = SocketIO(app, cors_allowed_origins=allowed_origins, async_mode='gevent')

# Deployment info
DEPLOYMENT_MODE = os.environ.get('DEPLOYMENT_MODE', 'demo')
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'https://github.com/veldorq/GesturaPrototype')


# Security Headers Middleware
@app.after_request
def add_security_headers(response):
    """Add comprehensive security headers to all responses"""
    
    # Content Security Policy - Prevent XSS attacks
    csp_directives = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.socket.io",
        "style-src 'self' 'unsafe-inline'",
        "font-src 'self' data:",
        "img-src 'self' data: blob:",
        "connect-src 'self' wss: ws: https://gestura-api.onrender.com",
        "frame-ancestors 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "upgrade-insecure-requests"
    ]
    response.headers['Content-Security-Policy'] = '; '.join(csp_directives)
    
    # HSTS - Force HTTPS with 2-year max-age
    response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    
    # Cross-Origin-Opener-Policy - Origin isolation
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    
    # Cross-Origin-Embedder-Policy
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    
    # Cross-Origin-Resource-Policy
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    
    # Prevent MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Clickjacking protection
    response.headers['X-Frame-Options'] = 'DENY'
    
    # XSS Protection (legacy browsers)
    response.headers['X-XSS-Protection'] = '1; mode=block'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Permissions Policy - Disable unnecessary features
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), interest-cohort=()'
    
    return response


@app.route('/')
def home():
    """Redirect to product page"""
    response = app.make_response(render_template('product.html'))
    response.headers['Cache-Control'] = 'public, max-age=300'  # 5 minutes
    return response


@app.route('/product')
def product():
    """Render product landing page"""
    response = app.make_response(render_template('product.html'))
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response


@app.route('/dashboard')
def dashboard():
    """Render demo dashboard (info only - requires local install for full functionality)"""
    response = app.make_response(render_template('dashboard.html'))
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response


@app.route('/api/status')
def get_status():
    """Get deployment status"""
    app.logger.info("📊 Status endpoint called")
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
            'accuracy': '99%'
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
    app.logger.info(f"🌐 Starting server on port {port}")
    app.logger.info(f"📍 GitHub Repo: {GITHUB_REPO}")
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
