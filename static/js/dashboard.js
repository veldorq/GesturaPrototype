/**
 * Gestura Dashboard - Client-Side JavaScript
 * Handles WebSocket communication and UI updates with RAF batching
 */

// Check if we're in demo mode
let isDemoMode = false;
fetch('/api/status')
    .then(res => res.json())
    .then(data => {
        if (data.mode === 'demo' || data.deployment === 'production') {
            isDemoMode = true;
            initDemoMode();
        }
    })
    .catch(() => {
        // If API fails, assume local mode
        isDemoMode = false;
    });

// Socket.IO connection with enhanced reconnection
const socket = io({
    reconnection: true,
    reconnectionDelay: 1000,
    reconnectionDelayMax: 5000,
    reconnectionAttempts: 5,
    timeout: 20000
});

// Reconnection tracking
let reconnectAttempts = 0;
let lastHeartbeat = Date.now();
let heartbeatInterval = null;

// UI Elements
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const connectionStatus = document.getElementById('connection-status');
const connectionText = document.getElementById('connection-text');
const statusBanner = document.getElementById('status-banner');
const statusMessage = document.getElementById('status-message');
const cameraFeed = document.getElementById('camera-feed');
const cameraPlaceholder = document.getElementById('camera-placeholder');
const currentGesture = document.getElementById('current-gesture');
const lastAction = document.getElementById('last-action');
const fpsDisplay = document.getElementById('fps-display');
const gestureCount = document.getElementById('gesture-count');
const systemStatus = document.getElementById('system-status');
const gestureHistory = document.getElementById('gesture-history');

// State
let gestureCounter = 0;
let historyItems = [];
const MAX_HISTORY = 10;

// Performance Optimization: RAF Batching
let pendingUpdates = {};
let rafScheduled = false;

function scheduleUpdate(key, updateFn) {
    pendingUpdates[key] = updateFn;
    if (!rafScheduled) {
        rafScheduled = true;
        requestAnimationFrame(flushUpdates);
    }
}

function flushUpdates() {
    const updates = pendingUpdates;
    pendingUpdates = {};
    rafScheduled = false;
    
    for (const key in updates) {
        updates[key]();
    }
}

// Demo Mode Handler
function initDemoMode() {
    console.log('[DEMO] Initializing demo mode...');
    
    // Update button to show it's demo
    startBtn.textContent = 'Start Demo';
    startBtn.disabled = false;
    startBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    
    // Update connection status
    connectionText.textContent = 'Demo Mode';
    connectionStatus.style.background = '#00D9FF';
    connectionStatus.classList.add('pulse-cyan');
    
    // Update system status
    systemStatus.textContent = 'Demo Ready';
    systemStatus.className = 'text-sm font-semibold text-cyan-400 px-3 py-1 bg-cyan-400/10 rounded-full border border-cyan-400/30';
    
    // Override start button to run demo
    startBtn.onclick = startDemoSimulation;
}

// Demo simulation data
const demoGestures = [
    { gesture: 'OPEN_PALM', action: 'Scroll Down', icon: '✋', color: 'cyan' },
    { gesture: 'CLOSED_FIST', action: 'Scroll Up', icon: '✊', color: 'purple' },
    { gesture: 'INDEX_FINGER', action: 'Mouse Move', icon: '☝️', color: 'cyan' },
    { gesture: 'PEACE_SIGN', action: 'Click', icon: '✌️', color: 'purple' },
    { gesture: 'SWIPE_LEFT', action: 'Previous Tab', icon: '👈', color: 'cyan' },
    { gesture: 'SWIPE_RIGHT', action: 'Next Tab', icon: '👉', color: 'purple' },
    { gesture: 'PINCH_ZOOM', action: 'Zoom In/Out', icon: '🤏', color: 'cyan' },
    { gesture: 'THUMB_DOWN', action: 'Mute/Unmute', icon: '👎', color: 'purple' }
];

let demoInterval = null;
let demoRunning = false;
let demoIndex = 0;
let demoFPS = 30;

