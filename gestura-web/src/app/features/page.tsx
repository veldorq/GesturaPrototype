'use client';

import { useEffect } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import { gestureFeatures, featureHighlights } from '@/data/features';

// Lazy load non-critical components
const CustomCursor = dynamic(() => import('@/components/CustomCursor'), { ssr: false });
const ScrollProgressBar = dynamic(() => import('@/components/ScrollProgressBar'), { ssr: false });
const ScrollToTop = dynamic(() => import('@/components/ScrollToTop'), { ssr: false });
const MinimalNav = dynamic(() => import('@/components/MinimalNav'));
const MinimalFooter = dynamic(() => import('@/components/MinimalFooter'));

export default function FeaturesPage() {
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
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-400/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
          </div>

          {/* Grid overlay */}
          <div className="absolute inset-0 opacity-[0.02]">
            <div className="absolute inset-0" style={{
              backgroundImage: `
                linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)
              `,
              backgroundSize: '40px 40px'
            }} />
          </div>

          <div className="max-w-5xl mx-auto text-center relative z-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
            >
              <span className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
              <span className="text-gestura-cyan text-xs font-semibold uppercase tracking-widest">
                Feature Overview
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="text-5xl md:text-7xl font-light leading-tight mb-6"
            >
              Control Everything<br />
              <span className="gradient-text-specs font-bold">With Your Hands</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-lg md:text-xl text-neutral-400 max-w-3xl mx-auto mb-10 font-light"
            >
              11+ natural gestures for seamless interaction. From navigation to media control, 
              Gestura transforms your hands into the ultimate input device.
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center"
            >
              <Link
                href="/download"
                className="px-10 py-4 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
              >
                Download Now
              </Link>
              
              <Link
                href="/how-it-works"
                className="px-10 py-4 text-white/60 hover:text-white transition-colors duration-300 font-light tracking-wide"
              >
                See How It Works
              </Link>
            </motion.div>
          </div>
        </section>

        {/* Feature Highlights Grid */}
        <section className="relative py-20 px-6">
          <div className="max-w-7xl mx-auto">
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-20">
              {featureHighlights.map((highlight, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  
                  {/* Label */}
                  {highlight.metricLabel && (
                    <div className="text-sm text-neutral-500 uppercase tracking-wider mb-2">
                      {highlight.metricLabel}
                    </div>
                  )}
                  
                  {/* Value */}
                  {highlight.metric && (
                    <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 mb-3 py-1 leading-relaxed">
                      {highlight.metric}
                    </div>
                  )}
                  
                  {/* Title */}
                  <h3 className="text-xl font-medium mb-3">{highlight.title}</h3>
                  
                  {/* Description */}
                  <p className="text-sm text-neutral-400 leading-relaxed">{highlight.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Gesture Categories */}
        <section className="relative py-20 px-6">
          {/* Japanese character background */}
          <div className="max-w-7xl mx-auto relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16 px-4"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Gesture Library
              </h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto">Master all available gestures for full control</p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {gestureFeatures.map((feature, index) => (
                <motion.div
                  key={feature.id}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  whileHover={{ y: -5 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300 overflow-hidden"
                >
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />

                  {/* Icon */}
                  <div className="text-4xl mb-4">{feature.icon}</div>

                  {/* Category Label */}
                  <div className="text-sm text-neutral-500 uppercase tracking-wider mb-2">
                    {feature.category}
                  </div>

                  {/* Name */}
                  <h3 className="text-xl font-medium mb-2 group-hover:text-cyan-400 transition-colors">
                    {feature.name}
                  </h3>

                  {/* Action */}
                  <p className="text-sm text-purple-400 mb-3">{feature.action}</p>

                  {/* Description */}
                  <p className="text-sm text-neutral-400 leading-relaxed">
                    {feature.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Key Benefits Section */}
        <section className="relative py-32 px-6">
          <div className="max-w-6xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-20"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Why Choose Gestura
              </h2>
              <p className="text-lg text-neutral-400 max-w-2xl mx-auto font-light">
                Built for creators, professionals, and anyone who wants a better way to interact with technology
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8">
              {[
                {
                  title: 'Accessibility First',
                  description: 'Empowers users with limited mobility to control their devices naturally and intuitively.',
                  icon: '♿',
                },
                {
                  title: 'Productivity Boost',
                  description: 'Speed up your workflow with instant gesture commands. No more reaching for mouse or keyboard.',
                  icon: '⚡',
                },
                {
                  title: 'Presentation Mode',
                  description: 'Control slides and media from a distance. Perfect for speakers, educators, and performers.',
                  icon: '🎤',
                },
                {
                  title: 'Privacy Protected',
                  description: 'All processing happens on your device. Zero telemetry, no cloud uploads, complete control.',
                  icon: '🔒',
                },
              ].map((benefit, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.95 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  
                  <div className="text-4xl mb-4">{benefit.icon}</div>
                  <h3 className="text-xl font-medium mb-3">{benefit.title}</h3>
                  <p className="text-sm text-neutral-400 leading-relaxed">{benefit.description}</p>
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
                Ready to Get Started?
              </h2>
              <p className="text-lg text-neutral-400 mb-10 font-light">
                Download Gestura and experience the future of hands-free control
              </p>
              <Link
                href="/download"
                className="inline-block px-12 py-5 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
              >
                Download Now
              </Link>
            </motion.div>
          </div>
        </section>

        <div className="h-20" />
      </main>

      <MinimalFooter />
    </>
  );
}
