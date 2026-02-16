"use client";

import { motion } from "framer-motion";
import { useState } from "react";

interface Gesture {
  name: string;
  action: string;
  handPose: string;
  category: string;
  icon: string;
  debounce: string;
}

const gestures: Gesture[] = [
  {
    name: "Open Palm",
    action: "Scroll Down",
    handPose: "All 5 fingers spread apart",
    category: "Scrolling",
    icon: "✋",
    debounce: "400ms hold"
  },
  {
    name: "Closed Fist",
    action: "Scroll Up",
    handPose: "All fingers folded into palm",
    category: "Scrolling",
    icon: "✊",
    debounce: "400ms hold"
  },
  {
    name: "Index Only",
    action: "Mouse Move",
    handPose: "Index finger extended, others folded",
    category: "Pointing",
    icon: "☝️",
    debounce: "Real-time"
  },
  {
    name: "Peace Sign",
    action: "Left Click",
    handPose: "Index + middle fingers extended",
    category: "Clicking",
    icon: "✌️",
    debounce: "500ms"
  },
  {
    name: "Three Fingers",
    action: "Left Click (Alt)",
    handPose: "Index, middle, ring extended",
    category: "Clicking",
    icon: "🖖",
    debounce: "500ms"
  },
  {
    name: "Swipe Left",
    action: "Browser Back",
    handPose: "Hand motion to the left",
    category: "Navigation",
    icon: "👈",
    debounce: "800ms"
  },
  {
    name: "Swipe Right",
    action: "Browser Forward",
    handPose: "Hand motion to the right",
    category: "Navigation",
    icon: "👉",
    debounce: "800ms"
  },
  {
    name: "Thumb Up",
    action: "Zoom In",
    handPose: "Thumb extended upward, fingers folded",
    category: "Zoom",
    icon: "👍",
    debounce: "600ms"
  },
  {
    name: "Four Fingers",
    action: "Refresh Page",
    handPose: "4 fingers extended, thumb tucked",
    category: "Page Actions",
    icon: "🖐️",
    debounce: "800ms"
  },
  {
    name: "Pinky Only",
    action: "Mute/Unmute",
    handPose: "Only pinky finger extended",
    category: "Accessibility",
    icon: "🤙",
    debounce: "600ms"
  },
  {
    name: "Rock Sign",
    action: "Exit Program",
    handPose: "Index + pinky extended (hold 1.5s)",
    category: "System",
    icon: "🤘",
    debounce: "1500ms hold"
  }
];

const categories = ["All", "Scrolling", "Pointing", "Clicking", "Navigation", "Zoom", "Page Actions", "Accessibility", "System"];

export default function GestureLibrary() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  
  // Filter gestures based on selected category
  const filteredGestures = selectedCategory === "All" 
    ? gestures 
    : gestures.filter(gesture => gesture.category === selectedCategory);
  
  return (
    <section className="relative py-32 px-6 bg-[#0a0a0a] overflow-x-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-radial from-purple-900/10 via-transparent to-transparent opacity-20 pointer-events-none" />

      <div className="max-w-7xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 px-4"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-purple-200 to-cyan-300 bg-clip-text text-transparent py-2 leading-relaxed">
            Complete Gesture Library
          </h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto mb-8">
            {selectedCategory === "All" 
              ? "11 production-ready gestures covering all essential browser interactions. Each gesture has built-in debouncing to prevent accidental triggers."
              : `Showing ${filteredGestures.length} ${selectedCategory.toLowerCase()} gesture${filteredGestures.length !== 1 ? 's' : ''}. Click "All" to view all gestures.`
            }
          </p>
          
          {/* Category filters */}
          <div className="flex flex-wrap justify-center gap-3 mb-4">
            {categories.map((category, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-full text-xs font-medium border transition-all duration-300 cursor-pointer
                  ${selectedCategory === category 
                    ? 'border-cyan-500 bg-cyan-500/20 text-cyan-300 shadow-lg shadow-cyan-500/20' 
                    : 'border-neutral-700 bg-neutral-800/40 text-neutral-300 hover:border-cyan-500/50 hover:bg-neutral-800/60'
                  }`}
              >
                {category}
              </button>
            ))}
          </div>
        </motion.div>

        {/* Gesture Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {filteredGestures.map((gesture, index) => (
            <motion.div
              key={`${selectedCategory}-${gesture.name}`}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.4, delay: index * 0.05 }}
              className="group relative border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-purple-500/30 transition-all duration-300"
            >
              {/* Category badge */}
              <div className="absolute top-4 right-4 px-3 py-1 rounded-full text-xs font-medium bg-purple-500/10 text-purple-400 border border-purple-500/20">
                {gesture.category}
              </div>

              {/* Icon */}
              <div className="text-5xl mb-4">{gesture.icon}</div>

              {/* Gesture name */}
              <h3 className="text-xl font-bold text-white mb-2">
                {gesture.name}
              </h3>

              {/* Action */}
              <div className="flex items-center gap-2 mb-4">
                <span className="text-sm text-neutral-500">Action:</span>
                <span className="text-sm font-semibold text-cyan-400">
                  {gesture.action}
                </span>
              </div>

              {/* Hand pose */}
              <p className="text-sm text-neutral-400 mb-3 leading-relaxed">
                {gesture.handPose}
              </p>

              {/* Debounce info */}
              <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-neutral-800/50 border border-neutral-700/50">
                <svg className="w-4 h-4 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span className="text-xs text-neutral-400">{gesture.debounce}</span>
              </div>

              {/* Hover effect */}
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-purple-500/5 to-cyan-500/5 opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none" />
            </motion.div>
          ))}
        </div>

        {/* Implementation note */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.5 }}
          className="p-6 border border-purple-500/20 rounded-2xl bg-purple-500/5 backdrop-blur-sm"
        >
          <div className="flex items-start gap-4">
            <div className="text-3xl">🧠</div>
            <div>
              <h4 className="text-lg font-semibold text-white mb-2">
                Hybrid Recognition System
              </h4>
              <p className="text-neutral-300 leading-relaxed">
                Gestures are recognized using a hybrid approach: <span className="text-cyan-400 font-medium">MediaPipe Hands</span> tracks 21 hand landmarks in real-time, while a custom <span className="text-purple-400 font-medium">CNN (Convolutional Neural Network)</span> classifies complex gestures like swipes and scrolls. This two-stage pipeline achieves 99% accuracy by combining geometric rules with machine learning.
              </p>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
