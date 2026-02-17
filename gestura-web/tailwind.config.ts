import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        'gestura': {
          // Accent Colors - Refined Cyan Theme
          'cyan': '#22d3ee',          // Primary accent - bright cyan
          'blue': '#3b82f6',          // Secondary accent - blue
          'purple': '#6C63FF',        // Tertiary accent - purple (legacy)
          
          // Background Colors - Premium Dark Theme
          'navy-dark': '#0a0f1a',     // Primary background - darkest blue-black
          'navy': '#111827',          // Secondary background - dark blue-gray
          'navy-light': '#1f2937',    // Tertiary background - blue-gray
          
          // Text Colors - Refined Hierarchy
          'text-primary': '#f9fafb',  // Primary text - near white
          'text-secondary': '#9ca3af', // Secondary text - slate gray
          'text-tertiary': '#6b7280', // Tertiary text - medium gray
          'text-muted': '#4b5563',    // Muted text - dim gray
          
          // Legacy accent colors (preserved for compatibility)
          'accent-teal': '#4F9C8F',
          'accent-gold': '#D4A574',
        },
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'space': ['Space Grotesk', 'sans-serif'], // Display font for headings
      },
      fontSize: {
        // Fluid typography scale (mobile-first, responsive)
        'xs': ['clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem)', { lineHeight: '1.4' }],
        'sm': ['clamp(0.875rem, 0.8rem + 0.35vw, 1rem)', { lineHeight: '1.5' }],
        'base': ['clamp(1rem, 0.95rem + 0.5vw, 1.125rem)', { lineHeight: '1.6' }],
        'lg': ['clamp(1.125rem, 1rem + 0.75vw, 1.375rem)', { lineHeight: '1.6' }],
        'xl': ['clamp(1.5rem, 1.25rem + 1vw, 2rem)', { lineHeight: '1.4' }],
        '2xl': ['clamp(2rem, 1.5rem + 2vw, 3rem)', { lineHeight: '1.3' }],
        '3xl': ['clamp(3rem, 2rem + 3vw, 4.5rem)', { lineHeight: '1.2' }],
        '4xl': ['clamp(4rem, 3rem + 4vw, 6rem)', { lineHeight: '1.1' }],
        '5xl': ['clamp(6rem, 4rem + 6vw, 9rem)', { lineHeight: '1' }],
        '6xl': ['clamp(8rem, 5rem + 8vw, 12rem)', { lineHeight: '1' }],
      },
      animation: {
        'float': 'float 3s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'slide-up': 'slide-up 0.6s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' },
        },
        glow: {
          '0%': { 'box-shadow': '0 0 20px rgba(34, 211, 238, 0.3)' },
          '100%': { 'box-shadow': '0 0 40px rgba(34, 211, 238, 0.6)' },
        },
        'slide-up': {
          '0%': { opacity: '0', transform: 'translateY(30px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
      backdropBlur: {
        'xs': '2px',
      },
    },
  },
  plugins: [],
}

export default config
