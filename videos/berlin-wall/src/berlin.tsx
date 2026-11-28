// Berlin 1961–1990 set pieces and cast (reused from the Short, generalised for 16:9), all in the doodle style.
import React from 'react';
import {C, W, H, blinkAt, clamp, rng} from './lib';
import {Doodle, DoodleProps, SlickHair, WoolCap} from './Hero';
import {HAND, Sweat, Txt} from './fx';

export const feet = (yFeet: number, s: number) => yFeet - 456 * s;
export const Hero: React.FC<DoodleProps> = (p) => <Doodle blink={blinkAt(p.x * 0.013 + (p.walk ?? 0))} {...p} />;
export const Fill: React.FC<{c: string; a: number}> = ({c, a}) => (a > 0.001 ? <rect x={0} y={0} width={W} height={H} fill={c} opacity={clamp(a)} /> : null);
export const GRAF = ['#ff4a8a', '#ffd84d', '#3ad0ff', '#7ae05a', '#ff8a3a', '#b88aff'];

// ------------------------------------------------------------------ skies, city, ground
export const NightSky: React.FC<{t: number; id: string; warm?: number}> = ({t, id, warm = 0}) => {
  const R = rng(4);
  return (
    <g>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={warm ? '#3a3a7a' : '#0a1030'} />
          <stop offset="1" stopColor={warm ? '#ffb070' : '#2c3466'} />
        </linearGradient>
      </defs>
      <rect x={-3000} y={-3000} width={9000} height={7000} fill={`url(#${id})`} />
      {!warm && Array.from({length: 140}).map((_, i) => (
        <circle key={i} cx={-1200 + R() * 4400} cy={-800 + R() * 1500} r={1.5 + R() * 2.5} fill="#fff" opacity={0.35 + 0.35 * Math.sin(t * 2 + i)} />
      ))}
    </g>
  );
};

export const DaySky: React.FC<{id: string; top?: string; bot?: string}> = ({id, top = '#8ec8ee', bot = '#dff0fa'}) => (
  <g>
    <defs>
      <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={top} />
        <stop offset="1" stopColor={bot} />
      </linearGradient>
    </defs>
    <rect x={-3000} y={-3000} width={9000} height={7000} fill={`url(#${id})`} />
  </g>
);

export const BrandenburgGate: React.FC<{x: number; y: number; s?: number; fill?: string; detail?: boolean}> = ({x, y, s = 1, fill = '#1a2040', detail}) => {
  const st = detail ? {stroke: C.ink, strokeWidth: 6, strokeLinejoin: 'round' as const} : {};
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <rect x={-260} y={-300} width={520} height={60} fill={fill} {...st} />
      <rect x={-270} y={-330} width={540} height={34} fill={fill} {...st} />
      {[0, 1, 2, 3, 4, 5].map((k) => <rect key={k} x={-250 + k * 92} y={-240} width={34} height={240} fill={fill} {...st} />)}
      <path d="M-50,-330 L-30,-390 L40,-390 L60,-330 Z" fill={fill} {...st} />
      {detail && <g>
        <path d="M-40,-390 L-20,-440 L30,-440 L44,-390 Z" fill="#5a8a6a" stroke={C.ink} strokeWidth={5} />
        <circle cx={4} cy={-452} r={14} fill="#5a8a6a" stroke={C.ink} strokeWidth={4} />
      </g>}
    </g>
  );
};

