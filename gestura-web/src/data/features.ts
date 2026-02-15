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
    id: 'pinch-zoom',
    name: 'Pinch Zoom',
    description: 'Zoom in and out naturally like on a touchscreen. Perfect for presentations, image editing, and detailed work.',
    icon: '🤏',
    action: 'Zoom Control',
    rating: 5.0,
    category: 'Navigation',
    color: 'from-cyan-500 to-blue-500',
  },
  {
    id: 'swipe-navigation',
    name: 'Swipe Navigation',
    description: 'Navigate through slides, tabs, and pages with fluid swipe gestures. Browser control at your fingertips.',
    icon: '👈',
    action: 'Tab Switching',
    rating: 4.9,
    category: 'Navigation',
    color: 'from-purple-500 to-pink-500',
  },
  {
    id: 'scroll-control',
    name: 'Scroll Control',
    description: 'Scroll pages, documents, and feeds with natural hand movements. No mouse wheel needed.',
    icon: '☝️',
    action: 'Smooth Scrolling',
    rating: 4.8,
    category: 'Navigation',
    color: 'from-emerald-500 to-teal-500',
  },
  {
    id: 'mute-toggle',
    name: 'Mute Toggle',
    description: 'Instantly mute/unmute during calls and meetings. Perfect for quick privacy control.',
    icon: '🤫',
    action: 'Audio Control',
    rating: 4.7,
    category: 'Media',
    color: 'from-orange-500 to-red-500',
  },
  {
    id: 'closed-fist',
    name: 'Fist Pause',
    description: 'Close your fist to pause media playback. Intuitive control for videos and music.',
    icon: '✊',
    action: 'Media Pause',
    rating: 4.6,
    category: 'Media',
    color: 'from-violet-500 to-purple-500',
  },
  {
    id: 'thumbs-down',
    name: 'Thumbs Down Close',
    description: 'Close windows and applications with a quick thumbs-down gesture. Fast and satisfying.',
    icon: '👎',
    action: 'Close App',
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
    title: 'Real-Time Recognition',
    description: 'Advanced AI detects gestures in under 30ms with 99% accuracy. Experience instant, lag-free control that feels like magic.',
    position: 'left',
    metric: '<30ms',
    metricLabel: 'latency',
  },
  {
    title: 'Works Everywhere',
    description: 'Compatible with all major applications. Browser, media players, video calls, presentations—Gestura works seamlessly.',
    position: 'right',
    metric: '11+',
    metricLabel: 'gestures',
  },
  {
    title: 'Privacy First',
    description: 'All processing happens locally on your device. No cloud uploads, no data collection. Your gestures stay private.',
    position: 'left',
    metric: '100%',
    metricLabel: 'local',
  },
  {
    title: 'Easy Setup',
    description: 'Get started in under 2 minutes. No special hardware required—just your webcam and Gestura software.',
    position: 'right',
    metric: '2min',
    metricLabel: 'setup',
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
    title: 'Presenters',
    description: 'Control slides without touching keyboard. Maintain eye contact and engage your audience naturally.',
    icon: '🎤',
    gradient: 'from-cyan-500/20 to-blue-500/20',
  },
  {
    title: 'Developers',
    description: 'Navigate code, zoom into docs, and control demos hands-free. Boost productivity during coding sessions.',
    icon: '💻',
    gradient: 'from-purple-500/20 to-pink-500/20',
  },
  {
    title: 'Accessibility',
    description: 'Empowering users with limited mobility. Alternative input method for computer control and independence.',
    icon: '♿',
    gradient: 'from-emerald-500/20 to-teal-500/20',
  },
  {
    title: 'Creative Work',
    description: 'Artists and designers control zoom, brush size, and tools without interrupting creative flow.',
    icon: '🎨',
    gradient: 'from-orange-500/20 to-red-500/20',
  },
];
