"use client";

import { motion } from "framer-motion";

const specs = [
  {
    metric: "Frame Rate",
    value: "30 FPS",
    detail: "Real-time processing at 30 frames per second with adaptive throttling",
    icon: "🎯"
  },
  {
    metric: "Detection Confidence",
    value: "70%",
    detail: "MediaPipe hand detection threshold - reduces false positives",
    icon: "🔍"
  },
  {
    metric: "Tracking Confidence",
    value: "70%",
    detail: "Continuous hand tracking threshold for stable frame-to-frame recognition",
    icon: "📍"
  },
  {
    metric: "Gesture Confidence",
    value: "75%",
    detail: "CNN prediction threshold - only high-confidence gestures trigger actions",
    icon: "🤖"
  },
  {
    metric: "Buffer Size",
    value: "5 Frames",
    detail: "Gesture stabilization buffer - prevents accidental triggers",
    icon: "🛡️"
  },
  {
    metric: "Debounce Time",
    value: "400ms",
    detail: "Cooldown between repeated actions - prevents double-triggering",
    icon: "⏱️"
  },
  {
    metric: "Mouse Smoothing",
    value: "0.35",
    detail: "Exponential smoothing factor (0=instant, 1=no movement) for silky pointer control",
    icon: "✨"
  },
  {
    metric: "Resolution",
    value: "1280×720",
    detail: "Camera capture resolution optimized for detection accuracy and performance",
    icon: "📹"
  },
  {
    metric: "Dead Zone",
    value: "0.4%",
    detail: "Minimum movement threshold to ignore micro-jitter and hand tremors",
    icon: "🎚️"
  },
  {
    metric: "Latency",
    value: "<33ms",
    detail: "End-to-end processing time per frame (30 FPS = 33ms frame budget)",
    icon: "⚡"
  }
];

export default function TechnicalSpecs() {
  return (
    <section className="relative py-32 px-6 bg-[#0f1419] overflow-x-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-radial from-cyan-900/10 via-transparent to-transparent opacity-30 pointer-events-none" />
      
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

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <div className="text-center mb-16 px-4">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
            Technical Specifications
          </h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Real performance metrics from the PROTOTYPE.PY configuration. No marketing fluff—just the actual numbers running in production.
          </p>
        </div>

        {/* Specs Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {specs.map((spec, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 1 }}
              animate={{ opacity: 1 }}
              className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-colors duration-300 will-change-transform"
              style={{ 
                transform: 'translateZ(0)',
                backfaceVisibility: 'hidden',
                WebkitBackfaceVisibility: 'hidden'
              }}
            >
              {/* Icon */}
              <div className="text-4xl mb-4">{spec.icon}</div>
              
              {/* Metric name */}
              <div className="text-sm text-neutral-500 uppercase tracking-wider mb-2">
                {spec.metric}
              </div>
              
              {/* Value */}
              <div className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-purple-400 mb-3 py-1 leading-relaxed">
                {spec.value}
              </div>
              
              {/* Detail */}
              <p className="text-sm text-neutral-400 leading-relaxed">
                {spec.detail}
              </p>

              {/* Hover gradient */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-cyan-500/5 to-purple-500/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
            </motion.div>
          ))}
        </div>

        {/* Bottom note */}
        <div className="mt-12 p-6 border border-cyan-500/20 rounded-2xl bg-cyan-500/5 backdrop-blur-sm">
          <p className="text-neutral-300 text-center">
            <span className="text-cyan-400 font-semibold">Developer Note:</span> These values are tuned for <span className="text-white font-medium">hackathon-stable reliability</span>. They prioritize consistent recognition over maximum speed, preventing false triggers during demos and daily use.
          </p>
        </div>
      </div>
    </section>
  );
}
