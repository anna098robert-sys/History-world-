import React from 'react';
import {random, useCurrentFrame} from 'remotion';

export const W = 1080;
export const H = 1920;
const INK = '#141414';
const MARBLE = '#f4eee0';
const MARBLE_D = '#d9cfb8';

export const CityDefs: React.FC = () => (
  <defs>
    <linearGradient id="citySky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#3f8fd8" />
      <stop offset="100%" stopColor="#bfe2f5" />
    </linearGradient>
    <linearGradient id="warSky" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#2a1a18" />
      <stop offset="50%" stopColor="#8a3a1e" />
      <stop offset="100%" stopColor="#f0a25a" />
    </linearGradient>
    <linearGradient id="hall" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#5a3a2a" />
      <stop offset="100%" stopColor="#8a5a3a" />
    </linearGradient>
    <pattern id="meander" width="48" height="24" patternUnits="userSpaceOnUse">
      <rect width="48" height="24" fill="#b3201a" />
      <path d="M2 22 L2 2 L22 2 L22 16 L10 16 L10 10 L16 10 M26 22 L26 2 L46 2 L46 16 L34 16 L34 10 L40 10" stroke="#f2d27a" strokeWidth={3} fill="none" />
    </pattern>
  </defs>
);

/* ------------------------------------------------------------ buildings */
export const Column: React.FC<{x: number; y: number; h: number; w?: number}> = ({x, y, h, w = 44}) => (
  <g>
    <rect x={x - w / 2} y={y - h} width={w} height={h} fill={MARBLE} stroke={INK} strokeWidth={5} />
    {[-0.25, 0, 0.25].map((k) => (
      <line key={k} x1={x + k * w} x2={x + k * w} y1={y - h + 20} y2={y - 10} stroke={MARBLE_D} strokeWidth={4} />
    ))}
    <rect x={x - w * 0.75} y={y - h - 18} width={w * 1.5} height={20} fill={MARBLE} stroke={INK} strokeWidth={5} />
    <rect x={x - w * 0.65} y={y - 12} width={w * 1.3} height={12} fill={MARBLE_D} stroke={INK} strokeWidth={4} />
  </g>
);

/** Colonnaded stoa / temple front. */
export const Stoa: React.FC<{x: number; y: number; w: number; h?: number; cols?: number; pediment?: boolean}> = ({x, y, w, h = 420, cols = 5, pediment = true}) => (
  <g>
    <rect x={x} y={y - h} width={w} height={h} fill="#e9dcc0" stroke={INK} strokeWidth={6} />
    <rect x={x + 20} y={y - h + 40} width={w - 40} height={h - 40} fill="#c9b48e" />
    {new Array(cols).fill(0).map((_, i) => (
      <Column key={i} x={x + 40 + (i * (w - 80)) / (cols - 1)} y={y} h={h - 60} />
    ))}
    <rect x={x - 20} y={y - h - 20} width={w + 40} height={44} fill={MARBLE} stroke={INK} strokeWidth={6} />
    <rect x={x - 20} y={y - h + 6} width={w + 40} height={16} fill="url(#meander)" />
    {pediment && <path d={`M${x - 30} ${y - h - 20} L${x + w / 2} ${y - h - 20 - w * 0.22} L${x + w + 30} ${y - h - 20} Z`} fill={MARBLE} stroke={INK} strokeWidth={6} />}
  </g>
);

/** Whitewashed house with terracotta tile roof. */
export const GreekHouse: React.FC<{x: number; y: number; w: number; h: number; seed?: number; shutters?: number}> = ({x, y, w, h, seed = 0, shutters = 0}) => {
  const wall = ['#f3ead6', '#efe0c4', '#f7f1e3', '#ead8b8'][seed % 4];
  const door = ['#2f6f9a', '#7a3a24', '#3f7a4a'][seed % 3];
  return (
    <g>
      <rect x={x} y={y - h} width={w} height={h} fill={wall} stroke={INK} strokeWidth={6} />
      <path d={`M${x - 24} ${y - h} L${x + w / 2} ${y - h - 80} L${x + w + 24} ${y - h} Z`} fill="#c0582e" stroke={INK} strokeWidth={6} />
      {new Array(6).fill(0).map((_, i) => (
        <line key={i} x1={x + (i * w) / 5} y1={y - h - 4} x2={x + w / 2 + (i - 2.5) * 10} y2={y - h - 70} stroke="#8a3a1e" strokeWidth={3} />
      ))}
      <rect x={x + w * 0.38} y={y - 150} width={w * 0.24} height={150} rx={6} fill={door} stroke={INK} strokeWidth={5} />
      {/* window with wooden shutters (close when scared) */}
      <rect x={x + w * 0.3} y={y - h + 50} width={w * 0.4} height={90} fill="#1d1712" stroke={INK} strokeWidth={5} />
      <rect x={x + w * 0.3} y={y - h + 50} width={w * 0.2 * shutters} height={90} fill={door} stroke={INK} strokeWidth={4} />
      <rect x={x + w * 0.7 - w * 0.2 * shutters} y={y - h + 50} width={w * 0.2 * shutters} height={90} fill={door} stroke={INK} strokeWidth={4} />
      {/* potted plant */}
      <path d={`M${x + 20} ${y} L${x + 30} ${y - 50} L${x + 70} ${y - 50} L${x + 80} ${y} Z`} fill="#c0582e" stroke={INK} strokeWidth={4} />
      <ellipse cx={x + 50} cy={y - 70} rx={34} ry={26} fill="#5f8a3c" stroke={INK} strokeWidth={4} />
    </g>
  );
};

