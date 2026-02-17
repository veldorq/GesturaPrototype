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

export default function DownloadPage() {
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

      <main className="bg-[#0A0118] min-h-screen overflow-x-hidden">
        {/* Hero Section */}
        <section className="relative min-h-[70vh] flex items-center justify-center px-6 pt-32 pb-20">
          {/* Background Effects */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-gradient-radial from-cyan-900/10 via-transparent to-transparent opacity-30 pointer-events-none" />
            <div className="absolute top-1/3 left-1/3 w-96 h-96 bg-cyan-400/10 rounded-full blur-3xl animate-pulse" />
            <div className="absolute bottom-1/3 right-1/3 w-96 h-96 bg-purple-400/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
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

          <div className="max-w-4xl mx-auto text-center relative z-10">
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center gap-2 px-4 py-2 mb-8 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
            >
              <span className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
              <span className="text-gestura-cyan text-xs font-semibold uppercase tracking-widest">
                Get Started
              </span>
            </motion.div>

            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1, duration: 0.6 }}
              className="text-5xl md:text-7xl font-light leading-tight mb-6"
            >
              Download <span className="gradient-text-specs font-bold">Gestura</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2, duration: 0.6 }}
              className="text-lg md:text-xl text-neutral-400 max-w-3xl mx-auto mb-10 font-light"
            >
              Get instant access to hands-free computer control. 
              Simple installation, zero configuration required.
            </motion.p>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3, duration: 0.6 }}
              className="flex flex-col items-center gap-4"
            >
              <a
                href="https://github.com/veldorq/GesturaPrototype/releases/latest"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-400 to-purple-400 text-white hover:scale-105 transition-all duration-300 rounded-full font-semibold tracking-wide cursor-pointer shadow-2xl shadow-cyan-400/30"
              >
                Download Latest Version
              </a>
              <p className="text-xs text-neutral-500">
                Version 1.0 • Windows, macOS, Linux • Free & Open Source
              </p>
            </motion.div>
          </div>
        </section>

        {/* Installation Steps */}
        <section className="relative py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Quick Installation
              </h2>
              <p className="text-neutral-400 font-light">
                Get up and running in three simple steps
              </p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-8 mb-20">
              {[
                {
                  number: '01',
                  title: 'Download',
                  description: 'Download the installer for your operating system from GitHub releases',
                  icon: '⬇️',
                },
                {
                  number: '02',
                  title: 'Install',
                  description: 'Run the installer and follow the setup wizard. Gestura will install all dependencies automatically',
                  icon: '⚙️',
                },
                {
                  number: '03',
                  title: 'Launch',
                  description: 'Open Gestura and grant camera permissions. Start controlling your computer with hand gestures',
                  icon: '🚀',
                },
              ].map((step, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 40 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.15 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300 hover:scale-105"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  
                  <div className="text-4xl mb-4">{step.icon}</div>
                  <div className="text-sm text-neutral-500 uppercase tracking-wider mb-2">{step.number}</div>
                  <h3 className="text-xl font-medium mb-3">{step.title}</h3>
                  <p className="text-sm text-neutral-400 leading-relaxed">{step.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* System Requirements */}
        <section className="relative py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                System Requirements
              </h2>
              <p className="text-neutral-400 font-light">
                Runs smoothly on most modern computers
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 gap-8">
              {/* Minimum Requirements */}
              <motion.div
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30"
              >
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-3xl">💻</span>
                  <h3 className="text-2xl font-light">Minimum</h3>
                </div>
                <ul className="space-y-4">
                  {[
                    { label: 'OS', value: 'Windows 10, macOS 10.15, Ubuntu 20.04' },
                    { label: 'Processor', value: 'Intel Core i3 or equivalent' },
                    { label: 'RAM', value: '4 GB' },
                    { label: 'Webcam', value: '720p (30 FPS)' },
                    { label: 'Storage', value: '500 MB available space' },
                  ].map((req, i) => (
                    <li key={i} className="flex justify-between items-start gap-4 pb-4 border-b border-white/5">
                      <span className="text-neutral-500 text-sm">{req.label}</span>
                      <span className="text-neutral-300 text-sm text-right">{req.value}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>

              {/* Recommended Requirements */}
              <motion.div
                initial={{ opacity: 0, x: 30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="border border-cyan-500/30 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30"
              >
                <div className="flex items-center gap-3 mb-6">
                  <span className="text-3xl">⚡</span>
                  <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
                    Recommended
                  </h3>
                </div>
                <ul className="space-y-4">
                  {[
                    { label: 'OS', value: 'Windows 11, macOS 12+, Ubuntu 22.04' },
                    { label: 'Processor', value: 'Intel Core i5 or better' },
                    { label: 'RAM', value: '8 GB or more' },
                    { label: 'Webcam', value: '1080p (60 FPS)' },
                    { label: 'Storage', value: '1 GB available space' },
                  ].map((req, i) => (
                    <li key={i} className="flex justify-between items-start gap-4 pb-4 border-b border-white/5">
                      <span className="text-neutral-500 text-sm">{req.label}</span>
                      <span className="text-neutral-300 text-sm text-right">{req.value}</span>
                    </li>
                  ))}
                </ul>
              </motion.div>
            </div>

            {/* Additional Notes */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="mt-8 border border-cyan-500/20 rounded-2xl p-6 backdrop-blur-sm bg-cyan-500/5"
            >
              <div className="flex items-start gap-3">
                <span className="text-2xl">💡</span>
                <div>
                  <h4 className="font-semibold mb-2 text-cyan-400">Note</h4>
                  <p className="text-sm text-neutral-400 leading-relaxed">
                    A working webcam is required for hand tracking. Good lighting conditions improve gesture recognition accuracy. 
                    All processing happens locally on your device—no internet connection required after installation.
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Platform Support */}
        <section className="relative py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Available On All Platforms
              </h2>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-6 mb-12">
              {[
                {
                  platform: 'Windows',
                  icon: '🪟',
                  description: 'Windows 10 and 11 (64-bit)',
                  download: 'Download .exe',
                },
                {
                  platform: 'macOS',
                  icon: '🍎',
                  description: 'macOS 10.15 and later',
                  download: 'Download .dmg',
                },
                {
                  platform: 'Linux',
                  icon: '🐧',
                  description: 'Ubuntu, Debian, Fedora',
                  download: 'Download .AppImage',
                },
              ].map((platform, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                  className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 text-center hover:border-cyan-500/30 transition-colors duration-300 hover:scale-105 cursor-pointer"
                >
                  {/* Hover gradient */}
                  <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
                  
                  <div className="text-5xl mb-4">{platform.icon}</div>
                  <h3 className="text-xl font-medium mb-2">{platform.platform}</h3>
                  <p className="text-sm text-neutral-400 mb-4">{platform.description}</p>
                  <a
                    href="https://github.com/veldorq/GesturaPrototype/releases/latest"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-cyan-400 hover:text-white transition-colors"
                  >
                    {platform.download} →
                  </a>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* Getting Help */}
        <section className="relative py-20 px-6">
          <div className="max-w-4xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="border border-neutral-800 rounded-2xl p-10 backdrop-blur-sm bg-neutral-900/30 text-center"
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-4 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
                Need Help?
              </h2>
              <p className="text-neutral-400 mb-8 font-light">
                Check out our documentation or reach out to the community
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <a
                  href="https://github.com/veldorq/GesturaPrototype"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-8 py-3 border border-white/20 text-white hover:border-white/60 transition-all duration-300 rounded-full font-light"
                >
                  📚 Documentation
                </a>
                <a
                  href="https://github.com/veldorq/GesturaPrototype/issues"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-8 py-3 border border-white/20 text-white hover:border-white/60 transition-all duration-300 rounded-full font-light"
                >
                  💬 Support Forum
                </a>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Quick Links */}
        <section className="relative py-20 px-6">
          <div className="max-w-5xl mx-auto">
            <div className="grid md:grid-cols-2 gap-6">
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30"
              >
                <h3 className="text-xl font-medium mb-3">Explore Features</h3>
                <p className="text-sm text-neutral-400 mb-6">
                  Discover all the gestures and capabilities Gestura offers
                </p>
                <Link
                  href="/features"
                  className="inline-block text-sm text-cyan-400 hover:text-white transition-colors"
                >
                  View All Features →
                </Link>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, x: 20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                className="border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30"
              >
                <h3 className="text-xl font-medium mb-3">How It Works</h3>
                <p className="text-sm text-neutral-400 mb-6">
                  Learn about the technology behind gesture recognition
                </p>
                <Link
                  href="/how-it-works"
                  className="inline-block text-sm text-cyan-400 hover:text-white transition-colors"
                >
                  See the Technology →
                </Link>
              </motion.div>
            </div>
          </div>
        </section>

        {/* Final CTA */}
        <section className="relative py-20 px-6">
          <div className="max-w-3xl mx-auto text-center">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl md:text-5xl font-light mb-6">
                Ready to Begin?
              </h2>
              <p className="text-lg text-neutral-400 mb-10 font-light">
                Download Gestura now and transform how you interact with your computer
              </p>
              <a
                href="https://github.com/veldorq/GesturaPrototype/releases/latest"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block px-12 py-5 border border-white text-white hover:bg-white hover:text-black transition-all duration-300 rounded-full font-light tracking-wide cursor-pointer"
              >
                Download Now
              </a>
            </motion.div>
          </div>
        </section>

        <div className="h-20" />
      </main>

      <MinimalFooter />
    </>
  );
}
