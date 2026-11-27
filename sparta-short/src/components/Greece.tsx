import React from 'react';
import {random, useCurrentFrame} from 'remotion';

export const W = 1080;
export const H = 1920;
const INK = '#141414';

export const GreeceDefs: React.FC = () => (
  <defs>
    <linearGradient id="sky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#3f8fd8" />
      <stop offset="65%" stopColor="#9fd0f0" />
      <stop offset="100%" stopColor="#f5e3b3" />
    </linearGradient>
    <linearGradient id="plain" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#d9b56a" />
      <stop offset="100%" stopColor="#a87b3c" />
    </linearGradient>
    <linearGradient id="bronze" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stopColor="#ffd98a" />
      <stop offset="45%" stopColor="#d9962e" />
      <stop offset="100%" stopColor="#8a5512" />
    </linearGradient>
    <radialGradient id="sun">
      <stop offset="0%" stopColor="rgba(255,250,220,1)" />
      <stop offset="40%" stopColor="rgba(255,240,180,0.6)" />
      <stop offset="100%" stopColor="rgba(255,240,180,0)" />
    </radialGradient>
  </defs>
);

/* ------------------------------------------------------------ landscape */
const OliveTree: React.FC<{x: number; y: number; s?: number; sway: number}> = ({x, y, s = 1, sway}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-10 0 Q-20 -60 0 -110 Q14 -60 10 0 Z" fill="#6b4a2a" stroke={INK} strokeWidth={5} />
    <g transform={`rotate(${sway} 0 -110)`}>
      {[[-50, -140, 60], [30, -150, 64], [-10, -185, 58], [55, -110, 44], [-60, -100, 44]].map(([cx, cy, r], i) => (
        <ellipse key={i} cx={cx} cy={cy} rx={r} ry={r * 0.72} fill={i % 2 ? '#7d9a5a' : '#6b8a4c'} stroke={INK} strokeWidth={5} />
      ))}
    </g>
  </g>
);

export const Landscape: React.FC<{horizon?: number}> = ({horizon = 1050}) => {
  const f = useCurrentFrame();
  const sway = Math.sin(f * 0.06) * 2;
  return (
    <g>
      <rect x={-400} y={-400} width={W + 800} height={horizon + 400} fill="url(#sky)" />
      <circle cx={820} cy={360} r={360} fill="url(#sun)" />
      {/* drifting clouds */}
      {[0, 1, 2].map((i) => {
        const cx = ((i * 520 + f * (0.6 + i * 0.2)) % 1800) - 400;
        return (
          <g key={i} transform={`translate(${cx} ${220 + i * 140})`} opacity={0.9}>
            <ellipse cx={0} cy={0} rx={130} ry={46} fill="#fff" />
            <ellipse cx={-70} cy={14} rx={80} ry={36} fill="#fff" />
            <ellipse cx={80} cy={12} rx={90} ry={38} fill="#fff" />
          </g>
        );
      })}
      {/* distant mountains */}
      <path d={`M-400 ${horizon} L-120 ${horizon - 330} L120 ${horizon - 180} L380 ${horizon - 400} L640 ${horizon - 200} L880 ${horizon - 360} L1180 ${horizon - 150} L1480 ${horizon - 280} L1480 ${horizon} Z`} fill="#8aa3b8" />
      <path d={`M-400 ${horizon} L-60 ${horizon - 180} L260 ${horizon - 90} L560 ${horizon - 210} L900 ${horizon - 100} L1480 ${horizon - 190} L1480 ${horizon} Z`} fill="#9fae86" />
      {/* hilltop temple (Doric) */}
      <g transform={`translate(560 ${horizon - 200})`}>
        <path d="M-160 0 Q0 -60 160 0 Z" fill="#9fae86" />
        <g transform="translate(0 -40) scale(0.6)">
          <rect x={-150} y={-14} width={300} height={22} fill="#f2ead8" stroke={INK} strokeWidth={5} />
          {[-120, -72, -24, 24, 72, 120].map((c) => (
            <rect key={c} x={c - 11} y={-130} width={22} height={118} fill="#f7f1e2" stroke={INK} strokeWidth={4} />
          ))}
          <rect x={-160} y={-152} width={320} height={24} fill="#f2ead8" stroke={INK} strokeWidth={5} />
          <path d="M-165 -152 L0 -205 L165 -152 Z" fill="#f2ead8" stroke={INK} strokeWidth={5} />
        </g>
      </g>
      {/* plain */}
      <rect x={-400} y={horizon} width={W + 800} height={H - horizon + 400} fill="url(#plain)" />
      {new Array(30).fill(0).map((_, i) => (
        <path
          key={i}
          d={`M${random(`g${i}`) * W} ${horizon + 40 + random(`gy${i}`) * 800} l-8 -18 m8 18 l0 -22 m0 22 l8 -18`}
          stroke="#8a6a2e"
          strokeWidth={4}
          strokeLinecap="round"
        />
      ))}
      <OliveTree x={60} y={horizon + 30} s={0.8} sway={sway} />
      <OliveTree x={1010} y={horizon + 20} s={0.9} sway={-sway} />
      <OliveTree x={300} y={horizon + 10} s={0.5} sway={sway} />
    </g>
  );
};

