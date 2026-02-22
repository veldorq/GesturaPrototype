'use client';

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import dynamic from 'next/dynamic';

// Lazy load non-critical components
const CustomCursor = dynamic(() => import('@/components/CustomCursor'), { ssr: false });
const ScrollProgressBar = dynamic(() => import('@/components/ScrollProgressBar'), { ssr: false });
const ScrollToTop = dynamic(() => import('@/components/ScrollToTop'), { ssr: false });
const MinimalNav = dynamic(() => import('@/components/MinimalNav'));
const MinimalFooter = dynamic(() => import('@/components/MinimalFooter'));

const steps = [
  {
    number: '01',
    title: 'Hand Detection',
    subtitle: 'AI-Powered Recognition',
    description: 'Advanced computer vision algorithms detect your hand in real-time using your webcam. MediaPipe technology identifies 21 key landmarks on each hand with sub-millimeter precision.',
    tech: ['MediaPipe', 'TensorFlow Lite', 'WebAssembly'],
    details: [
      'Real-time hand tracking at 30 FPS',
      '21 3D hand landmarks detected per frame',
      'Works in various lighting conditions',
      'Supports both hands simultaneously',
    ],
  },
  {
    number: '02',
    title: 'Gesture Classification',
    subtitle: 'Neural Network Processing',
    description: 'Custom-trained convolutional neural network analyzes hand landmarks and classifies gestures instantly. Recognizes 11+ distinct gestures with 99% accuracy.',
    tech: ['CNN Model', 'Real-time Inference', 'Edge Computing'],
    details: [
      'Custom-trained CNN architecture',
      '99% gesture recognition accuracy',
      'Supports 11+ unique gestures',
      'Continuous learning from usage patterns',
    ],
  },
  {
    number: '03',
    title: 'Motion Mapping',
    subtitle: 'Gesture to Action',
    description: 'Each recognized gesture triggers specific system actions. Smooth interpolation ensures natural, responsive control without lag or jitter.',
    tech: ['Action Mapping', 'Smoothing Pipeline', 'Event Handling'],
    details: [
      'Configurable gesture-to-action mapping',
      'Adaptive smoothing algorithms',
      'Debouncing for stable recognition',
      'Multi-stage filtering pipeline',
    ],
  },
  {
    number: '04',
    title: 'System Control',
    subtitle: 'Direct Integration',
    description: 'Gestures become system commands - zoom, scroll, navigate, pause. All processing happens locally on your device. Zero latency, complete privacy.',
    tech: ['Native APIs', 'Local Processing', 'Zero Cloud'],
    details: [
      'Direct OS-level integration',
      '100% local processing',
      'No internet connection required',
      'Zero data collection or telemetry',
    ],
  },
];

const gestures = [
  {
    icon: '🤏',
    name: 'Pinch Zoom',
    action: 'Zoom in/out',
    description: 'Pinch fingers together to zoom into content, spread apart to zoom out',
    gif: '/gestures/pinch-zoom.gif',
  },
  {
    icon: '👆',
    name: 'Swipe',
    action: 'Navigate tabs',
    description: 'Point with index finger and move left/right to switch between tabs',
    gif: '/gestures/swipe.gif',
  },
  {
    icon: '✋',
    name: 'Open Palm',
    action: 'Scroll pages',
    description: 'Show open palm and move up/down to scroll through content smoothly',
    gif: '/gestures/open-palm.gif',
  },
  {
    icon: '✊',
    name: 'Fist',
    action: 'Pause media',
    description: 'Make a fist to pause/play videos and audio instantly',
    gif: '/gestures/fist.gif',
  },
  {
    icon: '🤙',
    name: 'Call Sign',
    action: 'Toggle mute',
    description: 'Shaka hand sign to mute/unmute audio with a single gesture',
    gif: '/gestures/call-sign.gif',
  },
  {
    icon: '👎',
    name: 'Thumbs Down',
    action: 'Close window',
    description: 'Point thumb down to close the active window or application',
    gif: '/gestures/thumbs-down.gif',
  },
];