export const Amphora: React.FC<{x: number; y: number; s?: number; c?: string}> = ({x, y, s = 1, c = '#c0582e'}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-14 -110 L14 -110 L12 -90 Q40 -70 30 -30 Q20 0 0 6 Q-20 0 -30 -30 Q-40 -70 -12 -90 Z" fill={c} stroke={INK} strokeWidth={5} />
    <path d="M-12 -96 Q-34 -96 -24 -70 M12 -96 Q34 -96 24 -70" stroke={INK} strokeWidth={5} fill="none" />
    <path d="M-28 -50 L28 -50" stroke="#141414" strokeWidth={6} />
  </g>
);

/** Side-scrolling Greek city street: houses, a stoa, market stall, amphorae. */
export const CityStreet: React.FC<{scroll: number; groundY?: number; shutters?: number; sky?: string}> = ({scroll, groundY = 1560, shutters = 0, sky = 'url(#citySky)'}) => {
  const unit = 1500;
  const start = Math.floor(scroll / unit) - 1;
  const blocks = [];
  for (let b = start; b < start + 3; b++) {
    const ox = b * unit - scroll;
    blocks.push(
      <g key={b} transform={`translate(${ox} 0)`}>
        <GreekHouse x={20} y={groundY} w={300} h={420} seed={Math.abs(b) * 3} shutters={shutters} />
        <Stoa x={380} y={groundY} w={520} h={500} cols={5} />
        <GreekHouse x={960} y={groundY} w={260} h={380} seed={Math.abs(b) * 3 + 1} shutters={shutters} />
        {/* market stall with awning */}
        <g>
          <rect x={1260} y={groundY - 160} width={220} height={160} fill="#a8743c" stroke={INK} strokeWidth={5} />
          <path d={`M1240 ${groundY - 160} L1500 ${groundY - 160} L1480 ${groundY - 230} L1260 ${groundY - 230} Z`} fill="#2f7fa0" stroke={INK} strokeWidth={5} />
          {[0, 1, 2, 3].map((k) => (
            <path key={k} d={`M${1260 + k * 60} ${groundY - 160} L${1290 + k * 60} ${groundY - 160} L${1285 + k * 60} ${groundY - 228} L${1268 + k * 60} ${groundY - 228} Z`} fill="#f2ead8" />
          ))}
          <Amphora x={1300} y={groundY - 160} s={0.6} />
          <Amphora x={1360} y={groundY - 160} s={0.55} c="#1d1712" />
          <circle cx={1420} cy={groundY - 175} r={16} fill="#6b8a2c" stroke={INK} strokeWidth={3} />
          <circle cx={1445} cy={groundY - 172} r={14} fill="#6b8a2c" stroke={INK} strokeWidth={3} />
        </g>
      </g>,
    );
  }
  return (
    <g>
      <rect x={-300} y={-300} width={W + 600} height={groundY + 300} fill={sky} />
      {/* acropolis on the hill */}
      <path d={`M-300 ${groundY - 480} Q300 ${groundY - 760} 900 ${groundY - 560} L1400 ${groundY - 500} L1400 ${groundY} L-300 ${groundY} Z`} fill="#a9b88c" />
      <g transform={`translate(${520 - scroll * 0.08} ${groundY - 690}) scale(0.4)`}>
        <Stoa x={-300} y={0} w={600} h={300} cols={8} />
      </g>
      {blocks}
      <rect x={-300} y={groundY} width={W + 600} height={H - groundY + 300} fill="#cfae74" />
      {new Array(12).fill(0).map((_, i) => {
        const sx = ((i * 180 - scroll) % 2160 + 2160) % 2160 - 300;
        return <rect key={i} x={sx} y={groundY + 30 + (i % 3) * 90} width={150} height={60} rx={10} fill="rgba(0,0,0,0.08)" />;
      })}
      <line x1={-300} x2={W + 300} y1={groundY} y2={groundY} stroke={INK} strokeWidth={8} />
    </g>
  );
};

/* ------------------------------------------------------------- people */
type Robe = {robe: string; trim: string; skin: string; hair: string};
const ROBES: Robe[] = [
  {robe: '#f2ead8', trim: '#2f7fa0', skin: '#e9be9a', hair: '#3a2a1a'},
  {robe: '#c46a3a', trim: '#f2d27a', skin: '#d9a57f', hair: '#1d1712'},
  {robe: '#6b8a4c', trim: '#f2ead8', skin: '#f0c9a6', hair: '#6b4a2a'},
  {robe: '#8a6ab0', trim: '#f2d27a', skin: '#e9be9a', hair: '#2a1a12'},
];

