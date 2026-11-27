import React from 'react';

const INK = '#141414';
const WRAP = '#e9dcbc';
const WRAP_D = '#c9b88f';

export type MummyProps = {
  x: number;
  y: number; // feet
  scale?: number;
  facing?: 1 | -1;
  /** 0..1 eye glow intensity */
  glow?: number;
  /** 0..1 how open the eyes are */
  eyesOpen?: number;
  armL?: number;
  armR?: number;
  legL?: number;
  legR?: number;
  bodyTilt?: number;
  headTilt?: number;
  /** 0 = lying, 1 = upright (rise from coffin) */
  frame?: number;
  mouth?: 'none' | 'groan' | 'talk' | 'polite';
  sweat?: boolean;
  /** hide legs (when inside sarcophagus) */
  noLegs?: boolean;
  /** knees-together "needs the bathroom" wiggle 0..1 */
  wiggle?: number;
};

const Bandages: React.FC<{w: number; h: number; seed: number}> = ({w, h, seed}) => {
  const lines = [];
  for (let i = 0; i < Math.floor(h / 22); i++) {
    const y = -h + 14 + i * 22;
    const tilt = ((i * 7 + seed) % 5) - 2;
    lines.push(
      <path
        key={i}
        d={`M${-w} ${y + tilt * 3} Q0 ${y - tilt * 2 + 6} ${w} ${y - tilt * 3}`}
        stroke={WRAP_D}
        strokeWidth={4}
        fill="none"
      />,
    );
  }
  return <>{lines}</>;
};

const Arm: React.FC<{x: number; y: number; angle: number}> = ({x, y, angle}) => (
  <g transform={`translate(${x} ${y}) rotate(${angle})`}>
    <rect x={-17} y={-6} width={34} height={118} rx={16} fill={WRAP} stroke={INK} strokeWidth={8} />
    <path d="M-15 30 L15 22 M-15 60 L15 52 M-15 88 L15 82" stroke={WRAP_D} strokeWidth={4} />
    {/* loose dangling bandage */}
    <path d="M12 96 Q30 120 18 146" stroke={WRAP} strokeWidth={9} fill="none" strokeLinecap="round" />
    <path d="M12 96 Q30 120 18 146" stroke={INK} strokeWidth={2} fill="none" strokeLinecap="round" opacity={0.5} />
  </g>
);

const Leg: React.FC<{x: number; y: number; angle: number}> = ({x, y, angle}) => (
  <g transform={`translate(${x} ${y}) rotate(${angle})`}>
    <rect x={-20} y={0} width={40} height={120} rx={16} fill={WRAP} stroke={INK} strokeWidth={8} />
    <path d="M-18 40 L18 32 M-18 80 L18 72" stroke={WRAP_D} strokeWidth={4} />
    <ellipse cx={10} cy={122} rx={28} ry={14} fill={WRAP} stroke={INK} strokeWidth={8} />
  </g>
);

export const Mummy: React.FC<MummyProps> = ({
  x,
  y,
  scale = 1,
  facing = 1,
  glow = 1,
  eyesOpen = 1,
  armL = -80,
  armR = -80,
  legL = 0,
  legR = 0,
  bodyTilt = 0,
  headTilt = 0,
  frame = 0,
  mouth = 'none',
  sweat = false,
  noLegs = false,
  wiggle = 0,
}) => {
  const talk = mouth === 'talk' ? Math.abs(Math.sin(frame * 0.9)) : 0;
  const wig = wiggle * Math.sin(frame * 1.4) * 10;
  return (
    <g transform={`translate(${x} ${y}) scale(${scale * facing} ${scale})`}>
      {!noLegs && <ellipse cx={0} cy={6} rx={90} ry={14} fill="rgba(0,0,0,0.35)" />}
      {!noLegs && (
        <>
          <Leg x={-26 + wig * 0.4} y={-140} angle={legL + wig} />
          <Leg x={26 - wig * 0.4} y={-140} angle={legR - wig} />
        </>
      )}
      <g transform={`rotate(${bodyTilt} 0 -140)`}>
        <Arm x={-60} y={-290} angle={armL} />
        {/* torso */}
        <path
          d="M-66 -300 Q-74 -200 -58 -130 Q0 -116 58 -130 Q74 -200 66 -300 Q0 -322 -66 -300 Z"
          fill={WRAP}
          stroke={INK}
          strokeWidth={9}
          strokeLinejoin="round"
        />
        <g transform="translate(0 -130)">
          <Bandages w={62} h={170} seed={1} />
        </g>
        {/* head */}
        <g transform={`translate(0 -380) rotate(${headTilt})`}>
          <ellipse cx={0} cy={0} rx={78} ry={88} fill={WRAP} stroke={INK} strokeWidth={9} />
          <path d="M-74 -40 Q0 -20 76 -52" stroke={WRAP_D} strokeWidth={5} fill="none" />
          <path d="M-76 30 Q0 50 76 20" stroke={WRAP_D} strokeWidth={5} fill="none" />
          <path d="M-70 60 Q0 74 64 56" stroke={WRAP_D} strokeWidth={5} fill="none" />
          <path d="M-60 -70 Q10 -60 60 -78" stroke={WRAP_D} strokeWidth={5} fill="none" />
          {/* dark eye slit */}
          <path d="M-66 -18 Q0 -34 70 -22 L70 10 Q0 -2 -66 14 Z" fill="#2a2116" stroke={INK} strokeWidth={6} />
          {/* glowing eyes */}
          <g opacity={eyesOpen}>
            <circle cx={-28} cy={-6} r={26 * glow} fill="rgba(80,255,170,0.35)" />
            <circle cx={30} cy={-8} r={26 * glow} fill="rgba(80,255,170,0.35)" />
            <ellipse cx={-28} cy={-6} rx={13} ry={11 * eyesOpen} fill="#b6ffd9" />
            <ellipse cx={30} cy={-8} rx={13} ry={11 * eyesOpen} fill="#b6ffd9" />
            <circle cx={-28} cy={-6} r={5} fill="#ffffff" />
            <circle cx={30} cy={-8} r={5} fill="#ffffff" />
          </g>
          {mouth === 'groan' && <ellipse cx={4} cy={44} rx={18} ry={22} fill="#2a2116" stroke={INK} strokeWidth={5} />}
          {mouth === 'talk' && <ellipse cx={4} cy={44} rx={16} ry={4 + talk * 14} fill="#2a2116" stroke={INK} strokeWidth={5} />}
          {mouth === 'polite' && <path d="M-18 42 Q4 54 26 40" stroke={INK} strokeWidth={6} fill="none" strokeLinecap="round" />}
          {/* loose head wrap */}
          <path d="M60 -60 Q110 -70 120 -20 Q126 10 110 30" stroke={WRAP} strokeWidth={14} fill="none" strokeLinecap="round" />
          <path d="M60 -60 Q110 -70 120 -20 Q126 10 110 30" stroke={INK} strokeWidth={2} fill="none" opacity={0.4} />
          {sweat && (
            <path d="M-84 -40 Q-98 -16 -84 -8 Q-70 -16 -84 -40 Z" fill="#7fd3ff" stroke={INK} strokeWidth={4} />
          )}
        </g>
        <Arm x={60} y={-290} angle={armR} />
      </g>
    </g>
  );
};
