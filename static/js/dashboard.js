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

// Socket.IO connection
const socket = io();

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
    // Disable start button
    startBtn.disabled = true;
    startBtn.textContent = 'Demo Mode - Download to Use';
    startBtn.classList.add('opacity-50', 'cursor-not-allowed');
    
    // Update connection status
    connectionText.textContent = 'Demo Mode';
    connectionStatus.style.background = '#FFA500';
    
    // Show demo message
    showStatus('This is a preview. Download Gestura to use gesture control on your computer.', 'info');
    
    // Update system status
    systemStatus.textContent = 'Demo Only';
    systemStatus.className = 'text-sm font-semibold text-orange-400 px-3 py-1 bg-orange-400/10 rounded-full border border-orange-400/30';
}

// ============================================================================
// Socket Event Handlers
// ============================================================================

socket.on('connect', () => {
    console.log('[CLIENT] Connected to server');
    updateConnectionStatus(true);
});

socket.on('disconnect', () => {
    console.log('[CLIENT] Disconnected from server');
    updateConnectionStatus(false);
    showStatus('Connection lost. Refresh page to reconnect.', 'error');
});

socket.on('connection_status', (data) => {
    console.log('[CLIENT] Connection status:', data);
    if (data.running) {
        updateSystemRunning(true);
    }
});

socket.on('status_update', (data) => {
    console.log('[CLIENT] Status update:', data);
    
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
    showStatus(data.message, 'error');
    updateSystemRunning(false);
});

socket.on('frame_update', (data) => {
    // Update camera feed with RAF batching and image decode hint
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
        showStatus('Download Gestura to enable gesture control on your local machine', 'info');
        return;
    }
    
    console.log('[CLIENT] Starting system...');
    startBtn.disabled = true;
    startBtn.textContent = 'Starting...';
    socket.emit('start_system');
});

stopBtn.addEventListener('click', () => {
    if (isDemoMode) {
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
