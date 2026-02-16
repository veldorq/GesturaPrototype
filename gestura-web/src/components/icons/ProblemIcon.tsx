/**
 * PREMIUM PROBLEM ICON - PRODUCTION IMPLEMENTATION
 * Multiple icon types for different problem categories
 */

interface ProblemIconProps {
  size?: number;
  className?: string;
  glow?: boolean;
  type?: 'alert' | 'disconnect' | 'strain' | 'barrier';
}

export default function ProblemIcon({ 
  size = 24, 
  className = '',
  glow = false,
  type = 'alert'
}: ProblemIconProps) {
  
  const renderIcon = () => {
    switch (type) {
      case 'disconnect':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`relative z-10 transition-all duration-300 ease-out ${className}`}
          >
            {/* Broken link/connection with arrows showing interruption */}
            <path
              d="M8 16L4 12L8 8"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M16 8L20 12L16 16"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M9 12H11"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
            <path
              d="M13 12H15"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
            <line
              x1="11.5"
              y1="11.5"
              x2="12.5"
              y2="12.5"
              stroke="url(#problem-gradient)"
              strokeWidth="2"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="problem-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FF4D6D" />
                <stop offset="50%" stopColor="#FF5A77" />
                <stop offset="100%" stopColor="#FF6B6B" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'strain':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`relative z-10 transition-all duration-300 ease-out ${className}`}
          >
            {/* Hand with pain/strain indicator */}
            <path
              d="M13 5V10M16 5V10M19 8V15C19 18.31 16.31 21 13 21H12C9.79 21 7.96 19.5 7.37 17.45"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M10 5V11M7 8V16"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            {/* Pain indicator lines */}
            <path
              d="M4 16L3 18M6 16L5 18"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="problem-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FF4D6D" />
                <stop offset="50%" stopColor="#FF5A77" />
                <stop offset="100%" stopColor="#FF6B6B" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'barrier':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`relative z-10 transition-all duration-300 ease-out ${className}`}
          >
            {/* Lock with person silhouette - accessibility barrier */}
            <circle
              cx="12"
              cy="8"
              r="3"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
            />
            <path
              d="M7 20V18C7 15.7909 8.79086 14 11 14H13C15.2091 14 17 15.7909 17 18V20"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M6 14L18 20M18 14L6 20"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="problem-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FF4D6D" />
                <stop offset="50%" stopColor="#FF5A77" />
                <stop offset="100%" stopColor="#FF6B6B" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'alert':
      default:
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`relative z-10 transition-all duration-300 ease-out ${className}`}
          >
            {/* Anchor/chain - being tied down */}
            <circle
              cx="12"
              cy="13"
              r="4"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
            />
            <path
              d="M12 3V9M9 6H15"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M16 16.5L19 19.5M8 16.5L5 19.5"
              stroke="url(#problem-gradient)"
              strokeWidth="1.8"
              strokeLinecap="round"
            />
            <defs>
              <linearGradient id="problem-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FF4D6D" />
                <stop offset="50%" stopColor="#FF5A77" />
                <stop offset="100%" stopColor="#FF6B6B" />
              </linearGradient>
            </defs>
          </svg>
        );
    }
  };

  return (
    <div className="relative inline-flex items-center justify-center">
      {glow && (
        <div className="absolute inset-0 blur-md opacity-60 animate-pulse">
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="url(#problem-glow)"
              strokeWidth="2"
            />
            <defs>
              <linearGradient id="problem-glow" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#FF4D6D" />
                <stop offset="100%" stopColor="#FF6B6B" />
              </linearGradient>
            </defs>
          </svg>
        </div>
      )}
      {renderIcon()}
    </div>
  );
}
