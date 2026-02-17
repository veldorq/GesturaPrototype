'use client';

import { useRef, useEffect, useState } from 'react';
import { motion, useScroll, useTransform, useSpring, useVelocity } from 'framer-motion';

const TOTAL_FRAMES = 120; // Adjust based on your frame count
const FRAME_PATH = '/frames'; // Folder containing frame_0.webp to frame_119.webp

export default function HeroCanvasAnimation() {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [images, setImages] = useState<HTMLImageElement[]>([]);
  const [imagesLoaded, setImagesLoaded] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);

  // Scroll progress tracking
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ['start start', 'end start']
  });

  // Smooth spring animation for buttery scroll
  const smoothProgress = useSpring(scrollYProgress, {
    stiffness: 100,
    damping: 30,
    restDelta: 0.001
  });

  // Anti-gravity effect based on scroll velocity
  const scrollVelocity = useVelocity(scrollYProgress);
  const yOffset = useTransform(
    scrollVelocity,
    [-1, 0, 1],
    [15, 0, -15] // Floats up when scrolling down
  );

  // Map scroll to frame index (bi-directional)
  const frameIndex = useTransform(
    smoothProgress,
    [0, 1],
    [0, TOTAL_FRAMES - 1]
  );

  // Preload all frames
  useEffect(() => {
    const loadImages = async () => {
      const imagePromises = Array.from({ length: TOTAL_FRAMES }, (_, i) => {
        return new Promise<HTMLImageElement>((resolve, reject) => {
          const img = new Image();
          img.src = `${FRAME_PATH}/frame_${i}.webp`;
          img.onload = () => {
            setLoadProgress((prev) => prev + (100 / TOTAL_FRAMES));
            resolve(img);
          };
          img.onerror = reject;
        });
      });

      const loadedImages = await Promise.all(imagePromises);
      setImages(loadedImages);
      setImagesLoaded(true);
    };

    loadImages();
  }, []);

  // Canvas rendering
  useEffect(() => {
    if (!imagesLoaded || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const renderFrame = () => {
      const currentFrame = Math.round(frameIndex.get());
      const img = images[Math.max(0, Math.min(currentFrame, TOTAL_FRAMES - 1))];

      if (img) {
        // Responsive canvas sizing
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Calculate scaling (contain fit)
        const scale = Math.min(
          canvas.width / img.width,
          canvas.height / img.height
        );
        const x = (canvas.width - img.width * scale) / 2;
        const y = (canvas.height - img.height * scale) / 2;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      }
    };

    const unsubscribe = frameIndex.on('change', renderFrame);
    renderFrame(); // Initial render

    // Handle window resize
    const handleResize = () => renderFrame();
    window.addEventListener('resize', handleResize);

    return () => {
      unsubscribe();
      window.removeEventListener('resize', handleResize);
    };
  }, [imagesLoaded, images, frameIndex]);

  // Text overlay animations
  const section1Opacity = useTransform(smoothProgress, [0, 0.1, 0.2, 0.25], [0, 1, 1, 0]);
  const section2Opacity = useTransform(smoothProgress, [0.3, 0.35, 0.5, 0.55], [0, 1, 1, 0]);
  const section3Opacity = useTransform(smoothProgress, [0.6, 0.65, 0.8, 0.85], [0, 1, 1, 0]);
  const section4Opacity = useTransform(smoothProgress, [0.9, 0.92, 0.98, 1], [0, 1, 1, 0]);
  const scrollIndicatorOpacity = useTransform(smoothProgress, [0, 0.1], [1, 0]);

  if (!imagesLoaded) {
    return (
      <div className="fixed inset-0 bg-[#0A0118] flex flex-col items-center justify-center z-50">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative mb-8"
        >
          {/* Logo/Icon Animation */}
          <div className="w-24 h-24 relative">
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ repeat: Infinity, duration: 2, ease: 'linear' }}
              className="absolute inset-0 border-4 border-gestura-cyan/30 border-t-gestura-cyan rounded-full"
            />
            <div className="absolute inset-0 flex items-center justify-center text-4xl">
              ✋
            </div>
          </div>
        </motion.div>

        <div className="w-80 h-3 bg-gestura-navy/50 rounded-full overflow-hidden mb-4">
          <motion.div
            className="h-full bg-gradient-to-r from-gestura-cyan via-gestura-purple to-gestura-cyan glow-cyan"
            initial={{ width: '0%' }}
            animate={{ width: `${loadProgress}%` }}
            transition={{ duration: 0.3 }}
          />
        </div>
        <p className="text-gestura-text-secondary text-lg font-inter">
          Loading Experience... {Math.round(loadProgress)}%
        </p>
      </div>
    );
  }

  return (
    <div ref={containerRef} className="relative h-[500vh]">
      <div className="sticky top-0 h-screen w-full overflow-hidden">
        <motion.div style={{ y: yOffset }} className="w-full h-full">
          <canvas
            ref={canvasRef}
            className="w-full h-full"
          />
        </motion.div>

        {/* Text Overlays */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center">
          {/* Section 1: Main Hero */}
          <motion.div
            style={{ opacity: section1Opacity }}
            className="absolute text-center px-4"
          >
            <h1 className="text-7xl md:text-9xl font-playfair font-bold gradient-text mb-6 tracking-tight">
              GESTURA
            </h1>
            <p className="text-2xl md:text-4xl text-gestura-text-primary font-inter font-light tracking-wide">
              Hands Speak. System Listens.
            </p>
          </motion.div>

          {/* Section 2: Experience */}
          <motion.div
            style={{ opacity: section2Opacity }}
            className="absolute text-left px-8 md:px-16 max-w-3xl"
          >
            <h2 className="text-6xl md:text-8xl font-playfair font-semibold text-gestura-text-primary mb-4">
              Natural Control
            </h2>
            <p className="text-xl md:text-2xl text-gestura-text-secondary font-inter">
              Command your computer with intuitive hand gestures — no touch required
            </p>
          </motion.div>

          {/* Section 3: Technology */}
          <motion.div
            style={{ opacity: section3Opacity }}
            className="absolute text-right px-8 md:px-16 max-w-3xl ml-auto"
          >
            <h2 className="text-6xl md:text-8xl font-playfair font-semibold gradient-text mb-4">
              AI-Powered
            </h2>
            <p className="text-xl md:text-2xl text-gestura-text-secondary font-inter">
              Real-time gesture recognition with &lt;30ms latency and 99% accuracy
            </p>
          </motion.div>

          {/* Section 4: CTA */}
          <motion.div
            style={{ opacity: section4Opacity }}
            className="absolute text-center px-4"
          >
            <h2 className="text-6xl md:text-9xl font-playfair font-bold text-gestura-text-primary mb-8">
              Experience the Future
            </h2>
            <motion.a
              href="#features"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="inline-block px-12 py-5 bg-gradient-to-r from-gestura-cyan to-gestura-purple text-white rounded-full text-xl font-semibold shadow-2xl glow-cyan pointer-events-auto transition-all"
            >
              Explore Features ↓
            </motion.a>
          </motion.div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          style={{ opacity: scrollIndicatorOpacity }}
          className="absolute bottom-12 left-1/2 -translate-x-1/2 flex flex-col items-center gap-3"
        >
          <p className="text-gestura-text-secondary text-sm font-inter tracking-widest uppercase">
            Scroll to Explore
          </p>
          <motion.div
            animate={{ y: [0, 10, 0] }}
            transition={{ repeat: Infinity, duration: 1.5 }}
            className="w-6 h-11 border-2 border-gestura-cyan/60 rounded-full flex items-start justify-center p-2"
          >
            <div className="w-1.5 h-3 bg-gestura-cyan rounded-full" />
          </motion.div>
        </motion.div>
      </div>
    </div>
  );
}
