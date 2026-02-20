'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

interface DownloadOption {
  os: string;
  icon: string;
  filename: string;
  size: string;
  downloadUrl: string;
  instructions: string[];
}

export default function DownloadButtons() {
  const [detectedOS, setDetectedOS] = useState<string>('windows');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
    // Detect user's operating system
    const userAgent = window.navigator.userAgent.toLowerCase();
    if (userAgent.includes('mac')) {
      setDetectedOS('macos');
    } else if (userAgent.includes('linux')) {
      setDetectedOS('linux');
    } else {
      setDetectedOS('windows');
    }
  }, []);

  const REPO_URL = 'https://github.com/veldorq/GesturaPrototype';
  const LATEST_RELEASE = `${REPO_URL}/releases/latest/download`;
  
  // UPDATE THIS LINK after building and uploading your file!
  // Instructions: Run BUILD_AND_SHARE.bat, upload to Google Drive/Dropbox,
  // then paste the direct download link here
  const CUSTOM_DOWNLOAD_URL = ''; // Example: 'https://drive.google.com/uc?export=download&id=YOUR_FILE_ID'
  
  // If you have a custom download link, use it. Otherwise, fall back to GitHub releases.
  const USE_CUSTOM_DOWNLOAD = CUSTOM_DOWNLOAD_URL.length > 0;

  const downloadOptions: DownloadOption[] = [
    {
      os: 'windows',
      icon: '🪟',
      filename: 'Gestura-Windows-x64.zip',
      size: '~85 MB',
      downloadUrl: USE_CUSTOM_DOWNLOAD 
        ? CUSTOM_DOWNLOAD_URL
        : `${LATEST_RELEASE}/Gestura-Windows-x64.zip`,
      instructions: [
        'Extract the ZIP file',
        'Run Gestura.exe',
        'Allow camera permissions',
        'Start using gestures!'
      ]
    },
    {
      os: 'macos',
      icon: '🍎',
      filename: 'Gestura-macOS-x64.zip',
      size: '~90 MB',
      downloadUrl: USE_CUSTOM_DOWNLOAD
        ? CUSTOM_DOWNLOAD_URL
        : `${LATEST_RELEASE}/Gestura-macOS-x64.zip`,
      instructions: [
        'Extract the ZIP file',
        'Right-click Gestura → Open',
        'Allow camera permissions',
        'Start using gestures!'
      ]
    },
    {
      os: 'linux',
      icon: '🐧',
      filename: 'Gestura-Linux-x64.zip',
      size: '~80 MB',
      downloadUrl: USE_CUSTOM_DOWNLOAD
        ? CUSTOM_DOWNLOAD_URL
        : `${LATEST_RELEASE}/Gestura-Linux-x64.zip`,
      instructions: [
        'Extract: unzip Gestura-Linux-x64.zip',
        'Make executable: chmod +x Gestura',
        'Run: ./Gestura',
        'Start using gestures!'
      ]
    }
  ];

  const recommendedOption = downloadOptions.find(opt => opt.os === detectedOS) || downloadOptions[0];
  const otherOptions = downloadOptions.filter(opt => opt.os !== detectedOS);

  if (!isClient) {
    // Server-side render fallback - show generic download button
    return (
      <div className="flex flex-col items-center gap-4">
        <a
          href={CUSTOM_DOWNLOAD_URL || `${REPO_URL}/releases/latest`}
          className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-400 to-purple-400 text-white hover:scale-105 transition-all duration-300 rounded-full font-semibold tracking-wide cursor-pointer shadow-2xl shadow-cyan-400/30"
        >
          Download Gestura
        </a>
        <p className="text-xs text-neutral-500">
          Windows, macOS, Linux • Free & Open Source
        </p>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      {/* Recommended Download */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-12"
      >
        <div className="text-center mb-6">
          <div className="inline-block px-4 py-2 bg-gestura-cyan/10 backdrop-blur-sm border border-gestura-cyan/30 rounded-full mb-4">
            <span className="text-gestura-cyan text-xs font-semibold uppercase tracking-widest">
              Recommended for you
            </span>
          </div>
        </div>

        <div className="relative border-2 border-gestura-cyan/50 rounded-3xl p-8 backdrop-blur-sm bg-neutral-900/50 hover:border-gestura-cyan transition-all duration-300">
          {/* Glow effect */}
          <div className="absolute inset-0 rounded-3xl bg-gradient-to-br from-cyan-500/10 to-purple-500/10 opacity-50 pointer-events-none" />
          
          <div className="relative">
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
              <div className="flex-1 text-center md:text-left">
                <div className="text-6xl mb-4">{recommendedOption.icon}</div>
                <h3 className="text-3xl font-bold mb-2 capitalize">
                  {recommendedOption.os === 'macos' ? 'macOS' : recommendedOption.os}
                </h3>
                <p className="text-neutral-400 mb-4">{recommendedOption.filename}</p>
                <p className="text-sm text-neutral-500">{recommendedOption.size}</p>
              </div>

              <div className="flex-shrink-0">
                <a
                  href={recommendedOption.downloadUrl}
                  className="inline-block px-12 py-5 bg-gradient-to-r from-cyan-400 to-purple-400 text-white hover:scale-105 transition-all duration-300 rounded-full font-semibold tracking-wide cursor-pointer shadow-2xl shadow-cyan-400/30"
                >
                  Download Now
                </a>
              </div>
            </div>

            {/* Quick Instructions */}
            <div className="mt-8 pt-8 border-t border-neutral-800">
              <h4 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider mb-4">
                Quick Installation:
              </h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {recommendedOption.instructions.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-2">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-gestura-cyan/20 text-gestura-cyan text-xs flex items-center justify-center font-bold">
                      {idx + 1}
                    </span>
                    <span className="text-sm text-neutral-400">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Other Platforms */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <h3 className="text-xl font-semibold text-center mb-6 text-neutral-400">
          Other Platforms
        </h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          {otherOptions.map((option) => (
            <div
              key={option.os}
              className="border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30 hover:border-neutral-700 transition-all duration-300 hover:scale-105"
            >
              <div className="text-center">
                <div className="text-4xl mb-3">{option.icon}</div>
                <h4 className="text-xl font-semibold mb-2 capitalize">
                  {option.os === 'macos' ? 'macOS' : option.os}
                </h4>
                <p className="text-sm text-neutral-400 mb-4">{option.size}</p>
                <a
                  href={option.downloadUrl}
                  className="inline-block px-8 py-3 border border-gestura-cyan/30 text-gestura-cyan hover:bg-gestura-cyan/10 transition-all duration-300 rounded-full font-medium"
                >
                  Download
                </a>
              </div>
            </div>
          ))}
        </div>
      </motion.div>

      {/* Alternative: Source Code */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.4 }}
        className="mt-12 text-center"
      >
        <div className="inline-block border border-neutral-800 rounded-2xl p-6 backdrop-blur-sm bg-neutral-900/30">
          <p className="text-neutral-400 mb-4">
            <strong>For Developers:</strong> Build from source or contribute
          </p>
          <div className="flex flex-wrap justify-center gap-4">
            <a
              href={`${REPO_URL}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 border border-neutral-700 text-neutral-300 hover:border-white hover:text-white transition-all duration-300 rounded-full font-medium"
            >
              <span>📦</span>
              <span>View on GitHub</span>
            </a>
            <a
              href={`${REPO_URL}/releases`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 border border-neutral-700 text-neutral-300 hover:border-white hover:text-white transition-all duration-300 rounded-full font-medium"
            >
              <span>📋</span>
              <span>All Releases</span>
            </a>
          </div>
        </div>
      </motion.div>

      {/* Version Info */}
      <div className="mt-8 text-center">
        <p className="text-xs text-neutral-600">
          Latest Version: 1.0.0 • Released February 2026 • Free & Open Source
        </p>
        <p className="text-xs text-neutral-600 mt-2">
          Windows 10+, macOS 10.15+, Ubuntu 20.04+ • No internet required after installation
        </p>
      </div>
    </div>
  );
}
