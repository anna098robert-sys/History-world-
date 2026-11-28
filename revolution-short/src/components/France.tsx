import React from 'react';
import {random, useCurrentFrame} from 'remotion';

export const W = 1080;
export const H = 1920;
const INK = '#141414';

export const FranceDefs: React.FC = () => (
  <defs>
    <linearGradient id="stone" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#3a3a44" />
      <stop offset="100%" stopColor="#5a5560" />
    </linearGradient>
    <linearGradient id="dawn" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#7fa8d8" />
      <stop offset="60%" stopColor="#f2c9a0" />
      <stop offset="100%" stopColor="#ffe2b0" />
    </linearGradient>
    <linearGradient id="night" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#0b1024" />
      <stop offset="100%" stopColor="#2a2e50" />
    </linearGradient>
    <radialGradient id="flameGlow">
      <stop offset="0%" stopColor="rgba(255,200,110,0.9)" />
      <stop offset="40%" stopColor="rgba(255,160,60,0.35)" />
      <stop offset="100%" stopColor="rgba(255,140,40,0)" />
    </radialGradient>
    <filter id="soft">
      <feGaussianBlur stdDeviation={8} />
    </filter>
  </defs>
);

/**
 * Darkness with a warm pool of light around a point (the lantern). Rendered
 * as a full-frame dark layer with a radial "hole" whose centre follows the light.
 */
export const LightPool: React.FC<{id: string; x: number; y: number; r: number; dark?: number; flicker?: boolean}> = ({id, x, y, r: r0, dark: d0 = 0.9, flicker = true}) => {
  const f = useCurrentFrame();
  // keep shadows deep but readable on a phone screen
  const dark = d0 * 0.86;
  const r = r0 * 1.15;
  const fl = flicker ? 1 + Math.sin(f * 0.9) * 0.03 + Math.sin(f * 2.3) * 0.02 : 1;
  return (
    <g style={{pointerEvents: 'none'}}>
      <defs>
        <radialGradient id={id} cx={x} cy={y} r={r * fl} gradientUnits="userSpaceOnUse">
          <stop offset="0%" stopColor={`rgba(0,0,0,0)`} />
          <stop offset="45%" stopColor={`rgba(5,4,10,${dark * 0.35})`} />
          <stop offset="100%" stopColor={`rgba(5,4,10,${dark})`} />
        </radialGradient>
      </defs>
      <rect x={-1000} y={-1000} width={W + 2000} height={H + 2000} fill={`url(#${id})`} />
      <circle cx={x} cy={y} r={r * 0.55 * fl} fill="rgba(255,170,70,0.12)" />
    </g>
  );
};

/* -------------------------------------------------------------- props */
export const Lantern: React.FC<{x: number; y: number; s?: number; swing?: number}> = ({x, y, s = 1, swing = 0}) => {
  const f = useCurrentFrame();
  const fl = 0.85 + Math.sin(f * 1.1) * 0.15;
  return (
    <g transform={`translate(${x} ${y}) rotate(${swing}) scale(${s})`}>
      <circle cx={0} cy={70} r={160 * fl} fill="url(#flameGlow)" />
      <path d="M-14 0 Q0 -26 14 0" stroke={INK} strokeWidth={6} fill="none" />
      <path d="M-30 14 L30 14 L24 30 L-24 30 Z" fill="#3a3530" stroke={INK} strokeWidth={5} />
      <rect x={-26} y={30} width={52} height={74} fill="rgba(255,220,140,0.55)" stroke={INK} strokeWidth={6} />
      <line x1={0} y1={30} x2={0} y2={104} stroke={INK} strokeWidth={4} />
      <ellipse cx={0} cy={74} rx={8 * fl} ry={16 * fl} fill="#ffcf5a" />
      <ellipse cx={0} cy={78} rx={4} ry={8} fill="#fff6d0" />
      <path d="M-32 104 L32 104 L26 118 L-26 118 Z" fill="#3a3530" stroke={INK} strokeWidth={5} />
    </g>
  );
};

export const IronKey: React.FC<{x: number; y: number; s?: number; rot?: number; glint?: number}> = ({x, y, s = 1, rot = 0, glint = 0}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
    <circle cx={-70} cy={0} r={34} fill="none" stroke={INK} strokeWidth={22} />
    <circle cx={-70} cy={0} r={34} fill="none" stroke="#6e6a66" strokeWidth={12} />
    <rect x={-40} y={-9} width={130} height={18} fill="#6e6a66" stroke={INK} strokeWidth={5} />
    <path d="M60 9 L60 40 L74 40 L74 26 L84 26 L84 9 Z" fill="#6e6a66" stroke={INK} strokeWidth={5} />
    {glint > 0 && (
      <g transform={`translate(20 -12) scale(${glint})`}>
        <path d="M0 -30 L6 -6 L30 0 L6 6 L0 30 L-6 6 L-30 0 L-6 -6 Z" fill="#fff" />
      </g>
    )}
  </g>
);

