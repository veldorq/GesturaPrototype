# 🚀 Release Checklist for Gestura Maintainers

This document provides step-by-step instructions for creating and publishing a new Gestura release.

---

## Pre-Release Checklist

### 1. Code Preparation

- [ ] All features for this release are merged to `main` branch
- [ ] All tests pass locally
- [ ] No merge conflicts or pending PRs
- [ ] Code review completed
- [ ] CHANGELOG.md updated with release notes

### 2. Version Update

Update version numbers in:

- [ ] `README.md` - Version badge
- [ ] `config/constants.py` - VERSION constant
- [ ] `END_USER_INSTALL_GUIDE.md` - Version footer
- [ ] `package.json` (if applicable)

Example:
```python
# In config/constants.py
VERSION = "1.1.0"
RELEASE_DATE = "2026-02-20"
```

### 3. Documentation Review

- [ ] README.md is up-to-date
- [ ] END_USER_INSTALL_GUIDE.md reflects current installation process
- [ ] USER_GUIDE.md includes all new features
- [ ] TECHNICAL_DETAILS.md is accurate
- [ ] All screenshots are current
- [ ] Links are not broken

### 4. Testing

Run complete test suite:

```bash
# Unit tests
pytest tests/

# Integration tests
python test_gesture_detection.py
python test_pointer.py
python test_closed_fist.py

# Full application test
python main.py
# Test all gestures manually
# Verify performance metrics (press M)
```

Test on all platforms:
- [ ] Windows 10
- [ ] Windows 11
- [ ] macOS 12+
- [ ] Ubuntu 22.04

### 5. Build Verification

Test local build before triggering CI:

**Windows:**
```bash
.\BUILD_EXE.bat
# Verify dist\Gestura.exe exists and runs
# Test on fresh Windows VM if possible
```

**macOS/Linux:**
```bash
chmod +x build.sh
./build.sh
# Verify dist/Gestura exists and runs
```

---

## Release Process

### Step 1: Create Release Branch

```bash
# Create and checkout release branch
git checkout -b release/v1.1.0

# Push to remote
git push origin release/v1.1.0
```

### Step 2: Create Release Tag

```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release version 1.1.0"

# Push tag to trigger GitHub Actions
git push origin v1.1.0
```

**Tag Naming Convention:**
- Major release: `v1.0.0`
- Minor release: `v1.1.0`
- Patch release: `v1.1.1`
- Pre-release: `v1.1.0-beta.1`

### Step 3: Monitor GitHub Actions Build

1. Go to: `https://github.com/YOUR_USERNAME/GesturaPrototype/actions`
2. Find the "Build and Release Gestura" workflow
3. Monitor all three build jobs:
   - `build-windows`
   - `build-macos`
   - `build-linux`
4. Ensure all jobs complete successfully (green checkmarks)

**If build fails:**
- Check error logs
- Fix issues locally
- Delete failed tag: `git tag -d v1.1.0 && git push origin :refs/tags/v1.1.0`
- Re-create tag after fixes

### Step 4: Verify Release Artifacts

Once workflow completes:

1. Go to: `https://github.com/YOUR_USERNAME/GesturaPrototype/releases`
2. Find the newly created release
3. Verify presence of all files:
   - [ ] `Gestura-Windows-x64.zip`
   - [ ] `Gestura-macOS-x64.zip`
   - [ ] `Gestura-Linux-x64.zip`

### Step 5: Test Release Downloads

**Critical: Test download and installation as end user**

**Windows Test:**
```
1. Download Gestura-Windows-x64.zip
2. Extract to desktop
3. Run Gestura.exe
4. Test camera permission flow
5. Test 5-7 gestures
6. Verify no errors in console
```

**macOS Test:**
```
1. Download Gestura-macOS-x64.zip
2. Extract
3. Run Gestura (test Gatekeeper prompt)
4. Test camera permission
5. Verify all gestures work
```

**Linux Test:**
```bash
wget https://github.com/USER/GesturaPrototype/releases/download/v1.1.0/Gestura-Linux-x64.zip
unzip Gestura-Linux-x64.zip
cd Gestura
./Gestura
# Test gestures
```

### Step 6: Update Release Notes

Edit the GitHub release:

1. Go to release page
2. Click "Edit release"
3. Enhance auto-generated notes with:

```markdown
## 🎉 What's New in v1.1.0

### New Features
- ✨ Adaptive thresholding for improved accuracy
- ✨ User calibration system for personalized recognition
- ✨ Performance metrics display (press M)

### Improvements
- ⚡ 15% faster frame processing
- 🎯 20% better gesture recognition accuracy
- 🐛 Fixed false positive detection in low light

### Breaking Changes
- ⚠️ Configuration file format updated (auto-migrated)

### Known Issues
- 🔍 Occasional lag on Intel HD graphics
- 🔍 Calibration wizard not localized

### Installation
[Standard installation instructions...]

### Upgrading from v1.0.0
[Upgrade instructions if needed...]
```

### Step 7: Update Website

If you have a website:

- [ ] Update "Latest Version" badge
- [ ] Update download links
- [ ] Publish blog post about release
- [ ] Update documentation pages
- [ ] Clear CDN cache

**Update Download Links:**

