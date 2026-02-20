export interface GestureFeature {
  id: string;
  name: string;
  description: string;
  icon: string;
  action: string;
  rating: number;
  category: 'Navigation' | 'Media' | 'System' | 'Productivity';
  color: string;
}

export const gestureFeatures: GestureFeature[] = [
  {
    id: 'gesture-detection',
    name: 'Real-Time Detection',
    description: 'Single-hand detection at approximately 30 FPS with landmark-based recognition. Supports limited-motion usage without background assumptions.',
    icon: '👐',
    action: 'Hand Tracking',
    rating: 5.0,
    category: 'System',
    color: 'from-cyan-500 to-blue-500',
  },
  {
    id: 'stabilization',
    name: 'Smart Stabilization',
    description: 'Multi-stage stabilization with tremor compensation, dwell-based activation, and confidence thresholds to prevent false triggers.',
    icon: '🎯',
    action: 'Gesture Handling',
    rating: 4.9,
    category: 'System',
    color: 'from-purple-500 to-pink-500',
  },
  {
    id: 'scroll-control',
    name: 'Scroll Navigation',
    description: 'Smooth vertical scrolling through documents and pages with natural hand movements. Adjustable sensitivity and speed.',
    icon: '📜',
    action: 'Scroll Up/Down',
    rating: 4.8,
    category: 'Navigation',
    color: 'from-emerald-500 to-teal-500',
  },
  {
    id: 'click-actions',
    name: 'Click Simulation',
    description: 'Left and right click actions triggered by specific gestures. Deliberate activation through dwell-time prevents accidental clicks.',
    icon: '🖱️',
    action: 'Mouse Control',
    rating: 4.7,
    category: 'Navigation',
    color: 'from-orange-500 to-red-500',
  },
  {
    id: 'custom-gestures',
    name: 'Custom Gestures',
    description: 'Record and define personalized gestures through the gesture recording system. Persistent configuration saved to JSON.',
    icon: '✨',
    action: 'Gesture Recording',
    rating: 4.6,
    category: 'Productivity',
    color: 'from-violet-500 to-purple-500',
  },
  {
    id: 'visual-feedback',
    name: 'Visual Overlay',
    description: 'Real-time display of detected gestures, action previews, dwell progress bars, and system status indicators.',
    icon: '👀',
    action: 'User Feedback',
    rating: 4.5,
    category: 'System',
    color: 'from-rose-500 to-pink-500',
  },
];

export interface FeatureHighlight {
  title: string;
  description: string;
  position: 'left' | 'right';
  metric?: string;
  metricLabel?: string;
}

export const featureHighlights: FeatureHighlight[] = [
  {
    title: 'Real-Time Performance',
    description: 'Hand detection and gesture recognition at approximately 30 FPS. Responsive interaction with minimal latency through optimized processing pipeline.',
    position: 'left',
    metric: '~30',
    metricLabel: 'FPS',
  },
  {
    title: 'Tremor Compensation',
    description: 'Multi-frame averaging and stabilization accommodate involuntary movements. Deliberate activation through dwell-time prevents false triggers.',
    position: 'right',
    metric: '1.5s',
    metricLabel: 'dwell time',
  },
  {
    title: 'Local Processing',
    description: 'All hand tracking and gesture recognition happens on your device. No video frames or hand landmarks are transmitted externally.',
    position: 'left',
    metric: '100%',
    metricLabel: 'local',
  },
  {
    title: 'Low Physical Effort',
    description: 'Designed for single-hand operation with limited-motion gestures. Customizable mappings accommodate individual capabilities.',
    position: 'right',
    metric: 'Single',
    metricLabel: 'hand',
  },
];

export interface UseCaseCard {
  title: string;
  description: string;
  icon: string;
  gradient: string;
}

export const useCases: UseCaseCard[] = [
  {
    title: 'Accessibility Support',
    description: 'Provides touchless interaction for users with partial motor impairments. Low-effort, single-hand operation reduces physical strain.',
    icon: '♿',
    gradient: 'from-cyan-500/20 to-blue-500/20',
  },
  {
    title: 'Browser Navigation',
    description: 'Scroll through pages, navigate forward and back, and trigger clicks without mouse or keyboard interaction.',
    icon: '🌐',
    gradient: 'from-purple-500/20 to-pink-500/20',
  },
  {
    title: 'Hands-Free Control',
    description: 'Operate computer functions while hands are occupied, during video calls, or when maintaining distance from input devices.',
    icon: '👋',
    gradient: 'from-emerald-500/20 to-teal-500/20',
  },
  {
    title: 'Custom Workflows',
    description: 'Record personalized gestures and map them to specific actions. Persistent configuration adapts to individual needs.',
    icon: '⚙️',
    gradient: 'from-orange-500/20 to-red-500/20',
  },
];
