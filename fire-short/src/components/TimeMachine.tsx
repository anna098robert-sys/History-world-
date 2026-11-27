import React from 'react';
import {useCurrentFrame} from 'remotion';

const INK = '#141414';

/** Handheld time machine with a glowing screen. */
export const TimeMachine: React.FC<{
  x: number;
  y: number;
  s?: number;
  rot?: number;
  power?: number; // 0..1 glow
  screen?: 'off' | 'boot' | 'pompeii';
}> = ({x, y, s = 1, rot = 0, power = 1, screen = 'pompeii'}) => {
  const f = useCurrentFrame();
  const blink = Math.floor(f / 6) % 2 === 0;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
      <circle r={260} fill="url(#machineGlow)" opacity={power} />
      <rect x={-170} y={-120} width={340} height={240} rx={34} fill="#3a3f4a" stroke={INK} strokeWidth={10} />
      <rect x={-150} y={-100} width={300} height={170} rx={16} fill={screen === 'off' ? '#10161a' : screen === 'pompeii' && blink ? '#3a0a08' : '#08241c'} stroke={INK} strokeWidth={6} />
      {screen === 'boot' && (
        <g>
          <rect x={-120} y={-20} width={240 * Math.min(1, (f % 40) / 30)} height={20} fill="#48ffb0" />
          <text x={0} y={-40} textAnchor="middle" fontFamily="monospace" fontWeight={700} fontSize={26} fill="#48ffb0">CALCULATING…</text>
        </g>
      )}
      {screen === 'pompeii' && (
        <g>
          <text x={0} y={-58} textAnchor="middle" fontFamily="monospace" fontWeight={700} fontSize={22} fill="#ff6b5a">DESTINATION:</text>
          <text x={0} y={-6} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={52} fill="#ffd400">POMPEII</text>
          <text x={0} y={46} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={40} fill="#ff6b5a">AD 79</text>
          {/* tiny volcano icon */}
          <g transform="translate(118 40) scale(0.5)">
            <path d="M-40 20 L-10 -30 L10 -30 L40 20 Z" fill="#7a4a2a" />
            <circle cx={0} cy={-44} r={14} fill={blink ? '#ff5a1a' : '#ffb347'} />
          </g>
        </g>
      )}
      {[-110, -55, 0, 55, 110].map((bx, i) => (
        <circle key={bx} cx={bx} cy={96} r={12} fill={i === 2 ? '#e2231a' : i % 2 ? '#48ffb0' : '#ffd400'} stroke={INK} strokeWidth={4} />
      ))}
      <line x1={120} y1={-120} x2={150} y2={-190} stroke={INK} strokeWidth={8} />
      <circle cx={150} cy={-196} r={12} fill={blink ? '#ff3b2a' : '#5a1a14'} stroke={INK} strokeWidth={4} />
    </g>
  );
};

/** Swirling time portal. */
export const Portal: React.FC<{x: number; y: number; open: number}> = ({x, y, open}) => {
  const f = useCurrentFrame();
  if (open <= 0) return null;
  return (
    <g transform={`translate(${x} ${y}) scale(${open})`}>
      <circle r={520} fill="url(#portalGlow)" />
      {new Array(9).fill(0).map((_, i) => (
        <ellipse
          key={i}
          rx={440 - i * 44}
          ry={(440 - i * 44) * 1.15}
          fill="none"
          stroke={i % 2 ? '#7af7ff' : '#c08bff'}
          strokeWidth={22 - i * 1.5}
          strokeDasharray={`${120 - i * 8} ${40 + i * 6}`}
          transform={`rotate(${f * (8 + i * 3) * (i % 2 ? -1 : 1)})`}
          opacity={0.9}
        />
      ))}
      <circle r={90} fill="#ffffff" />
    </g>
  );
};

export const MachineDefs: React.FC = () => (
  <defs>
    <radialGradient id="machineGlow">
      <stop offset="0%" stopColor="rgba(80,255,180,0.7)" />
      <stop offset="100%" stopColor="rgba(80,255,180,0)" />
    </radialGradient>
    <radialGradient id="portalGlow">
      <stop offset="0%" stopColor="rgba(255,255,255,1)" />
      <stop offset="30%" stopColor="rgba(140,230,255,0.9)" />
      <stop offset="70%" stopColor="rgba(150,90,255,0.5)" />
      <stop offset="100%" stopColor="rgba(120,60,255,0)" />
    </radialGradient>
  </defs>
);