/** distant skyline: Fernsehturm, Brandenburg Gate, Plattenbau blocks with lit windows. dx shifts it sideways */
export const Skyline: React.FC<{y: number; t: number; warm?: boolean; dx?: number; gate?: boolean; tower?: boolean; day?: boolean}> = ({
  y, t, warm, dx = 0, gate = true, tower = true, day,
}) => {
  const R = rng(9);
  const sil = day ? '#9aa8bc' : warm ? '#7a5a6a' : '#1a2040';
  const win = day ? '#c8d4e2' : warm ? '#ffd9a0' : '#f6d98a';
  return (
    <g transform={`translate(${dx},0)`}>
      {tower && <g>
        <rect x={1440} y={y - 900} width={26} height={900} fill={sil} />
        <circle cx={1453} cy={y - 760} r={60} fill={sil} />
        <rect x={1449} y={y - 1020} width={8} height={160} fill={sil} />
        {!day && <circle cx={1453} cy={y - 1022} r={6} fill="#ff5050" opacity={0.6 + 0.4 * Math.sin(t * 4)} />}
      </g>}
      {gate && <BrandenburgGate x={300} y={y} fill={sil} />}
      {Array.from({length: 18}).map((_, i) => {
        const x = -1300 + i * 260 + R() * 40;
        const h = 200 + R() * 300;
        if (gate && x > 0 && x < 560) return null;
        return (
          <g key={i}>
            <rect x={x} y={y - h} width={220} height={h} fill={sil} />
            {Array.from({length: Math.floor(h / 60)}).map((_, r) =>
              [0, 1, 2, 3].map((c) => (R() < 0.35 ? <rect key={`${r}${c}`} x={x + 20 + c * 50} y={y - h + 20 + r * 60} width={26} height={30} fill={win} opacity={0.85} /> : null)),
            )}
          </g>
        );
      })}
    </g>
  );
};

/** a street of 1960s houses (front view) */
export const Street: React.FC<{y: number; x0?: number; n?: number; seed?: number; grey?: boolean; lit?: boolean}> = ({y, x0 = -200, n = 9, seed = 2, grey, lit}) => {
  const R = rng(seed);
  const cols = grey ? ['#8a8a92', '#9a9aa0', '#7a7a84'] : ['#e8c89a', '#d8a888', '#c8d0b0', '#e0b8a0', '#b8c8d8'];
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const x = x0 + i * 300;
        const h = 420 + R() * 180;
        const c = cols[i % cols.length];
        return (
          <g key={i}>
            <rect x={x} y={y - h} width={290} height={h} fill={c} stroke={C.ink} strokeWidth={6} />
            <rect x={x - 6} y={y - h - 20} width={302} height={26} fill={grey ? '#5a5a62' : '#a05a3a'} stroke={C.ink} strokeWidth={5} />
            {Array.from({length: Math.floor((h - 140) / 110)}).map((_, r) => [0, 1, 2].map((k) => (
              <rect key={`${r}${k}`} x={x + 30 + k * 85} y={y - h + 40 + r * 110} width={60} height={74}
                fill={lit ? (R() < 0.5 ? '#ffe08a' : '#3a4060') : '#cfe6f2'} stroke={C.ink} strokeWidth={4} />
            )))}
            <rect x={x + 115} y={y - 120} width={60} height={120} fill="#7a4a2a" stroke={C.ink} strokeWidth={5} />
          </g>
        );
      })}
    </g>
  );
};

export const Ground: React.FC<{y: number; night?: boolean; warm?: boolean; color?: string}> = ({y, night = true, warm, color}) => (
  <g>
    <rect x={-3000} y={y} width={9000} height={2000} fill={color ?? (warm ? '#b89a8a' : night ? '#3a3a48' : '#9a9aa2')} stroke={C.ink} strokeWidth={6} />
    {Array.from({length: 60}).map((_, k) => <line key={k} x1={-2000 + k * 150} y1={y} x2={-2400 + k * 150} y2={y + 700} stroke={warm ? '#a08a7a' : night ? '#2e2e3a' : '#8a8a92'} strokeWidth={4} />)}
  </g>
);

