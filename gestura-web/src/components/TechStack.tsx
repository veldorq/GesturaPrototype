'use client';

import { motion } from 'framer-motion';

const technologies = [
  {
    category: 'Computer Vision',
    items: [
      { name: 'MediaPipe', description: 'Real-time hand tracking with 21 landmarks per hand' },
      { name: 'OpenCV', description: 'Image processing and transformation pipeline' },
      { name: 'TensorFlow Lite', description: 'Lightweight ML inference on edge devices' },
    ],
  },
  {
    category: 'Machine Learning',
    items: [
      { name: 'CNN Architecture', description: 'Custom convolutional neural network for gesture classification' },
      { name: 'Data Augmentation', description: 'Robust training with rotation, scaling, and noise injection' },
      { name: 'Transfer Learning', description: 'Fine-tuned models for specific gesture recognition' },
    ],
  },
  {
    category: 'System Integration',
    items: [
      { name: 'PyAutoGUI', description: 'Cross-platform system control and automation' },
      { name: 'Threading', description: 'Parallel processing for camera, inference, and actions' },
      { name: 'Kalman Filtering', description: 'Smooth motion prediction and noise reduction' },
    ],
  },
  {
    category: 'Performance',
    items: [
      { name: 'WebAssembly', description: 'Near-native speed in browser environments' },
      { name: 'GPU Acceleration', description: 'Hardware-accelerated neural network inference' },
      { name: 'Frame Skipping', description: 'Intelligent processing to maintain 30 FPS' },
    ],
  },
];

export default function TechStack() {
  return (
    <section className="relative py-24 px-6 bg-[#151515] overflow-x-hidden">
      <div className="max-w-7xl mx-auto relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mb-16 px-4"
        >
          <h2 className="text-3xl md:text-4xl font-light mb-4">
            Built on <span className="gradient-text">Modern Technology</span>
          </h2>
          <p className="text-neutral-400 text-sm max-w-2xl mx-auto">
            Industry-leading tools and frameworks power Gestura's gesture recognition
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
            {['Python 3.11', 'MediaPipe 0.10', 'TensorFlow 2.x', 'OpenCV 4.x'].map((tech, i) => (
              <span
                key={i}
                className="px-4 py-2 text-xs bg-white/5 border border-white/10 rounded-full text-neutral-400"
              >
                {tech}
              </span>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
