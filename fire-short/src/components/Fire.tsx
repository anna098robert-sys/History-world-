import React from 'react';
import {random, useCurrentFrame} from 'remotion';

/**
 * Fire, embers and smoke. Flames are built from many short-lived "tongues"
 * that rise, shrink and cool from white-yellow to deep red, blended with
 * `screen` and softened by a turbulence displacement filter — this reads as
 * real, licking fire rather than a static cartoon shape.
 */

export const FireDefs: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <defs>
      <filter id="flameWarp" x="-30%" y="-30%" width="160%" height="160%">
        <feTurbulence type="fractalNoise" baseFrequency="0.018 0.045" numOctaves={2} seed={Math.floor(f / 2) % 50} result="n" />
        <feDisplacementMap in="SourceGraphic" in2="n" scale={38} xChannelSelector="R" yChannelSelector="G" result="d" />
        <feGaussianBlur in="d" stdDeviation={2.2} />
      </filter>
      <filter id="glowBlur" x="-50%" y="-50%" width="200%" height="200%">
        <feGaussianBlur stdDeviation={18} />
      </filter>
      <filter id="smokeBlur" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation={14} />
      </filter>
      <radialGradient id="fireGlow">
        <stop offset="0%" stopColor="rgba(255,190,80,0.75)" />
        <stop offset="45%" stopColor="rgba(255,110,20,0.3)" />
        <stop offset="100%" stopColor="rgba(255,80,0,0)" />
      </radialGradient>
      <radialGradient id="tongue" cx="50%" cy="70%" r="60%">
        <stop offset="0%" stopColor="#fffbe0" />
        <stop offset="35%" stopColor="#ffd34a" />
        <stop offset="70%" stopColor="#ff7a12" />
        <stop offset="100%" stopColor="rgba(200,30,0,0)" />
      </radialGradient>
    </defs>
  );
};

const lerpColor = (life: number) => {
  // young = hot (white/yellow) → old = cool (red)
  if (life < 0.25) return '#fff3b0';
  if (life < 0.5) return '#ffc531';
  if (life < 0.75) return '#ff7d14';
  return '#d9330b';
};

export const Flame: React.FC<{
  x: number;
  y: number; // base
  w: number;
  h: number;
  seed?: number | string;
  intensity?: number; // 0..1 scales height + count
  lean?: number; // wind lean in px at the top (negative = left)
  tongues?: number;
  glow?: boolean;
}> = ({x, y, w, h, seed = 0, intensity = 1, lean = -60, tongues = 16, glow = true}) => {
  const f = useCurrentFrame();
  if (intensity <= 0.01) return null;
  const H = h * (0.35 + 0.65 * intensity);
  const n = Math.max(4, Math.round(tongues * (0.4 + 0.6 * intensity)));
  const items = [];
  for (let i = 0; i < n; i++) {
    const period = 14 + random(`${seed}-p${i}`) * 14; // frames
    const life = ((f + random(`${seed}-o${i}`) * period) % period) / period;
    const bx = (random(`${seed}-x${i}`) - 0.5) * w * 0.9;
    const centre = 1 - Math.abs(bx) / (w * 0.5); // tongues near centre rise higher
    const hh = H * (0.45 + 0.55 * centre) * (0.75 + random(`${seed}-h${i}`) * 0.5);
    const cy = y - life * hh;
    const cx = x + bx * (1 - life * 0.6) + lean * life * life + Math.sin(f * 0.3 + i) * 8 * life;
    const r = (w / 5) * (1 - life * 0.75) * (0.7 + random(`${seed}-r${i}`) * 0.6);
    items.push(
      <ellipse
        key={i}
        cx={cx}
        cy={cy}
        rx={r}
        ry={r * (1.6 + life)}
        fill={lerpColor(life)}
        opacity={(1 - life) * 0.95}
      />,
    );
  }
  return (
    <g>
      {glow && <ellipse cx={x} cy={y - H * 0.4} rx={w * 1.6} ry={H * 1.1} fill="url(#fireGlow)" opacity={0.85 * intensity} />}
      <g filter="url(#flameWarp)" style={{mixBlendMode: 'screen'}}>
        {/* solid body so the base never looks hollow */}
        <path
          d={`M${x - w / 2} ${y} Q${x - w * 0.45} ${y - H * 0.45} ${x + lean * 0.5} ${y - H * 0.85} Q${x + w * 0.45} ${y - H * 0.45} ${x + w / 2} ${y} Z`}
          fill="url(#tongue)"
          opacity={0.9}
        />
        {items}
        <ellipse cx={x} cy={y - H * 0.12} rx={w * 0.38} ry={H * 0.14} fill="#fff7cf" opacity={0.85} />
      </g>
    </g>
  );
};

