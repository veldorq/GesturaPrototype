/**
 * PREMIUM UI COMPONENTS - USAGE GUIDE
 * ===================================
 * 
 * This file contains examples of how to use the premium UI components
 * in your Gestura website.
 */

// ============================================
// 1. SPOTLIGHT CARD
// ============================================
import SpotlightCard from '@/components/premium/SpotlightCard';

function FeatureCardExample() {
  return (
    <SpotlightCard className="p-8">
      <h3 className="text-xl font-semibold mb-4">Amazing Feature</h3>
      <p className="text-gray-400">
        This card has a beautiful spotlight effect that follows your mouse.
      </p>
    </SpotlightCard>
  );
}

// ============================================
// 2. MAGNETIC BUTTON
// ============================================
import MagneticButton from '@/components/premium/MagneticButton';

function CTAExample() {
  return (
    <MagneticButton 
      onClick={() => console.log('Downloaded!')}
      className="text-white"
    >
      Download Now
    </MagneticButton>
  );
}

// ============================================
// 3. PREMIUM CSS CLASSES
// ============================================

// Glass Card with hover effect
function GlassCardExample() {
  return (
    <div className="glass-card p-6">
      <h3>Glass Effect Card</h3>
      <p>Beautiful glassmorphism design</p>
    </div>
  );
}

// Premium Button
function PremiumButtonExample() {
  return (
    <button className="btn-premium btn-accent">
      Get Started
    </button>
  );
}

// Premium Stat Display
function StatExample() {
  return (
    <div className="stat-premium stat-accent">
      <span className="stat-value">&lt;30ms</span>
      <span className="stat-label">Latency</span>
    </div>
  );
}

// Process Steps with connector
function ProcessStepExample() {
  return (
    <div>
      <div className="process-step-premium" data-step="1">
        <h4 className="heading-subsection">Step One</h4>
        <p className="text-body">Description of first step</p>
      </div>
      <div className="process-step-premium" data-step="2">
        <h4 className="heading-subsection">Step Two</h4>
        <p className="text-body">Description of second step</p>
      </div>
    </div>
  );
}

// Tech Badge
function TechBadgeExample() {
  return (
    <div className="flex gap-2 flex-wrap">
      <span className="tech-badge-premium">React</span>
      <span className="tech-badge-premium">TypeScript</span>
      <span className="tech-badge-premium">Next.js</span>
    </div>
  );
}

// Feature Item with icon
function FeatureItemExample() {
  return (
    <div className="feature-item-premium">
      <div className="feature-icon-premium">
        🚀
      </div>
      <h4 className="heading-subsection">Fast Performance</h4>
      <p className="text-body">Optimized for speed</p>
    </div>
  );
}

// Premium Link with underline animation
function LinkExample() {
  return (
    <a href="#" className="link-premium">
      Learn More
    </a>
  );
}

// Image with zoom effect
function ImageZoomExample() {
  return (
    <div className="img-zoom">
      <img src="/demo.jpg" alt="Demo" />
    </div>
  );
}

// Floating label input
function InputExample() {
  return (
    <div className="input-group">
      <input 
        type="text" 
        className="input-premium" 
        placeholder=" "
        id="email"
      />
      <label htmlFor="email" className="input-label">
        Email Address
      </label>
    </div>
  );
}

// Skeleton loader
function SkeletonExample() {
  return (
    <div className="space-y-4">
      <div className="skeleton h-8 w-3/4"></div>
      <div className="skeleton h-4 w-full"></div>
      <div className="skeleton h-4 w-5/6"></div>
    </div>
  );
}

// Empty state
function EmptyStateExample() {
  return (
    <div className="empty-state-premium">
      <div className="empty-icon">
        📭
      </div>
      <h3 className="empty-title">No Items Found</h3>
      <p className="empty-desc">
        There are no items to display at the moment. Check back later!
      </p>
      <button className="btn-premium btn-accent mt-4">
        Add New Item
      </button>
    </div>
  );
}

// ============================================
// 4. TYPOGRAPHY CLASSES
// ============================================
function TypographyExample() {
  return (
    <div className="space-y-6">
      <h1 className="heading-hero">
        Hero Heading
      </h1>
      <h2 className="heading-section">
        Section Heading
      </h2>
      <h3 className="heading-subsection">
        Subsection Heading
      </h3>
      <p className="text-body">
        Body text with proper line height and color
      </p>
      <p className="text-small">
        Small text for captions and metadata
      </p>
      <span className="gradient-text">
        Gradient Text Effect
      </span>
    </div>
  );
}

// ============================================
// 5. SECTION LAYOUT
// ============================================
function SectionExample() {
  return (
    <section className="section-premium section-alt">
      <div className="container-premium">
        <h2 className="heading-section mb-8">Section Title</h2>
        {/* Your content here */}
      </div>
    </section>
  );
}

// ============================================
// 6. DEPTH LAYERS
// ============================================
function DepthExample() {
  return (
    <div className="space-y-4">
      <div className="depth-1 p-4 bg-white/5 rounded-lg">
        Subtle depth
      </div>
      <div className="depth-2 p-4 bg-white/5 rounded-lg">
        Medium depth
      </div>
      <div className="depth-3 p-4 bg-white/5 rounded-lg">
        Strong depth
      </div>
    </div>
  );
}

// ============================================
// 7. HORIZONTAL SCROLL GALLERY
// ============================================
function HorizontalScrollExample() {
  return (
    <div className="horizontal-scroll">
      <div className="w-80 h-64 bg-white/5 rounded-lg flex-shrink-0" />
      <div className="w-80 h-64 bg-white/5 rounded-lg flex-shrink-0" />
      <div className="w-80 h-64 bg-white/5 rounded-lg flex-shrink-0" />
    </div>
  );
}

// ============================================
// 8. DIVIDER
// ============================================
function DividerExample() {
  return (
    <div>
      <p>Content above</p>
      <div className="divider-premium" />
      <p>Content below</p>
    </div>
  );
}

export {
  FeatureCardExample,
  CTAExample,
  GlassCardExample,
  PremiumButtonExample,
  StatExample,
  ProcessStepExample,
  TechBadgeExample,
  FeatureItemExample,
  LinkExample,
  ImageZoomExample,
  InputExample,
  SkeletonExample,
  EmptyStateExample,
  TypographyExample,
  SectionExample,
  DepthExample,
  HorizontalScrollExample,
  DividerExample,
};
