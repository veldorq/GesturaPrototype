interface SolutionIconProps {
  size?: number;
  className?: string;
  type?: 'lightning' | 'target' | 'hand' | 'accessibility';
}

export default function SolutionIcon({ 
  size = 24, 
  className = '',
  type = 'lightning'
}: SolutionIconProps) {
  const renderIcon = () => {
    switch (type) {
      case 'lightning':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`transition-all duration-300 ${className}`}
          >
            <path
              d="M13 2L3 14H12L11 22L21 10H12L13 2Z"
              stroke="url(#solution-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
              fill="url(#solution-gradient-fill)"
              fillOpacity="0.1"
            />
            <defs>
              <linearGradient id="solution-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D9FF" />
                <stop offset="100%" stopColor="#0099CC" />
              </linearGradient>
              <linearGradient id="solution-gradient-fill" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D9FF" />
                <stop offset="100%" stopColor="#0099CC" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'target':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`transition-all duration-300 ${className}`}
          >
            <circle cx="12" cy="12" r="10" stroke="url(#solution-gradient)" strokeWidth="1.5" />
            <circle cx="12" cy="12" r="6" stroke="url(#solution-gradient)" strokeWidth="1.5" />
            <circle cx="12" cy="12" r="2" fill="url(#solution-gradient)" />
            <defs>
              <linearGradient id="solution-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D9FF" />
                <stop offset="100%" stopColor="#0099CC" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'hand':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`transition-all duration-300 ${className}`}
          >
            <path
              d="M13 4.5C13 3.67 13.67 3 14.5 3C15.33 3 16 3.67 16 4.5V10M16 4.5C16 3.67 16.67 3 17.5 3C18.33 3 19 3.67 19 4.5V10M19 10V8.5C19 7.67 19.67 7 20.5 7C21.33 7 22 7.67 22 8.5V15C22 18.87 18.87 22 15 22H14C10.69 22 8 19.31 8 16V10C8 9.17 8.67 8.5 9.5 8.5C10.33 8.5 11 9.17 11 10V4.5C11 3.67 11.67 3 12.5 3C13.33 3 14 3.67 14 4.5"
              stroke="url(#solution-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <defs>
              <linearGradient id="solution-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D9FF" />
                <stop offset="100%" stopColor="#0099CC" />
              </linearGradient>
            </defs>
          </svg>
        );
      
      case 'accessibility':
        return (
          <svg
            width={size}
            height={size}
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className={`transition-all duration-300 ${className}`}
          >
            <circle cx="12" cy="5" r="2" fill="url(#solution-gradient)" />
            <path
              d="M4 10H20M12 10V20M12 20L8 16M12 20L16 16"
              stroke="url(#solution-gradient)"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <defs>
              <linearGradient id="solution-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#00D9FF" />
                <stop offset="100%" stopColor="#0099CC" />
              </linearGradient>
            </defs>
          </svg>
        );
    }
  };

  return (
    <div className="relative inline-flex items-center justify-center">
      {renderIcon()}
    </div>
  );
}
