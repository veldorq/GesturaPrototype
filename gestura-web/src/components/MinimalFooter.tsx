'use client';

import { motion } from 'framer-motion';

export default function MinimalFooter() {
  return (
    <footer className="relative py-16 px-6 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center gap-8">
          {/* Logo */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-2xl font-light tracking-tight"
          >
            Gestura
          </motion.div>

          {/* Links */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.1 }}
            className="flex gap-8 text-sm text-neutral-500"
          >
            <a href="/download" className="hover:text-white transition-colors">
              Download
            </a>
            <a href="/dashboard" className="hover:text-white transition-colors">
              Demo
            </a>
            <a href="#features" className="hover:text-white transition-colors">
              Features
            </a>
          </motion.div>

          {/* Copyright */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ delay: 0.2 }}
            className="text-sm text-neutral-600 font-light"
          >
            © 2026 Gestura
          </motion.div>
        </div>

        {/* Tagline */}
        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ delay: 0.3 }}
          className="mt-8 text-center text-xs text-neutral-600 tracking-[0.3em] uppercase"
        >
          Hands Speak. System Listens.
        </motion.div>
      </div>
    </footer>
  );
}