/* -------------------------------------------------------------- hoplite */
export type Side = 'sparta' | 'athens';

const SIDE = {
  sparta: {cloak: '#b3201a', tunic: '#d8352b', crest: '#c41a12', crestDark: '#7a0f0a'},
  athens: {cloak: '#2a5d9a', tunic: '#f2ead8', crest: '#f2ead8', crestDark: '#b5ab96'},
};

/**
 * Greek hoplite, c. 431 BC: Corinthian bronze helmet with horsehair crest,
 * round bronze aspis shield, linen cuirass, greaves, long dory spear.
 * Spartans: red cloaks, lambda (Λ) shield device. Athenians: owl devices.
 */
export const Hoplite: React.FC<{
  x: number;
  y: number;
  side: Side;
  s?: number;
  march?: number; // phase (radians); undefined = standing
  spear?: number; // 0 upright … 1 lowered for attack
  seed?: number;
  shout?: number; // 0..1 open mouth
}> = ({x, y, side, s = 1, march, spear = 0, seed = 0, shout = 0}) => {
  const c = SIDE[side];
  const dir = side === 'sparta' ? 1 : -1; // Spartans face right, Athenians face left
  const marching = march !== undefined;
  const sw = marching ? Math.sin(march!) : 0;
  const bob = marching ? Math.abs(Math.cos(march!)) * 8 : 0;
  const spearAngle = 78 * spear + (1 - spear) * (-4 + Math.sin(seed) * 3); // lowered = pointing forward
  const device = side === 'sparta' ? (
    <path d="M-34 34 L0 -36 L34 34" stroke="#141414" strokeWidth={14} fill="none" strokeLinejoin="round" />
  ) : (
    <g>
      {/* owl of Athena */}
      <ellipse cx={0} cy={6} rx={26} ry={32} fill="#3a2a18" />
      <circle cx={-11} cy={-8} r={10} fill="#ffe9a8" />
      <circle cx={11} cy={-8} r={10} fill="#ffe9a8" />
      <circle cx={-11} cy={-8} r={4} fill="#141414" />
      <circle cx={11} cy={-8} r={4} fill="#141414" />
      <path d="M-4 4 L0 12 L4 4 Z" fill="#d9962e" />
      <path d="M-26 -26 L-16 -18 M26 -26 L16 -18" stroke="#3a2a18" strokeWidth={6} />
    </g>
  );
  return (
    <g transform={`translate(${x} ${y - bob * s}) scale(${s * dir} ${s})`}>
      <ellipse cx={0} cy={4} rx={70} ry={11} fill="rgba(0,0,0,0.28)" />
      {/* cloak behind */}
      <path d="M-30 -230 Q-80 -140 -70 -60 L-20 -70 Z" fill={c.cloak} stroke={INK} strokeWidth={5} />
      {/* legs with bronze greaves */}
      {[-1, 1].map((k) => (
        <g key={k} transform={`translate(${k * 14} -110) rotate(${k * sw * 26})`}>
          <rect x={-10} y={0} width={20} height={58} rx={8} fill="#e8b58a" stroke={INK} strokeWidth={5} />
          <rect x={-12} y={50} width={24} height={52} rx={9} fill="url(#bronze)" stroke={INK} strokeWidth={5} />
          <path d="M-6 104 L22 106 L22 112 L-10 112 Z" fill="#6b4a2a" stroke={INK} strokeWidth={4} />
        </g>
      ))}
      {/* tunic + linen cuirass */}
      <path d="M-34 -120 L-40 -96 L40 -96 L34 -120 Z" fill={c.tunic} stroke={INK} strokeWidth={5} />
      <path d="M-32 -232 L-36 -118 L36 -118 L32 -232 Z" fill="#f4ecd6" stroke={INK} strokeWidth={6} />
      {[-24, -8, 8, 24].map((p) => (
        <rect key={p} x={p - 7} y={-122} width={14} height={26} fill="#e6dcc0" stroke={INK} strokeWidth={3} />
      ))}
      <path d="M-32 -200 L32 -200" stroke="#c9a96a" strokeWidth={6} />
      {/* spear (dory) held in right hand */}
      <g transform={`translate(30 -190) rotate(${spearAngle})`}>
        <line x1={0} y1={160} x2={0} y2={-260} stroke="#7a5228" strokeWidth={10} strokeLinecap="round" />
        <path d="M0 -300 L12 -262 L0 -250 L-12 -262 Z" fill="#c9ced6" stroke={INK} strokeWidth={4} />
        <rect x={-6} y={150} width={12} height={22} fill="#c9ced6" stroke={INK} strokeWidth={3} />
        <circle cx={0} cy={0} r={11} fill="#e8b58a" stroke={INK} strokeWidth={4} />
      </g>
      {/* head: Corinthian helmet */}
      <g transform="translate(0 -278)">
        <path d="M-40 -6 Q-42 -56 0 -60 Q44 -56 42 -4 L42 40 L14 44 L14 12 L-2 12 L-2 44 L-40 40 Z" fill="url(#bronze)" stroke={INK} strokeWidth={6} />
        {/* eye slit with angry eyes */}
        <path d="M-2 -6 L40 -10 L40 8 L-2 10 Z" fill="#1d140c" />
        <circle cx={22} cy={0} r={4} fill="#fff" />
        <path d="M8 -12 L34 -4" stroke="#1d140c" strokeWidth={6} strokeLinecap="round" />
        {shout > 0 && <ellipse cx={6} cy={34} rx={7} ry={4 + shout * 8} fill="#1d140c" />}
        {/* horsehair crest */}
        <path d={`M-46 -40 Q-10 ${-110 - sw * 4} 40 -52 L34 -40 Q-6 -78 -38 -30 Z`} fill={c.crest} stroke={INK} strokeWidth={5} />
        <path d="M-40 -46 Q-8 -96 32 -50" stroke={c.crestDark} strokeWidth={5} fill="none" />
      </g>
      {/* round bronze aspis shield on left arm, held in front */}
      <g transform={`translate(10 -170) rotate(${sw * 2})`}>
        <circle r={88} fill="url(#bronze)" stroke={INK} strokeWidth={8} />
        <circle r={74} fill="none" stroke="#8a5512" strokeWidth={6} />
        {device}
        <path d="M-60 -40 Q-40 -66 -10 -74" stroke="rgba(255,255,255,0.55)" strokeWidth={8} fill="none" strokeLinecap="round" />
      </g>
    </g>
  );
};

