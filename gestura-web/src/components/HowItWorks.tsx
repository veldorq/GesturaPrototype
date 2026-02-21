'use client';

import { motion } from 'framer-motion';

const steps = [
  {
    number: '01',
    title: 'Hand Landmark Detection',
    subtitle: 'MediaPipe Computer Vision',
    description: 'MediaPipe detects 21 three-dimensional hand landmarks in real-time. The system processes one hand at a time at approximately 30 frames per second, extracting wrist, finger joints, and fingertip positions.',
    tech: ['MediaPipe Hands', 'Landmark Tracking', '30 FPS'],
  },
  {
    number: '02',
    title: 'Feature Extraction',
    subtitle: 'Geometric Analysis',
    description: 'Landmarks are normalized by palm dimensions to handle varying distances from camera. Geometric features including finger extension states, fingertip spacing, and thumb orientation are extracted from normalized positions.',
    tech: ['Normalization', 'Geometric Features', 'Distance Invariant'],
  },
  {
    number: '03',
    title: 'Gesture Recognition',
    subtitle: 'Pattern Matching',
    description: 'Extracted features are compared against the gesture library using normalized Euclidean distance. Matches accumulate in a temporal buffer for consistency validation across multiple frames.',
    tech: ['Pattern Matching', 'Temporal Filtering', 'Confidence Scoring'],
  },
  {
    number: '04',
    title: 'Stabilization & Action',
    subtitle: 'Deliberate Activation',
    description: 'Multi-stage stabilization through confidence thresholds, temporal consistency, and dwell-time monitoring ensures deliberate activation. Actions trigger after successful dwell completion and debounce validation.',
    tech: ['Dwell-Time', 'Tremor Compensation', 'Debounce Logic'],
  },
];

const gestures = [
  {
    icon: '🖐️',
    name: 'Open Palm',
    action: 'Pause State',
    description: 'Show open palm to enter pause state. No actions will trigger while in this neutral position.',
  },
  {
    icon: '✊',
    name: 'Closed Fist',
    action: 'Left Click',
    description: 'Make a closed fist and maintain dwell time to trigger left mouse click action.',
  },
  {
    icon: '✌️',
    name: 'Peace Sign',
    action: 'Right Click',
    description: 'Show peace sign gesture to trigger right mouse click after dwell completion.',
  },
  {
    icon: '👍',
    name: 'Thumbs Up',
    action: 'Scroll Up',
    description: 'Point thumb up to scroll upward through pages and documents smoothly.',
  },
  {
    icon: '👎',
    name: 'Thumbs Down',
    action: 'Scroll Down',
    description: 'Point thumb down to scroll downward through content with controlled speed.',
  },
  {
    icon: '👉',
    name: 'Browser Back',
    action: 'Navigate Back',
    description: 'Use designated gesture to navigate backward in browser history.',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-16 sm:py-24 md:py-32 px-4 sm:px-6 overflow-x-hidden bg-[#0f1419] scroll-mt-20">
      {/* Grid overlay */}
      <div
        className="absolute inset-0 opacity-10 pointer-events-none"
        style={{
          backgroundImage: `
            linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)
          `,
          backgroundSize: '50px 50px',
        }}
      />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-20 px-4"
        >
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
          >
            <span className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
            <span className="text-gestura-cyan text-sm font-semibold uppercase tracking-wider">
              🔬 Technical Process
            </span>
          </motion.div>

          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-light leading-tight mb-4 sm:mb-6">
            How <span className="gradient-text">Gestura</span> Works
          </h2>
          <p className="text-sm sm:text-base md:text-lg text-neutral-400 max-w-3xl mx-auto font-light">
            From hand detection to action execution through multi-stage recognition and stabilization
          </p>
        </motion.div>

        {/* Process Steps */}
        <div className="grid md:grid-cols-2 gap-x-8 gap-y-16 mb-32">
          {steps.map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 60 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              className="relative"
            >
              {/* Connection Line */}
              {index < steps.length - 1 && index % 2 === 0 && (
                <div className="hidden md:block absolute top-20 left-full w-8 h-px bg-gradient-to-r from-gestura-cyan/50 to-transparent" />
              )}

              <div className="glass-panel p-8 rounded-lg group hover:border-gestura-cyan/50 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-gestura-cyan/20">
                {/* Number */}
                <motion.div 
                  className="text-gestura-cyan text-sm font-mono mb-4"
                  whileHover={{ scale: 1.2, rotate: 5 }}
                >
                  {step.number}
                </motion.div>

                {/* Title & Subtitle */}
                <h3 className="text-2xl font-light mb-2 group-hover:text-gestura-cyan transition-colors">
                  {step.title}
                </h3>
                <p className="text-sm text-gestura-purple font-medium mb-4">{step.subtitle}</p>

                {/* Description */}
                <p className="text-neutral-400 text-sm leading-relaxed mb-6">
                  {step.description}
                </p>

                {/* Tech Stack */}
                <div className="flex flex-wrap gap-2">
                  {step.tech.map((tech, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 text-xs bg-white/5 border border-white/10 rounded-full text-neutral-300"
                    >
                      {tech}
                    </span>
                  ))}
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Divider */}
        <motion.div
          initial={{ scaleX: 0 }}
          whileInView={{ scaleX: 1 }}
          viewport={{ once: true }}
          className="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent mb-32"
        />

        {/* Gesture Reference */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mb-12 sm:mb-16"
        >
          <h3 className="text-xl sm:text-2xl md:text-3xl font-light text-center mb-3 sm:mb-4 break-words">
            Gesture <span className="gradient-text">Reference</span>
          </h3>
          <p className="text-center text-neutral-400 text-xs sm:text-sm mb-8 sm:mb-12 px-4">
            Master these gestures to control your computer naturally
          </p>
        </motion.div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {gestures.map((gesture, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="glass-panel p-4 sm:p-6 rounded-lg group cursor-pointer"
            >
              {/* Icon */}
              <div className="text-4xl sm:text-5xl mb-3 sm:mb-4 group-hover:scale-110 transition-transform">
                {gesture.icon}
              </div>

              {/* Name & Action */}
              <h4 className="text-base sm:text-lg font-medium mb-1 group-hover:text-gestura-cyan transition-colors">
                {gesture.name}
              </h4>
              <p className="text-[10px] sm:text-xs text-gestura-purple uppercase tracking-wider mb-2 sm:mb-3">
                {gesture.action}
              </p>

              {/* Description */}
              <p className="text-xs sm:text-sm text-neutral-400 leading-relaxed">
                {gesture.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Technical Specs */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-24 glass-panel p-8 rounded-lg"
        >
          <h3 className="text-xl font-light mb-8 text-center">Technical Specifications</h3>
          
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-light gradient-text mb-2">~30</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">FPS Target</div>
              <p className="text-xs text-neutral-600 mt-2">Real-time frame processing</p>
            </div>
            <div>
              <div className="text-3xl font-light gradient-text mb-2">1.5s</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Dwell Time</div>
              <p className="text-xs text-neutral-600 mt-2">Deliberate activation period</p>
            </div>
            <div>
              <div className="text-3xl font-light gradient-text mb-2">21</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Landmarks</div>
              <p className="text-xs text-neutral-600 mt-2">Hand points tracked per frame</p>
            </div>
            <div>
              <div className="text-3xl font-light gradient-text mb-2">100%</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Local</div>
              <p className="text-xs text-neutral-600 mt-2">No cloud, all on-device</p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