/** Ancient Greek citizen in chiton/himation. */
export const Citizen: React.FC<{
  x: number;
  y: number;
  s?: number;
  seed?: number;
  facing?: 1 | -1;
  mood?: 'calm' | 'scared' | 'angry';
  female?: boolean;
  run?: number;
  child?: boolean;
}> = ({x, y, s = 1, seed = 0, facing = 1, mood = 'calm', female = false, run, child = false}) => {
  const r = ROBES[seed % ROBES.length];
  const f = useCurrentFrame();
  const isRun = run !== undefined;
  const sw = isRun ? Math.sin(run!) : 0;
  const bob = isRun ? Math.abs(Math.cos(run!)) * 10 : 0;
  const tremble = mood === 'scared' ? Math.sin(f * 2.1) * 2 : 0;
  const sc = child ? s * 0.6 : s;
  return (
    <g transform={`translate(${x + tremble} ${y - bob}) scale(${sc * facing} ${sc})`}>
      <ellipse cx={0} cy={2} rx={48} ry={9} fill="rgba(0,0,0,0.25)" />
      {/* sandalled feet */}
      <ellipse cx={-14 + sw * 30} cy={-6} rx={16} ry={7} fill="#6b4a2a" />
      <ellipse cx={14 - sw * 30} cy={-6} rx={16} ry={7} fill="#6b4a2a" />
      {/* robe */}
      <path d={`M-34 -200 L-44 ${-4} L44 ${-4} L34 -200 Z`} fill={r.robe} stroke={INK} strokeWidth={6} />
      <path d="M-34 -200 L30 -60" stroke={r.trim} strokeWidth={14} />
      <path d={`M-44 -18 L44 -18`} stroke={r.trim} strokeWidth={8} />
      {/* arms */}
      <g transform={`translate(-28 -185) rotate(${mood === 'scared' ? -150 : isRun ? -sw * 45 : 12})`}>
        <line x1={0} y1={0} x2={0} y2={78} stroke={r.skin} strokeWidth={14} strokeLinecap="round" />
      </g>
      <g transform={`translate(28 -185) rotate(${mood === 'scared' ? 150 : mood === 'angry' ? -100 : isRun ? sw * 45 : -12})`}>
        <line x1={0} y1={0} x2={0} y2={78} stroke={r.skin} strokeWidth={14} strokeLinecap="round" />
      </g>
      {/* head */}
      <circle cx={0} cy={-232} r={32} fill={r.skin} stroke={INK} strokeWidth={5} />
      {female ? (
        <path d="M-34 -236 Q-36 -276 0 -274 Q34 -276 34 -236 Q28 -256 0 -258 Q-28 -256 -34 -236 Z M18 -262 Q44 -262 40 -236" fill={r.hair} stroke={INK} strokeWidth={4} />
      ) : (
        <>
          <path d="M-32 -244 Q-30 -272 0 -270 Q30 -272 32 -244 Q18 -258 -32 -244 Z" fill={r.hair} stroke={INK} strokeWidth={4} />
          {!child && <path d="M-24 -226 Q-22 -192 4 -190 Q28 -192 30 -222 Q14 -208 -24 -226 Z" fill={r.hair} stroke={INK} strokeWidth={4} />}
        </>
      )}
      <circle cx={12} cy={-238} r={4} fill={INK} />
      {mood === 'scared' && <ellipse cx={14} cy={-214} rx={6} ry={9} fill={INK} />}
      {mood === 'angry' && <path d="M2 -250 L22 -244" stroke={INK} strokeWidth={5} />}
      {mood === 'calm' && <path d="M6 -218 Q14 -212 22 -218" stroke={INK} strokeWidth={3} fill="none" />}
    </g>
  );
};

