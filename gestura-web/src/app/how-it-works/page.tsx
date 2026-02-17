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

      <main className="bg-[#0B0B0F] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <section className="relative min-h-[70vh] flex items-center justify-center px-6 pt-32 pb-20">
          {/* Background Effects */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-gradient-to-b from-gestura-purple/5 via-transparent to-transparent" />
            <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-gestura-purple/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-gestura-cyan/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          </div>

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

          <div className="max-w-5xl mx-auto text-center relative z-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-gestura-purple/10 backdrop-blur-sm border border-gestura-purple/30 rounded-full"
            >
              <span className="w-2 h-2 bg-gestura-purple rounded-full animate-pulse" />
              <span className="text-gestura-purple text-xs font-semibold uppercase tracking-widest">
                The Technology
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="text-5xl md:text-7xl font-light leading-tight mb-6"
            >
              How <span className="gradient-text">Gestura</span><br />
              Works
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-lg md:text-xl text-neutral-400 max-w-3xl mx-auto mb-10 font-light"
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
                className="px-10 py-4 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
              >
                Explore Features
              </Link>
              
              <Link
                href="/download"
                className="px-10 py-4 text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide"
              >
                Download Now
              </Link>
            </motion.div>
          </div>
        </section>

        {/* Process Steps */}
        <section className="relative py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-20"
            >
              <h2 className="text-4xl md:text-5xl font-light mb-4">
                Four-Step <span className="gradient-text">Process</span>
              </h2>
              <p className="text-neutral-400 font-light">
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

                    {/* Detailed Points */}
                    <ul className="space-y-2 mb-6">
                      {step.details.map((detail, i) => (
                        <li key={i} className="text-xs text-neutral-500 flex items-start gap-2">
                          <span className="text-gestura-cyan mt-1">▸</span>
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
        <section className="relative py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="mb-16"
            >
              <h3 className="text-3xl md:text-4xl font-light text-center mb-4">
                Gesture <span className="gradient-text">Reference</span>
              </h3>
              <p className="text-center text-neutral-400 font-light mb-2">
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
          </div>
        </section>

        {/* Technical Specs */}
        <section className="relative py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="glass-panel p-8 md:p-12 rounded-lg"
            >
              <h3 className="text-2xl md:text-3xl font-light mb-12 text-center">
                Technical <span className="gradient-text">Specifications</span>
              </h3>
              
              <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
                <div>
                  <div className="text-4xl md:text-5xl font-light gradient-text mb-3">&lt;30ms</div>
                  <div className="text-xs text-neutral-400 uppercase tracking-wider mb-2">Latency</div>
                  <p className="text-xs text-neutral-600">End-to-end processing</p>
                </div>
                <div>
                  <div className="text-4xl md:text-5xl font-light gradient-text mb-3">99%</div>
                  <div className="text-xs text-neutral-400 uppercase tracking-wider mb-2">Accuracy</div>
                  <p className="text-xs text-neutral-600">Recognition rate</p>
                </div>
                <div>
                  <div className="text-4xl md:text-5xl font-light gradient-text mb-3">30 FPS</div>
                  <div className="text-xs text-neutral-400 uppercase tracking-wider mb-2">Tracking</div>
                  <p className="text-xs text-neutral-600">Real-time detection</p>
                </div>
                <div>
                  <div className="text-4xl md:text-5xl font-light gradient-text mb-3">100%</div>
                  <div className="text-xs text-neutral-400 uppercase tracking-wider mb-2">Local</div>
                  <p className="text-xs text-neutral-600">No cloud processing</p>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Technology Stack */}
        <section className="relative py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h3 className="text-3xl md:text-4xl font-light mb-4">
                Built With <span className="gradient-text">Modern Tech</span>
              </h3>
              <p className="text-neutral-400 font-light">
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
                  className="glass-panel p-6 rounded-lg hover:border-gestura-cyan/50 transition-colors"
                >
                  <div className="text-xs text-gestura-cyan uppercase tracking-wider mb-2">
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
        <section className="relative py-20 px-6">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl md:text-5xl font-light mb-6">
                Experience the Technology
              </h2>
              <p className="text-lg text-neutral-400 mb-10 font-light">
                See Gestura in action. Download now and control your computer with natural hand gestures.
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                  href="/download"
                  className="inline-block px-12 py-5 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
                >
                  Download Gestura
                </Link>
                <Link
                  href="/features"
                  className="inline-block px-12 py-5 text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide"
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
