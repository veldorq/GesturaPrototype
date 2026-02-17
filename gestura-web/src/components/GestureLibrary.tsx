"use client";

import { motion } from "framer-motion";
import { useState } from "react";

interface Gesture {
  name: string;
  action: string;
  handPose: string;
  category: string;
  debounce: string;
}

const gestures: Gesture[] = [
  {
    name: "Open Palm",
    action: "Scroll Down",
    handPose: "All 5 fingers spread apart",
    category: "Scrolling",
    debounce: "400ms hold"
  },
  {
    name: "Closed Fist",
    action: "Scroll Up",
    handPose: "All fingers folded into palm",
    category: "Scrolling",
    debounce: "400ms hold"
  },
  {
    name: "Index Only",
    action: "Mouse Move",
    handPose: "Index finger extended, others folded",
    category: "Pointing",
    debounce: "Real-time"
  },
  {
    name: "Peace Sign",
    action: "Left Click",
    handPose: "Index + middle fingers extended",
    category: "Clicking",
    debounce: "500ms"
  },
  {
    name: "Three Fingers",
    action: "Left Click (Alt)",
    handPose: "Index, middle, ring extended",
    category: "Clicking",
    debounce: "500ms"
  },
  {
    name: "Swipe Left",
    action: "Browser Back",
    handPose: "Hand motion to the left",
    category: "Navigation",
    debounce: "800ms"
  },
  {
    name: "Swipe Right",
    action: "Browser Forward",
    handPose: "Hand motion to the right",
    category: "Navigation",
    debounce: "800ms"
  },
  {
    name: "Thumb Up",
    action: "Zoom In",
    handPose: "Thumb extended upward, fingers folded",
    category: "Zoom",
    debounce: "600ms"
  },
  {
    name: "Four Fingers",
    action: "Refresh Page",
    handPose: "4 fingers extended, thumb tucked",
    category: "Page Actions",
    debounce: "800ms"
  },
  {
    name: "Pinky Only",
    action: "Mute/Unmute",
    handPose: "Only pinky finger extended",
    category: "Accessibility",
    debounce: "600ms"
  },
  {
    name: "Rock Sign",
    action: "Exit Program",
    handPose: "Index + pinky extended (hold 1.5s)",
    category: "System",
    debounce: "1500ms hold"
  }
];

const GestureIcon = ({ name }: { name: string }) => {
  const iconClass = "w-[18px] h-[18px] text-zinc-400 group-hover:text-[#6C63FF] transition-all duration-200 group-hover:scale-110 flex-shrink-0";
  
  switch (name) {
    case "Open Palm":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M19 14l-7 7m0 0l-7-7m7 7V3" />
        </svg>
      );
    case "Closed Fist":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M5 10l7-7m0 0l7 7m-7-7v18" />
        </svg>
      );
    case "Index Only":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
        </svg>
      );
    case "Peace Sign":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5" />
        </svg>
      );
    case "Three Fingers":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7 11.5V14m0-2.5v-6a1.5 1.5 0 113 0m-3 6a1.5 1.5 0 00-3 0v2a7.5 7.5 0 0015 0v-5a1.5 1.5 0 00-3 0m-6-3V11m0-5.5v-1a1.5 1.5 0 013 0v1m0 0V11m0-5.5a1.5 1.5 0 013 0v3m0 0V11" />
        </svg>
      );
    case "Swipe Left":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
      );
    case "Swipe Right":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      );
    case "Thumb Up":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM13 10h-.01" />
        </svg>
      );
    case "Four Fingers":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
        </svg>
      );
    case "Pinky Only":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2" />
        </svg>
      );
    case "Rock Sign":
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
        </svg>
      );
    default:
      return (
        <svg className={iconClass} fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M7 11.5V14m0-2.5v-6a1.5 1.5 0 113 0m-3 6a1.5 1.5 0 00-3 0v2a7.5 7.5 0 0015 0v-5a1.5 1.5 0 00-3 0m-6-3V11m0-5.5v-1a1.5 1.5 0 013 0v1m0 0V11m0-5.5a1.5 1.5 0 013 0v3m0 0V11" />
        </svg>
      );
  }
};

const categories = ["All", "Scrolling", "Pointing", "Clicking", "Navigation", "Zoom", "Page Actions", "Accessibility", "System"];

export default function GestureLibrary() {
  const [selectedCategory, setSelectedCategory] = useState<string>("All");
  
  // Filter gestures based on selected category
  const filteredGestures = selectedCategory === "All" 
    ? gestures 
    : gestures.filter(gesture => gesture.category === selectedCategory);
  
  return (
    <section className="relative py-32 px-6 bg-[#0B0B0F] overflow-x-hidden">
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

              {/* Gesture name with icon */}
              <div className="flex items-center gap-2 mb-3">
                <GestureIcon name={gesture.name} />
                <h3 className="text-xl font-bold text-white">
                  {gesture.name}
                </h3>
              </div>

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
            <svg className="w-6 h-6 text-purple-400 flex-shrink-0 mt-1" fill="none" stroke="currentColor" strokeWidth="1.75" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
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
