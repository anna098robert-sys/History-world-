// Props: the flea-market time machine, the Titanic, the iceberg, lifeboats, ...
import React from 'react';
import {C, rng} from './lib';
import {Txt, TITLE, HAND, Glow} from './fx';

const S = {stroke: C.ink, strokeWidth: 7, strokeLinejoin: 'round' as const};

/** brass time machine. screen = text shown on its little screen; lever 0 (up) .. 1 (pulled) */
export const TimeMachine: React.FC<{x: number; y: number; s?: number; t: number; screen?: string; lever?: number; glow?: number; shake?: number; screenColor?: string}> = ({
  x, y, s = 1, t, screen = '', lever = 0, glow = 0, shake = 0, screenColor = '#7dffb0',
}) => {
  const sx = Math.sin(t * 55) * 6 * shake;
  return (
    <g transform={`translate(${x + sx},${y}) scale(${s}) rotate(${Math.sin(t * 41) * 2 * shake})`}>
      {glow > 0 && <Glow id={`tmg${Math.round(x)}${Math.round(y)}`} x={0} y={-90} r={420} color="#9ad8ff" a={0.7 * glow} />}
      {/* feet */}
      {[-150, 150].map((fx) => <rect key={fx} x={fx - 22} y={-10} width={44} height={30} rx={8} fill="#6a4a1a" {...S} />)}
      {/* body */}
      <rect x={-200} y={-230} width={400} height={230} rx={30} fill="#d9a23a" {...S} />
      <rect x={-200} y={-230} width={400} height={50} rx={24} fill="#f0c25a" {...S} />
      {[-170, 170].map((rx) => <circle key={rx} cx={rx} cy={-30} r={9} fill="#8a5a1a" stroke={C.ink} strokeWidth={3} />)}
      {/* screen */}
      <rect x={-150} y={-160} width={200} height={90} rx={12} fill="#0f2a1e" {...S} />
      <Txt x={-50} y={-115} size={screen.length > 10 ? 22 : 30} color={screenColor} font={TITLE} outline={0} shadow={false}>{screen}</Txt>
      {/* dials */}
      {[0, 1].map((k) => {
        const cx = 110;
        const cy = -150 + k * 80;
        const a = t * (k ? -7 : 5) * (1 + shake * 3);
        return (
          <g key={k}>
            <circle cx={cx} cy={cy} r={32} fill="#f6efe0" {...S} />
            <line x1={cx} y1={cy} x2={cx + Math.sin(a) * 24} y2={cy - Math.cos(a) * 24} stroke={C.red} strokeWidth={6} strokeLinecap="round" />
          </g>
        );
      })}
      {/* buttons */}
      {['#3a7ad8', '#2bb36b', '#ffd84d', '#ff8ad8'].map((c, k) => <circle key={c} cx={-130 + k * 50} cy={-35} r={15} fill={c} stroke={C.ink} strokeWidth={5} />)}
      {/* red lever */}
      <g transform={`translate(205,-120) rotate(${-30 + lever * 80})`}>
        <line x1={0} y1={0} x2={0} y2={-120} stroke={C.ink} strokeWidth={18} strokeLinecap="round" />
        <line x1={0} y1={0} x2={0} y2={-120} stroke="#c9ccd2" strokeWidth={10} strokeLinecap="round" />
        <circle cx={0} cy={-128} r={26} fill={C.red} {...S} />
      </g>
      {/* antenna */}
      <line x1={-60} y1={-230} x2={-90} y2={-320} stroke={C.ink} strokeWidth={8} />
      <circle cx={-92} cy={-326} r={14} fill={glow > 0.2 && Math.sin(t * 12) > 0 ? '#ff5a5a' : '#8a1a1a'} stroke={C.ink} strokeWidth={5} />
    </g>
  );
};

