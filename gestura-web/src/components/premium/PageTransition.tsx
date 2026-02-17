'use client';

import { useEffect, useState } from 'react';

export default function PageTransition() {
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    // Instant load - no artificial delay
    setLoaded(true);
  }, []);

  return (
    <div className={`page-transition ${loaded ? 'loaded' : ''}`}>
      <div className="loader" />
    </div>
  );
}
