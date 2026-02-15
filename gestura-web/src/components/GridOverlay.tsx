'use client';

export default function GridOverlay() {
  return (
    <div
      className="fixed inset-0 pointer-events-none z-0 opacity-30"
      style={{
        backgroundImage: `
          linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
          linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px)
        `,
        backgroundSize: '100px 100px',
      }}
    />
  );
}
