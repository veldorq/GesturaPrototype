'use client';

import { motion } from 'framer-motion';

const techBadges = [
  { name: 'Python 3.10+', url: 'https://www.python.org' },
  { name: 'MediaPipe', url: 'https://developers.google.com/mediapipe' },
  { name: 'OpenCV 4.x', url: 'https://opencv.org' },
  { name: 'PyAutoGUI', url: 'https://pyautogui.readthedocs.io' },
];

const technologies = [
  {
    category: 'Computer Vision',
    items: [
      { name: 'MediaPipe Hands', description: 'Real-time hand landmark detection with 21 tracked points per hand' },
      { name: 'OpenCV', description: 'Camera capture, frame processing, and image transformation pipeline' },
      { name: 'Landmark Normalization', description: 'Palm-based scaling for distance-invariant feature extraction' },
    ],
  },
  {
    category: 'Recognition System',
    items: [
      { name: 'Geometric Features', description: 'Finger extension, spread, thumb angle, and curl measurements' },
      { name: 'Euclidean Distance', description: 'Normalized distance comparison for gesture matching' },
      { name: 'Temporal Filtering', description: 'Multi-frame consistency validation to reduce false positives' },
    ],
  },
  {
    category: 'System Integration',
    items: [
      { name: 'PyAutoGUI', description: 'Cross-platform system automation for action execution' },
      { name: 'JSON Configuration', description: 'Persistent gesture mappings and user preferences' },
      { name: 'Resource Management', description: 'Context managers for camera acquisition and cleanup' },
    ],
  },
  {
    category: 'Stabilization',
    items: [
      { name: 'Confidence Thresholds', description: 'Minimum confidence requirements for gesture validation' },
      { name: 'Dwell-Time Activation', description: 'Sustained gesture requirements prevent accidental triggers' },
      { name: 'Debounce Logic', description: 'Cooldown periods between successive action executions' },
    ],
  },
];

export default function TechStack() {
  return (
    <section className="relative py-24 px-6 bg-[#0f1419] overflow-x-hidden">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16 px-4"
        >
          <h2 className="text-3xl md:text-4xl font-light mb-4">
            Built on <span className="gradient-text">Proven Technology</span>
          </h2>
          <p className="text-neutral-400 text-sm max-w-2xl mx-auto">
            Established libraries and frameworks provide reliable hand tracking and system automation
          </p>
        </motion.div>

        {/* Tech Grid */}
        <div className="grid md:grid-cols-2 gap-8">
          {technologies.map((tech, catIndex) => (
            <motion.div
              key={catIndex}
              initial={{ opacity: 0, x: catIndex % 2 === 0 ? -30 : 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: catIndex * 0.1 }}
              className="glass-panel p-6 rounded-lg"
            >
              <h3 className="text-lg font-medium text-gestura-cyan mb-4">{tech.category}</h3>
              <div className="space-y-4">
                {tech.items.map((item, itemIndex) => (
                  <div key={itemIndex} className="border-l-2 border-white/10 pl-4 hover:border-gestura-cyan/50 transition-colors">
                    <div className="text-sm font-medium text-white mb-1">{item.name}</div>
                    <p className="text-xs text-neutral-500 leading-relaxed">{item.description}</p>
                  </div>
                ))}
              </div>
            </motion.div>
          ))}
        </div>

        {/* Open Source Note */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16 text-center"
        >
          <p className="text-neutral-500 text-sm mb-4">
            Built with open-source technologies, designed for privacy
          </p>
          <div className="flex justify-center gap-4 flex-wrap">
            {techBadges.map((tech, i) => (
              <a
                key={i}
                href={tech.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group px-4 py-2 text-xs bg-white/5 border border-white/10 rounded-full text-neutral-400 hover:text-white hover:bg-white/10 hover:border-gestura-cyan/50 hover:shadow-lg hover:shadow-gestura-cyan/10 transition-all duration-200 cursor-pointer"
              >
                {tech.name}
              </a>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
