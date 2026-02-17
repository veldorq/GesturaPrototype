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

      <main className="bg-[#0B0B0F] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <section className="relative min-h-[70vh] flex items-center justify-center px-6 pt-32 pb-20">
          {/* Background Effects */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-gradient-to-b from-gestura-cyan/5 via-transparent to-transparent" />
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-gestura-cyan/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gestura-purple/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
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
              <span className="gradient-text">With Your Hands</span>
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
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
              {featureHighlights.map((highlight, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.6, delay: index * 0.1 }}
                  className="glass-panel p-8 rounded-lg hover:border-gestura-cyan/50 transition-all duration-300"
                >
                  {highlight.metric && (
                    <div className="mb-4">
                      <span className="text-5xl font-light gradient-text">
                        {highlight.metric}
                      </span>
                      {highlight.metricLabel && (
                        <span className="block text-sm text-gestura-cyan/70 mt-1">
                          {highlight.metricLabel}
                        </span>
                      )}
                    </div>
                  )}
                  <h3 className="text-2xl font-light mb-3">{highlight.title}</h3>
                  <p className="text-neutral-400 text-sm leading-relaxed">{highlight.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Gesture Categories */}
        <section className="relative py-20 px-6">
          {/* Japanese character background */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 0.03 }}
            viewport={{ once: true }}
            className="absolute left-10 top-20 text-[10rem] font-bold text-white pointer-events-none hidden lg:block"
            style={{ writingMode: 'vertical-rl', textOrientation: 'upright' }}
          >
            機能
          </motion.div>

          <div className="max-w-7xl mx-auto relative z-10">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-light mb-4">
                Gesture <span className="gradient-text">Library</span>
              </h2>
              <div className="w-24 h-1 bg-gestura-cyan mx-auto" />
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
                  className="group relative glass-panel p-8 rounded-lg overflow-hidden"
                >
                  {/* Gradient overlay on hover */}
                  <div className="absolute inset-0 bg-gradient-to-br from-gestura-cyan/10 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />

                  {/* Number */}
                  <div className="relative text-gestura-cyan text-sm font-mono mb-4">
                    {String(index + 1).padStart(2, '0')}
                  </div>

                  {/* Icon */}
                  <div className="relative text-4xl mb-4">{feature.icon}</div>

                  {/* Content */}
                  <h3 className="relative text-2xl font-light mb-2 group-hover:text-gestura-cyan transition-colors">
                    {feature.name}
                  </h3>

                  <p className="relative text-sm text-gestura-purple mb-4 font-medium">{feature.action}</p>

                  <p className="relative text-sm text-neutral-400 leading-relaxed">
                    {feature.description}
                  </p>

                  {/* Category Badge */}
                  <div className="relative mt-4 inline-block">
                    <span className="text-xs px-3 py-1 bg-gestura-cyan/10 border border-gestura-cyan/30 rounded-full text-gestura-cyan">
                      {feature.category}
                    </span>
                  </div>
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
              <h2 className="text-4xl md:text-5xl font-light mb-6">
                Why Choose <span className="gradient-text">Gestura</span>
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
                  className="glass-panel p-8 rounded-lg hover:border-gestura-cyan/50 transition-all duration-300"
                >
                  <div className="text-5xl mb-4">{benefit.icon}</div>
                  <h3 className="text-2xl font-light mb-3">{benefit.title}</h3>
                  <p className="text-neutral-400 leading-relaxed">{benefit.description}</p>
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