/** The important official: grey beard, white himation with blue border. */
export const Official: React.FC<{x: number; y: number; s?: number; armR?: number; armL?: number; talk?: number; facing?: 1 | -1}> = ({x, y, s = 1, armR = -20, armL = 20, talk = 0, facing = -1}) => (
  <g transform={`translate(${x} ${y}) scale(${s * facing} ${s})`}>
    <ellipse cx={0} cy={4} rx={70} ry={12} fill="rgba(0,0,0,0.25)" />
    <path d="M-50 -280 L-62 0 L62 0 L50 -280 Z" fill="#f4eee0" stroke={INK} strokeWidth={7} />
    <path d="M-50 -280 L40 -40 L62 0" stroke="#2f5f9a" strokeWidth={16} fill="none" />
    <path d="M-62 -20 L62 -20" stroke="#2f5f9a" strokeWidth={10} />
    <g transform={`translate(-40 -262) rotate(${armL})`}>
      <line x1={0} y1={0} x2={0} y2={110} stroke="#f4eee0" strokeWidth={26} strokeLinecap="round" />
      <line x1={0} y1={0} x2={0} y2={110} stroke={INK} strokeWidth={3} opacity={0.3} />
      <circle cx={0} cy={118} r={14} fill="#e9be9a" stroke={INK} strokeWidth={4} />
    </g>
    <g transform={`translate(40 -262) rotate(${armR})`}>
      <line x1={0} y1={0} x2={0} y2={110} stroke="#f4eee0" strokeWidth={26} strokeLinecap="round" />
      <circle cx={0} cy={118} r={14} fill="#e9be9a" stroke={INK} strokeWidth={4} />
    </g>
    <g transform="translate(0 -330)">
      <circle r={52} fill="#e9be9a" stroke={INK} strokeWidth={6} />
      <path d="M-50 -10 Q-56 -60 0 -58 Q56 -60 50 -10 Q30 -40 -50 -10 Z" fill="#b8b2a8" stroke={INK} strokeWidth={5} />
      {/* long grey beard */}
      <path d="M-44 6 Q-48 90 10 100 Q56 90 50 4 Q30 30 0 26 Q-24 30 -44 6 Z" fill="#cfc9be" stroke={INK} strokeWidth={5} />
      <path d={`M2 ${28 + talk * 4} Q14 ${34 + talk * 10} 26 ${28 + talk * 4}`} stroke={INK} strokeWidth={4} fill={talk > 0.2 ? '#3a1a12' : 'none'} />
      <circle cx={20} cy={-6} r={5} fill={INK} />
      <path d="M8 -22 L32 -20" stroke={INK} strokeWidth={5} />
      {/* olive wreath */}
      <path d="M-50 -24 Q0 -70 50 -24" stroke="#5f8a3c" strokeWidth={10} fill="none" strokeDasharray="14 6" />
    </g>
  </g>
);

/** The angry king: big black beard, gold diadem, purple robe. rage 0..1 reddens the face. */
export const King: React.FC<{
  x: number;
  y: number;
  s?: number;
  rage?: number;
  armR?: number;
  armL?: number;
  mouth?: number; // 0 closed … 1 roaring
  facing?: 1 | -1;
  seated?: boolean;
  eyes?: 'angry' | 'squint' | 'wide';
}> = ({x, y, s = 1, rage = 0, armR = -20, armL = 20, mouth = 0, facing = -1, seated = false, eyes = 'angry'}) => {
  const f = useCurrentFrame();
  const skinR = Math.round(233 + rage * 10);
  const skinG = Math.round(190 - rage * 130);
  const skinB = Math.round(154 - rage * 110);
  const skin = `rgb(${skinR},${skinG},${skinB})`;
  return (
    <g transform={`translate(${x} ${y}) scale(${s * facing} ${s})`}>
      {!seated && <ellipse cx={0} cy={4} rx={80} ry={12} fill="rgba(0,0,0,0.3)" />}
      <path d={seated ? 'M-64 -300 L-74 -120 L74 -120 L64 -300 Z' : 'M-64 -300 L-76 0 L76 0 L64 -300 Z'} fill="#5a2a7a" stroke={INK} strokeWidth={7} />
      <path d={seated ? 'M-74 -132 L74 -132' : 'M-76 -24 L76 -24'} stroke="url(#meander)" strokeWidth={22} />
      <path d="M-30 -300 L0 -200 L30 -300" fill="#f2ead8" stroke={INK} strokeWidth={5} />
      {seated && <path d="M-74 -120 L-60 0 M74 -120 L60 0" stroke="#5a2a7a" strokeWidth={30} />}
      <g transform={`translate(-54 -282) rotate(${armL})`}>
        <line x1={0} y1={0} x2={0} y2={120} stroke="#5a2a7a" strokeWidth={30} strokeLinecap="round" />
        <circle cx={0} cy={128} r={17} fill={skin} stroke={INK} strokeWidth={5} />
      </g>
      <g transform={`translate(54 -282) rotate(${armR})`}>
        <line x1={0} y1={0} x2={0} y2={120} stroke="#5a2a7a" strokeWidth={30} strokeLinecap="round" />
        <circle cx={0} cy={128} r={17} fill={skin} stroke={INK} strokeWidth={5} />
        {armR < -100 && <path d="M0 140 L0 186" stroke={skin} strokeWidth={12} strokeLinecap="round" />}
      </g>
      <g transform={`translate(0 -360) rotate(${rage > 0.8 ? Math.sin(f * 1.8) * 3 : 0})`}>
        <circle r={60} fill={skin} stroke={INK} strokeWidth={7} />
        {/* big black curly beard */}
        <path d="M-58 0 Q-70 110 6 124 Q76 110 60 -2 Q40 36 0 32 Q-36 36 -58 0 Z" fill="#1d1712" stroke={INK} strokeWidth={5} />
        {[-36, -12, 12, 36].map((bx) => (
          <path key={bx} d={`M${bx} 60 q8 14 0 28`} stroke="#3a2a1a" strokeWidth={5} fill="none" />
        ))}
        <path d="M-60 -10 Q-64 -70 0 -66 Q64 -70 60 -10 Q34 -44 -60 -10 Z" fill="#1d1712" stroke={INK} strokeWidth={5} />
        {/* mouth */}
        <ellipse cx={18} cy={36} rx={16 + mouth * 6} ry={3 + mouth * 22} fill="#3a0e0a" stroke={INK} strokeWidth={4} />
        {/* eyes + brows */}
        {eyes === 'wide' ? (
          <>
            <circle cx={4} cy={-8} r={10} fill="#fff" stroke={INK} strokeWidth={3} />
            <circle cx={36} cy={-8} r={10} fill="#fff" stroke={INK} strokeWidth={3} />
            <circle cx={6} cy={-8} r={4} fill={INK} />
            <circle cx={38} cy={-8} r={4} fill={INK} />
          </>
        ) : (
          <>
            <circle cx={6} cy={-6} r={eyes === 'squint' ? 3 : 5} fill={INK} />
            <circle cx={36} cy={-6} r={eyes === 'squint' ? 3 : 5} fill={INK} />
          </>
        )}
        <path d="M-12 -30 L18 -18 M54 -30 L26 -18" stroke={INK} strokeWidth={9} strokeLinecap="round" />
        {/* gold diadem */}
        <path d="M-58 -36 L-46 -76 L-24 -50 L0 -88 L24 -50 L46 -76 L58 -36 Z" fill="#f2c230" stroke={INK} strokeWidth={5} />
        <circle cx={0} cy={-60} r={8} fill="#c41a12" stroke={INK} strokeWidth={3} />
        {/* steam! */}
        {rage > 0.6 &&
          [-1, 1].map((d) => {
            const p = (f % 12) / 12;
            return (
              <g key={d} opacity={1 - p}>
                <circle cx={d * (70 + p * 40)} cy={-40 - p * 80} r={18 + p * 22} fill="#ffffff" stroke="#c9c9c9" strokeWidth={3} />
              </g>
            );
          })}
      </g>
    </g>
  );
};