function startDemoSimulation() {
    if (demoRunning) return;
    
    demoRunning = true;
    startBtn.disabled = true;
    startBtn.textContent = 'Demo Running...';
    stopBtn.classList.remove('hidden');
    stopBtn.disabled = false;
    
    // Show demo camera placeholder
    cameraPlaceholder.innerHTML = `
        <div class="text-center">
            <div class="w-32 h-32 mx-auto mb-6 bg-gradient-to-br from-cyan-500/30 to-purple-500/30 rounded-full flex items-center justify-center relative overflow-hidden demo-pulse">
                <div id="demo-hand" class="text-8xl transition-all duration-500">✋</div>
                <div class="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 animate-pulse"></div>
            </div>
            <p class="text-cyan-200/80 text-lg font-medium mb-2">Demo Simulation Running</p>
            <p class="text-sm text-cyan-300/50">Showing all 11 gestures</p>
        </div>
    `;
    
    cameraPlaceholder.classList.remove('hidden');
    cameraFeed.classList.add('hidden');
    
    showStatus('Demo started! Watch the gestures cycle through automatically', 'success');
    
    systemStatus.textContent = 'Running';
    systemStatus.className = 'text-sm font-semibold text-green-400 px-3 py-1 bg-green-400/10 rounded-full border border-green-400/30';
    
    // Simulate FPS
    demoFPS = 30;
    updateDemoMetrics();
    
    // Start gesture cycling
    demoIndex = 0;
    cycleNextGesture();
    demoInterval = setInterval(cycleNextGesture, 2500);
    
    // Override stop button
    stopBtn.onclick = stopDemoSimulation;
}

function cycleNextGesture() {
    const gesture = demoGestures[demoIndex];
    
    // Update hand icon
    const handIcon = document.getElementById('demo-hand');
    if (handIcon) {
        handIcon.textContent = gesture.icon;
        handIcon.style.transform = 'scale(1.1)';
        setTimeout(() => {
            handIcon.style.transform = 'scale(1)';
        }, 200);
    }
    
    // Trigger gesture detection animation
    currentGesture.textContent = gesture.gesture;
    currentGesture.classList.add('gesture-flash');
    setTimeout(() => currentGesture.classList.remove('gesture-flash'), 400);
    
    // Update action
    lastAction.textContent = gesture.action;
    lastAction.classList.add('pulse-purple');
    setTimeout(() => lastAction.classList.remove('pulse-purple'), 600);
    
    // Increment counter
    gestureCounter++;
    gestureCount.textContent = gestureCounter;
    
    // Add to history
    addHistoryItem({
        gesture: gesture.gesture,
        action: gesture.action,
        timestamp: new Date().toISOString()
    });
    
    // Move to next gesture
    demoIndex = (demoIndex + 1) % demoGestures.length;
    
    // Vary FPS slightly for realism
    demoFPS = 28 + Math.floor(Math.random() * 5);
    fpsDisplay.textContent = demoFPS;
}

function updateDemoMetrics() {
    if (!demoRunning) return;
    
    fpsDisplay.textContent = demoFPS;
    fpsDisplay.className = 'text-3xl font-bold text-green-400';
    
    setTimeout(updateDemoMetrics, 100);
}

function stopDemoSimulation() {
    demoRunning = false;
    
    if (demoInterval) {
        clearInterval(demoInterval);
        demoInterval = null;
    }
    
    startBtn.disabled = false;
    startBtn.textContent = 'Start Demo';
    stopBtn.classList.add('hidden');
    
    // Reset display
    cameraPlaceholder.innerHTML = `
        <div class="text-center">
            <div class="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-cyan-500/20 to-purple-500/20 rounded-2xl flex items-center justify-center">
                <svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"/>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"/>
                </svg>
            </div>
            <p class="text-cyan-200/80 text-lg font-medium">Click "Start Demo" to see gestures</p>
            <p class="text-sm text-cyan-300/50 mt-3">Demo cycles through all 11 gestures</p>
        </div>
    `;
    
    currentGesture.textContent = 'NONE';
    lastAction.textContent = '—';
    fpsDisplay.textContent = '0';
    
    systemStatus.textContent = 'Demo Ready';
    systemStatus.className = 'text-sm font-semibold text-cyan-400 px-3 py-1 bg-cyan-400/10 rounded-full border border-cyan-400/30';
    
    showStatus('Demo stopped. Click "Start Demo" to run again', 'info');
}

// ============================================================================
// Socket Event Handlers
// ============================================================================

socket.on('connect', () => {
    console.log('[CLIENT] Connected to server');
    reconnectAttempts = 0;
    lastHeartbeat = Date.now();
    updateConnectionStatus(true);
    
    if (reconnectAttempts > 0) {
        showStatus('Reconnected to server successfully', 'success');
    }
    
    // Start heartbeat monitoring
    if (heartbeatInterval) clearInterval(heartbeatInterval);
    heartbeatInterval = setInterval(() => {
        const elapsed = Date.now() - lastHeartbeat;
        if (elapsed > 30000) { // 30 seconds stale
            console.warn('[CLIENT] Connection appears stale, reconnecting...');
            socket.disconnect();
            socket.connect();
        }
    }, 10000); // Check every 10 seconds
});