// ------------------------------------------------------------------ the Wall and the border
/** the Wall (Grenzmauer 75): slabs with a pipe on top, seen from the West (graffiti) or the East (bare) */
export const Wall: React.FC<{x0: number; x1: number; y: number; h?: number; t: number; west?: boolean; shake?: number; crack?: number; night?: boolean; gap?: [number, number]}> = ({
  x0, x1, y, h = 420, t, west = true, shake = 0, crack = 0, night = true, gap,
}) => {
  const R = rng(3);
  const n = Math.ceil((x1 - x0) / 120);
  const base = night ? '#9a9a9e' : '#bdbdc0';
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const x = x0 + i * 120;
        const seed = R();
        if (gap && x + 120 > gap[0] && x < gap[1]) return null;
        const dy = shake * Math.sin(t * 40 + i * 1.7) * 6;
        const col = i % 2 ? base : night ? '#929296' : '#b4b4b8';
        return (
          <g key={i} transform={`translate(0,${dy})`}>
            <rect x={x} y={y - h} width={120} height={h} fill={col} stroke={C.ink} strokeWidth={5} />
            <rect x={x} y={y - h - 40} width={120} height={56} rx={i === 0 ? 28 : 0} fill={night ? '#b4b4b8' : '#d4d4d6'} stroke={C.ink} strokeWidth={5} />
            {west && seed < 0.85 && (
              <g opacity={night ? 0.85 : 1}>
                <path d={`M${x + 10},${y - 60 - seed * 120} C${x + 40},${y - 220} ${x + 80},${y - 40} ${x + 110},${y - 160 - seed * 60}`}
                  fill="none" stroke={GRAF[i % 6]} strokeWidth={16} strokeLinecap="round" />
                {seed > 0.45 && <circle cx={x + 60} cy={y - 260 - seed * 60} r={30} fill={GRAF[(i + 2) % 6]} stroke={C.ink} strokeWidth={3} />}
                {seed < 0.3 && <path d={`M${x + 40},${y - 300} l20,-30 l20,30 l-20,20 Z`} fill={GRAF[(i + 4) % 6]} stroke={C.ink} strokeWidth={3} />}
                {seed > 0.7 && <Txt x={x + 60} y={y - 120} size={30} color={GRAF[(i + 3) % 6]} font={HAND} outline={0} shadow={false}>{['FREI', 'LOVE', 'PEACE', 'JA!'][i % 4]}</Txt>}
              </g>
            )}
            {crack > 0 && seed > 0.4 && (
              <path d={`M${x + 30},${y - h} L${x + 50},${y - h + 120 * crack} L${x + 30},${y - h + 200 * crack} L${x + 60},${y - h + 280 * crack}`}
                fill="none" stroke={C.ink} strokeWidth={5} />
            )}
          </g>
        );
      })}
    </g>
  );
};

/** a line of barbed-wire coils on posts; k = 0..1 unrolled from x0 to x1 */
export const BarbedWire: React.FC<{x0: number; x1: number; y: number; k?: number; h?: number; color?: string}> = ({x0, x1, y, k = 1, h = 110, color = '#3a3a40'}) => {
  const xe = x0 + (x1 - x0) * clamp(k);
  const loops: React.ReactNode[] = [];
  for (let x = x0; x < xe; x += 44) loops.push(<ellipse key={x} cx={x} cy={y - h / 2} rx={34} ry={h / 2} fill="none" stroke={color} strokeWidth={4} />);
  const posts: React.ReactNode[] = [];
  for (let x = x0; x <= xe; x += 260) posts.push(<line key={'p' + x} x1={x} y1={y + 6} x2={x} y2={y - h - 30} stroke="#6b4428" strokeWidth={12} strokeLinecap="round" />);
  return (
    <g>
      {posts}
      {loops}
      {[0.25, 0.6, 0.95].map((f) => <line key={f} x1={x0} y1={y - h * f} x2={xe} y2={y - h * f} stroke={color} strokeWidth={3} strokeDasharray="10 8" />)}
    </g>
  );
};