In `gestura-web/src/components/MinimalCTA.tsx` and similar:
```tsx
<a href="https://github.com/USER/GesturaPrototype/releases/download/v1.1.0/Gestura-Windows-x64.zip">
  Download for Windows
</a>
```

### Step 8: Announce Release

Post announcements:

- [ ] **GitHub Discussions** - Create announcement thread
- [ ] **Reddit** - r/opensource, r/linux, r/accessibility
- [ ] **Hacker News** - If major release
- [ ] **Twitter/X** - With demo video
- [ ] **LinkedIn** - Professional audience
- [ ] **Product Hunt** - For major releases
- [ ] **Dev.to** - Write detailed release article

**Announcement Template:**

```
🎉 Gestura v1.1.0 is out!

Control your computer with hand gestures through your webcam. 

🆕 What's new:
- Adaptive thresholding
- User calibration
- Performance improvements

⬇️ Download: [link]
📚 Docs: [link]
⭐ Star us on GitHub!

#opensource #accessibility #python #computervision
```

### Step 9: Monitor Initial Feedback

In the first 48 hours:

- [ ] Monitor GitHub Issues for bug reports
- [ ] Check Discussions for questions
- [ ] Respond to social media comments
- [ ] Watch for download analytics

Create hotfix if critical bugs found:
```bash
git checkout -b hotfix/v1.1.1
# Fix critical bug
git tag v1.1.1
git push origin v1.1.1
```

---

## Post-Release Tasks

### Update Main Branch

```bash
# Merge release branch back to main
git checkout main
git merge release/v1.1.0
git push origin main
```

### Update Project Board

- [ ] Move completed issues to "Released"
- [ ] Archive release milestone
- [ ] Create next milestone (v1.2.0)

### Performance Tracking

Monitor:
- Download counts (GitHub Insights)
- GitHub stars/forks growth
- Issue types (bugs vs features)
- Community engagement

### Documentation

- [ ] Update CHANGELOG.md with final stats
- [ ] Archive release notes
- [ ] Update roadmap with completed items

---

## Emergency Procedures

### Critical Bug Found After Release

1. **Assess Severity:**
   - Critical: Crashes, data loss, security issues → Hotfix immediately
   - High: Major feature broken → Hotfix within 24h
   - Medium: Minor issues → Include in next release

2. **Hotfix Process:**
```bash
# Create hotfix branch from tag
git checkout -b hotfix/v1.1.1 v1.1.0

# Fix bug
# ... make changes ...

# Test thoroughly
pytest tests/
python main.py

# Commit and tag
git commit -am "Hotfix: Critical bug in gesture recognition"
git tag v1.1.1
git push origin hotfix/v1.1.1
git push origin v1.1.1
```

3. **Communicate:**
   - Update GitHub release with warning
   - Post issue explaining problem
   - Notify users via all channels

### Rolling Back a Release

If release is fundamentally broken:

1. **Mark as Pre-release:**
   - Edit GitHub release
   - Check "This is a pre-release"
   - Add warning banner

2. **Delete Tag (if severe):**
```bash
git tag -d v1.1.0
git push origin :refs/tags/v1.1.0
```

3. **Promote Previous Release:**
   - Mark v1.0.0 as "Latest"
   - Update download links

---

## Automation Improvements

### CI/CD Enhancements

**Add automatic tests before release:**

```yaml
# In .github/workflows/build-release.yml

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: |
          pip install pytest
          pytest tests/
```

**Add code signing:**

```yaml
# Windows code signing
- name: Sign Windows executable
  uses: dlemstra/code-sign-action@v1
  with:
    certificate: ${{ secrets.WINDOWS_CERT }}
    password: ${{ secrets.CERT_PASSWORD }}
    folder: dist
```

**Add release notes automation:**

```yaml
- name: Generate release notes
  uses: release-drafter/release-drafter@v5
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

---

## Quality Gates

Before releasing, all must be ✅:

### Code Quality
- [ ] Linting passes (flake8, pylint)
- [ ] Type checking passes (mypy)
- [ ] Test coverage > 70%
- [ ] No critical security vulnerabilities

### Performance
- [ ] Frame rate > 25 FPS on minimum hardware
- [ ] CPU usage < 30% average
- [ ] Memory usage < 500 MB
- [ ] Startup time < 5 seconds

### User Experience
- [ ] Clear error messages
- [ ] Proper permission dialogs
- [ ] Intuitive UI
- [ ] Responsive controls

### Documentation
- [ ] Installation guide tested
- [ ] Troubleshooting section comprehensive
- [ ] All features documented
- [ ] Code examples work

---

## Release Checklist Summary

**Pre-Release:**
- [ ] Code complete and tested
- [ ] Version numbers updated
- [ ] Documentation current
- [ ] Local build verified

**Release:**
- [ ] Tag created and pushed
- [ ] CI builds successful
- [ ] Artifacts verified
- [ ] Release notes enhanced

**Post-Release:**
- [ ] Website updated
- [ ] Announcements posted
- [ ] Feedback monitored
- [ ] Next milestone planned

---

## Contact

Questions about release process?
- Open an issue with label `release-question`
- Contact maintainers directly

---

*This checklist is maintained by the Gestura development team.*  
*Last updated: February 2026*