/** Throne room: columns, meander frieze, red curtains, throne, table. */
export const ThroneRoom: React.FC<{floorY?: number}> = ({floorY = 1600}) => (
  <g>
    <rect x={-300} y={-300} width={W + 600} height={floorY + 300} fill="url(#hall)" />
    <rect x={-300} y={300} width={W + 600} height={40} fill="url(#meander)" />
    {/* wall fresco: dolphins */}
    <rect x={240} y={420} width={600} height={260} fill="#bfe2f5" stroke={INK} strokeWidth={6} />
    {[0, 1, 2].map((i) => (
      <path key={i} d={`M${300 + i * 180} ${560 + (i % 2) * 30} q40 -60 100 -10 q-20 10 -30 30 l20 20 l-40 -10 q-40 10 -50 -30 Z`} fill="#2f7fa0" stroke={INK} strokeWidth={4} />
    ))}
    {[-60, 200, 880, 1140].map((cx) => (
      <Column key={cx} x={cx} y={floorY} h={1250} w={90} />
    ))}
    {/* curtains */}
    <path d="M-100 330 Q120 700 40 1500 L-100 1500 Z" fill="#9a1d17" stroke={INK} strokeWidth={6} />
    <path d="M1180 330 Q960 700 1040 1500 L1180 1500 Z" fill="#9a1d17" stroke={INK} strokeWidth={6} />
    <rect x={-300} y={floorY} width={W + 600} height={H - floorY + 300} fill="#c9b48e" />
    {new Array(10).fill(0).map((_, i) => (
      <path key={i} d={`M${-200 + i * 160} ${floorY} L${-500 + i * 220} ${H + 100}`} stroke="rgba(0,0,0,0.12)" strokeWidth={5} />
    ))}
    <line x1={-300} x2={W + 300} y1={floorY} y2={floorY} stroke={INK} strokeWidth={8} />
  </g>
);

export const Throne: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <rect x={-120} y={-520} width={240} height={420} rx={20} fill="#f2c230" stroke={INK} strokeWidth={8} />
    <rect x={-90} y={-490} width={180} height={340} rx={12} fill="#7a2a9a" stroke={INK} strokeWidth={5} />
    <rect x={-140} y={-140} width={280} height={60} rx={10} fill="#f2c230" stroke={INK} strokeWidth={8} />
    <rect x={-130} y={-80} width={36} height={80} fill="#d9962e" stroke={INK} strokeWidth={6} />
    <rect x={94} y={-80} width={36} height={80} fill="#d9962e" stroke={INK} strokeWidth={6} />
    <circle cx={0} cy={-540} r={30} fill="#f2c230" stroke={INK} strokeWidth={6} />
  </g>
);