export const Watchtower: React.FC<{x: number; y: number; s?: number; t: number; beam?: boolean}> = ({x, y, s = 1, t, beam = true}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    {beam && <path d={`M-30,-520 L${-700 + Math.sin(t * 0.8) * 200},0 L${-360 + Math.sin(t * 0.8) * 200},0 Z`} fill="#fff6c0" opacity={0.12} />}
    <rect x={-30} y={-460} width={60} height={460} fill="#8a8a8e" stroke={C.ink} strokeWidth={6} />
    <rect x={-80} y={-570} width={160} height={110} fill="#9a9a9e" stroke={C.ink} strokeWidth={6} />
    <rect x={-64} y={-550} width={128} height={48} fill="#2a2e3a" />
    <rect x={-90} y={-590} width={180} height={26} fill="#6a6a70" stroke={C.ink} strokeWidth={5} />
    <circle cx={60} cy={-600} r={16} fill="#fff6c0" stroke={C.ink} strokeWidth={4} />
  </g>
);

export const Floodlight: React.FC<{x: number; y: number; t: number; a?: number; h?: number}> = ({x, y, t, a = 1, h = 640}) => (
  <g>
    <line x1={x} y1={y} x2={x} y2={y - h} stroke="#2a2a30" strokeWidth={14} />
    <path d={`M${x - 30},${y - h} L${x + 30},${y - h} L${x + 420},${y} L${x - 420},${y} Z`} fill="#fff6c0" opacity={0.08 * a * (0.9 + 0.1 * Math.sin(t * 6))} />
    <rect x={x - 34} y={y - h - 30} width={68} height={34} rx={8} fill="#fff6c0" stroke={C.ink} strokeWidth={5} />
  </g>
);

export const Dog: React.FC<{x: number; y: number; s?: number; t: number; flip?: boolean}> = ({x, y, s = 1, t, flip}) => (
  <g transform={`translate(${x},${y}) scale(${flip ? -s : s},${s})`}>
    <path d="M-90,-60 C-90,-110 60,-110 70,-70 L70,-20 L-90,-20 Z" fill="#6a4a2a" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
    {[-70, -30, 30, 60].map((lx, i) => <line key={lx} x1={lx} y1={-24} x2={lx + Math.sin(t * 10 + i) * 8} y2={0} stroke={C.ink} strokeWidth={10} strokeLinecap="round" />)}
    <path d={`M-90,-80 C-120,${-110 + Math.sin(t * 9) * 10} -130,-100 -130,-90`} fill="none" stroke={C.ink} strokeWidth={8} strokeLinecap="round" />
    <circle cx={90} cy={-100} r={38} fill="#6a4a2a" stroke={C.ink} strokeWidth={6} />
    <path d="M100,-90 L150,-84 L146,-66 L104,-70 Z" fill="#6a4a2a" stroke={C.ink} strokeWidth={5} />
    <path d="M70,-130 L80,-160 L96,-130 Z" fill="#4a3018" stroke={C.ink} strokeWidth={4} />
    <circle cx={100} cy={-108} r={5} fill={C.ink} />
    <circle cx={150} cy={-78} r={6} fill={C.ink} />
  </g>
);

// ------------------------------------------------------------------ cast (never a red cap)
const HAIR = ['#2a1e14', '#7a4a24', '#d9b05a', '#3a3a3a', '#a03a1a'];
const JACKET = ['#3a6ab8', '#c83a5a', '#2a9a8a', '#7a4ab8', '#e0a030', '#5a6a3a', '#8a8a92', '#d05a2a'];