/** the Titanic side view (bow to the right). (x,y) = waterline at the centre. length ~1600*s */
export const Ship: React.FC<{x: number; y: number; s?: number; t: number; night?: boolean; lights?: boolean; tilt?: number; smoke?: boolean}> = ({
  x, y, s = 1, t, night = false, lights = false, tilt = 0, smoke = true,
}) => {
  const hull = night ? '#0c0c12' : C.hull;
  const sup = night ? '#8a8ea0' : '#fbf8f0';
  const fun = night ? '#8a6a3a' : C.funnel;
  return (
    <g transform={`translate(${x},${y}) scale(${s}) rotate(${tilt})`}>
      {/* smoke */}
      {smoke && [-420, -180, 60].map((fx, k) =>
        [0, 1, 2, 3, 4].map((j) => {
          const ph = (t * 0.25 + j / 5 + k * 0.13) % 1;
          return <circle key={`${k}${j}`} cx={fx - ph * 260} cy={-560 - ph * 180} r={30 + ph * 60} fill={night ? '#5a5a6a' : '#9a9aa4'} opacity={0.5 * (1 - ph)} />;
        }),
      )}
      {/* masts + wires */}
      <line x1={-700} y1={-200} x2={-700} y2={-640} stroke={C.ink} strokeWidth={10} />
      <line x1={620} y1={-200} x2={620} y2={-640} stroke={C.ink} strokeWidth={10} />
      <line x1={-700} y1={-620} x2={620} y2={-620} stroke={C.ink} strokeWidth={3} />
      <rect x={608} y={-500} width={24} height={30} fill={C.ink} />
      {/* funnels */}
      {[-480, -240, 0, 240].map((fx) => (
        <g key={fx} transform="skewX(-8)">
          <rect x={fx - 50} y={-560} width={100} height={300} fill={fun} {...S} />
          <rect x={fx - 50} y={-560} width={100} height={60} fill={C.ink} />
        </g>
      ))}
      {/* superstructure decks */}
      <rect x={-640} y={-300} width={1180} height={110} fill={sup} {...S} />
      <rect x={-560} y={-370} width={960} height={74} fill={sup} {...S} />
      {Array.from({length: 26}).map((_, k) => (
        <rect key={k} x={-620 + k * 44} y={-270} width={24} height={30} rx={6}
          fill={lights ? (k % 4 === 2 ? '#3a3a4a' : '#ffd98a') : night ? '#3a3a4a' : '#4a6a8a'} />
      ))}
      {/* lifeboats on the boat deck */}
      {[-520, -420, -320, 120, 220, 320].map((bx) => (
        <path key={bx} d={`M${bx - 40},-380 C${bx - 30},-360 ${bx + 30},-360 ${bx + 40},-380 Z`} fill="#fff" stroke={C.ink} strokeWidth={4} />
      ))}
      {/* bridge */}
      <rect x={400} y={-400} width={120} height={40} fill={sup} {...S} />
      {/* hull */}
      <path d="M-820,-190 L760,-190 C800,-120 820,-40 790,60 L-760,60 C-800,0 -820,-100 -820,-190 Z" fill={hull} {...S} />
      <path d="M-772,10 L800,10 C796,30 793,46 790,60 L-760,60 C-768,46 -772,30 -772,10 Z" fill={night ? '#4a1a16' : C.hullRed} />
      <line x1={-820} y1={-176} x2={762} y2={-176} stroke="#d9a23a" strokeWidth={6} />
      {Array.from({length: 40}).map((_, k) => (
        <circle key={k} cx={-760 + k * 38} cy={-120 + (k % 2) * 30} r={7} fill={lights ? '#ffd98a' : '#3a4a5a'} />
      ))}
      <Txt x={560} y={-140} size={30} color="#d9a23a" outline={0} shadow={false}>TITANIC</Txt>
    </g>
  );
};

export const Iceberg: React.FC<{x: number; y: number; s?: number; night?: boolean}> = ({x, y, s = 1, night}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <path d="M-320,0 L-260,-160 L-170,-200 L-120,-340 L-40,-300 L20,-420 L110,-280 L190,-300 L260,-140 L330,0 Z"
      fill={night ? '#9ab8d8' : '#e8f6ff'} {...S} />
    <path d="M20,-420 L110,-280 L190,-300 L260,-140 L330,0 L120,0 L60,-200 Z" fill={night ? '#7a98c0' : '#c4e0f4'} />
    <path d="M-320,0 L-260,-160 L-170,-200 L-120,-340 L-40,-300 L20,-420 L110,-280 L190,-300 L260,-140 L330,0 Z" fill="none" {...S} />
    <path d="M-360,0 L-300,120 L-120,200 L140,180 L340,90 L380,0 Z" fill={night ? '#3a5a8a' : '#9ad0f0'} opacity={0.55} />
  </g>
);