export const Table: React.FC<{x: number; y: number; w?: number; jump?: number}> = ({x, y, w = 420, jump = 0}) => (
  <g transform={`translate(${x} ${y})`}>
    <rect x={-w / 2} y={-200} width={w} height={34} rx={6} fill="#8a5a2e" stroke={INK} strokeWidth={6} />
    <path d={`M${-w / 2 + 30} -166 L${-w / 2 + 40} 0 M${w / 2 - 30} -166 L${w / 2 - 40} 0`} stroke="#6b4220" strokeWidth={18} />
    {/* drinking cups (kylix) and fruit bowl jump on slam */}
    <g transform={`translate(${-w / 4} ${-200 - jump * 60}) rotate(${jump * -25})`}>
      <path d="M-34 0 Q0 30 34 0 Z" fill="#1d1712" stroke={INK} strokeWidth={4} />
      <rect x={-5} y={10} width={10} height={20} fill="#1d1712" />
      <path d="M-34 0 Q0 22 34 0" stroke="#c0582e" strokeWidth={4} fill="none" />
    </g>
    <g transform={`translate(${w / 4} ${-200 - jump * 80}) rotate(${jump * 30})`}>
      <path d="M-40 0 Q0 40 40 0 Z" fill="#c0582e" stroke={INK} strokeWidth={4} />
      <circle cx={-14} cy={-10} r={14} fill="#6b2a7a" stroke={INK} strokeWidth={3} />
      <circle cx={10} cy={-14} r={14} fill="#e2a23a" stroke={INK} strokeWidth={3} />
    </g>
  </g>
);

/* ------------------------------------------------------- scrolls & icons */
/**
 * Rolled papyrus letter with a wax seal. color tells the two letters apart:
 * BLUE = peace offer (for the king), RED = private joke (not for the king).
 */