export const Berliner: React.FC<DoodleProps & {seed?: number; grey?: boolean}> = ({seed = 0, grey, ...p}) => {
  const style = seed % 5;
  const hair = HAIR[(seed * 3) % HAIR.length];
  let back: React.ReactNode = null;
  let front: React.ReactNode = null;
  const jacket = grey ? ['#6a6a72', '#5a6070', '#7a7068', '#585860'][seed % 4] : JACKET[seed % JACKET.length];
  if (style === 0) front = <SlickHair color={hair} />;
  if (style === 1) front = <WoolCap color={grey ? '#4a4a52' : JACKET[(seed + 3) % JACKET.length]} />;
  if (style === 2) front = <g>{[-80, -40, 0, 40, 80, -60, 60, -20, 20].map((dx, i) => <circle key={i} cx={dx} cy={-70 - (i > 4 ? 40 : 0) + Math.abs(dx) * 0.2} r={36} fill={hair} stroke={C.ink} strokeWidth={5} />)}</g>;
  if (style === 3) {
    back = <path d="M-108,-10 C-130,120 -110,190 -70,200 L70,200 C110,190 130,120 108,-10 Z" fill={hair} stroke={C.ink} strokeWidth={7} />;
    front = <path d="M-100,-20 C-104,-140 104,-150 102,-20 C60,-80 -60,-80 -100,-20 Z" fill={hair} stroke={C.ink} strokeWidth={7} />;
  }
  if (style === 4) front = <g><path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill={hair} stroke={C.ink} strokeWidth={6} />
    {[-30, 32].map((ex) => <circle key={ex} cx={ex + (p.face ?? 0.9) * 34} cy={-24} r={20} fill="none" stroke={C.ink} strokeWidth={4.5} />)}</g>;
  const scarf = seed % 3 === 0 ? <path d="M-50,76 C-20,96 20,96 50,76 L46,100 C20,116 -20,116 -46,100 Z" fill={JACKET[(seed + 5) % JACKET.length]} stroke={C.ink} strokeWidth={4} /> : null;
  return <Doodle cap={false} body={jacket} blink={blinkAt(seed * 0.9 + p.x * 0.001, seed)} back={back} front={front} bodyExtra={scarf} {...p} />;
};

export const Guard: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#6a7a5a" blink={blinkAt(2.3 + p.x * 0.001, 4)}
    front={<g><path d="M-100,-30 C-110,-120 110,-120 100,-30 Z" fill="#5a6a4a" stroke={C.ink} strokeWidth={7} />
      <rect x={-104} y={-50} width={208} height={24} fill="#3a4430" stroke={C.ink} strokeWidth={5} />
      <path d="M10,-28 C60,-28 120,-30 150,-12 C120,-4 60,-8 10,-12 Z" fill="#222" stroke={C.ink} strokeWidth={4} /></g>}
    bodyExtra={<g>{[150, 200, 250].map((y) => <circle key={y} cx={10} cy={y} r={6} fill="#c9b04a" stroke={C.ink} strokeWidth={2} />)}</g>} {...p} />
);

/** a grey-haired official in a suit with big glasses (the press-conference spokesman) */
export const Official: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#4a4e5a" blink={blinkAt(1.1, 2)}
    front={<g>
      <path d="M-100,-20 C-108,-110 -40,-120 0,-118 C50,-118 106,-100 100,-20 C80,-70 40,-84 0,-84 C-50,-84 -84,-60 -100,-20 Z" fill="#c8c8cc" stroke={C.ink} strokeWidth={6} />
      {[-30, 32].map((ex) => <rect key={ex} x={ex + (p.face ?? 0) * 34 - 24} y={-46} width={48} height={40} rx={10} fill="none" stroke={C.ink} strokeWidth={5} />)}
    </g>}
    bodyExtra={<g><path d="M-30,72 L0,140 L30,72 Z" fill="#fff" stroke={C.ink} strokeWidth={4} /><path d="M-8,90 L8,90 L12,170 L0,186 L-12,170 Z" fill="#7a2a2a" stroke={C.ink} strokeWidth={3} /></g>}
    {...p} />
);

/** a politician at a podium: dark suit, side parting */
export const Speaker: React.FC<DoodleProps & {hair?: string}> = ({hair = '#7a4a24', ...p}) => (
  <Doodle cap={false} body="#22242c" blink={blinkAt(0.7 + p.x * 0.002, 1)}
    front={<path d="M-100,-24 C-110,-120 30,-140 100,-60 C96,-40 98,-30 100,-24 C80,-80 0,-96 -40,-70 C-60,-60 -86,-44 -100,-24 Z" fill={hair} stroke={C.ink} strokeWidth={6} />}
    bodyExtra={<g><path d="M-30,72 L0,140 L30,72 Z" fill="#fff" stroke={C.ink} strokeWidth={4} /><path d="M-8,90 L8,90 L12,170 L0,186 L-12,170 Z" fill="#2a4a8a" stroke={C.ink} strokeWidth={3} /></g>}
    {...p} />
);