/** A phalanx: several ranks of hoplites, deep rows drawn first. */
export const Phalanx: React.FC<{
  side: Side;
  frontX: number; // x of the front file (leading edge)
  y: number; // ground line of front rank
  ranks?: number;
  files?: number;
  s?: number;
  march?: boolean;
  spear?: number;
  shout?: number;
  frame: number;
}> = ({side, frontX, y, ranks = 3, files = 6, s = 1, march = false, spear = 0, shout = 0, frame}) => {
  const dir = side === 'sparta' ? 1 : -1;
  const men = [];
  for (let r = ranks - 1; r >= 0; r--) {
    const rs = s * (1 - r * 0.16);
    const ry = y - r * 70 * s;
    for (let fi = files - 1; fi >= 0; fi--) {
      const jitter = (random(`${side}${r}${fi}`) - 0.5) * 30 * s;
      const px = frontX - dir * (fi * 120 * rs + r * 40 * s) + jitter;
      men.push(
        <Hoplite
          key={`${r}-${fi}`}
          x={px}
          y={ry}
          side={side}
          s={rs}
          march={march ? frame * 0.32 + fi * 0.6 + r : undefined}
          spear={Math.max(0, Math.min(1, spear * (1.2 - fi * 0.04)))}
          seed={r * 10 + fi}
          shout={shout * (0.6 + random(`sh${side}${r}${fi}`) * 0.4)}
        />,
      );
    }
  }
  return <g>{men}</g>;
};

