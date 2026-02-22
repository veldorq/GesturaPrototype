# 🎤 Voice Recognition & UI Improvements Guide

## ✅ What's Been Improved

### 🔊 Voice Recognition Enhancements

1. **Higher Sensitivity** 
   - Energy threshold lowered from 1000 → 300 for better voice pickup
   - Dynamic adjustment enabled for ambient noise compensation
   - Calibration time increased to 2 seconds for accuracy

2. **Better Response Time**
   - Phrase timeout reduced from 5s → 3s  
   - Pause threshold increased to 1.2s for clearer phrase detection
   - Real-time voice status tracking

3. **Status Feedback**
   - Live voice recognition status displayed in UI
   - Shows: "🎤 Listening...", "⏳ Processing...", "✓ [recognized text]"
   - Console feedback for calibration and detection

### 🎨 UI Improvements

#### Voice Status Indicator (Top-Left)
- **🎤 VOICE: ON** (blinking green) - Actively listening
- **🔇 VOICE: OFF** (gray) - Voice control disabled
- Shows last recognized command below status

#### Lighting Quality Warnings (Top-Center)
- **⚠️ TOO DARK** - Room brightness below 60 (increase lighting)
- **⚠️ TOO BRIGHT** - Room brightness above 200 (reduce glare/sunlight)
- **⚠️ LOW CONTRAST** - Uneven lighting (adjust light placement)
- **Brightness meter** on right side (green = optimal)

#### Hand Positioning Guidance (Top-Center)
- **👈 Move hand RIGHT** - Too far left
- **👉 Move hand LEFT** - Too far right  
- **👇 Move hand DOWN** - Too high
- **👆 Move hand UP** - Too low
- **🔍 Move CLOSER** - Hand too small/far
- **🔍 Move FURTHER** - Hand too large/close

### ⌨️ New Keyboard Shortcuts
- **'v'** - Toggle voice control on/off
- **'q'** - Quit
- **'s'** - Show statistics
- **'h'** - Toggle advanced UI
- **'c'** - Toggle CNN mode
- **'b'** - Launch browser

## 🎯 How to Get Best Voice Recognition

### Environment Setup

1. **Quiet Environment**
   - Minimize background noise (TV, music, fans)
   - Close windows to reduce outside noise
   - Use in quiet room for best results

2. **Microphone Position**
   - Speak 6-12 inches from microphone
   - Position mic away from speakers to avoid feedback
   - Use directional mic if available

3. **Optimal Lighting for Camera**
   - Brightness: 60-200 (check meter on UI)
   - Avoid backlighting (window behind you)
   - Even front lighting works best
   - Avoid harsh shadows on hands

### Speaking Tips

1. **Clear Speech**
   - Speak clearly and at normal pace
   - Don't whisper or shout
   - Pronounce words distinctly
   - Pause briefly between commands

2. **Command Format**
   - Use exact command phrases (see list below)
   - Wait for "🎤 Listening..." before speaking
   - Wait for processing to complete
   - Allow 1-2 seconds between commands

3. **If Recognition Fails**
   - Check console for "Speech unclear" message
   - Adjust microphone position
   - Increase speaking volume slightly
   - Reduce background noise
   - Try recalibrating (toggle voice off/on)

## 📋 Supported Voice Commands

### Mouse Actions
- **"click"** - Left click at cursor
- **"double click"** - Double click
- **"right click"** - Right click

### Scrolling
- **"scroll up"** - Scroll page up
- **"scroll down"** - Scroll page down
- **"page up"** - Jump one page up
- **"page down"** - Jump one page down

### Browser Navigation
- **"go back"** - Previous page
- **"go forward"** - Next page
- **"new tab"** - Open new tab
- **"close tab"** - Close current tab
- **"refresh"** or **"refresh page"** - Reload page

### Zoom Controls
- **"zoom in"** - Zoom in
- **"zoom out"** - Zoom out
- **"reset zoom"** - Reset to 100%

### Media Controls
- **"mute"** - Mute/unmute
- **"unmute"** - Unmute
- **"volume up"** - Increase volume
- **"volume down"** - Decrease volume

### Utilities
- **"screenshot"** or **"take screenshot"** - Capture screen
- **"pause gestura"** - Pause gesture recognition
- **"resume gestura"** - Resume gesture recognition
- **"show help"** - Display help

## 🔧 Troubleshooting

### Voice Not Working

**Problem:** Voice indicator shows OFF
- **Solution:** Press 'v' key to enable voice control

**Problem:** "Could not understand audio" in console
- **Solution:** 
  - Speak louder and clearer
  - Move closer to microphone
  - Reduce background noise
  - Check microphone permissions