/* ------------------------------------------------------------- prison */
const Stones: React.FC<{w: number; h: number; seed: string; tone?: string}> = ({w, h, seed, tone = 'rgba(0,0,0,0.25)'}) => (
  <g>
    {new Array(Math.ceil(h / 110)).fill(0).map((_, r) => (
      <g key={r}>
        <line x1={0} x2={w} y1={r * 110} y2={r * 110} stroke={tone} strokeWidth={5} />
        {new Array(Math.ceil(w / 180) + 1).fill(0).map((__, c) => {
          const x = c * 180 + (r % 2) * 90 + random(`${seed}${r}${c}`) * 20;
          return <line key={c} x1={x} x2={x} y1={r * 110} y2={(r + 1) * 110} stroke={tone} strokeWidth={5} />;
        })}
      </g>
    ))}
  </g>
);

export const Candle: React.FC<{x: number; y: number; s?: number; seed?: number}> = ({x, y, s = 1, seed = 0}) => {
  const f = useCurrentFrame();
  const fl = Math.sin(f * 0.8 + seed) * 0.5 + Math.sin(f * 2.1 + seed * 2) * 0.3;
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <circle cx={0} cy={-60} r={130 + fl * 14} fill="url(#flameGlow)" opacity={0.7} />
      <path d="M-40 0 L40 0 L30 14 L-30 14 Z" fill="#3a3530" stroke={INK} strokeWidth={5} />
      <rect x={-14} y={-50} width={28} height={50} fill="#efe6cc" stroke={INK} strokeWidth={5} />
      <path d={`M-9 -52 Q${-10 + fl * 3} -78 ${fl * 4} -96 Q10 -78 9 -52 Z`} fill="#ffb02e" stroke={INK} strokeWidth={3} />
      <ellipse cx={0} cy={-62} rx={4} ry={8} fill="#fff4c0" />
    </g>
  );
};

