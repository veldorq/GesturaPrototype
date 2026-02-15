# Gestura 3D Website

Premium scroll-triggered canvas animation website for Gestura hand gesture control system.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Generate Placeholder Frames

Since you'll replace these with AI-generated frames later, we've created placeholders:

```bash
npm run generate-frames
```

This creates 120 gradient placeholder frames in `public/frames/`

### 3. Run Development Server

```bash
npm run dev
```

Visit http://localhost:3000

### 4. Build for Production

```bash
npm run build
```

The static site will be in the `out/` folder, ready to deploy to Netlify, Vercel, or any static host.

## 📁 Project Structure

```
gestura-web/
├── src/
│   ├── app/
│   │   ├── globals.css          # Tailwind + custom styles
│   │   ├── layout.tsx            # Root layout with fonts
│   │   └── page.tsx              # Main home page
│   ├── components/
│   │   ├── HeroCanvasAnimation.tsx    # Scroll-triggered canvas animation
│   │   ├── GestureCard.tsx            # Individual gesture feature card
│   │   ├── GestureShowcase.tsx        # Gesture features grid
│   │   ├── FeatureHighlights.tsx      # Feature highlights section
│   │   ├── UseCases.tsx               # Use cases grid
│   │   └── FinalCTA.tsx               # Final call-to-action
│   └── data/
│       └── features.ts            # Gesture data and content
├── public/
│   └── frames/                    # Animation frames (120 WebP images)
├── next.config.mjs                # Next.js config (static export)
├── tailwind.config.ts             # Tailwind with Gestura colors
└── package.json
```

## 🎨 Replacing Placeholder Frames with AI-Generated Frames

### Step 1: Generate Frames with AI

Use the prompts from the guide to generate frames using:
- **Runway ML** (Gen-2 or Gen-3)
- **Pika Labs**
- **Stable Diffusion Video**

**Prompts to use:**
1. **Starting Frame** - Calm state of hand gesture
2. **Ending Frame** - Dramatic action state with gesture
3. **Animation Sequence** - 60-120 transition frames

### Step 2: Extract Frames

Once you have the video:

```bash
# Using FFmpeg (recommended)
ffmpeg -i your-animation.mp4 -vf "fps=30,scale=1920:1080" public/frames/frame_%d.webp
```

### Step 3: Rename Frames

Ensure frames are named: `frame_0.webp`, `frame_1.webp`, ..., `frame_N.webp`

### Step 4: Update Frame Count

In `src/components/HeroCanvasAnimation.tsx`, update:

```typescript
const TOTAL_FRAMES = 120; // Change to your actual frame count
```

### Step 5: Test

```bash
npm run dev
```

Scroll down the page to see your animation play forward/backward!

## 🎯 Key Features

### Hero Canvas Animation
- ✅ Bi-directional scroll (plays forward/reverse)
- ✅ Anti-gravity physics using scroll velocity
- ✅ Smooth spring interpolation (no stutter)
- ✅ Preload with progress bar
- ✅ Responsive canvas scaling
- ✅ Text overlays with fade animations

### Gestura Branding
- Colors: Cyan (#00D9FF), Purple (#7B61FF), Navy (#0A0E27, #151B3D)
- Fonts: Inter (body), Playfair Display (headings)
- Effects: Glassmorphism, glow effects, smooth animations

### Performance
- Static export (no server needed)
- 60fps smooth animations
- Optimized frame loading
- Mobile responsive

## 🛠️ Customization

### Colors

Edit `tailwind.config.ts`:

```typescript
colors: {
  'gestura': {
    'cyan': '#00D9FF',      // Change this
    'purple': '#7B61FF',    // Change this
    // ...
  }
}
```

### Content

Edit `src/data/features.ts` to change:
- Gesture features
- Feature highlights
- Use cases
- Stats

### Scroll Duration

Adjust hero container height in `src/components/HeroCanvasAnimation.tsx`:

```typescript
<div ref={containerRef} className="relative h-[500vh]"> // Increase for slower scroll
```

### Animation Effects

Modify `yOffset` in `HeroCanvasAnimation.tsx` for anti-gravity strength:

```typescript
const yOffset = useTransform(
  scrollVelocity,
  [-1, 0, 1],
  [15, 0, -15] // Increase values for stronger effect
);
```

## 📦 Deployment

### Netlify

1. Push to GitHub
2. Connect repository in Netlify
3. Build command: `npm run build`
4. Publish directory: `out`

### Vercel

```bash
vercel
```

### Manual Static Deploy

```bash
npm run build
# Upload the `out/` folder to any static host
```

## 🔧 Troubleshooting

### Frames not loading?

Check:
1. Frames are in `public/frames/` folder
2. Named correctly: `frame_0.webp`, `frame_1.webp`, etc.
3. `TOTAL_FRAMES` constant matches your frame count

### Animation stuttering?

Try:
1. Reduce frame count (every 2nd frame)
2. Compress images more
3. Adjust spring stiffness/damping values

### Build errors?

```bash
rm -rf node_modules .next
npm install
npm run build
```

## 📚 Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animation**: Framer Motion
- **Fonts**: Google Fonts (Inter, Playfair Display)
- **Deployment**: Static Export

## 🎓 Learning Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [Framer Motion API](https://www.framer.com/motion/)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Canvas API Reference](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API)

## 🤝 Support

Created for Gestura by Souvik © 2026

---

**Ready to launch your premium 3D website? Start with `npm install && npm run dev`!** ✨