export const Scroll: React.FC<{x: number; y: number; s?: number; rot?: number; seal: 'red' | 'blue'; broken?: boolean}> = ({x, y, s = 1, rot = 0, seal, broken = false}) => (
  <g transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`}>
    <rect x={-70} y={-24} width={140} height={48} rx={22} fill="#f0dfb0" stroke={INK} strokeWidth={6} />
    <ellipse cx={-70} cy={0} rx={10} ry={24} fill="#d9c58e" stroke={INK} strokeWidth={5} />
    <ellipse cx={70} cy={0} rx={10} ry={24} fill="#d9c58e" stroke={INK} strokeWidth={5} />
    <rect x={-6} y={-26} width={12} height={52} fill={seal === 'red' ? '#9a1d17' : '#1f4f8a'} />
    {!broken ? (
      <circle cx={0} cy={0} r={22} fill={seal === 'red' ? '#d02a1e' : '#2f6fc0'} stroke={INK} strokeWidth={5} />
    ) : (
      <g fill={seal === 'red' ? '#d02a1e' : '#2f6fc0'} stroke={INK} strokeWidth={4}>
        <path d="M-22 0 L-4 -20 L2 0 L-6 18 Z" />
        <path d="M6 -18 L22 0 L8 20 L4 2 Z" />
      </g>
    )}
  </g>
);

/** The unrolled red letter: a rude doodle of the king with donkey ears (no writing). */
export const OpenLetter: React.FC<{x: number; y: number; s?: number; unroll: number}> = ({x, y, s = 1, unroll}) => {
  const h = 520 * unroll;
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <rect x={-300} y={-h / 2} width={600} height={h} fill="#f3e4b8" stroke={INK} strokeWidth={8} />
      <rect x={-320} y={-h / 2 - 30} width={640} height={44} rx={20} fill="#d9c58e" stroke={INK} strokeWidth={6} />
      <rect x={-320} y={h / 2 - 14} width={640} height={44} rx={20} fill="#d9c58e" stroke={INK} strokeWidth={6} />
      {unroll > 0.7 && (
        <g opacity={(unroll - 0.7) / 0.3} stroke="#3a2a1a" strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round">
          {/* donkey ears */}
          <path d="M-70 -110 L-110 -240 L-40 -140" fill="#d9c9a0" />
          <path d="M70 -110 L110 -240 L40 -140" fill="#d9c9a0" />
          {/* king face + crown + beard, drawn badly */}
          <circle cx={0} cy={-40} r={100} />
          <path d="M-70 -120 L-50 -170 L-20 -130 L0 -180 L20 -130 L50 -170 L70 -120" />
          <circle cx={-34} cy={-60} r={10} fill="#3a2a1a" />
          <circle cx={34} cy={-56} r={18} />
          <path d="M-40 10 Q0 -10 40 20" />
          <path d="M-90 10 Q-80 160 0 170 Q80 160 90 10" />
          {/* tongue out */}
          <path d="M0 4 Q10 40 26 20" fill="#e07a7a" />
          {/* stink lines */}
          <path d="M-170 -30 q-20 -20 0 -40 q20 -20 0 -40 M170 -30 q20 -20 0 -40 q-20 -20 0 -40" />
          {/* tiny smiley signature */}
          <circle cx={210} cy={180} r={22} />
          <path d="M200 186 Q210 196 220 186" />
        </g>
      )}
    </g>
  );
};

/** Thought/speech bubble holding icons (no text). */
export const IconBubble: React.FC<{x: number; y: number; s?: number; children: React.ReactNode; tail?: 'left' | 'right'}> = ({x, y, s = 1, children, tail = 'left'}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path
      d={`M-200 -120 Q-200 -160 -160 -160 L160 -160 Q200 -160 200 -120 L200 60 Q200 100 160 100 L${tail === 'left' ? '-40' : '80'} 100 L${tail === 'left' ? '-110' : '150'} 170 L${tail === 'left' ? '-90' : '120'} 100 L-160 100 Q-200 100 -200 60 Z`}
      fill="#fff"
      stroke={INK}
      strokeWidth={9}
    />
    {children}
  </g>
);

export const CrownIcon: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <path transform={`translate(${x} ${y}) scale(${s})`} d="M-50 30 L-50 -20 L-25 10 L0 -36 L25 10 L50 -20 L50 30 Z" fill="#f2c230" stroke={INK} strokeWidth={6} strokeLinejoin="round" />
);
export const FriendIcon: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={40} fill="#ffd400" stroke={INK} strokeWidth={6} />
    <circle cx={-14} cy={-8} r={5} fill={INK} />
    <circle cx={14} cy={-8} r={5} fill={INK} />
    <path d="M-18 10 Q0 30 18 10" stroke={INK} strokeWidth={5} fill="none" />
  </g>
);
export const OliveIcon: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <path d="M-40 30 Q0 0 40 -36" stroke="#6b4a2a" strokeWidth={6} fill="none" />
    {[-24, -4, 16, 32].map((p, i) => (
      <ellipse key={i} cx={p} cy={18 - (p + 30) * 0.7} rx={14} ry={7} fill="#5f8a3c" stroke={INK} strokeWidth={3} transform={`rotate(-40 ${p} ${18 - (p + 30) * 0.7})`} />
    ))}
  </g>
);
export const Arrow: React.FC<{x: number; y: number; s?: number; rot?: number}> = ({x, y, s = 1, rot = 0}) => (
  <path transform={`translate(${x} ${y}) rotate(${rot}) scale(${s})`} d="M-40 -10 L10 -10 L10 -26 L40 0 L10 26 L10 10 L-40 10 Z" fill="#141414" />
);

/* -------------------------------------------------------- cavalry */
export const Horseman: React.FC<{x: number; y: number; s?: number; facing?: 1 | -1; phase: number; coat?: string; cloak?: string}> = ({x, y, s = 1, facing = 1, phase, coat = '#7a4a2a', cloak = '#b3201a'}) => {
  const g = Math.sin(phase);
  const bob = Math.abs(Math.cos(phase)) * 16;
  const leg = (lx: number, a: number) => (
    <g transform={`translate(${lx} -170) rotate(${a})`}>
      <path d="M0 0 L0 80 L6 150" stroke={coat} strokeWidth={22} fill="none" strokeLinecap="round" />
      <path d="M0 0 L0 80 L6 150" stroke={INK} strokeWidth={3} fill="none" opacity={0.4} />
      <rect x={-6} y={146} width={26} height={16} rx={4} fill="#1d1712" />
    </g>
  );
  return (
    <g transform={`translate(${x} ${y - bob * s}) scale(${s * facing} ${s})`}>
      <ellipse cx={0} cy={bob + 6} rx={150} ry={16} fill="rgba(0,0,0,0.25)" />
      {leg(-100, -g * 40)}
      {leg(90, g * 45)}
      {/* body */}
      <ellipse cx={0} cy={-210} rx={150} ry={70} fill={coat} stroke={INK} strokeWidth={7} />
      {leg(-70, g * 35)}
      {leg(120, -g * 40)}
      {/* tail */}
      <path d={`M-145 -230 Q-210 ${-200 + g * 20} -200 -130`} stroke="#1d1712" strokeWidth={24} fill="none" strokeLinecap="round" />
      {/* neck + head */}
      <path d="M100 -250 L170 -360 L210 -340 L150 -220 Z" fill={coat} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      <path d="M170 -360 Q230 -380 260 -320 L240 -300 Q210 -320 190 -320 Z" fill={coat} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      <circle cx={208} cy={-344} r={6} fill={INK} />
      <path d="M150 -340 Q130 -300 120 -250" stroke="#1d1712" strokeWidth={16} fill="none" />
      {/* rider: helmet + cloak */}
      <g transform="translate(0 -270)">
        <path d={`M-20 -10 Q-80 ${-60 + g * 10} -110 ${-10 + g * 20} L-20 10 Z`} fill={cloak} stroke={INK} strokeWidth={5} />
        <rect x={-26} y={-120} width={52} height={110} rx={10} fill="#f4ecd6" stroke={INK} strokeWidth={6} />
        <path d="M-10 0 L-30 70 M10 0 L30 60" stroke="#e8b58a" strokeWidth={14} strokeLinecap="round" />
        <circle cx={0} cy={-150} r={32} fill="url(#bronze)" stroke={INK} strokeWidth={6} />
        <path d="M-30 -168 Q0 -230 34 -170" fill={cloak} stroke={INK} strokeWidth={5} />
        <path d="M20 -100 L110 -170" stroke="#7a5228" strokeWidth={8} />
        <path d="M110 -170 L126 -186 L118 -160 Z" fill="#c9ced6" stroke={INK} strokeWidth={3} />
      </g>
    </g>
  );
};

/** Bearded general in crested helmet (for the war council). */
export const General: React.FC<{x: number; y: number; s?: number; facing?: 1 | -1; armR?: number; shout?: number; crest?: string}> = ({x, y, s = 1, facing = 1, armR = -20, shout = 0, crest = '#c41a12'}) => (
  <g transform={`translate(${x} ${y}) scale(${s * facing} ${s})`}>
    <path d="M-50 -260 L-56 0 L56 0 L50 -260 Z" fill={crest === '#c41a12' ? '#b3201a' : '#2a5d9a'} stroke={INK} strokeWidth={7} />
    <path d="M-40 -260 L-44 -120 L44 -120 L40 -260 Z" fill="url(#bronze)" stroke={INK} strokeWidth={6} />
    <path d="M-30 -220 Q0 -200 30 -220 M-30 -180 Q0 -160 30 -180" stroke="#8a5512" strokeWidth={5} fill="none" />
    <g transform={`translate(40 -240) rotate(${armR})`}>
      <line x1={0} y1={0} x2={0} y2={110} stroke="#e8b58a" strokeWidth={24} strokeLinecap="round" />
      <circle cx={0} cy={118} r={15} fill="#e8b58a" stroke={INK} strokeWidth={4} />
    </g>
    <g transform="translate(0 -320)">
      <circle r={54} fill="#e8b58a" stroke={INK} strokeWidth={6} />
      <path d="M-50 10 Q-50 80 6 86 Q54 80 52 8 Q30 30 0 28 Q-26 30 -50 10 Z" fill="#3a2a1a" stroke={INK} strokeWidth={5} />
      <ellipse cx={20} cy={34} rx={12} ry={3 + shout * 16} fill="#3a0e0a" />
      <circle cx={22} cy={-6} r={5} fill={INK} />
      <path d="M6 -24 L36 -12" stroke={INK} strokeWidth={7} strokeLinecap="round" />
      {/* helmet pushed up on the head, crest on top */}
      <path d="M-56 -20 Q-56 -76 0 -78 Q56 -76 56 -20 Z" fill="url(#bronze)" stroke={INK} strokeWidth={6} />
      <path d="M-60 -60 Q-10 -150 60 -66 L50 -56 Q-6 -110 -50 -48 Z" fill={crest} stroke={INK} strokeWidth={5} />
    </g>
  </g>
);

/** Hoplite busy sharpening a short sword (xiphos) on a whetstone, close-up. */
export const Sharpener: React.FC<{x: number; y: number; s?: number; phase: number}> = ({x, y, s = 1, phase}) => {
  const stroke = Math.sin(phase);
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {/* whetstone on block */}
      <rect x={-220} y={20} width={440} height={140} fill="#7a5a3a" stroke={INK} strokeWidth={7} />
      <rect x={-160} y={-30} width={320} height={56} rx={10} fill="#8a8f96" stroke={INK} strokeWidth={7} />
      {/* sword sliding back and forth */}
      <g transform={`translate(${stroke * 110} -40) rotate(-8)`}>
        <path d="M-60 0 L240 -8 L270 0 L240 8 Z" fill="#c9ced6" stroke={INK} strokeWidth={6} />
        <line x1={-40} y1={0} x2={230} y2={0} stroke="#eef1f4" strokeWidth={4} />
        <rect x={-80} y={-26} width={22} height={52} rx={6} fill="#d9962e" stroke={INK} strokeWidth={5} />
        <rect x={-150} y={-12} width={72} height={24} rx={8} fill="#6b4220" stroke={INK} strokeWidth={5} />
        {/* hands */}
        <circle cx={-114} cy={0} r={26} fill="#e8b58a" stroke={INK} strokeWidth={5} />
        <circle cx={120} cy={-14} r={22} fill="#e8b58a" stroke={INK} strokeWidth={5} />
      </g>
      {/* sparks */}
      {Math.abs(stroke) > 0.4 &&
        new Array(8).fill(0).map((_, i) => {
          const a = -Math.PI / 2 + (random(`sk${i}${Math.floor(phase * 3)}`) - 0.5) * 2;
          const r = 40 + random(`skr${i}${Math.floor(phase * 3)}`) * 120;
          return <line key={i} x1={stroke * 110} y1={-40} x2={stroke * 110 + Math.cos(a) * r} y2={-40 + Math.sin(a) * r} stroke="#ffd65a" strokeWidth={5} strokeLinecap="round" />;
        })}
    </g>
  );
};
