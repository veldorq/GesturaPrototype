"""
Gestura Web Dashboard - Flask Backend
======================================
Provides web interface for hand gesture control system.

Usage:
    python app.py
    Then open: http://localhost:5000
"""

from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import cv2
import base64
import sys
import traceback

# Import gesture system
from PROTOTYPE import HandGestureControlSystem, Config

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gestura-secret-key-2026'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global state
gesture_system = None
system_thread = None
is_running = False


@app.route('/')
def dashboard():
    """Render main dashboard page"""
    return render_template('dashboard.html')


@app.route('/product')
def product():
    """Render product page"""
    return render_template('product.html')


@app.route('/dashboard')
def dashboard_page():
    """Render dashboard (alias for compatibility)"""
    return render_template('dashboard.html')


@app.route('/api/status')
def get_status():
    """Get system status"""
    return jsonify({
        'running': is_running,
        'gestures_available': 11,
        'fps_target': Config.FPS_TARGET,
        'camera_index': Config.CAMERA_INDEX
    })


@app.route('/api/config')
def get_config():
    """Get system configuration"""
    return jsonify({
        'debug_mode': Config.DEBUG_GESTURE_DETECTION,
        'smoothing': Config.MOUSE_SMOOTHING,
        'buffer_size': Config.GESTURE_BUFFER_SIZE,
        'confidence_threshold': Config.CONFIDENCE_THRESHOLD
    })


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"[WEB] Client connected: {threading.current_thread().name}")
    emit('connection_status', {'status': 'connected', 'running': is_running})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print("[WEB] Client disconnected")


@socketio.on('start_system')
def start_gesture_system():
    """Start the gesture control system"""
    global gesture_system, system_thread, is_running
    
    if is_running:
        emit('error', {'message': 'System already running'})
        return
    
    try:
        print("\n[WEB] Starting gesture system...")
        emit('status_update', {'status': 'initializing', 'message': 'Starting gesture engine...'})
        
        # Create gesture system with SocketIO integration
        gesture_system = HandGestureControlSystem(socketio=socketio)
        
        # Start in separate thread
        system_thread = threading.Thread(target=run_gesture_system, daemon=True)
        system_thread.start()
        
        is_running = True
        emit('status_update', {'status': 'running', 'message': 'System started successfully!'})
        print("[WEB] Gesture system started successfully")
        
    except Exception as e:
        error_msg = f"Failed to start system: {str(e)}"
        print(f"[ERROR] {error_msg}")
        traceback.print_exc()
        emit('error', {'message': error_msg, 'details': traceback.format_exc()})


@socketio.on('stop_system')
def stop_gesture_system():
    """Stop the gesture control system"""
    global gesture_system, is_running
    
    if not is_running:
        emit('error', {'message': 'System not running'})
        return
    
    try:
        print("\n[WEB] Stopping gesture system...")
        
        if gesture_system:
            gesture_system.running = False
            time.sleep(0.5)  # Allow cleanup
            gesture_system.cleanup()
        
        is_running = False
        emit('status_update', {'status': 'stopped', 'message': 'System stopped'})
        print("[WEB] Gesture system stopped")
        
    except Exception as e:
        error_msg = f"Error stopping system: {str(e)}"
        print(f"[ERROR] {error_msg}")
        emit('error', {'message': error_msg})


def run_gesture_system():
    """Run gesture system in background thread"""
    global gesture_system, is_running
    
    try:
        gesture_system.run()
    except Exception as e:
        print(f"[ERROR] Gesture system crashed: {e}")
        traceback.print_exc()
        is_running = False
        socketio.emit('error', {
            'message': 'System crashed',
            'details': str(e),
            'recovery': 'Click Restart to try again'
        })


def emit_frame(frame):
    """Emit video frame to web client"""
    try:
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 75])
        frame_b64 = base64.b64encode(buffer.tobytes()).decode('utf-8')
        
        socketio.emit('frame_update', {'image': frame_b64})
    except Exception as e:
        print(f"[ERROR] Frame encoding failed: {e}")


def emit_gesture_event(gesture_name, action, confidence=1.0):
    """Emit gesture detection event"""
    socketio.emit('gesture_detected', {
        'gesture': gesture_name,
        'action': action,
        'confidence': confidence,
        'timestamp': time.time()
    })


def emit_metrics(fps, gesture_count):
    """Emit system metrics"""
    socketio.emit('metrics_update', {
        'fps': round(fps, 1),
        'gesture_count': gesture_count,
        'timestamp': time.time()
    })


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  GESTURA WEB DASHBOARD")
    print("="*70)
    print("\n🚀 Starting Flask server...")
    print(f"📍 Dashboard URL: http://localhost:5000")
    print(f"📷 Camera Index: {Config.CAMERA_INDEX}")
    print(f"🎯 Target FPS: {Config.FPS_TARGET}")
    print("\n💡 Tips:")
    print("   • Open the URL in your browser")
    print("   • Click 'Start System' to begin gesture control")
    print("   • Press Ctrl+C to stop the server")
    print("\n" + "="*70 + "\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n\n[SHUTDOWN] Server stopped by user")
        if gesture_system:
            gesture_system.cleanup()
    except Exception as e:
        print(f"\n[ERROR] Server error: {e}")
        traceback.print_exc()
