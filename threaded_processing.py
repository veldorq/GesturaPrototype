"""
Threaded Frame Processing for Real-Time Gesture Recognition
============================================================
Author: Senior Python Accessibility Engineer & Performance Optimizer
Date: February 9, 2026

Purpose:
    Decouple camera capture from CNN inference to prevent frame drops and UI lag.
    Maintains stable 30 FPS camera loop even during CNN inference latency spikes.

Integration:
    Drop-in replacement for synchronous frame processing in main loop.

Safety Guarantees:
    - Thread-safe frame buffer with locks
    - Graceful shutdown on errors
    - Preserves existing execution order and APIs
    - No architectural changes to gesture recognition logic
"""

import threading
import queue
import time
import cv2
from collections import deque


class ThreadedFrameProcessor:
    """
    Thread-safe frame processing pipeline.
    
    Architecture:
        Main Thread (Camera Loop @ 30 FPS):
            Capture frame → Store in buffer → Display UI → Repeat
        
        Worker Thread (CNN Inference):
            Fetch frame from buffer → Run CNN → Store result → Repeat
    
    Benefits:
        - Camera loop never blocked by CNN inference
        - UI remains responsive during heavy computation
        - Frame drops eliminated during latency spikes
        - Graceful degradation if worker thread slow
    """
    
    def __init__(self, max_queue_size=2):
        """
        Initialize threaded processor.
        
        Args:
            max_queue_size: Maximum frames to buffer (2 = process every other frame if CNN slow)
        """
        # Frame queues (thread-safe)
        self.input_queue = queue.Queue(maxsize=max_queue_size)
        self.result_queue = queue.Queue(maxsize=1)  # Only store latest result
        
        # Thread control
        self.worker_thread = None
        self.stop_event = threading.Event()
        self.running = False
        
        # Processing callback (set by user)
        self.process_callback = None
        
        # Statistics
        self.frames_captured = 0
        self.frames_processed = 0
        self.frames_dropped = 0
        
        # Latest result cache (for display thread)
        self.latest_result = None
        self.result_lock = threading.Lock()
        
        print("\nThreaded Frame Processor Initialized:")
        print(f"   - Max queue size: {max_queue_size}")
        print(f"   - Mode: Decoupled camera/inference")
    
    def set_process_callback(self, callback):
        """
        Set processing callback function.
        
        Args:
            callback: Function that takes (frame, hand_landmarks) and returns gesture result
        """
        self.process_callback = callback
    
    def _worker_loop(self):
        """
        Worker thread main loop.
        Fetches frames from queue, processes them, stores results.
        """
        print("🔄 Worker thread started")
        
        while not self.stop_event.is_set():
            try:
                # Get frame from queue (timeout to check stop_event periodically)
                try:
                    frame_data = self.input_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                
                # Process frame
                if self.process_callback is not None:
                    result = self.process_callback(frame_data)
                    
                    # Store result (overwrites previous if not consumed)
                    with self.result_lock:
                        self.latest_result = result
                    
                    self.frames_processed += 1
                
                # Mark task done
                self.input_queue.task_done()
            
            except Exception as e:
                print(f"WARNING: Worker thread error: {e}")
                continue
        
        print("🛑 Worker thread stopped")
    
    def start(self):
        """Start worker thread"""
        if self.running:
            print("WARNING: Worker thread already running")
            return
        
        self.stop_event.clear()
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
        self.running = True
        print("[SUCCESS] Worker thread started successfully")
    
    def stop(self):
        """Stop worker thread gracefully"""
        if not self.running:
            return
        
        print("🛑 Stopping worker thread...")
        self.stop_event.set()
        
        if self.worker_thread is not None:
            self.worker_thread.join(timeout=2.0)
        
        self.running = False
        print("[SUCCESS] Worker thread stopped")
    
    def submit_frame(self, frame_data):
        """
        Submit frame for processing.
        
        Args:
            frame_data: Dictionary with 'frame' and other metadata
        
        Returns:
            bool: True if frame queued, False if queue full (frame dropped)
        """
        try:
            self.input_queue.put_nowait(frame_data)
            self.frames_captured += 1
            return True
        except queue.Full:
            # Queue full - drop frame (camera stays at 30 FPS, worker catching up)
            self.frames_dropped += 1
            return False
    
    def get_latest_result(self):
        """
        Get most recent processing result.
        
        Returns:
            Latest result or None if no results yet
        """
        with self.result_lock:
            return self.latest_result
    
    def get_statistics(self):
        """Get processing statistics"""
        return {
            'frames_captured': self.frames_captured,
            'frames_processed': self.frames_processed,
            'frames_dropped': self.frames_dropped,
            'queue_size': self.input_queue.qsize(),
            'drop_rate': (self.frames_dropped / max(1, self.frames_captured)) * 100
        }
    
    def __enter__(self):
        """Context manager support"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager cleanup"""
        self.stop()