/** Waving cloth banner on a pole. */
export const Banner: React.FC<{x: number; y: number; side: Side; s?: number}> = ({x, y, side, s = 1}) => {
  const f = useCurrentFrame();
  const col = side === 'sparta' ? '#c41a12' : '#2a5d9a';
  const dir = side === 'sparta' ? 1 : -1;
  const pts: string[] = [];
  const L = 170;
  for (let i = 0; i <= 10; i++) {
    const t = i / 10;
    pts.push(`${t * L} ${Math.sin(f * 0.25 - t * 4) * 16 * t}`);
  }
  for (let i = 10; i >= 0; i--) {
    const t = i / 10;
    pts.push(`${t * L} ${110 + Math.sin(f * 0.25 - t * 4 + 0.5) * 16 * t}`);
  }
  return (
    <g transform={`translate(${x} ${y}) scale(${s * dir} ${s})`}>
      <line x1={0} y1={0} x2={0} y2={-520} stroke="#6b4a2a" strokeWidth={12} strokeLinecap="round" />
      <g transform="translate(0 -500)">
        <polygon points={pts.join(' ')} fill={col} stroke={INK} strokeWidth={6} strokeLinejoin="round" />
        {/* meander (Greek key) trim */}
        <polyline points={pts.slice(0, 11).map((p) => p.split(' ').map(Number)).map(([px, py]) => `${px} ${py + 18}`).join(' ')} fill="none" stroke="#f2d27a" strokeWidth={6} strokeDasharray="14 8" />
      </g>
      <circle cx={0} cy={-526} r={14} fill="url(#bronze)" stroke={INK} strokeWidth={4} />
    </g>
  );
};

/** Dust kicked up by marching feet, drifting across the plain. */
export const DustClouds: React.FC<{y: number; x0: number; x1: number; amount: number; seed?: string}> = ({y, x0, x1, amount, seed = 'd'}) => {
  const f = useCurrentFrame();
  if (amount <= 0) return null;
  return (
    <g opacity={amount}>
      {new Array(18).fill(0).map((_, i) => {
        const period = 50 + random(`${seed}p${i}`) * 40;
        const life = ((f + random(`${seed}o${i}`) * period) % period) / period;
        const x = x0 + random(`${seed}x${i}`) * (x1 - x0) + life * 60;
        const r = 40 + life * 120;
        return <circle key={i} cx={x} cy={y - life * 140} r={r} fill={`rgba(215,180,120,${0.55 * (1 - life)})`} />;
      })}
    </g>
  );
};