export const Lifeboat: React.FC<{x: number; y: number; s?: number; t?: number; children?: React.ReactNode}> = ({x, y, s = 1, t = 0, children}) => (
  <g transform={`translate(${x},${y + Math.sin(t * 1.6) * 6}) scale(${s}) rotate(${Math.sin(t * 1.3) * 2})`}>
    {children}
    <path d="M-300,-40 L300,-40 C280,40 200,70 0,70 C-200,70 -280,40 -300,-40 Z" fill="#f4f0e4" {...S} />
    <line x1={-290} y1={-20} x2={290} y2={-20} stroke="#c9b48a" strokeWidth={8} />
    <Txt x={0} y={30} size={30} color={C.ink} font={HAND} outline={0} shadow={false}>TITANIC</Txt>
  </g>
);

export const Waves: React.FC<{y: number; t: number; color?: string; dark?: string; x0?: number; x1?: number; amp?: number}> = ({
  y, t, color = C.sea, dark = C.seaD, x0 = -2000, x1 = 4000, amp = 14,
}) => {
  let d = `M${x0},${y}`;
  for (let x = x0; x <= x1; x += 40) d += ` L${x},${y + Math.sin(x * 0.012 + t * 2) * amp}`;
  d += ` L${x1},${y + 2000} L${x0},${y + 2000} Z`;
  return (
    <g>
      <path d={d} fill={color} stroke={C.ink} strokeWidth={5} />
      {Array.from({length: 24}).map((_, k) => {
        const ph = (t * 0.3 + k / 24) % 1;
        const xx = x0 + 200 + ((k * 263) % (x1 - x0 - 400)) + ph * 60;
        const yy = y + 60 + (k % 4) * 70;
        return <line key={k} x1={xx} y1={yy} x2={xx + 70} y2={yy} stroke={dark === C.seaD ? '#ffffff' : '#9ab0d8'} strokeWidth={5} strokeLinecap="round" opacity={0.5} />;
      })}
    </g>
  );
};

export const Chandelier: React.FC<{x: number; y: number; s?: number; t: number; lit?: number}> = ({x, y, s = 1, t, lit = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s}) rotate(${Math.sin(t * 1.2) * 1.5})`}>
    <line x1={0} y1={-300} x2={0} y2={-60} stroke={C.ink} strokeWidth={5} />
    {lit > 0 && <Glow id={`ch${Math.round(x)}`} x={0} y={0} r={240} a={0.5 * lit} />}
    <path d="M-120,-40 C-120,40 120,40 120,-40 Z" fill="#f0c25a" {...S} />
    {[-90, -45, 0, 45, 90].map((dx) => (
      <g key={dx}>
        <line x1={dx} y1={10} x2={dx} y2={70} stroke="#cfe6f2" strokeWidth={6} />
        <path d={`M${dx},70 L${dx - 10},90 L${dx},110 L${dx + 10},90 Z`} fill="#e8f6ff" stroke={C.ink} strokeWidth={3} />
      </g>
    ))}
    {[-100, -30, 30, 100].map((dx) => <ellipse key={dx} cx={dx} cy={-60} rx={9} ry={16} fill="#fff6c0" stroke={C.ink} strokeWidth={3} />)}
  </g>
);

export const ShipBell: React.FC<{x: number; y: number; s?: number; swing?: number}> = ({x, y, s = 1, swing = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s}) rotate(${swing * 25})`}>
    <line x1={0} y1={-90} x2={0} y2={-40} stroke={C.ink} strokeWidth={8} />
    <path d="M-60,40 C-60,-60 60,-60 60,40 L76,60 L-76,60 Z" fill="#e3b23a" {...S} />
    <circle cx={0} cy={72} r={14} fill="#c9922a" stroke={C.ink} strokeWidth={5} />
  </g>
);

export const Stars: React.FC<{t: number; n?: number; seed?: number; x0?: number; x1?: number; y0?: number; y1?: number}> = ({
  t, n = 150, seed = 2, x0 = -1500, x1 = 3500, y0 = -1500, y1 = 700,
}) => {
  const R = rng(seed);
  return (
    <g>
      {Array.from({length: n}).map((_, i) => (
        <circle key={i} cx={x0 + R() * (x1 - x0)} cy={y0 + R() * (y1 - y0)} r={1.5 + R() * 2.5} fill="#fff" opacity={0.4 + 0.4 * Math.sin(t * 2 + i)} />
      ))}
    </g>
  );
};

export const Blanket: React.FC = () => (
  <path d="M-80,60 C-90,180 -70,320 -60,340 L60,340 C70,320 90,180 80,60 C40,40 -40,40 -80,60 Z" fill="#9a6a4a" stroke={C.ink} strokeWidth={5} />
);
