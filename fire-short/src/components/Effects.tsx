import React from 'react';
import {AbsoluteFill, interpolate, random, useCurrentFrame} from 'remotion';
import {H, W} from './London';

/** Camera: zoom/pan/rotate around a focus point, with optional shake. */
export const Camera: React.FC<{
  zoom?: number;
  focusX?: number;
  focusY?: number;
  rotate?: number;
  shake?: number;
  children: React.ReactNode;
}> = ({zoom = 1, focusX = W / 2, focusY = H / 2, rotate = 0, shake = 0, children}) => {
  const f = useCurrentFrame();
  const sx = shake ? (random(`sx${f}`) - 0.5) * 2 * shake : 0;
  const sy = shake ? (random(`sy${f}`) - 0.5) * 2 * shake : 0;
  const tx = W / 2 - focusX * zoom + sx;
  const ty = H / 2 - focusY * zoom + sy;
  return (
    <g transform={`translate(${tx} ${ty}) rotate(${rotate} ${focusX * zoom} ${focusY * zoom}) scale(${zoom})`}>{children}</g>
  );
};

export const Stage: React.FC<{children: React.ReactNode; bg?: string}> = ({children, bg = '#000'}) => (
  <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0, background: bg}}>
    {children}
  </svg>
);

export const Vignette: React.FC<{strength?: number; color?: string}> = ({strength = 0.75, color = '0,0,0'}) => (
  <AbsoluteFill
    style={{
      background: `radial-gradient(ellipse at 50% 45%, rgba(${color},0) 40%, rgba(${color},${strength}) 100%)`,
      pointerEvents: 'none',
    }}
  />
);

/** Floating dust motes catching torch light. */
export const Dust: React.FC<{count?: number; color?: string}> = ({count = 40, color = 'rgba(255,220,160,0.6)'}) => {
  const f = useCurrentFrame();
  return (
    <g>
      {new Array(count).fill(0).map((_, i) => {
        const x = (random(`dx${i}`) * W + f * (0.4 + random(`dvx${i}`))) % W;
        const y = (random(`dy${i}`) * H - f * (0.6 + random(`dvy${i}`) * 1.2) + H * 10) % H;
        const r = 2 + random(`dr${i}`) * 4;
        return <circle key={i} cx={x} cy={y} r={r} fill={color} opacity={0.4 + 0.6 * Math.abs(Math.sin(f * 0.05 + i))} />;
      })}
    </g>
  );
};

/** Billowing mysterious smoke from a point. progress 0..1 */
export const Smoke: React.FC<{x: number; y: number; progress: number; spread?: number; color?: string; count?: number}> = ({
  x,
  y,
  progress,
  spread = 500,
  color = '170,255,210',
  count = 26,
}) => {
  const f = useCurrentFrame();
  if (progress <= 0) return null;
  return (
    <g>
      {new Array(count).fill(0).map((_, i) => {
        const delay = random(`sd${i}`) * 0.5;
        const p = Math.max(0, Math.min(1, (progress - delay) / (1 - delay)));
        if (p <= 0) return null;
        const ang = -Math.PI / 2 + (random(`sa${i}`) - 0.5) * 2.2;
        const dist = p * spread * (0.5 + random(`sr${i}`));
        const cx = x + Math.cos(ang) * dist + Math.sin(f * 0.05 + i) * 30;
        const cy = y + Math.sin(ang) * dist * 1.2;
        const r = 60 + p * 160 * (0.6 + random(`ss${i}`));
        const op = (1 - p) * 0.55 + 0.05;
        return <circle key={i} cx={cx} cy={cy} r={r} fill={`rgba(${color},${op})`} />;
      })}
    </g>
  );
};

/** Comic speed lines radiating from center (for shock / chase). */
export const SpeedLines: React.FC<{opacity?: number; cx?: number; cy?: number; color?: string}> = ({
  opacity = 1,
  cx = W / 2,
  cy = H / 2,
  color = 'rgba(255,255,255,0.85)',
}) => {
  const f = useCurrentFrame();
  if (opacity <= 0) return null;
  return (
    <g opacity={opacity}>
      {new Array(44).fill(0).map((_, i) => {
        const a = (i / 44) * Math.PI * 2 + random(`sl${i}-${Math.floor(f / 2)}`) * 0.1;
        const r0 = 520 + random(`slr${i}-${Math.floor(f / 2)}`) * 220;
        const r1 = 1500;
        const w = 6 + random(`slw${i}`) * 14;
        const x0 = cx + Math.cos(a) * r0;
        const y0 = cy + Math.sin(a) * r0;
        const x1 = cx + Math.cos(a) * r1;
        const y1 = cy + Math.sin(a) * r1;
        return <line key={i} x1={x0} y1={y0} x2={x1} y2={y1} stroke={color} strokeWidth={w} strokeLinecap="round" />;
      })}
    </g>
  );
};

/** Horizontal motion streaks for running. */
export const MotionStreaks: React.FC<{opacity?: number; dir?: 1 | -1}> = ({opacity = 1, dir = 1}) => {
  const f = useCurrentFrame();
  return (
    <g opacity={opacity}>
      {new Array(16).fill(0).map((_, i) => {
        const y = random(`ms${i}`) * H;
        const len = 200 + random(`ml${i}`) * 400;
        const x = ((random(`mx${i}`) * W * 2 - f * 60 * dir) % (W * 2) + W * 2) % (W * 2) - W / 2;
        return <line key={i} x1={x} x2={x + len} y1={y} y2={y} stroke="rgba(255,255,255,0.35)" strokeWidth={6} strokeLinecap="round" />;
      })}
    </g>
  );
};

/** Full-screen flash overlay. */
export const Flash: React.FC<{at: number; dur?: number; color?: string; peak?: number}> = ({at, dur = 8, color = '#fff', peak = 1}) => {
  const f = useCurrentFrame();
  const o = interpolate(f, [at - 1, at, at + dur], [0, peak, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  if (o <= 0) return null;
  return <AbsoluteFill style={{background: color, opacity: o, pointerEvents: 'none'}} />;
};

/** Comic text burst like "!!" or "BOOM". */
export const Burst: React.FC<{x: number; y: number; text: string; t: number; color?: string; size?: number; rot?: number}> = ({
  x,
  y,
  text,
  t,
  color = '#ffd400',
  size = 120,
  rot = -8,
}) => {
  if (t < 0 || t > 1.2) return null;
  const s = t < 0.2 ? interpolate(t, [0, 0.2], [0.2, 1.15]) : interpolate(t, [0.2, 0.35, 1.2], [1.15, 1, 1], {extrapolateRight: 'clamp'});
  const o = t > 1 ? interpolate(t, [1, 1.2], [1, 0]) : 1;
  const pts = new Array(24)
    .fill(0)
    .map((_, i) => {
      const a = (i / 24) * Math.PI * 2;
      const r = i % 2 ? size * 1.1 : size * 1.9;
      return `${Math.cos(a) * r * 1.4},${Math.sin(a) * r}`;
    })
    .join(' ');
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`} opacity={o}>
      <polygon points={pts} fill={color} stroke="#141414" strokeWidth={10} strokeLinejoin="round" />
      <text
        x={0}
        y={size * 0.32}
        textAnchor="middle"
        fontFamily="LuckiestGuy"
        fontSize={size}
        fill="#e2231a"
        stroke="#141414"
        strokeWidth={8}
        paintOrder="stroke"
      >
        {text}
      </text>
    </g>
  );
};
