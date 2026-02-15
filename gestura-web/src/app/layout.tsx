import type { Metadata } from 'next';
import { Inter, Playfair_Display } from 'next/font/google';
import './globals.css';

const inter = Inter({
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const playfair = Playfair_Display({
  subsets: ['latin'],
  variable: '--font-playfair',
  display: 'swap',
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
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${playfair.variable}`}>
      <body className="overflow-x-hidden">{children}</body>
    </html>
  );
}