export const IronDoor: React.FC<{x: number; y: number; w?: number; h?: number; open?: number; eyes?: boolean}> = ({x, y, w = 240, h = 460, open = 0, eyes = false}) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x} ${y})`}>
      <rect x={-w / 2 - 20} y={-h - 20} width={w + 40} height={h + 20} fill="#2a2a30" stroke={INK} strokeWidth={8} />
      <rect x={-w / 2} y={-h} width={w} height={h} fill="#08070b" />
      <g transform={`translate(${-w / 2} 0) scale(${1 - open * 0.8} 1) translate(${w / 2} 0)`}>
        <rect x={-w / 2} y={-h} width={w} height={h} fill="#4a3f38" stroke={INK} strokeWidth={8} />
        {[0.2, 0.5, 0.8].map((k) => (
          <rect key={k} x={-w / 2} y={-h + h * k - 12} width={w} height={24} fill="#2e2a28" stroke={INK} strokeWidth={4} />
        ))}
        {new Array(9).fill(0).map((_, i) => (
          <circle key={i} cx={-w / 2 + 20 + (i % 3) * (w - 40) / 2} cy={-h + h * [0.2, 0.5, 0.8][Math.floor(i / 3)]} r={7} fill="#7a706a" stroke={INK} strokeWidth={3} />
        ))}
        {/* barred grille */}
        <rect x={-50} y={-h + 60} width={100} height={70} fill="#050407" stroke={INK} strokeWidth={6} />
        {[-25, 0, 25].map((bx) => (
          <line key={bx} x1={bx} x2={bx} y1={-h + 60} y2={-h + 130} stroke="#3a3530" strokeWidth={8} />
        ))}
        {eyes && (
          <g opacity={(f % 50) > 4 ? 1 : 0}>
            <circle cx={-12} cy={-h + 95} r={5} fill="#ffe680" />
            <circle cx={12} cy={-h + 95} r={5} fill="#ffe680" />
          </g>
        )}
        {/* lock plate */}
        <rect x={w / 2 - 60} y={-h / 2 - 40} width={40} height={70} rx={6} fill="#6e6a66" stroke={INK} strokeWidth={5} />
        <path d={`M${w / 2 - 40} ${-h / 2 - 16} l0 22`} stroke={INK} strokeWidth={8} strokeLinecap="round" />
      </g>
    </g>
  );
};

/** Side view of a prison corridor (scrolls horizontally). */
export const PrisonCorridor: React.FC<{scroll?: number; floorY?: number}> = ({scroll = 0, floorY = 1580}) => {
  const unit = 600;
  const start = Math.floor(scroll / unit) - 1;
  const items = [];
  for (let i = start; i < start + 4; i++) {
    const ox = i * unit - scroll;
    items.push(
      <g key={i} transform={`translate(${ox} 0)`}>
        <IronDoor x={200} y={floorY} eyes={Math.abs(i) % 3 === 1} />
        <g>
          {/* arched niche with a candle */}
          <path d={`M430 ${floorY - 520} L430 ${floorY - 700} Q480 ${floorY - 770} 530 ${floorY - 700} L530 ${floorY - 520} Z`} fill="#1d1b22" stroke={INK} strokeWidth={6} />
          <Candle x={480} y={floorY - 520} s={0.8} seed={i} />
        </g>
        {/* chains on the wall */}
        <path d={`M${560} ${floorY - 900} q-10 60 0 120 q10 60 0 120`} stroke="#5a5550" strokeWidth={10} fill="none" strokeDasharray="18 8" />
      </g>,
    );
  }
  return (
    <g>
      <rect x={-500} y={-500} width={W + 1000} height={floorY + 500} fill="url(#stone)" />
      <g transform={`translate(${-((scroll * 1) % 180)} 0)`}>
        <Stones w={W + 400} h={floorY} seed="pc" />
      </g>
      {/* vaulted ceiling */}
      <rect x={-500} y={-500} width={W + 1000} height={720} fill="#1a1820" />
      {new Array(5).fill(0).map((_, k) => {
        const ax = ((k * 600 - scroll) % 3000 + 3000) % 3000 - 600;
        return <path key={k} d={`M${ax} 220 Q${ax + 300} -60 ${ax + 600} 220`} stroke="#2e2b36" strokeWidth={40} fill="none" />;
      })}
      {items}
      <rect x={-500} y={floorY} width={W + 1000} height={H - floorY + 500} fill="#2a2730" />
      <g transform={`translate(${-((scroll * 1.2) % 260)} 0)`}>
        {new Array(8).fill(0).map((_, k) => (
          <path key={k} d={`M${k * 260} ${floorY} L${k * 260 - 120} ${H}`} stroke="rgba(0,0,0,0.35)" strokeWidth={5} />
        ))}
      </g>
      {/* straw on the floor */}
      {new Array(18).fill(0).map((_, k) => {
        const sx = ((k * 137 - scroll) % 1400 + 1400) % 1400 - 160;
        return <line key={`s${k}`} x1={sx} y1={floorY + 40 + (k % 4) * 30} x2={sx + 40} y2={floorY + 30 + (k % 4) * 30} stroke="#b59a4a" strokeWidth={5} />;
      })}
      <line x1={-500} x2={W + 500} y1={floorY} y2={floorY} stroke={INK} strokeWidth={8} />
    </g>
  );
};

/** Head-on vanishing-point corridor. */
export const PrisonDeep: React.FC<{travel?: number; vpY?: number}> = ({travel = 0, vpY = 980}) => {
  const vx = W / 2;
  const rings = [];
  for (let i = 0; i < 8; i++) {
    const z = 1 - ((i + travel) % 8) / 8;
    const sc = Math.pow(0.3, z * 3);
    const w = 1500 * sc;
    const h = 2300 * sc;
    const x0 = vx - w / 2;
    const y0 = vpY - h * 0.5;
    rings.push({
      z,
      el: (
        <g key={i} opacity={Math.max(0.15, 1 - z)}>
          <path d={`M${x0} ${y0 + h} L${x0} ${y0 + h * 0.25} Q${vx} ${y0 - h * 0.1} ${x0 + w} ${y0 + h * 0.25} L${x0 + w} ${y0 + h}`} fill="none" stroke="#2e2b36" strokeWidth={Math.max(3, 60 * sc)} />
          {i % 2 === 0 && <Candle x={x0 + w * 0.06} y={y0 + h * 0.55} s={sc * 2.2} seed={i} />}
          {i % 2 === 1 && <IronDoor x={x0 + w * 0.88} y={y0 + h * 0.98} w={240 * sc * 1.6} h={460 * sc * 1.6} />}
        </g>
      ),
    });
  }
  rings.sort((a, b) => b.z - a.z);
  return (
    <g>
      <rect x={-500} y={-500} width={W + 1000} height={H + 1000} fill="#2a2730" />
      <path d={`M-500 -500 L${vx - 30} ${vpY - 40} L${vx - 30} ${vpY + 40} L-500 ${H + 500} Z`} fill="#4a4652" />
      <path d={`M${W + 500} -500 L${vx + 30} ${vpY - 40} L${vx + 30} ${vpY + 40} L${W + 500} ${H + 500} Z`} fill="#3e3a46" />
      <path d={`M-500 ${H + 500} L${W + 500} ${H + 500} L${vx + 30} ${vpY + 40} L${vx - 30} ${vpY + 40} Z`} fill="#24212a" />
      <rect x={vx - 30} y={vpY - 40} width={60} height={80} fill="#020203" />
      {rings.map((r) => r.el)}
    </g>
  );
};

/** Foreground cell bars (front of the cell). */
export const CellBars: React.FC<{x0?: number; x1?: number; y0?: number; y1?: number; gap?: number; open?: number}> = ({x0 = -100, x1 = W + 100, y0 = 200, y1 = 1700, gap = 150, open = 0}) => {
  const bars = [];
  for (let x = x0; x <= x1; x += gap) bars.push(x);
  return (
    <g>
      {bars.map((bx, i) => (
        <g key={i} transform={i >= bars.length / 2 ? `translate(${open * 600} 0)` : undefined}>
          <rect x={bx - 14} y={y0} width={28} height={y1 - y0} fill="#3a3530" stroke={INK} strokeWidth={6} />
          <rect x={bx - 6} y={y0} width={6} height={y1 - y0} fill="rgba(255,255,255,0.15)" />
        </g>
      ))}
      <rect x={x0 - 40} y={y0 + 120} width={x1 - x0 + 80} height={30} fill="#3a3530" stroke={INK} strokeWidth={6} />
      <rect x={x0 - 40} y={y1 - 160} width={x1 - x0 + 80} height={30} fill="#3a3530" stroke={INK} strokeWidth={6} />
    </g>
  );
};

/* --------------------------------------------------------- the prisoner */
/**
 * Frightened young man: loose dark hair, open-collar white shirt, brown
 * waistcoat. `face` is also used for the wanted poster portrait.
 */
export const PrisonerFace: React.FC<{expr?: 'beg' | 'fear' | 'sly' | 'calm'; tears?: number; f?: number}> = ({expr = 'beg', tears = 0, f = 0}) => (
  <g>
    <path d="M-62 -10 Q-80 -86 0 -92 Q80 -86 62 -10 L66 40 Q40 10 0 6 Q-40 10 -66 40 Z" fill="#3a2414" stroke={INK} strokeWidth={6} />
    <ellipse cx={0} cy={6} rx={56} ry={66} fill="#f0c9a6" stroke={INK} strokeWidth={6} />
    <path d="M-56 -20 Q-30 -66 10 -54 Q40 -70 58 -24 Q30 -48 0 -36 Q-30 -48 -56 -20 Z" fill="#3a2414" stroke={INK} strokeWidth={4} />
    {/* stubble */}
    <path d="M-40 40 Q0 76 40 40" stroke="rgba(60,40,30,0.35)" strokeWidth={14} fill="none" />
    {expr === 'sly' ? (
      <>
        <path d="M-30 -2 Q-18 -10 -6 -2" stroke={INK} strokeWidth={5} fill="none" />
        <path d="M8 -2 Q20 -10 32 -2" stroke={INK} strokeWidth={5} fill="none" />
        <path d="M-36 -20 L-8 -12 M38 -20 L10 -12" stroke={INK} strokeWidth={5} />
        <path d="M-18 34 Q6 44 26 28" stroke={INK} strokeWidth={5} fill="none" />
      </>
    ) : (
      <>
        <ellipse cx={-18} cy={-2} rx={7} ry={9} fill={INK} />
        <ellipse cx={18} cy={-2} rx={7} ry={9} fill={INK} />
        <circle cx={-16} cy={-5} r={2.5} fill="#fff" />
        <circle cx={20} cy={-5} r={2.5} fill="#fff" />
        <path d="M-34 -22 L-8 -28 M34 -22 L8 -28" stroke={INK} strokeWidth={5} strokeLinecap="round" />
        {expr === 'calm' ? (
          <path d="M-14 34 L14 34" stroke={INK} strokeWidth={5} />
        ) : (
          <ellipse cx={0} cy={36} rx={14} ry={expr === 'beg' ? 10 + Math.abs(Math.sin(f * 0.6)) * 6 : 12} fill="#3a1a12" stroke={INK} strokeWidth={4} />
        )}
      </>
    )}
    {tears > 0 &&
      [-1, 1].map((d) => {
        const p = (f % 24) / 24;
        return <path key={d} d={`M${d * 20} ${8 + p * 50} q-7 12 0 16 q7 -4 0 -16 Z`} fill="#7fd3ff" stroke={INK} strokeWidth={2} opacity={tears * (1 - p)} />;
      })}
  </g>
);

export const Prisoner: React.FC<{
  x: number;
  y: number;
  s?: number;
  facing?: 1 | -1;
  expr?: 'beg' | 'fear' | 'sly' | 'calm';
  armL?: number;
  armR?: number;
  run?: number;
  tears?: number;
  cloak?: boolean;
}> = ({x, y, s = 1, facing = 1, expr = 'beg', armL = 20, armR = -20, run, tears = 0, cloak = false}) => {
  const f = useCurrentFrame();
  const isRun = run !== undefined;
  const sw = isRun ? Math.sin(run!) : 0;
  const bob = isRun ? Math.abs(Math.cos(run!)) * 12 : 0;
  return (
    <g transform={`translate(${x} ${y - bob * s}) scale(${s * facing} ${s})`}>
      <ellipse cx={0} cy={4} rx={60} ry={10} fill="rgba(0,0,0,0.3)" />
      {[-1, 1].map((k) => (
        <g key={k} transform={`translate(${k * 16} -130) rotate(${k * sw * 40})`}>
          <line x1={0} y1={0} x2={0} y2={124} stroke="#5a4636" strokeWidth={22} strokeLinecap="round" />
          <ellipse cx={8} cy={128} rx={20} ry={9} fill="#2a1a10" />
        </g>
      ))}
      <path d="M-42 -290 L-46 -120 L46 -120 L42 -290 Z" fill="#f4efe2" stroke={INK} strokeWidth={6} />
      <path d="M-40 -280 L-42 -130 L-12 -130 L-10 -280 Z M40 -280 L42 -130 L12 -130 L10 -280 Z" fill="#7a5034" stroke={INK} strokeWidth={4} />
      <path d="M-14 -290 L0 -250 L14 -290" fill="none" stroke={INK} strokeWidth={4} />
      {cloak && <path d="M-60 -300 Q-90 -150 -70 -40 L70 -40 Q90 -150 60 -300 Z" fill="#2a2420" stroke={INK} strokeWidth={6} />}
      {[
        [-38, armL],
        [38, armR],
      ].map(([sx, a], i) => (
        <g key={i} transform={`translate(${sx} -276) rotate(${isRun ? (i ? sw : -sw) * 50 : a})`}>
          <line x1={0} y1={0} x2={0} y2={112} stroke={cloak ? '#2a2420' : '#f4efe2'} strokeWidth={24} strokeLinecap="round" />
          <circle cx={0} cy={120} r={14} fill="#f0c9a6" stroke={INK} strokeWidth={4} />
        </g>
      ))}
      <g transform="translate(0 -360)">
        <PrisonerFace expr={expr} tears={tears} f={f} />
        {cloak && <path d="M-80 -40 L80 -40 L60 -60 Q0 -110 -60 -60 Z" fill="#1d1a18" stroke={INK} strokeWidth={5} />}
      </g>
    </g>
  );
};

export const Rat: React.FC<{x: number; y: number; s?: number; facing?: 1 | -1}> = ({x, y, s = 1, facing = 1}) => {
  const f = useCurrentFrame();
  return (
    <g transform={`translate(${x} ${y}) scale(${s * facing} ${s})`}>
      <path d={`M-40 0 Q-90 ${-10 + Math.sin(f * 0.5) * 8} -120 10`} stroke="#c9a0a0" strokeWidth={6} fill="none" />
      <ellipse cx={0} cy={-20} rx={46} ry={26} fill="#7a7070" stroke={INK} strokeWidth={5} />
      <circle cx={42} cy={-30} r={18} fill="#7a7070" stroke={INK} strokeWidth={5} />
      <circle cx={34} cy={-50} r={10} fill="#e0a0a0" stroke={INK} strokeWidth={4} />
      <circle cx={50} cy={-32} r={3.5} fill={INK} />
      <circle cx={60} cy={-26} r={4} fill="#e07070" />
      <path d="M58 -26 l18 -6 M58 -24 l18 4" stroke={INK} strokeWidth={2} />
    </g>
  );
};

/* ---------------------------------------------------------- Paris 1793 */
const Facade: React.FC<{x: number; y: number; w: number; floors: number; seed: number; tint?: string}> = ({x, y, w, floors, seed, tint}) => {
  const wall = ['#e8dcc2', '#ddd0b2', '#efe5cf', '#d9c8a6'][seed % 4];
  const fh = 170;
  const top = y - floors * fh;
  return (
    <g>
      <rect x={x} y={top} width={w} height={floors * fh} fill={wall} stroke={INK} strokeWidth={6} />
      {/* mansard roof with dormers */}
      <path d={`M${x - 10} ${top} L${x + 30} ${top - 140} L${x + w - 30} ${top - 140} L${x + w + 10} ${top} Z`} fill="#5a6070" stroke={INK} strokeWidth={6} />
      {[0.3, 0.7].map((k) => (
        <g key={k}>
          <rect x={x + w * k - 26} y={top - 110} width={52} height={70} fill="#e8dcc2" stroke={INK} strokeWidth={4} />
          <rect x={x + w * k - 16} y={top - 96} width={32} height={50} fill="#2a3040" />
        </g>
      ))}
      <rect x={x + w * 0.8} y={top - 200} width={30} height={70} fill="#9a6a4a" stroke={INK} strokeWidth={4} />
      {/* shuttered tall windows + wrought-iron balconies */}
      {new Array(floors).fill(0).map((_, r) =>
        [0.2, 0.5, 0.8].map((k) => {
          const wx = x + w * k - 26;
          const wy = top + r * fh + 30;
          return (
            <g key={`${r}-${k}`}>
              <rect x={wx} y={wy} width={52} height={100} fill="#2a3040" stroke={INK} strokeWidth={4} />
              <rect x={wx - 16} y={wy} width={16} height={100} fill="#4a6a5a" stroke={INK} strokeWidth={3} />
              <rect x={wx + 52} y={wy} width={16} height={100} fill="#4a6a5a" stroke={INK} strokeWidth={3} />
              {r === 0 && <path d={`M${wx - 10} ${wy + 100} L${wx + 62} ${wy + 100} M${wx - 10} ${wy + 80} L${wx + 62} ${wy + 80}`} stroke={INK} strokeWidth={4} />}
            </g>
          );
        }),
      )}
      {/* ground floor arcade / shop */}
      <path d={`M${x + 20} ${y} L${x + 20} ${y - 120} Q${x + w / 2} ${y - 190} ${x + w - 20} ${y - 120} L${x + w - 20} ${y}`} fill="#3a2a20" stroke={INK} strokeWidth={5} />
      {tint && <rect x={x - 10} y={top - 200} width={w + 20} height={floors * fh + 200} fill={tint} />}
    </g>
  );
};

/** Tricolour flag waving. */
export const Tricolour: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => {
  const f = useCurrentFrame();
  const L = 180;
  const wave = (t: number, off: number) => Math.sin(f * 0.22 - t * 4 + off) * 14 * t;
  const band = (i: number, col: string) => {
    const a = i / 3;
    const b = (i + 1) / 3;
    const pts = [
      `${a * L} ${wave(a, 0)}`,
      `${b * L} ${wave(b, 0)}`,
      `${b * L} ${120 + wave(b, 0.4)}`,
      `${a * L} ${120 + wave(a, 0.4)}`,
    ];
    return <polygon key={i} points={pts.join(' ')} fill={col} />;
  };
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <line x1={0} y1={0} x2={0} y2={-420} stroke="#6b4a2a" strokeWidth={10} />
      <g transform="translate(0 -410)">
        {band(0, '#1f3f8a')}
        {band(1, '#f4f1ea')}
        {band(2, '#c8312a')}
        <polygon points={`0 ${wave(0, 0)} ${L} ${wave(1, 0)} ${L} ${120 + wave(1, 0.4)} 0 120`} fill="none" stroke={INK} strokeWidth={5} />
      </g>
    </g>
  );
};

/** Distant scaffold silhouette (the guillotine) — never shown in use. */
export const Scaffold: React.FC<{x: number; y: number; s?: number; color?: string}> = ({x, y, s = 1, color = '#2a2430'}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill={color}>
    <rect x={-140} y={-80} width={280} height={80} />
    <rect x={-50} y={-420} width={16} height={340} />
    <rect x={34} y={-420} width={16} height={340} />
    <rect x={-60} y={-430} width={120} height={20} />
    <path d="M-34 -380 L34 -360 L34 -330 L-34 -330 Z" fill="#8a8f96" />
    <path d="M-60 -80 L-100 0 M60 -80 L100 0" stroke={color} strokeWidth={10} />
  </g>
);

export const ParisSquare: React.FC<{groundY?: number; scroll?: number; sky?: string; morning?: boolean}> = ({groundY = 1500, scroll = 0, sky = 'url(#dawn)', morning = true}) => (
  <g>
    <rect x={-500} y={-500} width={W + 1000} height={groundY + 500} fill={sky} />
    {morning && <circle cx={820} cy={520} r={200} fill="rgba(255,240,200,0.6)" filter="url(#soft)" />}
    {/* far skyline with Notre-Dame-like towers */}
    <g fill="#9a9ab0" opacity={0.8}>
      <rect x={-200 - scroll * 0.1} y={groundY - 520} width={1500} height={300} />
      <rect x={620 - scroll * 0.1} y={groundY - 760} width={70} height={260} />
      <rect x={720 - scroll * 0.1} y={groundY - 760} width={70} height={260} />
    </g>
    <g transform={`translate(${-scroll} 0)`}>
      {[
        [-200, 300, 4, 0],
        [100, 280, 5, 1],
        [380, 320, 4, 2],
        [700, 300, 5, 3],
        [1000, 280, 4, 4],
        [1280, 320, 5, 5],
      ].map(([fx, fw, fl, sd]) => (
        <Facade key={fx} x={fx} y={groundY - 60} w={fw} floors={fl} seed={sd} />
      ))}
      <Tricolour x={330} y={groundY - 760} s={0.8} />
      <Tricolour x={1010} y={groundY - 760} s={0.8} />
    </g>
    <rect x={-500} y={groundY - 60} width={W + 1000} height={H - groundY + 560} fill="#a89a84" />
    {new Array(16).fill(0).map((_, i) => {
      const cx = ((i * 140 - scroll * 1.2) % 2240 + 2240) % 2240 - 300;
      return <ellipse key={i} cx={cx} cy={groundY + (i % 4) * 90} rx={60} ry={16} fill="rgba(0,0,0,0.12)" />;
    })}
  </g>
);

/** Parisian crowd: sans-culottes in red Phrygian caps, women in bonnets. */
export const Parisian: React.FC<{x: number; y: number; s?: number; seed?: number; facing?: 1 | -1; walk?: number; silhouette?: string}> = ({x, y, s = 1, seed = 0, facing = 1, walk, silhouette}) => {
  const female = seed % 3 === 1;
  const coats = ['#6b4a2a', '#4a5a3a', '#7a3a2a', '#3a4a6a', '#8a6a3a'];
  const coat = silhouette ?? coats[seed % coats.length];
  const skin = silhouette ?? ['#f0c9a6', '#e0b08a', '#d9a57f'][seed % 3];
  const sw = walk !== undefined ? Math.sin(walk) : 0;
  const bob = walk !== undefined ? Math.abs(Math.cos(walk)) * 6 : 0;
  return (
    <g transform={`translate(${x} ${y - bob}) scale(${s * facing} ${s})`}>
      {[-1, 1].map((k) => (
        <line key={k} x1={k * 12} y1={-110} x2={k * 12 + (k > 0 ? sw : -sw) * 30} y2={-4} stroke={silhouette ?? (female ? '#3a2a20' : '#d8d0c0')} strokeWidth={14} strokeLinecap="round" />
      ))}
      {female ? (
        <path d="M-30 -210 L-46 -4 L46 -4 L30 -210 Z" fill={coat} stroke={silhouette ? 'none' : INK} strokeWidth={5} />
      ) : (
        <path d="M-32 -210 L-38 -100 L38 -100 L32 -210 Z" fill={coat} stroke={silhouette ? 'none' : INK} strokeWidth={5} />
      )}
      {!silhouette && female && <path d="M-26 -200 L0 -150 L26 -200" stroke="#f4efe2" strokeWidth={10} fill="none" />}
      <circle cx={0} cy={-240} r={30} fill={skin} stroke={silhouette ? 'none' : INK} strokeWidth={5} />
      {!silhouette && <circle cx={12} cy={-244} r={3.5} fill={INK} />}
      {female ? (
        <path d="M-36 -236 Q-36 -284 0 -282 Q36 -284 36 -236 Q20 -258 -36 -236 Z" fill={silhouette ?? '#f4efe2'} stroke={silhouette ? 'none' : INK} strokeWidth={4} />
      ) : seed % 3 === 0 ? (
        // red Phrygian "liberty" cap with cockade
        <g>
          <path d="M-32 -246 Q-30 -290 10 -286 Q40 -280 30 -246 Z M10 -286 Q-30 -290 -40 -262" fill={silhouette ?? '#c8312a'} stroke={silhouette ? 'none' : INK} strokeWidth={4} />
          {!silhouette && <circle cx={24} cy={-258} r={6} fill="#1f3f8a" stroke="#f4f1ea" strokeWidth={3} />}
        </g>
      ) : (
        <path d="M-40 -252 L40 -252 L26 -268 L-26 -268 Z M-24 -268 Q0 -290 24 -268" fill={silhouette ?? '#2a2420'} stroke={silhouette ? 'none' : INK} strokeWidth={4} />
      )}
    </g>
  );
};

/** National Guard soldier: blue coat, white facings, bicorne with cockade, musket. */
export const Guard: React.FC<{x: number; y: number; s?: number; facing?: 1 | -1; walk?: number; look?: number}> = ({x, y, s = 1, facing = 1, walk, look = 0}) => {
  const sw = walk !== undefined ? Math.sin(walk) : 0;
  const bob = walk !== undefined ? Math.abs(Math.cos(walk)) * 8 : 0;
  return (
    <g transform={`translate(${x} ${y - bob}) scale(${s * facing} ${s})`}>
      <ellipse cx={0} cy={4} rx={56} ry={10} fill="rgba(0,0,0,0.3)" />
      {[-1, 1].map((k) => (
        <g key={k} transform={`translate(${k * 14} -120) rotate(${k * sw * 28})`}>
          <line x1={0} y1={0} x2={0} y2={70} stroke="#f2ede2" strokeWidth={20} strokeLinecap="round" />
          <line x1={0} y1={70} x2={0} y2={118} stroke="#1d1a18" strokeWidth={20} strokeLinecap="round" />
        </g>
      ))}
      <path d="M-38 -250 L-44 -100 L44 -100 L38 -250 Z" fill="#1f3f8a" stroke={INK} strokeWidth={6} />
      <path d="M-20 -250 L-24 -110 L24 -110 L20 -250 Z" fill="#f2ede2" stroke={INK} strokeWidth={4} />
      <path d="M-44 -112 L-56 -60 L-30 -100 Z M44 -112 L56 -60 L30 -100 Z" fill="#1f3f8a" stroke={INK} strokeWidth={4} />
      <path d="M-38 -244 L38 -150 M38 -244 L-38 -150" stroke="#f2ede2" strokeWidth={8} />
      <rect x={-44} y={-256} width={88} height={14} fill="#c8312a" stroke={INK} strokeWidth={3} />
      {/* musket with bayonet on the shoulder */}
      <g transform="translate(34 -230) rotate(-8)">
        <line x1={0} y1={120} x2={0} y2={-150} stroke="#6b4220" strokeWidth={12} />
        <line x1={0} y1={-150} x2={0} y2={-250} stroke="#9aa0a8" strokeWidth={5} />
      </g>
      <g transform={`translate(0 -290) rotate(${look * 15})`}>
        <circle r={32} fill="#f0c9a6" stroke={INK} strokeWidth={5} />
        <circle cx={12} cy={-4} r={4} fill={INK} />
        <path d="M2 -16 L22 -12" stroke={INK} strokeWidth={4} />
        <path d="M6 14 L22 14" stroke={INK} strokeWidth={4} />
        <path d="M-26 6 Q-28 -10 -18 -14" stroke="#3a2a1a" strokeWidth={8} fill="none" />
        {/* bicorne */}
        <path d="M-64 -20 Q0 -90 64 -20 Q0 -44 -64 -20 Z" fill="#141414" stroke={INK} strokeWidth={4} />
        <circle cx={0} cy={-46} r={11} fill="#1f3f8a" stroke="#f4f1ea" strokeWidth={4} />
        <circle cx={0} cy={-46} r={4} fill="#c8312a" />
      </g>
    </g>
  );
};

/** Market stall with bread loaves, cabbages, onions; awning. */
export const MarketStall: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-260} y={-500} width={18} height={500} fill="#6b4a2a" stroke={INK} strokeWidth={4} />
    <rect x={242} y={-500} width={18} height={500} fill="#6b4a2a" stroke={INK} strokeWidth={4} />
    <path d="M-300 -500 L300 -500 L270 -400 L-270 -400 Z" fill="#c8312a" stroke={INK} strokeWidth={6} />
    {[0, 1, 2, 3, 4].map((k) => (
      <path key={k} d={`M${-270 + k * 108 + 30} -400 L${-270 + k * 108 + 70} -400 L${-300 + k * 120 + 75} -500 L${-300 + k * 120 + 35} -500 Z`} fill="#f4f1ea" />
    ))}
    <rect x={-280} y={-240} width={560} height={240} fill="#8a5a2e" stroke={INK} strokeWidth={7} />
    <path d="M-280 -170 L280 -170 M-280 -100 L280 -100" stroke="#6b4220" strokeWidth={6} />
    {/* long loaves */}
    {[-200, -110, -20].map((bx, i) => (
      <g key={bx} transform={`translate(${bx} -262) rotate(${i * 6 - 6})`}>
        <ellipse rx={56} ry={18} fill="#d9a050" stroke={INK} strokeWidth={4} />
        <path d="M-30 -8 l8 14 M-6 -10 l8 14 M18 -10 l8 14" stroke="#8a5a20" strokeWidth={3} />
      </g>
    ))}
    {[80, 150, 220].map((cx) => (
      <circle key={cx} cx={cx} cy={-268} r={30} fill="#7a9a4a" stroke={INK} strokeWidth={4} />
    ))}
    {[-230, -170].map((cx) => (
      <circle key={cx} cx={cx} cy={-30} r={20} fill="#c08a4a" stroke={INK} strokeWidth={3} />
    ))}
  </g>
);

/**
 * Wanted poster — picture only, no writing: a portrait, a wax seal and a
 * bag of coins for the reward. `who` picks whose face is on it.
 */
export const Poster: React.FC<{x: number; y: number; s?: number; rot?: number; who: 'prisoner' | 'hero'; f?: number}> = ({x, y, s = 1, rot = 0, who, f = 0}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
    <path d="M-170 -230 L170 -236 L176 236 L-176 230 Z" fill="#efe2bf" stroke={INK} strokeWidth={8} />
    <path d="M-150 -210 L150 -214 L154 120 L-154 116 Z" fill="none" stroke="#8a6a3a" strokeWidth={6} />
    <g transform="translate(0 -40) scale(1.25)">
      {who === 'prisoner' ? (
        <PrisonerFace expr="calm" />
      ) : (
        // the doodle guy's own face + red cap, as an engraved portrait
        <g>
          <circle r={74} fill="#fff" stroke={INK} strokeWidth={7} />
          <circle cx={-14} cy={-6} r={7} fill={INK} />
          <circle cx={20} cy={-6} r={7} fill={INK} />
          <path d="M-8 28 Q6 36 20 28" stroke={INK} strokeWidth={6} fill="none" />
          <path d="M-70 -26 Q-72 -92 0 -94 Q70 -92 72 -26 Q0 -40 -70 -26 Z" fill="#e2231a" stroke={INK} strokeWidth={7} />
          <path d="M32 -34 Q96 -42 122 -24 Q96 -12 32 -24 Z" fill="#c41b13" stroke={INK} strokeWidth={6} />
        </g>
      )}
    </g>
    {/* reward: coin purse + coins */}
    <g transform="translate(-80 180)">
      <path d="M-34 30 Q-44 -10 -14 -24 L14 -24 Q44 -10 34 30 Z" fill="#a8743c" stroke={INK} strokeWidth={5} />
      <path d="M-14 -24 Q0 -36 14 -24" stroke={INK} strokeWidth={5} fill="none" />
      {[40, 64, 88].map((cx, i) => (
        <ellipse key={cx} cx={cx} cy={20 - i * 4} rx={14} ry={14} fill="#f2c230" stroke={INK} strokeWidth={4} />
      ))}
    </g>
    {/* official wax seal with ribbon */}
    <g transform="translate(110 180)">
      <path d="M-14 10 L-24 60 L-4 46 L6 64 L10 12 Z" fill="#1f3f8a" />
      <circle r={30} fill="#c8312a" stroke={INK} strokeWidth={5} />
      <circle r={18} fill="none" stroke="#8a1a14" strokeWidth={4} />
    </g>
    {/* nail */}
    <circle cx={0} cy={-218} r={8} fill="#5a5550" stroke={INK} strokeWidth={3} />
  </g>
);

/** Dark attic room: sloped beams, small window with moon, door with a gap. */
export const DarkRoom: React.FC<{floorY?: number}> = ({floorY = 1600}) => (
  <g>
    <rect x={-500} y={-500} width={W + 1000} height={floorY + 500} fill="#1e1a22" />
    <path d={`M-500 200 L540 -200 L1580 200`} stroke="#2e2630" strokeWidth={70} fill="none" />
    <path d="M-200 300 L-200 1600 M1280 300 L1280 1600" stroke="#2e2630" strokeWidth={50} />
    {/* small round window with moonlight */}
    <circle cx={260} cy={620} r={110} fill="#2a3a6a" stroke={INK} strokeWidth={10} />
    <circle cx={290} cy={590} r={40} fill="#e8e6d0" />
    <path d="M150 620 L370 620 M260 510 L260 730" stroke={INK} strokeWidth={10} />
    <path d="M190 700 L-100 1600 L380 1600 L330 700 Z" fill="rgba(160,180,255,0.07)" />
    {/* door on the right with a gap under it */}
    <rect x={760} y={floorY - 640} width={300} height={640} fill="#3a2a22" stroke={INK} strokeWidth={8} />
    <rect x={790} y={floorY - 610} width={240} height={260} fill="none" stroke="#2a1e18" strokeWidth={6} />
    <rect x={790} y={floorY - 320} width={240} height={260} fill="none" stroke="#2a1e18" strokeWidth={6} />
    <circle cx={800} cy={floorY - 320} r={14} fill="#8a7a5a" stroke={INK} strokeWidth={4} />
    <rect x={760} y={floorY - 12} width={300} height={12} fill="rgba(255,200,120,0.5)" />
    <rect x={-500} y={floorY} width={W + 1000} height={H - floorY + 500} fill="#2a2224" />
    {new Array(7).fill(0).map((_, i) => (
      <line key={i} x1={-200 + i * 220} y1={floorY} x2={-500 + i * 280} y2={H + 200} stroke="rgba(0,0,0,0.3)" strokeWidth={5} />
    ))}
    <line x1={-500} x2={W + 500} y1={floorY} y2={floorY} stroke={INK} strokeWidth={8} />
  </g>
);

export const Stool: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <ellipse cx={0} cy={-150} rx={90} ry={22} fill="#6b4a2a" stroke={INK} strokeWidth={6} />
    <path d="M-60 -140 L-80 0 M60 -140 L80 0 M0 -140 L0 0" stroke="#5a3a20" strokeWidth={14} />
  </g>
);
