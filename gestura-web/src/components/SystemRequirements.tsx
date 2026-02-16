"use client";

import { motion } from "framer-motion";

const requirements = {
  minimum: [
    { item: "OS", value: "Windows 10/11 (64-bit)" },
    { item: "CPU", value: "Dual-core 2.0 GHz" },
    { item: "RAM", value: "4 GB" },
    { item: "Webcam", value: "Any 720p camera (30 FPS)" },
    { item: "Storage", value: "500 MB available space" },
    { item: "Browser", value: "Chrome, Edge, Firefox (latest)" }
  ],
  recommended: [
    { item: "OS", value: "Windows 11 (64-bit)" },
    { item: "CPU", value: "Quad-core 3.0 GHz or better" },
    { item: "RAM", value: "8 GB or more" },
    { item: "Webcam", value: "1080p camera (60 FPS)" },
    { item: "Storage", value: "1 GB available space" },
    { item: "Environment", value: "Well-lit room (reduces detection errors)" }
  ]
};

const dependencies = [
  {
    name: "Python",
    version: "3.10+",
    purpose: "Runtime environment for desktop application",
    icon: "🐍"
  },
  {
    name: "OpenCV",
    version: "4.5+",
    purpose: "Computer vision and camera capture",
    icon: "📷"
  },
  {
    name: "MediaPipe",
    version: "0.10+",
    purpose: "Real-time hand tracking and landmark detection",
    icon: "✋"
  },
  {
    name: "PyAutoGUI",
    version: "0.9.54",
    purpose: "Cross-platform mouse and keyboard automation",
    icon: "⌨️"
  },
  {
    name: "TensorFlow Lite",
    version: "2.13+",
    purpose: "CNN gesture classification inference",
    icon: "🧠"
  },
  {
    name: "NumPy",
    version: "1.24+",
    purpose: "Numerical computations and array operations",
    icon: "🔢"
  }
];

export default function SystemRequirements() {
  return (
    <section className="relative py-32 px-6 bg-[#0a0a0a] overflow-hidden">
      {/* Grid background */}
      <div className="absolute inset-0 opacity-[0.02]">
        <div className="absolute inset-0" style={{
          backgroundImage: `
            linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)
          `,
          backgroundSize: '60px 60px'
        }} />
      </div>

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
            System Requirements
          </h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Gestura runs on modest hardware. No GPU required—everything runs on your CPU.
          </p>
        </motion.div>

        {/* Requirements comparison */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
          {/* Minimum Requirements */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="border border-neutral-800 rounded-2xl p-8 backdrop-blur-sm bg-neutral-900/30"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-3xl">💻</div>
              <h3 className="text-2xl font-bold text-white">Minimum</h3>
            </div>
            <p className="text-sm text-neutral-400 mb-6">
              Runs at 20-25 FPS on budget laptops. Functional for basic gestures.
            </p>
            <div className="space-y-3">
              {requirements.minimum.map((req, idx) => (
                <div key={idx} className="flex justify-between items-center py-2 border-b border-neutral-800/50 last:border-0">
                  <span className="text-neutral-400 text-sm">{req.item}</span>
                  <span className="text-white text-sm font-medium">{req.value}</span>
                </div>
              ))}
            </div>
          </motion.div>

          {/* Recommended Requirements */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="border border-cyan-500/30 rounded-2xl p-8 backdrop-blur-sm bg-gradient-to-br from-cyan-500/5 to-purple-500/5"
          >
            <div className="flex items-center gap-3 mb-6">
              <div className="text-3xl">🚀</div>
              <h3 className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 py-1 leading-relaxed">
                Recommended
              </h3>
            </div>
            <p className="text-sm text-neutral-300 mb-6">
              Smooth 30 FPS performance. Best experience for daily use.
            </p>
            <div className="space-y-3">
              {requirements.recommended.map((req, idx) => (
                <div key={idx} className="flex justify-between items-center py-2 border-b border-neutral-700/50 last:border-0">
                  <span className="text-neutral-300 text-sm">{req.item}</span>
                  <span className="text-cyan-300 text-sm font-medium">{req.value}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Dependencies section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <h3 className="text-3xl font-bold text-white text-center mb-3">
            Software Dependencies
          </h3>
          <p className="text-neutral-400 text-center mb-10">
            All dependencies are installed automatically via <code className="px-2 py-1 rounded bg-neutral-800 text-cyan-400 text-sm font-mono">requirements.txt</code>
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dependencies.map((dep, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: idx * 0.05 }}
                className="border border-neutral-800 rounded-xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-purple-500/30 transition-all duration-300"
              >
                <div className="text-4xl mb-3">{dep.icon}</div>
                <h4 className="text-lg font-semibold text-white mb-1">
                  {dep.name}
                </h4>
                <div className="text-sm text-cyan-400 font-mono mb-3">
                  {dep.version}
                </div>
                <p className="text-sm text-neutral-400 leading-relaxed">
                  {dep.purpose}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Installation command */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-12 p-6 border border-neutral-700 rounded-2xl bg-neutral-900/50 backdrop-blur-sm"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <h4 className="text-lg font-semibold text-white mb-2">
                One-Command Setup
              </h4>
              <p className="text-neutral-400 text-sm">
                Install all dependencies automatically using pip
              </p>
            </div>
            <div className="bg-black/50 px-4 py-3 rounded-lg border border-neutral-700 font-mono text-sm text-cyan-400 whitespace-nowrap">
              pip install -r requirements.txt
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