socket.on('disconnect', (reason) => {
    console.log('[CLIENT] Disconnected from server:', reason);
    updateConnectionStatus(false);
    
    if (heartbeatInterval) {
        clearInterval(heartbeatInterval);
        heartbeatInterval = null;
    }
    
    if (reason === 'io server disconnect') {
        showStatus('Server closed connection. Click refresh to reconnect.', 'error');
    } else if (reason === 'transport close') {
        showStatus('Connection lost. Attempting to reconnect...', 'warning');
    } else {
        showStatus('Connection lost. Reconnecting automatically...', 'warning');
    }
});

socket.on('reconnect_attempt', (attempt) => {
    reconnectAttempts = attempt;
    console.log(`[CLIENT] Reconnection attempt ${attempt}/5`);
    showStatus(`Reconnecting... (Attempt ${attempt}/5)`, 'info');
});

socket.on('reconnect_error', (error) => {
    console.error('[CLIENT] Reconnection error:', error);
});

socket.on('reconnect_failed', () => {
    console.error('[CLIENT] Reconnection failed after 5 attempts');
    showStatus('Unable to reconnect. Please refresh the page.', 'error');
});

socket.on('connection_status', (data) => {
    console.log('[CLIENT] Connection status:', data);
    lastHeartbeat = Date.now(); // Update heartbeat
    if (data.running) {
        updateSystemRunning(true);
    }
});

socket.on('status_update', (data) => {
    console.log('[CLIENT] Status update:', data);
    lastHeartbeat = Date.now(); // Update heartbeat
    
    if (data.status === 'running') {
        updateSystemRunning(true);
        showStatus(data.message, 'success');
    } else if (data.status === 'stopped') {
        updateSystemRunning(false);
        showStatus(data.message, 'info');
    } else if (data.status === 'initializing') {
        showStatus(data.message, 'info');
    }
});

socket.on('error', (data) => {
    console.error('[CLIENT] Error:', data);
    lastHeartbeat = Date.now(); // Update heartbeat
    showStatus(data.message, 'error');
    updateSystemRunning(false);
});

socket.on('frame_update', (data) => {
    // Update camera feed with RAF batching and image decode hint
    lastHeartbeat = Date.now(); // Update heartbeat
    if (data.image) {
        scheduleUpdate('frame', () => {
            const img = new Image();
            img.decode().then(() => {
                cameraFeed.src = img.src;
                
                // Show feed, hide placeholder
                if (cameraFeed.classList.contains('hidden')) {
                    cameraFeed.classList.remove('hidden');
                    cameraPlaceholder.classList.add('hidden');
                }
            }).catch(() => {
                // Fallback for older browsers
                cameraFeed.src = 'data:image/jpeg;base64,' + data.image;
                
                if (cameraFeed.classList.contains('hidden')) {
                    cameraFeed.classList.remove('hidden');
                    cameraPlaceholder.classList.add('hidden');
                }
            });
            img.src = 'data:image/jpeg;base64,' + data.image;
        });
    }
});

socket.on('gesture_detected', (data) => {
    console.log('[CLIENT] Gesture detected:', data);
    lastHeartbeat = Date.now(); // Update heartbeat
    
    // Batch gesture updates with RAF
    scheduleUpdate('gesture', () => {
        // Update current gesture display
        currentGesture.textContent = data.gesture;
        currentGesture.classList.add('gesture-flash');
        setTimeout(() => currentGesture.classList.remove('gesture-flash'), 400);
        
        // Update last action
        lastAction.textContent = data.action || '—';
        lastAction.classList.add('pulse-purple');
        setTimeout(() => lastAction.classList.remove('pulse-purple'), 600);
    });
    
    // Increment counter
    gestureCounter++;
    
    scheduleUpdate('metrics', () => {
        gestureCount.textContent = gestureCounter;
    });
    
    // Add to history
    addHistoryItem(data);
});

socket.on('metrics_update', (data) => {
    lastHeartbeat = Date.now(); // Update heartbeat
    // Batch metrics updates with RAF
    scheduleUpdate('fps', () => {
        // Update FPS display
        if (data.fps !== undefined) {
            fpsDisplay.textContent = data.fps;
            
            // Color based on FPS performance
            if (data.fps >= 25) {
                fpsDisplay.className = 'text-3xl font-bold text-cyan-400';
            } else if (data.fps >= 15) {
                fpsDisplay.className = 'text-3xl font-bold text-yellow-400';
            } else {
                fpsDisplay.className = 'text-3xl font-bold text-red-400';
            }
        }
    });
    
    // Update gesture count
    if (data.gesture_count !== undefined) {
        gestureCounter = data.gesture_count;
        gestureCount.textContent = gestureCounter;
    }
});

// ============================================================================
// Button Event Handlers
// ============================================================================

