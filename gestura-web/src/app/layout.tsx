import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

// Only load Inter font - primary font
const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
  preload: true,
  fallback: ['system-ui', 'arial'],
});

export const metadata: Metadata = {
  title: 'Gestura | Hands Speak. System Listens.',
  description: 'Revolutionary hand gesture control system. Control your computer with natural hand movements using AI-powered gesture recognition.',
  keywords: ['gesture control', 'hand tracking', 'AI', 'accessibility', 'touchless control'],
  authors: [{ name: 'Souvik' }],
  openGraph: {
    title: 'Gestura | Revolutionary Gesture Control',
    description: 'Control your computer with natural hand movements',
    type: 'website',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export const viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 5,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={inter.variable}>
      <body className="overflow-x-hidden">{children}</body>
    </html>
  );
}
