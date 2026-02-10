# 🎯 Gestura Demo Quick Reference

## 🚀 Essential Commands

```bash
# Start Gestura
python PROTOTYPE.PY

# Stop Gestura
Press 'q' on keyboard
```

---

## ✋ 8 Core Gestures (Demo-Ready)

| Gesture | Finger Position | Action | Hold Time |
|---------|----------------|--------|-----------|
| ✋ **Open Palm** | All 5 fingers spread | Scroll Down | 0.4s |
| ✊ **Closed Fist** | All fingers folded | Scroll Up | 0.4s |
| 👆 **Index Only** | Only index extended | Pointer Mode | Continuous |
| ✌️ **Peace Sign** | Index + middle | Left Click | 0.4s |
| 👋 **Swipe Left** | Hand moves left | Browser Back | 0.5s |
| 👋 **Swipe Right** | Hand moves right | Browser Forward | 0.5s |
| 👍 **Thumb Up** | Thumb up | Zoom In | 0.4s |
| 🤙 **Pinky Extended** | Only pinky up | Mute Toggle | 0.4s |

---

## 🎬 60-Second Demo Script

**Opening (10s):**
> "Gestura gives people with limited mobility touchless computer control using just a webcam. Watch this..."

**Gestures (40s):**
1. **Open palm** → Scroll down  
   *"Five fingers spread scrolls naturally"*

2. **Closed fist** → Scroll up  
   *"Fist scrolls back up"*

3. **Peace sign** → Click  
   *"Two fingers clicks—see the instant feedback"*

4. **Swipe right** → Navigate  
   *"Natural swipe for browser navigation"*

5. **Thumb up** → Zoom  
   *"Simple gestures for essential actions"*

**Closing (10s):**
> "Eight gestures. Zero calibration. Works offline. Built for accessibility—simple, reliable, empowering."

---

## ⚙️ Key Settings (Already Configured)

- ✅ **5-frame confirmation** (167ms) — eliminates flicker
- ✅ **0.4-0.5s dwell times** — calm, intentional gestures
- ✅ **Movement-first priority** — prevents gesture conflicts
- ✅ **8 essential gestures only** — no experimental features
- ✅ **Exception handling** — zero mid-demo crashes

---

## 🚨 Troubleshooting

### Gesture Not Detected?
- **Hold gesture 0.5 seconds** (don't make quick movements)
- **Spread fingers clearly** (exaggerate for camera)
- **Check lighting** (need good contrast)
- **Distance: 1-2 feet** from camera

### Accidental Triggers?
- **Gesture detected but action didn't execute:**  
  This is normal! Dwell time (0.4-0.5s) must be met.
- **Console shows "NONE":**  
  Hand position doesn't match any of the 8 gestures exactly.

### Console Showing Multiple Gestures?
- **This means gesture overlap (bug!)**  
  Should never happen with current fixes.
  Report immediately if seen.

---

## 📊 What Judges Care About

### Technical Excellence
- ✅ Real-time hand tracking (30 FPS)
- ✅ MediaPipe integration (computer vision)
- ✅ State machine pattern (NONE → CANDIDATE → CONFIRMED → COOLDOWN)
- ✅ Temporal stabilization (multi-frame confirmation)

### User Experience
- ✅ Instant visual feedback (hand skeleton overlay)
- ✅ Calm, accessible interaction (0.4-0.5s timing)
- ✅ One gesture = one action (no ambiguity)
- ✅ Works offline (no cloud, no API keys)

### Accessibility Impact
- ✅ Built for partial motor control
- ✅ No calibration required
- ✅ Natural gestures (not arbitrary poses)
- ✅ Empowers independence

---

## ✨ Demo Tips

### Do:
- ✅ Make gestures deliberately (exaggerate slightly)
- ✅ Hold each gesture 0.5-1 second
- ✅ Narrate while gesturing (helps judges follow)
- ✅ Position camera facing you, 1-2 feet away
- ✅ Test 5 minutes before your slot

### Don't:
- ❌ Rush gestures (system needs 0.4s dwell time)
- ❌ Make gestures while talking with hands
- ❌ Move hand too fast (swipes need clear direction)
- ❌ Show all 8 gestures (pick 4-5 most impressive)
- ❌ Apologize if gesture fails (calmly retry)

---

## 🎯 Success Checklist

**Before Demo:**
- [ ] Tested on presentation laptop (not just dev machine)
- [ ] Camera working in venue lighting
- [ ] Browser open to demo page
- [ ] Practiced 60s script 3x with timer
- [ ] Backup video ready (if camera fails)

**During Demo:**
- [ ] Speak while gesturing (narrate actions)
- [ ] Make deliberate gestures (0.5s holds)
- [ ] Keep hand in frame (easy to drift out)
- [ ] Watch console for "DETECTED" messages
- [ ] If gesture fails → Calmly retry

**After Demo:**
- [ ] Ready to explain: "How does detection work?" (MediaPipe landmarks)
- [ ] Ready to explain: "Why these 8 gestures?" (Mutual exclusivity)
- [ ] Ready to show code if asked (clean Python structure)

---

## 💡 Judge Questions & Answers

**Q: "How does it detect gestures?"**  
A: "MediaPipe tracks 21 hand landmarks in 3D space. We analyze finger angles and positions to recognize gestures, then use a state machine with multi-frame confirmation to prevent false triggers."

**Q: "Why only 8 gestures?"**  
A: "We prioritize reliability over quantity. Each gesture is mutually exclusive—no overlapping detection. This ensures one gesture = one action, critical for accessibility."

**Q: "What about people with hand tremors?"**  
A: "We use 5-frame confirmation (167ms buffer) and 0.4s dwell times to filter hand tremor. The system is designed for partial motor control specifically."

**Q: "Could this scale beyond demos?"**  
A: "Absolutely. It runs entirely locally (no server needed), works on any laptop with a webcam, and MediaPipe is production-ready. The bottleneck is webcam FPS, not our code."

**Q: "What's the biggest technical challenge?"**  
A: "Preventing gesture conflicts during movement. We solved this by checking swipes BEFORE static poses and using strict mutual exclusivity—movement detection blocks finger counting."

---

## 🏆 Winning Points

1. **Accessibility First** — Built for users with limited mobility
2. **Zero Setup** — No calibration, training, or configuration needed
3. **Offline & Private** — Everything runs locally, no cloud APIs
4. **Reliable Demo** — 5-frame confirmation prevents glitches
5. **Production-Ready** — Clean code, exception handling, proper architecture

---

**Last Updated:** February 9, 2026  
**System Status:** ✅ Stable (8 gestures, conflict-free)  
**Demo Readiness:** ✅ Ready (60s script validated)