startBtn.addEventListener('click', () => {
    if (isDemoMode) {
        startDemoSimulation();
        return;
    }
    
    console.log('[CLIENT] Starting system...');
    startBtn.disabled = true;
    startBtn.textContent = 'Starting...';
    socket.emit('start_system');
});

stopBtn.addEventListener('click', () => {
    if (isDemoMode) {
        stopDemoSimulation();
        return;
    }
    
    console.log('[CLIENT] Stopping system...');
    stopBtn.disabled = true;
    stopBtn.textContent = 'Stopping...';
    socket.emit('stop_system');
});

// ============================================================================
// UI Helper Functions
// ============================================================================

function updateConnectionStatus(connected) {
    scheduleUpdate('connection', () => {
        if (connected) {
            connectionStatus.style.backgroundColor = '#00D9FF'; // cyan
            connectionStatus.classList.add('pulse-cyan');
            connectionText.textContent = 'Connected';
        } else {
            connectionStatus.style.backgroundColor = '#ef4444'; // red
            connectionStatus.classList.remove('pulse-cyan');
            connectionText.textContent = 'Disconnected';
        }
    });
}

function updateSystemRunning(running) {
    scheduleUpdate('systemState', () => {
        if (running) {
            // Show stop button, hide start button
            startBtn.classList.add('hidden');
            stopBtn.classList.remove('hidden');
            stopBtn.disabled = false;
            stopBtn.textContent = 'Stop System';
            
            // Update system status
            systemStatus.textContent = 'Running';
            systemStatus.className = 'text-sm font-semibold text-emerald-400 px-3 py-1 bg-emerald-400/10 rounded-full border border-emerald-400/30';
        } else {
            // Show start button, hide stop button
            stopBtn.classList.add('hidden');
            startBtn.classList.remove('hidden');
            startBtn.disabled = false;
            startBtn.textContent = 'Start System';
            
            // Update system status
            systemStatus.textContent = 'Offline';
            systemStatus.className = 'text-sm font-semibold text-yellow-400 px-3 py-1 bg-yellow-400/10 rounded-full border border-yellow-400/30';
            
            // Hide camera feed
            cameraFeed.classList.add('hidden');
            cameraPlaceholder.classList.remove('hidden');
            
            // Reset displays
            currentGesture.textContent = 'NONE';
            lastAction.textContent = '—';
            fpsDisplay.textContent = '0';
        }
    });
}

function showStatus(message, type = 'info') {
    statusMessage.textContent = message;
    statusBanner.classList.remove('hidden');
    
    // Remove old classes
    statusBanner.className = 'mb-6 p-4 rounded-lg';
    
    // Add type-specific styling
    if (type === 'success') {
        statusBanner.classList.add('bg-green-900', 'border', 'border-green-700', 'text-green-200');
    } else if (type === 'error') {
        statusBanner.classList.add('bg-red-900', 'border', 'border-red-700', 'text-red-200');
    } else if (type === 'info') {
        statusBanner.classList.add('bg-blue-900', 'border', 'border-blue-700', 'text-blue-200');
    }
    
    // Auto-hide after 5 seconds for non-error messages
    if (type !== 'error') {
        setTimeout(() => {
            statusBanner.classList.add('hidden');
        }, 5000);
    }
}

function addHistoryItem(data) {
    // Create history item
    const timestamp = new Date(data.timestamp * 1000).toLocaleTimeString();
    const item = {
        gesture: data.gesture,
        action: data.action,
        timestamp: timestamp
    };
    
    // Add to beginning of array
    historyItems.unshift(item);
    
    // Keep only last MAX_HISTORY items
    if (historyItems.length > MAX_HISTORY) {
        historyItems.pop();
    }
    
    // Render history
    renderHistory();
}

function renderHistory() {
    scheduleUpdate('history', () => {
        if (historyItems.length === 0) {
            gestureHistory.innerHTML = '<p class="text-sm text-cyan-300/50 text-center py-6 font-light">No actions yet</p>';
            return;
        }
        
        gestureHistory.innerHTML = historyItems.map(item => `
            <div class="p-3 glass-panel-strong rounded-lg text-sm border-l-2 border-cyan-500/50 hover:border-purple-500/50 transition-all duration-300">
                <div class="flex justify-between items-center">
                    <span class="font-semibold text-cyan-200">${item.gesture}</span>
                    <span class="text-cyan-400/60 text-xs">${item.timestamp}</span>
                </div>
                <div class="text-purple-300/80 text-xs mt-1">${item.action}</div>
            </div>
        `).join('');
    });
}

// ============================================================================
// Initialization
// ============================================================================

console.log('[CLIENT] Dashboard initialized');
showStatus('Connected to server. Click "Start System" to begin.', 'info');
