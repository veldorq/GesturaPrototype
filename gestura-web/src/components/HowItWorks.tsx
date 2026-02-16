'use client';

import { motion } from 'framer-motion';

const steps = [
  {
    number: '01',
    title: 'Hand Detection',
    subtitle: 'AI-Powered Recognition',
    description: 'Advanced computer vision algorithms detect your hand in real-time using your webcam. MediaPipe technology identifies 21 key landmarks on each hand with sub-millimeter precision.',
    tech: ['MediaPipe', 'TensorFlow Lite', 'WebAssembly'],
  },
  {
    number: '02',
    title: 'Gesture Classification',
    subtitle: 'Neural Network Processing',
    description: 'Custom-trained convolutional neural network analyzes hand landmarks and classifies gestures instantly. Recognizes 11+ distinct gestures with 99% accuracy.',
    tech: ['CNN Model', 'Real-time Inference', 'Edge Computing'],
  },
  {
    number: '03',
    title: 'Motion Mapping',
    subtitle: 'Gesture to Action',
    description: 'Each recognized gesture triggers specific system actions. Smooth interpolation ensures natural, responsive control without lag or jitter.',
    tech: ['Action Mapping', 'Smoothing Pipeline', 'Event Handling'],
  },
  {
    number: '04',
    title: 'System Control',
    subtitle: 'Direct Integration',
    description: 'Gestures become system commands - zoom, scroll, navigate, pause. All processing happens locally on your device. Zero latency, complete privacy.',
    tech: ['Native APIs', 'Local Processing', 'Zero Cloud'],
  },
];

const gestures = [
  {
    icon: '🤏',
    name: 'Pinch Zoom',
    action: 'Zoom in/out',
    description: 'Pinch fingers together to zoom into content, spread apart to zoom out',
  },
  {
    icon: '👆',
    name: 'Swipe',
    action: 'Navigate tabs',
    description: 'Point with index finger and move left/right to switch between tabs',
  },
  {
    icon: '✋',
    name: 'Open Palm',
    action: 'Scroll pages',
    description: 'Show open palm and move up/down to scroll through content smoothly',
  },
  {
    icon: '✊',
    name: 'Fist',
    action: 'Pause media',
    description: 'Make a fist to pause/play videos and audio instantly',
  },
  {
    icon: '🤙',
    name: 'Call Sign',
    action: 'Toggle mute',
    description: 'Shaka hand sign to mute/unmute audio with a single gesture',
  },
  {
    icon: '👎',
    name: 'Thumbs Down',
    action: 'Close window',
    description: 'Point thumb down to close the active window or application',
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="relative py-32 px-6 overflow-x-hidden bg-[#0a0a0a] scroll-mt-20">
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
            <span className="text-gestura-cyan text-xs font-semibold uppercase tracking-widest">
              The Technology
            </span>
          </motion.div>

          <h2 className="text-3xl md:text-5xl font-light leading-tight mb-6">
            How <span className="gradient-text">Gestura</span> Works
          </h2>
          <p className="text-base md:text-lg text-neutral-400 max-w-3xl mx-auto font-light">
            From hand detection to system control in under 30 milliseconds
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
          className="mb-16"
        >
          <h3 className="text-2xl md:text-3xl font-light text-center mb-4">
            Gesture <span className="gradient-text">Reference</span>
          </h3>
          <p className="text-center text-neutral-400 text-sm mb-12">
            Master these gestures to control your computer naturally
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {gestures.map((gesture, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.4, delay: index * 0.1 }}
              whileHover={{ scale: 1.05, y: -5 }}
              className="glass-panel p-6 rounded-lg group cursor-pointer"
            >
              {/* Icon */}
              <div className="text-5xl mb-4 group-hover:scale-110 transition-transform">
                {gesture.icon}
              </div>

              {/* Name & Action */}
              <h4 className="text-lg font-medium mb-1 group-hover:text-gestura-cyan transition-colors">
                {gesture.name}
              </h4>
              <p className="text-xs text-gestura-purple uppercase tracking-wider mb-3">
                {gesture.action}
              </p>

              {/* Description */}
              <p className="text-sm text-neutral-400 leading-relaxed">
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
              <div className="text-3xl font-light gradient-text mb-2">&lt;30ms</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Latency</div>
              <p className="text-xs text-neutral-600 mt-2">End-to-end processing time</p>
            </div>
            <div>
              <div className="text-3xl font-light gradient-text mb-2">99%</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Accuracy</div>
              <p className="text-xs text-neutral-600 mt-2">Gesture recognition rate</p>
            </div>
            <div>
              <div className="text-3xl font-light gradient-text mb-2">30 FPS</div>
              <div className="text-xs text-neutral-500 uppercase tracking-wider">Tracking</div>
              <p className="text-xs text-neutral-600 mt-2">Real-time hand detection</p>
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