export const OldMan: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#5a4a3a" blink={blinkAt(3.3, 5)}
    front={<g>
      <path d="M-96,-10 C-110,-90 -70,-60 -60,-90 M96,-10 C110,-90 70,-60 60,-90" fill="none" stroke="#e0e0e0" strokeWidth={22} strokeLinecap="round" />
      <path d={`M${-30 + (p.face ?? 0) * 34},40 C${-10 + (p.face ?? 0) * 34},30 ${30 + (p.face ?? 0) * 34},30 ${46 + (p.face ?? 0) * 34},40`} fill="none" stroke="#e0e0e0" strokeWidth={12} strokeLinecap="round" />
    </g>}
    {...p} />
);

export const OldLady: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#8a5a7a" blink={blinkAt(1.9, 3)}
    back={<circle cx={-20} cy={-110} r={42} fill="#d8d8dc" stroke={C.ink} strokeWidth={6} />}
    front={<path d="M-102,-10 C-110,-120 100,-130 102,-10 C70,-70 -70,-70 -102,-10 Z" fill="#d8d8dc" stroke={C.ink} strokeWidth={6} />}
    bodyExtra={<path d="M-50,76 C-20,96 20,96 50,76 L46,100 C20,116 -20,116 -46,100 Z" fill="#e8d0a0" stroke={C.ink} strokeWidth={4} />}
    {...p} />
);

export const Girl: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#f2a3c8" blink={blinkAt(0.4, 2)}
    back={<g>{[-1, 1].map((sd) => <g key={sd}><circle cx={sd * 112} cy={-30} r={34} fill="#7a4a24" stroke={C.ink} strokeWidth={6} /><circle cx={sd * 96} cy={-62} r={10} fill="#ff4a8a" stroke={C.ink} strokeWidth={3} /></g>)}</g>}
    front={<path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill="#7a4a24" stroke={C.ink} strokeWidth={6} />}
    {...p} />
);

// ------------------------------------------------------------------ props
export const Hammer: React.FC<{swing: number}> = ({swing}) => (
  <g transform={`rotate(${-30 + swing * 70})`}>
    <line x1={0} y1={10} x2={0} y2={-120} stroke="#8a5a2b" strokeWidth={14} strokeLinecap="round" />
    <rect x={-40} y={-150} width={80} height={36} rx={6} fill="#6a6a72" stroke={C.ink} strokeWidth={5} />
  </g>
);

export const Trabant: React.FC<{x: number; y: number; s?: number; t: number; color?: string; flip?: boolean}> = ({x, y, s = 1, t, color = '#a8d0c0', flip}) => (
  <g transform={`translate(${x},${y + Math.sin(t * 20) * 2}) scale(${flip ? -s : s},${s})`}>
    <path d="M-200,-60 L-190,-130 L-90,-140 L-50,-210 L110,-210 L150,-140 L210,-120 L210,-60 Z" fill={color} stroke={C.ink} strokeWidth={7} strokeLinejoin="round" />
    <path d="M-40,-200 L-70,-145 L30,-145 L30,-200 Z M45,-200 L45,-145 L135,-145 L105,-200 Z" fill="#cfe6f2" stroke={C.ink} strokeWidth={5} />
    <rect x={-200} y={-80} width={410} height={24} fill="#e8e8e8" stroke={C.ink} strokeWidth={4} />
    <circle cx={200} cy={-100} r={12} fill="#ffe28a" stroke={C.ink} strokeWidth={3} />
    {[-120, 130].map((wx) => (
      <g key={wx}><circle cx={wx} cy={-50} r={44} fill="#222" stroke={C.ink} strokeWidth={5} /><circle cx={wx} cy={-50} r={18} fill="#c9ccd2" stroke={C.ink} strokeWidth={4} /></g>
    ))}
    {[0, 1, 2].map((k) => {
      const ph = (t * 1.5 + k / 3) % 1;
      return <circle key={k} cx={-230 - ph * 160} cy={-60 - ph * 30} r={18 + ph * 30} fill="#bbb" opacity={0.5 * (1 - ph)} />;
    })}
  </g>
);