export default function HowItWorksPage() {
  useEffect(() => {
    document.documentElement.style.scrollBehavior = 'smooth';
    document.body.classList.add('loaded');
  }, []);

  return (
    <>
      <CustomCursor />
      <ScrollProgressBar />
      <ScrollToTop />

      <header>
        <MinimalNav />
      </header>

      <main className="bg-[#0f1419] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <section className="relative min-h-[70vh] flex items-center justify-center px-6 pt-32 pb-20">
          {/* Background Effects */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-gradient-radial from-cyan-900/10 via-transparent to-transparent opacity-30 pointer-events-none" />
            <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-cyan-400/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          </div>

          {/* Grid overlay */}
          <div className="absolute inset-0 opacity-[0.02]">
            <div 
              className="absolute inset-0"
              style={{
                backgroundImage: `
                  linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
                  linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)
                `,
                backgroundSize: '40px 40px',
              }}
            />
          </div>

          <div className="max-w-5xl mx-auto text-center relative z-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-cyan-500/10 backdrop-blur-sm border border-cyan-500/30 rounded-full"
            >
              <span className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse" />
              <span className="text-cyan-400 text-xs font-semibold uppercase tracking-widest">
                The Technology
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="text-3xl sm:text-4xl md:text-5xl lg:text-7xl font-light leading-tight mb-4 sm:mb-6 px-4"
            >
              How <span className="gradient-text-specs font-bold">Gestura</span><br />
              Works
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-base sm:text-lg md:text-xl text-neutral-400 max-w-3xl mx-auto mb-8 sm:mb-10 font-light px-4"
            >
              From hand detection to system control in under 30 milliseconds. 
              Discover the technology that makes hands-free control possible.
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link
                href="/features"
                className="px-8 sm:px-10 py-3 sm:py-4 min-h-[44px] border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer text-sm sm:text-base"
              >
                Explore Features
              </Link>
              
              <Link
                href="/download"
                className="px-8 sm:px-10 py-3 sm:py-4 min-h-[44px] text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide text-sm sm:text-base"
              >
                Download Now
              </Link>
            </motion.div>
          </div>
        </section>

        {/* Process Steps */}
        <section className="relative py-16 sm:py-20 px-4 sm:px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12 sm:mb-16 px-4"
            >
              <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-7xl font-bold mb-4 sm:mb-6 bg-gradient-to-r from-cyan-400 via-cyan-200 to-purple-400 bg-clip-text text-transparent py-2 leading-tight">
                Four-Step Process
              </h2>
              <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-neutral-300 max-w-3xl mx-auto font-light">
                Lightning-fast gesture recognition powered by advanced AI
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-x-8 gap-y-16">
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
                    <div className="hidden md:block absolute top-20 left-full w-8 h-px bg-gradient-to-r from-cyan-400/50 to-transparent" />
                  )}

                  <div className="border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 group hover:border-cyan-500/30 transition-colors duration-300 hover:scale-105">
                    {/* Number */}
                    <motion.div 
                      className="text-sm text-neutral-500 uppercase tracking-wider mb-2"
                      whileHover={{ scale: 1.1 }}
                    >
                      STEP {step.number}
                    </motion.div>

                    {/* Title & Subtitle */}
                    <h3 className="text-xl font-medium mb-2 group-hover:text-cyan-400 transition-colors">
                      {step.title}
                    </h3>
                    <p className="text-sm text-purple-400 mb-4">{step.subtitle}</p>

                    {/* Description */}
                    <p className="text-neutral-400 text-sm leading-relaxed mb-6">
                      {step.description}
                    </p>

                    {/* Detailed Points */}
                    <ul className="space-y-2 mb-6">
                      {step.details.map((detail, i) => (
                        <li key={i} className="text-xs text-neutral-500 flex items-start gap-2">
                          <span className="text-cyan-400 mt-1">▸</span>
                          <span>{detail}</span>
                        </li>
                      ))}
                    </ul>

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

                    {/* Hover gradient */}
                    <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Divider */}
        <motion.div
          initial={{ scaleX: 0 }}
          whileInView={{ scaleX: 1 }}
          viewport={{ once: true }}
          className="h-px bg-gradient-to-r from-transparent via-white/20 to-transparent max-w-7xl mx-auto mb-20"
        />

        {/* Gesture Reference */}
        <section className="relative py-16 sm:py-20 px-4 sm:px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-12 sm:mb-16 px-4"
            >
              <h3 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold mb-4 sm:mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Gesture Reference
              </h3>
              <p className="text-base sm:text-lg text-neutral-400 max-w-2xl mx-auto">
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
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300 cursor-pointer overflow-hidden"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  
                  {/* GIF/Icon Container */}
                  <div className="relative mb-4 h-32 flex items-center justify-center bg-neutral-950/50 rounded-xl overflow-hidden">
                    <img 
                      src={gesture.gif} 
                      alt={gesture.name}
                      className="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                      onError={(e) => {
                        // Fallback to icon if GIF fails to load
                        e.currentTarget.style.display = 'none';
                      }}
                    />
                    <div className="text-5xl group-hover:scale-110 transition-transform pointer-events-none">
                      {gesture.icon}
                    </div>
                  </div>

                  {/* Name & Action */}
                  <h4 className="text-xl font-semibold mb-2 group-hover:text-cyan-400 transition-colors">
                    {gesture.name}
                  </h4>
                  <p className="text-sm text-cyan-400 font-medium mb-3">
                    {gesture.action}
                  </p>

                  {/* Description */}
                  <p className="text-sm text-neutral-400 leading-relaxed">
                    {gesture.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Technical Specs */}
        <section className="relative py-16 sm:py-20 px-4 sm:px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="relative border border-neutral-800 rounded-2xl p-8 md:p-12 backdrop-blur-sm bg-neutral-900/30"
            >
              <h3 className="text-xl sm:text-2xl md:text-3xl font-bold mb-8 sm:mb-12 text-center bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed px-4">
                Technical Specifications
              </h3>
              
              <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 sm:gap-8 md:gap-10 lg:gap-12 text-center">
                <div className="flex flex-col items-center justify-start min-h-[140px] px-2">
                  <div className="text-3xl sm:text-4xl font-bold mb-3 gradient-text" style={{ WebkitTextFillColor: 'transparent' }}>
                    <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">&lt;30ms</span>
                  </div>
                  <div className="text-xs sm:text-sm text-neutral-500 uppercase tracking-wider mb-2 font-semibold">Latency</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">End-to-end processing</p>
                </div>
                <div className="flex flex-col items-center justify-start min-h-[140px] px-2">
                  <div className="text-3xl sm:text-4xl font-bold mb-3 gradient-text" style={{ WebkitTextFillColor: 'transparent' }}>
                    <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">99%</span>
                  </div>
                  <div className="text-xs sm:text-sm text-neutral-500 uppercase tracking-wider mb-2 font-semibold">Accuracy</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">Recognition rate</p>
                </div>
                <div className="flex flex-col items-center justify-start min-h-[140px] px-2">
                  <div className="text-3xl sm:text-4xl font-bold mb-3 gradient-text" style={{ WebkitTextFillColor: 'transparent' }}>
                    <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">30</span>
                  </div>
                  <div className="text-xs sm:text-sm text-neutral-500 uppercase tracking-wider mb-2 font-semibold">FPS</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">Real-time detection</p>
                </div>
                <div className="flex flex-col items-center justify-start min-h-[140px] px-2">
                  <div className="text-3xl sm:text-4xl font-bold mb-3 gradient-text" style={{ WebkitTextFillColor: 'transparent' }}>
                    <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">100%</span>
                  </div>
                  <div className="text-xs sm:text-sm text-neutral-500 uppercase tracking-wider mb-2 font-semibold">Local</div>
                  <p className="text-xs text-neutral-400 leading-relaxed">No cloud processing</p>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Technology Stack */}
        <section className="relative py-16 sm:py-20 px-4 sm:px-6">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16 px-4"
            >
              <h3 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Built With Modern Tech
              </h3>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                Industry-leading tools and frameworks
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-6">
              {[
                {
                  name: 'MediaPipe',
                  description: "Google's ML solution for hand tracking",
                  badge: 'Computer Vision',
                },
                {
                  name: 'TensorFlow',
                  description: 'Neural network training and inference',
                  badge: 'Deep Learning',
                },
                {
                  name: 'Python',
                  description: 'Core application framework',
                  badge: 'Backend',
                },
                {
                  name: 'OpenCV',
                  description: 'Real-time image processing',
                  badge: 'Vision',
                },
                {
                  name: 'PyAutoGUI',
                  description: 'System-level automation',
                  badge: 'Control',
                },
                {
                  name: 'NumPy',
                  description: 'High-performance computing',
                  badge: 'Mathematics',
                },
              ].map((tech, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  <div className="text-xs text-cyan-400 uppercase tracking-wider mb-2">
                    {tech.badge}
                  </div>
                  <h4 className="text-xl font-light mb-2">{tech.name}</h4>
                  <p className="text-sm text-neutral-400">{tech.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="relative py-16 sm:py-20 px-4 sm:px-6">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-light mb-4 sm:mb-6 px-4">
                Experience the Technology
              </h2>
              <p className="text-base sm:text-lg text-neutral-400 mb-8 sm:mb-10 font-light px-4">
                See Gestura in action. Download now and control your computer with natural hand gestures.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center px-4">
                <Link
                  href="/download"
                  className="inline-block px-8 sm:px-10 md:px-12 py-3 sm:py-4 md:py-5 min-h-[44px] border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer text-sm sm:text-base"
                >
                  Download Gestura
                </Link>
                <Link
                  href="/features"
                  className="inline-block px-8 sm:px-10 md:px-12 py-3 sm:py-4 md:py-5 min-h-[44px] text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide text-sm sm:text-base"
                >
                  View All Features
                </Link>
              </div>
            </motion.div>
          </div>
        </section>

        <div className="h-20" />
      </main>

      <MinimalFooter />
    </>
  );
}
