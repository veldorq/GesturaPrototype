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
            {/* Broken chain/connection */}
            <path
              d="M10 13L14 17M14 7L10 11"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <path
              d="M9 7C9 5.34315 10.3431 4 12 4C13.6569 4 15 5.34315 15 7"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <path
              d="M15 17C15 18.6569 13.6569 20 12 20C10.3431 20 9 18.6569 9 17"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              opacity="0.3"
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
            {/* Lightning bolt with X - representing strain/damage */}
            <path
              d="M13 3L8 12H12L11 21L16 12H12L13 3Z"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M17 7L19 9M19 7L17 9"
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
            {/* Block/barrier symbol */}
            <circle
              cx="12"
              cy="12"
              r="10"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
            <path
              d="M6 6L18 18"
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
            {/* Premium triangle alert */}
            <path
              d="M12 9V13M12 17H12.01"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M10.29 3.86L1.82 18C1.64537 18.3024 1.55296 18.6453 1.55199 18.9945C1.55101 19.3437 1.64151 19.6871 1.81445 19.9905C1.98738 20.2939 2.23675 20.5467 2.53773 20.7239C2.83871 20.901 3.18082 20.9962 3.53 21H20.47C20.8192 20.9962 21.1613 20.901 21.4623 20.7239C21.7633 20.5467 22.0126 20.2939 22.1856 19.9905C22.3585 19.6871 22.449 19.3437 22.448 18.9945C22.447 18.6453 22.3546 18.3024 22.18 18L13.71 3.86C13.5317 3.56611 13.2807 3.32312 12.9812 3.15448C12.6817 2.98585 12.3437 2.89725 12 2.89725C11.6563 2.89725 11.3183 2.98585 11.0188 3.15448C10.7193 3.32312 10.4683 3.56611 10.29 3.86Z"
              stroke="url(#problem-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
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