export const Heart: React.FC<{x: number; y: number; s?: number; a?: number}> = ({x, y, s = 1, a = 1}) => (
  <path transform={`translate(${x},${y}) scale(${s})`} opacity={a} d="M0,18 C-40,-10 -30,-46 0,-30 C30,-46 40,-10 0,18 Z" fill="#ff4a6a" stroke={C.ink} strokeWidth={4} />
);

export const Tear: React.FC<{x: number; y: number; t: number; s?: number}> = ({x, y, t, s = 0.6}) => <Sweat x={x} y={y} t={t} s={s} />;

export const Candle: React.FC<{x: number; y: number; s?: number; t: number; seed?: number}> = ({x, y, s = 1, t, seed = 0}) => {
  const fl = 1 + 0.15 * Math.sin(t * 13 + seed * 2.1) + 0.08 * Math.sin(t * 29 + seed);
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <circle cx={0} cy={-62} r={46 * fl} fill="#ffd86a" opacity={0.22} />
      <rect x={-14} y={-40} width={28} height={50} rx={5} fill="#f6efe0" stroke={C.ink} strokeWidth={4} />
      <path d={`M0,${-44 - 30 * fl} C14,-58 10,-44 0,-42 C-10,-44 -14,-58 0,${-44 - 30 * fl} Z`} fill="#ffb03a" stroke={C.ink} strokeWidth={3} />
    </g>
  );
};

