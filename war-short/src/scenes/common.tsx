import React from 'react';
import {AbsoluteFill} from 'remotion';
import {CityDefs} from '../components/City';
import {Stage} from '../components/Effects';
import {FireDefs} from '../components/Fire';
import {GreeceDefs} from '../components/Greece';

export const Scene: React.FC<{children: React.ReactNode; overlay?: React.ReactNode; bg?: string}> = ({children, overlay, bg = '#9fd0f0'}) => (
  <AbsoluteFill>
    <Stage bg={bg}>
      <GreeceDefs />
      <CityDefs />
      <FireDefs />
      {children}
    </Stage>
    {overlay}
  </AbsoluteFill>
);

/**
 * World position of the doodle guy's hand, so props (the letters) can be
 * attached to it. Mirrors the limb maths inside Character.tsx.
 * arm 'L' = back arm (shoulder -34), 'R' = front arm (shoulder +34).
 */
export const handPos = (x: number, y: number, s: number, facing: 1 | -1, angleDeg: number, arm: 'L' | 'R') => {
  const a = (angleDeg * Math.PI) / 180;
  const sx = arm === 'L' ? -34 : 34;
  const lx = sx - 104 * Math.sin(a);
  const ly = -238 + 104 * Math.cos(a);
  return {x: x + facing * s * lx, y: y + s * ly};
};

/** Pink cheeks for the embarrassed ending (drawn over the character's head). */
export const Blush: React.FC<{x: number; y: number; s: number; o: number}> = ({x, y, s, o}) => (
  <g opacity={o}>
    <ellipse cx={x - 44 * s} cy={y - 316 * s} rx={20 * s} ry={11 * s} fill="#ff7a8a" />
    <ellipse cx={x + 62 * s} cy={y - 316 * s} rx={20 * s} ry={11 * s} fill="#ff7a8a" />
  </g>
);

/** Spark star used for weapon clashes (no text). */
export const Clash: React.FC<{x: number; y: number; t: number; s?: number}> = ({x, y, t, s = 1}) => {
  if (t < 0 || t > 0.5) return null;
  const k = t < 0.1 ? t / 0.1 : 1 - (t - 0.1) / 0.4;
  const pts = new Array(16)
    .fill(0)
    .map((_, i) => {
      const a = (i / 16) * Math.PI * 2;
      const r = i % 2 ? 50 : 130;
      return `${Math.cos(a) * r},${Math.sin(a) * r}`;
    })
    .join(' ');
  return (
    <g transform={`translate(${x} ${y}) scale(${s * (0.6 + k * 0.6)})`} opacity={k}>
      <polygon points={pts} fill="#fff6b0" stroke="#ff9a2a" strokeWidth={8} />
    </g>
  );
};
