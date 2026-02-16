"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    question: "How long does it take to set up Gestura?",
    answer: "Less than 30 seconds. Just download the executable, grant camera permissions, and start waving. No installation wizards, no configuration files, no technical knowledge required."
  },
  {
    question: "Is my data being collected or sent anywhere?",
    answer: "Absolutely not. Gestura runs 100% locally on your computer. All hand tracking happens on your device using your CPU. No internet connection required after download, no data leaves your machine, no third-party servers involved."
  },
  {
    question: "What system requirements do I need?",
    answer: "Minimal requirements: Windows 10/11, any working webcam, and a dual-core CPU. Gestura is optimized to run at 30 FPS even on budget laptops. No GPU or fancy hardware needed."
  },
  {
    question: "Does Gestura work offline?",
    answer: "Yes! Once downloaded, Gestura works completely offline. It doesn't need internet connectivity to function. Perfect for presentations, private browsing, or air-gapped systems."
  },
  {
    question: "How accurate is the gesture recognition?",
    answer: "Gestura achieves 99% accuracy using a hybrid approach: MediaPipe for hand tracking + custom CNN trained on 100,000+ gesture samples. It adapts to different hand sizes, lighting conditions, and room setups."
  },
  {
    question: "Can I customize the gestures?",
    answer: "Not yet, but it's coming! The current version includes 11 pre-configured gestures optimized for web browsing. Future updates will add gesture remapping and custom action triggers."
  },
  {
    question: "Why isn't my camera working?",
    answer: "Common fixes: (1) Close other apps using your webcam (Zoom, Teams), (2) Check Windows Privacy Settings → Camera → Allow desktop apps, (3) Try restarting the application. Gestura includes automatic retry logic with detailed error messages."
  },
  {
    question: "Does it work with multiple monitors?",
    answer: "Yes! Gestura works seamlessly across multiple displays. Your hand movements control the cursor across all connected monitors, just like a traditional mouse."
  }
];

export default function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  const toggleFAQ = (index: number) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <section className="relative py-32 px-6 bg-[#0A0118] overflow-x-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-radial from-purple-900/10 via-transparent to-transparent opacity-30 pointer-events-none" />
      
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

      <div className="max-w-4xl mx-auto relative z-10">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16 px-4"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent py-2 leading-relaxed">
            Frequently Asked Questions
          </h2>
          <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
            Everything you need to know about Gestura. Can't find what you're looking for? Reach out on GitHub.
          </p>
        </motion.div>

        {/* FAQ Items */}
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.05 }}
              className="border border-neutral-800 rounded-2xl overflow-hidden backdrop-blur-sm bg-neutral-900/30 hover:border-cyan-500/30 transition-all duration-300"
            >
              {/* Question */}
              <button
                onClick={() => toggleFAQ(index)}
                className="w-full px-6 py-5 flex items-center justify-between text-left transition-colors duration-200 hover:bg-neutral-800/20"
              >
                <span className="text-lg font-semibold text-white pr-8">
                  {faq.question}
                </span>
                <motion.svg
                  animate={{ rotate: openIndex === index ? 180 : 0 }}
                  transition={{ duration: 0.3 }}
                  className="w-5 h-5 text-cyan-400 flex-shrink-0"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </motion.svg>
              </button>

              {/* Answer */}
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <div className="px-6 pb-5 pt-0">
                      <p className="text-neutral-300 leading-relaxed">
                        {faq.answer}
                      </p>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          ))}
        </div>

        {/* Bottom CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="mt-16 text-center"
        >
          <p className="text-neutral-400 mb-6">
            Still have questions?
          </p>
          <a
            href="https://github.com/veldorq/GesturaPrototype/issues"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full border border-cyan-500/30 text-cyan-400 hover:bg-cyan-500/10 hover:border-cyan-500/50 transition-all duration-300"
          >
            <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
            </svg>
            Open a GitHub Issue
          </a>
        </motion.div>
      </div>
    </section>
  );
}