/** A long continuous wall of fire made of overlapping flames. */
export const FireWall: React.FC<{
  x0: number;
  x1: number;
  y: number;
  h: number;
  seed?: string;
  intensity?: number;
  lean?: number;
  step?: number;
}> = ({x0, x1, y, h, seed = 'wall', intensity = 1, lean = -80, step = 150}) => {
  const els = [];
  let i = 0;
  for (let x = x0; x <= x1; x += step) {
    const hv = h * (0.7 + random(`${seed}${i}`) * 0.6);
    els.push(<Flame key={i} x={x} y={y} w={step * 1.8} h={hv} seed={`${seed}${i}`} intensity={intensity} lean={lean} tongues={12} glow={i % 2 === 0} />);
    i++;
  }
  return <g>{els}</g>;
};

/** Sparks / embers rising and blown by the wind. */
export const Embers: React.FC<{
  count?: number;
  wind?: number; // px per frame horizontal (negative = left)
  rise?: number;
  area?: {x: number; y: number; w: number; h: number};
  size?: number;
  seed?: string;
}> = ({count = 60, wind = -6, rise = 7, area = {x: 0, y: 0, w: 1080, h: 1920}, size = 1, seed = 'e'}) => {
  const f = useCurrentFrame();
  return (
    <g style={{mixBlendMode: 'screen'}}>
      {new Array(count).fill(0).map((_, i) => {
        const sp = 0.5 + random(`${seed}s${i}`);
        const span = area.w + 400;
        const x = ((random(`${seed}x${i}`) * span + f * wind * sp) % span + span) % span + area.x - 200;
        const y = ((random(`${seed}y${i}`) * area.h - f * rise * sp) % area.h + area.h) % area.h + area.y;
        const r = (2 + random(`${seed}r${i}`) * 5) * size;
        const tw = 0.5 + 0.5 * Math.sin(f * 0.6 + i * 1.7);
        return (
          <g key={i}>
            <line x1={x} y1={y} x2={x - wind * sp * 2.2} y2={y + rise * sp * 2.2} stroke="#ff9a2a" strokeWidth={r * 0.9} strokeLinecap="round" opacity={0.55 * tw} />
            <circle cx={x} cy={y} r={r} fill={i % 3 ? '#ffd65a' : '#fff1b8'} opacity={0.6 + 0.4 * tw} />
          </g>
        );
      })}
    </g>
  );
};

/** Thick rising smoke column, drifting with the wind. */
export const SmokeColumn: React.FC<{
  x: number;
  y: number;
  height?: number;
  width?: number;
  drift?: number;
  dark?: number; // 0 light grey .. 1 near-black
  seed?: string;
  opacity?: number;
  lit?: number; // orange underglow 0..1
}> = ({x, y, height = 1200, width = 260, drift = -500, dark = 0.6, seed = 'sm', opacity = 1, lit = 0.6}) => {
  const f = useCurrentFrame();
  const n = 22;
  const g = Math.round(110 - dark * 85);
  return (
    <g filter="url(#smokeBlur)" opacity={opacity}>
      {new Array(n).fill(0).map((_, i) => {
        const period = 120 + random(`${seed}p${i}`) * 80;
        const life = ((f + random(`${seed}o${i}`) * period) % period) / period;
        const cx = x + (random(`${seed}x${i}`) - 0.5) * width * 0.6 + drift * life * life + Math.sin(f * 0.03 + i) * 30;
        const cy = y - life * height;
        const r = width * (0.35 + life * 1.1) * (0.7 + random(`${seed}r${i}`) * 0.6);
        const warm = Math.max(0, 1 - life * 2.5) * lit;
        const col = `rgb(${Math.round(g + warm * 140)},${Math.round(g + warm * 50)},${Math.round(g)})`;
        return <circle key={i} cx={cx} cy={cy} r={r} fill={col} opacity={0.75 * (1 - life * 0.8)} />;
      })}
    </g>
  );
};

/** Wide smoky sky haze band. */
export const SmokeHaze: React.FC<{y?: number; opacity?: number; color?: string; seed?: string; speed?: number}> = ({
  y = 300,
  opacity = 0.7,
  color = '60,40,35',
  seed = 'hz',
  speed = -2,
}) => {
  const f = useCurrentFrame();
  return (
    <g filter="url(#smokeBlur)" opacity={opacity}>
      {new Array(14).fill(0).map((_, i) => {
        const span = 1800;
        const x = ((random(`${seed}${i}`) * span + f * speed * (0.6 + random(`${seed}v${i}`))) % span + span) % span - 360;
        const yy = y + (random(`${seed}y${i}`) - 0.5) * 400;
        const r = 160 + random(`${seed}r${i}`) * 220;
        return <circle key={i} cx={x} cy={yy} r={r} fill={`rgba(${color},0.55)`} />;
      })}
    </g>
  );
};
