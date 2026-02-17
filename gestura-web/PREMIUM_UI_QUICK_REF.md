# Premium UI - Quick Reference

## 🚀 Most Used Classes

```tsx
// CARDS
<div className="glass-card p-8">Glass card</div>
<div className="spotlight-card">Spotlight effect</div>
<div className="gesture-card-premium">Gesture card</div>

// BUTTONS
<button className="btn-premium">Button</button>
<button className="btn-premium btn-accent">CTA Button</button>
<MagneticButton>Magnetic</MagneticButton>

// TYPOGRAPHY
<h1 className="heading-hero">Hero</h1>
<h2 className="heading-section">Section</h2>
<h3 className="heading-subsection">Subsection</h3>
<p className="text-body">Body text</p>
<span className="gradient-text">Gradient</span>

// LAYOUT
<section className="section-premium section-alt">
  <div className="container-premium">
    Content
  </div>
</section>

// STATS
<div className="stat-premium stat-accent">
  <span className="stat-value">30ms</span>
  <span className="stat-label">Latency</span>
</div>

// LINKS
<a className="link-premium">Link with underline</a>

// BADGES
<span className="tech-badge-premium">React</span>

// FEATURES
<div className="feature-item-premium">
  <div className="feature-icon-premium">🚀</div>
  <h4>Feature</h4>
</div>

// DEPTH
<div className="depth-1">Subtle</div>
<div className="depth-2">Medium</div>
<div className="depth-3">Strong</div>

// EFFECTS
<div className="img-zoom"><img /></div>
<div className="skeleton h-8 w-full"></div>
<div className="divider-premium" />
```

## 📦 Components

```tsx
import { 
  SpotlightCard, 
  MagneticButton 
} from '@/components/premium';

// Use them
<SpotlightCard>Content</SpotlightCard>
<MagneticButton onClick={fn}>Click</MagneticButton>
```

## 🎨 CSS Variables

```css
var(--bg-primary)        /* #0a0f1a */
var(--text-primary)      /* #f9fafb */
var(--accent)            /* #22d3ee */
var(--border-subtle)     /* rgba(255,255,255,0.06) */
var(--space-lg)          /* 2.5rem */
var(--transition-base)   /* 250ms */
```

## 🎯 Priority Features

✅ Custom Cursor (auto)  
✅ Reading Progress (auto)  
✅ Ambient Lights (auto)  
✅ Noise Overlay (auto)  
✅ Spotlight Cards (import)  
✅ Magnetic Buttons (import)  

## 📱 Mobile Notes

- Custom cursor: Desktop only
- Reduced motion: Auto-respected
- Touch: Spotlight cards supported

## 🔗 Full Docs

See `PREMIUM_UI_GUIDE.md` for complete documentation.
