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
          // Accent Colors
          'purple': '#6C63FF',        // Primary accent - refined purple
          'cyan': '#00D9FF',          // Secondary accent - cyan
          
          // Background Colors
          'navy-dark': '#0B0B0F',     // Primary background - deep blue-black
          'navy': '#111827',          // Secondary background - blue-gray
          'navy-light': '#1F2937',    // Tertiary background - lighter blue-gray
          
          // Text Colors
          'text-primary': '#FFFFFF',  // Primary text - pure white
          'text-secondary': '#9CA3AF', // Secondary text - refined gray
          'text-muted': '#6B7280',    // Muted text - subtle gray
          
          // Legacy accent colors (preserved for compatibility)
          'accent-teal': '#4F9C8F',
          'accent-gold': '#D4A574',
        },
      },
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
        'space': ['Space Grotesk', 'sans-serif'], // Display font for headings
        'jp': ['Noto Serif JP', 'serif'], // Japanese aesthetic font
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
          '0%': { 'box-shadow': '0 0 20px rgba(108, 99, 255, 0.3)' },
          '100%': { 'box-shadow': '0 0 40px rgba(108, 99, 255, 0.6)' },
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
