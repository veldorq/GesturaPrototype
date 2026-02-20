# 🎮 Gestura - Installation Guide for Users

## Welcome to Gestura!

Control your computer using **hand gestures** through your webcam. No special hardware required - just a standard webcam and your hands!

---

## ⚡ Quick Installation (3 Steps)

### Step 1: Download Gestura

1. Go to the [Gestura Releases page](https://github.com/veldorq/GesturaPrototype/releases/latest)
2. Download the file for your operating system:
   - **Windows:** `Gestura-Windows-x64.zip`
   - **macOS:** `Gestura-macOS-x64.zip`
   - **Linux:** `Gestura-Linux-x64.zip`

### Step 2: Extract the Files

**Windows:**
1. Right-click the downloaded `.zip` file
2. Select **"Extract All..."**
3. Choose a location (e.g., `C:\Gestura` or your Desktop)
4. Click **"Extract"**

**macOS:**
1. Double-click the `.zip` file
2. macOS will automatically extract it
3. You'll see a `Gestura` folder

**Linux:**
```bash
unzip Gestura-Linux-x64.zip -d ~/Gestura
cd ~/Gestura
chmod +x Gestura
```

### Step 3: Run Gestura

**Windows:**
1. Open the extracted folder
2. Double-click **`Gestura.exe`**
3. If you see a Windows security warning, click **"More info"** → **"Run anyway"**
   - This is normal for new applications. Gestura is safe and open-source.

**macOS:**
1. Open the extracted folder  
2. Double-click **`Gestura`**
3. If macOS blocks it, go to **System Preferences** → **Security & Privacy**
4. Click **"Open Anyway"**

**Linux:**
```bash
./Gestura
```

### Step 4: Grant Camera Permission

When Gestura starts:
1. Your operating system will ask for **camera permission**
2. Click **"Allow"** or **"Yes"**
3. A window will open showing your camera feed

**🎉 You're ready to use Gestura!**

---

## 🎯 Basic Gestures to Get Started

Once Gestura is running, try these gestures:

| Gesture | Action | How to Do It |
|---------|--------|--------------|
| ✋ **Open Palm** | Scroll Down | Hold your hand flat with all fingers extended |
| ✊ **Closed Fist** | Scroll Up | Make a tight fist with all fingers curled |
| ☝️ **Index Finger** | Move Mouse | Point with index finger, others curled |
| ✌️ **Peace Sign** | Click | Hold up index and middle fingers |
| 👍 **Thumbs Up** | Page Up | Thumbs up gesture |
| 👎 **Thumbs Down** | Page Down | Thumbs down gesture |

### Tips for Best Results:

✅ **DO:**
- Use bright, even lighting
- Position camera 1-2 feet from your face
- Make clear, distinct gestures
- Hold gestures for 1-2 seconds
- Use one hand at a time

❌ **DON'T:**
- Use in dark rooms
- Move hand too fast
- Make ambiguous hand shapes
- Use both hands simultaneously

### Control Keys:

- **Q** - Quit Gestura
- **P** - Pause gesture recognition
- **R** - Resume gesture recognition
- **M** - Show performance metrics
- **C** - Start calibration

---

## 🔧 Troubleshooting

### "Camera not found" or "Cannot access camera"

**Solution:**

1. **Check camera is working:**
   - Windows: Open Camera app
   - macOS: Open Photo Booth
   - Linux: Run `cheese` command

2. **Close other apps using camera:**
   - Zoom, Skype, Teams, OBS, etc.

3. **Grant camera permissions:**
   - **Windows:** Settings → Privacy → Camera → Allow desktop apps
   - **macOS:** System Preferences → Security & Privacy → Camera → Check Gestura
   - **Linux:** Check if user is in `video` group: `sudo usermod -a -G video $USER`

4. **Try different camera:**
   - If you have multiple cameras, Gestura uses the default one
   - Configure default camera in your OS settings

### Gestures Not Being Recognized

**Solution:**

1. **Improve lighting** - Make sure your hand is well-lit
2. **Move closer** - Position hand 1-2 feet from camera
3. **Make clearer gestures** - Exaggerate hand positions
4. **Hold longer** - Keep gesture for 1.5-2 seconds
5. **Run calibration** - Press **C** to start calibration process
6. **Check hand visibility** - Ensure entire hand is in camera frame

### Application Won't Start

**Solution:**

**Windows:**
```
1. Right-click Gestura.exe → Properties
2. Check "Unblock" if present
3. Try running as Administrator
```

**macOS:**
```
1. Control-click Gestura → Open
2. Or: sudo spctl --master-disable (disable Gatekeeper temporarily)
```

**Linux:**
```bash
# Install missing libraries
sudo apt-get install python3-opencv libatk-bridge2.0-0 libgtk-3-0
```

### Performance Issues (Low FPS)

**Solution:**

1. **Close unnecessary applications** to free up CPU
2. **Lower camera resolution** in camera settings
3. **Use better lighting** - reduces processing load
4. **Update graphics drivers**
5. **Check system requirements** (see below)

---

## 📋 System Requirements

### Minimum Requirements:

- **OS:** Windows 10/11, macOS 10.15+, Ubuntu 20.04+
- **Processor:** Intel Core i3 (4th gen) or equivalent
- **RAM:** 4 GB
- **Webcam:** 720p @ 30 FPS
- **Storage:** 500 MB free space
- **Internet:** Not required (runs completely offline)

### Recommended:

- **OS:** Windows 11, macOS 12+, Ubuntu 22.04+
- **Processor:** Intel Core i5 (6th gen) or equivalent
- **RAM:** 8 GB
- **Webcam:** 1080p @ 30 FPS
- **Storage:** 1 GB free space

---

## 🔒 Privacy & Security

✅ **100% Local Processing** - All gesture recognition happens on your computer

✅ **No Internet Required** - No data is sent anywhere

✅ **No Account Needed** - No sign-up, login, or personal information required

✅ **Open Source** - Code is publicly available for review

✅ **No Analytics** - We don't collect any usage data

---

## 📚 Advanced Features

### Custom Gestures

Want to create your own gestures?

1. Run Gestura
2. Press **G** to enter Gesture Recording mode
3. Follow on-screen instructions
4. Assign an action to your custom gesture

### Calibration for Better Accuracy

If gestures aren't working well:

1. Press **C** to start calibration
2. Follow the on-screen guide
3. Perform each gesture as instructed
4. Calibration profile is saved automatically

### Gesture Sequences

Combine gestures for complex actions:

- **Fist → Peace Sign** = Copy
- **Peace Sign → Fist** = Paste
- **Thumbs Up → Thumbs Up** = Undo

---

## 🆘 Getting Help

### Documentation

- **Full User Guide:** [USER_GUIDE.md](https://github.com/veldorq/GesturaPrototype/blob/main/USER_GUIDE.md)
- **FAQ:** [Website FAQ](https://gestura.app/#faq)
- **Technical Details:** [TECHNICAL_DETAILS.md](https://github.com/veldorq/GesturaPrototype/blob/main/TECHNICAL_DETAILS.md)

### Support

- **Report a Bug:** [GitHub Issues](https://github.com/veldorq/GesturaPrototype/issues)
- **Feature Requests:** [GitHub Discussions](https://github.com/veldorq/GesturaPrototype/discussions)
- **Community:** Join our community for tips and support

### Quick Reference

```
Common Gestures:
  Open Palm    → Scroll Down
  Fist         → Scroll Up
  Index Point  → Move Mouse
  Peace Sign   → Click
  
Keyboard Controls:
  Q → Quit
  P → Pause
  R → Resume
  C → Calibrate
  M → Metrics
  G → Record Gesture
```

---

## 🎓 Learning Resources

### Video Tutorials

- **Getting Started** (2 min)
- **Advanced Gestures** (5 min)
- **Troubleshooting Common Issues** (3 min)

Visit: [gestura.app/tutorials](https://gestura.app/tutorials)

### Best Practices

1. **Spend 5 minutes practicing** basic gestures
2. **Run calibration** for your hand size
3. **Create custom gestures** for your workflow
4. **Adjust lighting** for optimal recognition

---

## ✨ What's Next?

Now that Gestura is installed:

1. ✅ **Practice basic gestures** (5 minutes)
2. ✅ **Run calibration** (Press C)
3. ✅ **Try custom gestures** (Press G)
4. ✅ **Share your experience** - Tell others about Gestura!

---

## 📄 License

Gestura is free and open-source software licensed under MIT License.

You can:
- ✅ Use it for free (personal or commercial)
- ✅ Modify the code
- ✅ Share it with others
- ✅ Contribute improvements

---

## 🙏 Support the Project

If you find Gestura useful:

- ⭐ **Star us on GitHub**
- 🐛 **Report bugs** to help us improve
- 💡 **Suggest features** you'd like to see
- 🤝 **Contribute code** if you're a developer
- 💬 **Spread the word** on social media

---

**Thank you for using Gestura!** 🎉

Control your world with a wave of your hand. ✋

---

*Last updated: February 2026*  
*Version: 1.0.0*