export const Flower: React.FC<{x: number; y: number; s?: number; color?: string; rot?: number}> = ({x, y, s = 1, color = '#ff6a8a', rot = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s}) rotate(${rot})`}>
    <line x1={0} y1={0} x2={0} y2={70} stroke="#3a8a3a" strokeWidth={6} />
    {[0, 1, 2, 3, 4].map((k) => <circle key={k} cx={Math.cos((k * 2 * Math.PI) / 5) * 14} cy={Math.sin((k * 2 * Math.PI) / 5) * 14} r={11} fill={color} stroke={C.ink} strokeWidth={3} />)}
    <circle cx={0} cy={0} r={8} fill="#ffd84d" stroke={C.ink} strokeWidth={3} />
  </g>
);

export const Bouquet: React.FC = () => (
  <g transform="translate(0,-40)">
    {[-18, 0, 18].map((dx, i) => <Flower key={dx} x={dx} y={-i * 6} s={0.8} color={['#ff6a8a', '#ffd84d', '#b88aff'][i]} rot={dx} />)}
  </g>
);

export const Bottle: React.FC = () => (
  <g transform="translate(0,-20) rotate(-20)">
    <path d="M-14,40 L-14,-20 C-14,-36 -6,-40 -6,-60 L6,-60 C6,-40 14,-36 14,-20 L14,40 Z" fill="#2a6a3a" stroke={C.ink} strokeWidth={4} />
    <rect x={-8} y={-70} width={16} height={12} fill="#d8b04a" stroke={C.ink} strokeWidth={3} />
    <rect x={-14} y={0} width={28} height={22} fill="#f6efe0" stroke={C.ink} strokeWidth={3} />
  </g>
);

export const Chocolate: React.FC = () => (
  <g transform="translate(0,-14) rotate(-10)">
    <rect x={-34} y={-20} width={68} height={40} rx={4} fill="#6a3a1a" stroke={C.ink} strokeWidth={4} />
    <rect x={-34} y={-20} width={36} height={40} fill="#7a3ab8" stroke={C.ink} strokeWidth={4} />
  </g>
);

export const Papers: React.FC<{shuffle?: number}> = ({shuffle = 0}) => (
  <g transform={`rotate(${-10 + shuffle * 14})`}>
    <rect x={-40} y={-70} width={80} height={100} fill="#fff" stroke={C.ink} strokeWidth={4} transform={`rotate(${shuffle * -8})`} />
    <rect x={-36} y={-66} width={80} height={100} fill="#fbf6e8" stroke={C.ink} strokeWidth={4} />
    {[0, 1, 2, 3].map((k) => <line key={k} x1={-26} y1={-48 + k * 18} x2={30} y2={-48 + k * 18} stroke="#8a8a92" strokeWidth={3} />)}
  </g>
);

/** small piece of the Wall with a splash of paint */
export const WallPiece: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = 0}) => (
  <g transform={`translate(${x},${y}) scale(${s}) rotate(${rot})`}>
    <path d="M-60,-30 L-20,-56 L40,-48 L66,-6 L50,40 L-10,52 L-58,26 Z" fill="#b4b4b8" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
    <path d="M-30,-30 C0,-46 30,-20 20,10 C10,30 -20,20 -26,0 Z" fill="#ff4a8a" />
    <path d="M10,20 C30,10 48,20 40,36 L10,40 Z" fill="#3ad0ff" />
    <path d="M-60,-30 L-20,-56 L40,-48 L66,-6 L50,40 L-10,52 L-58,26 Z" fill="none" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
  </g>
);

/** a crowd of Berliners streaming in one direction (dir 1 = right) */
export const Crowd: React.FC<{t: number; y: number; n: number; speed?: number; dir?: number; s?: number; seed?: number; x0?: number; span?: number; cheer?: boolean; grey?: boolean}> = ({
  t, y, n, speed = 140, dir = 1, s = 0.42, seed = 0, x0 = -400, span = 2800, cheer = false, grey,
}) => {
  const R = rng(seed + 11);
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const off = R() * span;
        const x = x0 + (((off + dir * t * speed * (0.8 + R() * 0.4)) % span) + span) % span;
        const yy = y + (i % 3) * 22;
        const sw = Math.sin(t * 7 + i);
        return <Berliner key={i} seed={seed + i} grey={grey} x={x} y={feet(yy, s)} s={s} face={0.85 * dir} walk={speed ? t * 1.6 + i * 0.3 : undefined} expr={cheer ? 'laugh' : i % 3 ? 'happy' : 'o'}
          larm={cheer && i % 2 ? [2.6, 0.2] : [0.3, 0.2]} rarm={cheer ? [-2.5 + 0.3 * sw, 0.3] : i % 4 === 0 ? [-2.4 + 0.3 * sw, 0.4] : [-0.3, -0.2]} />;
      })}
    </g>
  );
};

/** heads-and-shoulders crowd silhouette for foregrounds */
export const HeadRow: React.FC<{y: number; t: number; n?: number; seed?: number; s?: number; x0?: number; dx?: number; cheer?: boolean; candles?: boolean; grey?: boolean}> = ({
  y, t, n = 12, seed = 0, s = 0.42, x0 = -60, dx = 175, cheer = true, candles, grey,
}) => (
  <g>
    {Array.from({length: n}).map((_, i) => {
      const j = cheer ? Math.abs(Math.sin(t * 5 + i * 1.3)) * 10 : 0;
      return (
        <Berliner key={i} seed={seed + i} grey={grey} x={x0 + i * dx} y={y + (i % 2) * 24 - j} s={s} face={(i % 3 - 1) * 0.3} look={[0, -1]} expr={cheer ? 'laugh' : 'flat'} showLegs={false}
          larm={cheer && i % 3 === 0 ? [2.5, 0.3] : [0.3, 0.2]} rarm={candles ? [-1.2, 1.1] : cheer && i % 2 ? [-2.5 + 0.3 * Math.sin(t * 7 + i), 0.3] : [-0.3, -0.2]}
          hold={candles ? <Candle x={0} y={0} s={1.3} t={t} seed={i} /> : undefined} />
      );
    })}
  </g>
);
