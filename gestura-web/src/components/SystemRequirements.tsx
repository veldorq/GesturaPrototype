"use client";

import { motion } from "framer-motion";

const requirements = {
  minimum: [
    { item: "OS", value: "Windows 10/11, macOS, or Linux" },
    { item: "Python", value: "3.10 or higher" },
    { item: "Webcam", value: "Any standard webcam (built-in or USB)" },
    { item: "Storage", value: "Minimal space for dependencies" },
    { item: "Internet", value: "Required for initial setup only" }
  ],
  recommended: [
    { item: "OS", value: "Windows 11 or macOS latest" },
    { item: "Python", value: "3.10+ with pip installed" },
    { item: "RAM", value: "4 GB or more available" },
    { item: "Lighting", value: "Consistent front-facing light source" },
    { item: "Environment", value: "Minimal hand-like shapes in background" }
  ]
};

const dependencies = [
  {
    name: "Python",
    version: "3.10+",
    purpose: "Core runtime environment for the application",
    icon: "🐍"
  },
  {
    name: "OpenCV",
    version: "4.x",
    purpose: "Camera capture and image processing operations",
    icon: "📷"
  },
  {
    name: "MediaPipe",
    version: "Latest",
    purpose: "Hand landmark detection and tracking (21 landmarks)",
    icon: "🖐️"  },
  {
    name: "PyAutoGUI",
    version: "Latest",
    purpose: "Cross-platform GUI automation for action execution",
    icon: "⌨️"
  },
  {
    name: "NumPy",
    version: "Latest",
    purpose: "Numerical operations for feature extraction",
    icon: "🔢"
  }
];

export default function SystemRequirements() {
  return (
    <section className="relative py-32 px-6 bg-[#0f1419] overflow-x-hidden">
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
          className="text-center mb-16 px-4"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
            💻 System Requirements
          </h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Gestura requires Python 3.10+ and a working webcam. Compatible with Windows, macOS, and Linux.
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
              Basic requirements to run Gestura. Functional for testing and limited use.
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
              Optimal conditions for reliable recognition and consistent performance.
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
