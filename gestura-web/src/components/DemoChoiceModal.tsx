'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useState } from 'react';

interface DemoChoiceModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function DemoChoiceModal({ isOpen, onClose }: DemoChoiceModalProps) {
  const [hoveredOption, setHoveredOption] = useState<'watch' | 'try' | null>(null);

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/80 backdrop-blur-md z-50"
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 100 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 100 }}
            transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 pointer-events-none"
          >
            <div className="relative max-w-5xl w-full glass-panel rounded-3xl p-8 md:p-12 pointer-events-auto">
              {/* Close Button */}
              <button
                onClick={onClose}
                className="absolute top-6 right-6 w-10 h-10 flex items-center justify-center rounded-full bg-white/5 hover:bg-white/10 transition-colors text-gestura-text-secondary hover:text-white"
              >
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </button>

              {/* Header */}
              <div className="text-center mb-12">
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="inline-flex items-center gap-2 px-4 py-2 mb-6 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full"
                >
                  <span className="w-2 h-2 bg-gestura-cyan rounded-full animate-pulse" />
                  <span className="text-gestura-cyan text-sm font-semibold uppercase tracking-wider">
                    Choose Your Experience
                  </span>
                </motion.div>

                <motion.h2
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 }}
                  className="text-2xl md:text-3xl font-space font-semibold gradient-text mb-4"
                >
                  How would you like to see Gestura?
                </motion.h2>
                
                <motion.p
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="text-gestura-text-secondary font-inter text-base md:text-lg max-w-2xl mx-auto"
                >
                  Watch a quick demo or try it yourself with your webcam
                </motion.p>
              </div>

              {/* Options Grid */}
              <div className="grid md:grid-cols-2 gap-6">
                {/* Watch Demo Option */}
                <motion.a
                  href="#watch-demo"
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.3 }}
                  onMouseEnter={() => setHoveredOption('watch')}
                  onMouseLeave={() => setHoveredOption(null)}
                  whileHover={{ scale: 1.02, y: -5 }}
                  whileTap={{ scale: 0.98 }}
                  className="relative group glass-panel rounded-2xl p-8 border-2 border-gestura-purple/30 hover:border-gestura-purple transition-all overflow-hidden"
                >
                  {/* Background Glow */}
                  <div className="absolute inset-0 bg-gradient-to-br from-gestura-purple/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                  {/* Icon */}
                  <div className="relative mb-6 flex justify-center">
                    <motion.div
                      animate={{
                        scale: hoveredOption === 'watch' ? 1.1 : 1,
                        rotate: hoveredOption === 'watch' ? 5 : 0
                      }}
                      className="w-20 h-20 rounded-2xl bg-gradient-to-br from-gestura-purple to-pink-500 flex items-center justify-center shadow-2xl shadow-gestura-purple/50"
                    >
                      <svg width="40" height="40" viewBox="0 0 24 24" fill="white">
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    </motion.div>
                  </div>

                  {/* Content */}
                  <div className="relative text-center">
                    <h3 className="text-xl md:text-2xl font-space font-semibold text-white mb-3">
                      Watch Demo
                    </h3>
                    <p className="text-gestura-text-secondary font-inter mb-6 leading-relaxed text-sm md:text-base">
                      See Gestura in action with a
                      <br />
                      <span className="text-white font-medium">2-minute guided video</span>
                    </p>

                    {/* Features */}
                    <ul className="space-y-2 text-sm text-gestura-text-secondary font-inter text-left">
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-purple flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        No camera required
                      </li>
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-purple flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        Quick overview of all features
                      </li>
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-purple flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        Perfect for quick evaluation
                      </li>
                    </ul>

                    {/* Button */}
                    <motion.div
                      className="mt-6 py-3 px-6 bg-gradient-to-r from-gestura-purple to-pink-500 rounded-xl text-white font-semibold font-inter flex items-center justify-center gap-2"
                      whileHover={{ scale: 1.05 }}
                    >
                      Play Video
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="white">
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    </motion.div>
                  </div>
                </motion.a>

                {/* Try Live Option */}
                <motion.a
                  href="/dashboard"
                  initial={{ opacity: 0, x: 50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.4 }}
                  onMouseEnter={() => setHoveredOption('try')}
                  onMouseLeave={() => setHoveredOption(null)}
                  whileHover={{ scale: 1.02, y: -5 }}
                  whileTap={{ scale: 0.98 }}
                  className="relative group glass-panel rounded-2xl p-8 border-2 border-gestura-cyan/30 hover:border-gestura-cyan transition-all overflow-hidden"
                >
                  {/* Background Glow */}
                  <div className="absolute inset-0 bg-gradient-to-br from-gestura-cyan/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

                  {/* Recommended Badge */}
                  <div className="absolute top-4 right-4">
                    <span className="px-3 py-1 bg-gradient-to-r from-gestura-cyan to-blue-400 rounded-full text-xs font-bold text-white uppercase tracking-wider shadow-lg">
                      Recommended
                    </span>
                  </div>

                  {/* Icon */}
                  <div className="relative mb-6 flex justify-center">
                    <motion.div
                      animate={{
                        scale: hoveredOption === 'try' ? 1.1 : 1,
                        rotate: hoveredOption === 'try' ? -5 : 0
                      }}
                      className="w-20 h-20 rounded-2xl bg-gradient-to-br from-gestura-cyan to-blue-500 flex items-center justify-center shadow-2xl shadow-gestura-cyan/50"
                    >
                      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2">
                        <circle cx="12" cy="12" r="10" />
                        <path d="M12 6v6l4 2" />
                      </svg>
                    </motion.div>
                  </div>

                  {/* Content */}
                  <div className="relative text-center">
                    <h3 className="text-xl md:text-2xl font-space font-semibold text-white mb-3">
                      Try Live Demo
                    </h3>
                    <p className="text-gestura-text-secondary font-inter mb-6 leading-relaxed text-sm md:text-base">
                      Experience real-time control with
                      <br />
                      <span className="text-white font-medium">your own webcam</span>
                    </p>

                    {/* Features */}
                    <ul className="space-y-2 text-sm text-gestura-text-secondary font-inter text-left">
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-cyan flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        Try all gestures yourself
                      </li>
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-cyan flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        Real-time hand tracking
                      </li>
                      <li className="flex items-center gap-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-gestura-cyan flex-shrink-0">
                          <path d="M20 6L9 17l-5-5" />
                        </svg>
                        100% private, runs in browser
                      </li>
                    </ul>

                    {/* Button */}
                    <motion.div
                      className="mt-6 py-3 px-6 bg-gradient-to-r from-gestura-cyan to-blue-500 rounded-xl text-white font-semibold font-inter flex items-center justify-center gap-2"
                      whileHover={{ scale: 1.05 }}
                    >
                      Launch Demo
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M5 12h14M12 5l7 7-7 7" />
                      </svg>
                    </motion.div>
                  </div>
                </motion.a>
              </div>

              {/* Footer Note */}
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.6 }}
                className="text-center text-gestura-text-secondary/60 font-inter text-sm mt-8"
              >
                Both options are free • No signup required • Works on Chrome, Edge, and Firefox
              </motion.p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