class AdaptiveFrameRateController:
    """
    Adaptive frame rate control to maintain target FPS.
    
    Purpose:
        - Prevent resource overuse when system idle
        - Maintain stable frame rate during active use
        - Reduce CPU usage without sacrificing responsiveness
    """
    
    def __init__(self, target_fps=30):
        """
        Initialize frame rate controller.
        
        Args:
            target_fps: Target frames per second
        """
        self.target_fps = target_fps
        self.target_frame_time = 1.0 / target_fps
        
        self.last_frame_time = time.time()
        self.frame_times = deque(maxlen=30)  # Last 30 frame times
        
        self.actual_fps = 0.0
    
    def wait_for_next_frame(self):
        """
        Wait to maintain target FPS.
        
        Returns:
            float: Actual FPS achieved
        """
        current_time = time.time()
        elapsed = current_time - self.last_frame_time
        
        # Calculate sleep time to hit target FPS
        sleep_time = self.target_frame_time - elapsed
        
        if sleep_time > 0:
            time.sleep(sleep_time)
        
        # Update timing
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        self.last_frame_time = current_time
        
        # Track frame times
        self.frame_times.append(frame_time)
        
        # Calculate actual FPS (average over last 30 frames)
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.actual_fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        
        return self.actual_fps
    
    def get_statistics(self):
        """Get FPS statistics"""
        if len(self.frame_times) == 0:
            return {'actual_fps': 0.0, 'target_fps': self.target_fps, 'stability': 0.0}
        
        # Calculate FPS stability (lower variance = more stable)
        import numpy as np
        frame_times_array = np.array(list(self.frame_times))
        variance = np.var(frame_times_array)
        stability = 1.0 - min(variance * 100, 1.0)  # 1.0 = perfectly stable, 0.0 = very unstable
        
        return {
            'actual_fps': self.actual_fps,
            'target_fps': self.target_fps,
            'stability': stability * 100,  # Percentage
            'frame_time_variance': variance
        }


def test_threaded_processing():
    """Test threaded frame processor"""
    print("\n" + "="*70)
    print("  THREADED FRAME PROCESSOR TEST")
    print("="*70 + "\n")
    
    # Mock processing function (simulates CNN inference)
    def mock_process(frame_data):
        """Simulate CNN processing with variable latency"""
        import random
        time.sleep(random.uniform(0.02, 0.08))  # 20-80ms latency
        return {'gesture': 'scroll_down', 'confidence': 0.85}
    
    # Create processor
    processor = ThreadedFrameProcessor(max_queue_size=2)
    processor.set_process_callback(mock_process)
    
    # Start worker thread
    processor.start()
    
    # Simulate camera loop
    print("Simulating camera loop (30 FPS)...")
    fps_controller = AdaptiveFrameRateController(target_fps=30)
    
    for i in range(60):  # 2 seconds of frames
        # Submit frame
        frame_queued = processor.submit_frame({'frame': f'frame_{i}'})
        
        # Get latest result
        result = processor.get_latest_result()
        
        # Wait for next frame
        actual_fps = fps_controller.wait_for_next_frame()
        
        if i % 15 == 0:  # Print every 0.5s
            print(f"  Frame {i}: FPS={actual_fps:.1f}, Queued={frame_queued}, Result={result is not None}")
    
    # Get statistics
    proc_stats = processor.get_statistics()
    fps_stats = fps_controller.get_statistics()
    
    print(f"\n📊 Processing Statistics:")
    print(f"   - Frames captured: {proc_stats['frames_captured']}")
    print(f"   - Frames processed: {proc_stats['frames_processed']}")
    print(f"   - Frames dropped: {proc_stats['frames_dropped']}")
    print(f"   - Drop rate: {proc_stats['drop_rate']:.1f}%")
    
    print(f"\n📊 FPS Statistics:")
    print(f"   - Target FPS: {fps_stats['target_fps']}")
    print(f"   - Actual FPS: {fps_stats['actual_fps']:.1f}")
    print(f"   - Stability: {fps_stats['stability']:.1f}%")
    
    # Stop processor
    processor.stop()


if __name__ == "__main__":
    test_threaded_processing()