**Problem:** No audio detected
- **Solution:**
  - Check microphone is connected and working
  - Test mic in Windows Sound Settings
  - Verify microphone permissions for Python
  - Try different microphone

**Problem:** Voice picks up background noise
- **Solution:**
  - Toggle voice off/on to recalibrate (press 'v' twice)
  - Wait during 2-second calibration period
  - Reduce noise sources
  - Adjust energy threshold in config if needed

### Lighting Issues

**Too Dark Warning:**
- Add more light sources
- Turn on room lights
- Use desk lamp pointed at hands
- Open curtains (avoid backlighting)

**Too Bright Warning:**
- Close curtains/blinds
- Move away from direct sunlight
- Reduce light intensity
- Reposition camera angle

**Low Contrast Warning:**
- Add front lighting
- Avoid single-direction lighting
- Use diffused light sources
- Check brightness meter (aim for 60-200)

### Hand Positioning

**Hand Not Detected:**
- Move to center of frame
- Ensure hands are in camera view
- Check lighting (must see hand clearly)
- Wave hands to trigger detection

**Tracking Issues:**
- Follow on-screen positioning hints
- Keep hand 12-18 inches from camera
- Avoid moving too fast
- Ensure full hand visible

**Gestures Not Recognized:**
- Check temporal confidence score (TP section)
- Hold gesture steady for 0.4 seconds
- Improve lighting for better tracking
- Check FPS (should be >20)

## 📊 Understanding UI Elements

### Main Info Box (Top-Left)
```
FPS: 28.5 ⭐ Optimal        <- Performance
Gesture: PEACE_SIGN         <- Current gesture
Buffer: 10/10               <- Stability buffer
🎤 VOICE: ON                <- Voice status
✓ scroll down               <- Last command
```

### Performance Indicators
- **FPS Colors:**
  - Green (27+): ⭐ Optimal
  - Yellow (20-26): ⚠️ Low  
  - Red (<20): ❌ Poor

### Temporal Persistence (Bottom-Right)
```
TP: ON | Conf: 0.85         <- System active, confidence 85%
Stab: 90.0%                 <- Gesture stability score
```

### Brightness Meter (Right Side)
- Vertical bar shows current light level
- Green fill: Optimal (60-200)
- Orange fill: Too dark/bright

## 💡 Pro Tips

1. **Optimal Setup:**
   - Quiet room with even lighting
   - Camera at eye level, 12-18" away
   - Microphone 6-12" from mouth
   - Plain background behind hands

2. **Best Practices:**
   - Start with voice OFF, enable when needed
   - Use gestures for continuous control (scrolling, pointer)
   - Use voice for discrete actions (new tab, refresh)
   - Toggle advanced UI ('h') for full feedback

3. **Performance:**
   - Close unnecessary programs for better FPS
   - Ensure good lighting for faster tracking
   - Use USB headset mic for better voice accuracy
   - Keep hands in center 80% of frame

4. **Multimodal Control:**
   - Combine gestures and voice for efficiency
   - Use gestures for scrolling, voice for navigation
   - Use pointer mode (index finger) + voice commands
   - Press 'v' to disable voice when not needed

## 🎓 Example Workflows

### Web Browsing
1. Use **open palm/closed fist** for scrolling
2. Say **"new tab"** to open tab
3. Use **peace sign** or say **"click"** to select
4. Say **"go back"** to return

### Video Watching  
1. Use **index finger** to position cursor on video
2. Say **"click"** to play/pause
3. Say **"mute"** to toggle sound
4. Use **fist/palm** to scroll timeline

### Reading Articles
1. Say **"zoom in"** for better readability
2. Use **open palm** to scroll down
3. Use **closed fist** to scroll up
4. Say **"refresh"** to update content

## 📈 Adjusting Sensitivity (Advanced)

If voice recognition is too sensitive or not sensitive enough, edit:
`voice_assistant/config.py`

```python
# Lower number = more sensitive (picks up quieter sounds)
# Higher number = less sensitive (only loud sounds)
ENERGY_THRESHOLD = 300  # Default: 300, Range: 300-4000

# Debug mode for detailed feedback
DEBUG_MODE = True  # Set to True to see detection details
```

Then restart the program.

---

## 🆘 Need Help?

If issues persist:
1. Check console output for detailed error messages
2. Verify all dependencies installed: `pip install -r requirements.txt`
3. Test microphone in Windows settings
4. Try different lighting setups
5. Toggle voice off/on to recalibrate

**Enjoy hands-free control with Gestura! 🚀**
