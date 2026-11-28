// Backgrounds (world coordinates; scenes frame them with <Cam>).
import React from 'react';
import {C, W, H, rng, mixHex} from './lib';
import {Txt, HAND, TITLE, Glow} from './fx';
import {Chandelier, Ship, Stars, Waves} from './props';

const S = {stroke: C.ink, strokeWidth: 6, strokeLinejoin: 'round' as const};

export const Sky: React.FC<{t: number; top?: string; bot?: string; id: string; sun?: [number, number] | null; clouds?: boolean}> = ({
  t, top = '#5ab8f0', bot = '#dff3fb', id, sun = [1500, 160], clouds = true,
}) => (
  <g>
    <defs>
      <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={top} />
        <stop offset="1" stopColor={bot} />
      </linearGradient>
    </defs>
    <rect x={-3000} y={-2000} width={9000} height={4000} fill={`url(#${id})`} />
    {sun && (
      <g>
        <Glow id={id + 'sun'} x={sun[0]} y={sun[1]} r={280} color="#fff2a0" a={0.7} />
        <circle cx={sun[0]} cy={sun[1]} r={80} fill="#ffe066" stroke={C.ink} strokeWidth={6} />
      </g>
    )}
    {clouds && [0, 1, 2, 3].map((i) => <Cloud key={i} x={((i * 800 + t * 20) % 3600) - 900} y={120 + (i % 2) * 110} s={1 - i * 0.1} />)}
  </g>
);

export const Cloud: React.FC<{x: number; y: number; s?: number; color?: string; a?: number}> = ({x, y, s = 1, color = '#fff', a = 0.95}) => (
  <g transform={`translate(${x},${y}) scale(${s})`} opacity={a} fill={color}>
    <circle cx={-80} cy={10} r={50} />
    <circle cx={-20} cy={-20} r={70} />
    <circle cx={60} cy={0} r={55} />
    <circle cx={110} cy={20} r={38} />
    <rect x={-130} y={10} width={270} height={48} />
  </g>
);

export const FleaMarket: React.FC<{t: number}> = ({t}) => {
  const tents = ['#e8503a', '#3a7ad8', '#f2b53a', '#2bb36b', '#c86ad8'];
  return (
    <g>
      <Sky t={t} id="fmSky" />
      <rect x={-2000} y={560} width={6000} height={140} fill="#8fc87a" stroke={C.ink} strokeWidth={5} />
      {[-200, 300, 1500, 2000].map((tx, i) => (
        <g key={tx}>
          <line x1={tx} y1={700} x2={tx} y2={420} stroke="#6b4428" strokeWidth={16} />
          {[0, 1, 2].map((k) => <circle key={k} cx={tx - 60 + k * 60} cy={400 - (k % 2) * 40} r={80} fill="#5aa848" stroke={C.ink} strokeWidth={5} />)}
        </g>
      ))}
      <rect x={-2000} y={690} width={6000} height={1200} fill="#d9c08a" stroke={C.ink} strokeWidth={6} />
      {tents.map((c, i) => {
        const x = -500 + i * 560;
        return (
          <g key={i}>
            {[-230, 230].map((d) => <line key={d} x1={x + d} y1={840} x2={x + d} y2={540} stroke="#6b4428" strokeWidth={10} />)}
            <polygon points={`${x - 270},560 ${x + 270},560 ${x + 230},470 ${x - 230},470`} fill={c} {...S} />
            {[0, 1, 2, 3, 4, 5].map((k) => (
              <path key={k} d={`M${x - 270 + k * 90},560 q45,40 90,0`} fill={c} {...S} />
            ))}
            <rect x={x - 240} y={740} width={480} height={100} fill="#b8864a" {...S} />
            <Junk x={x} y={740} seed={i} />
          </g>
        );
      })}
    </g>
  );
};

const Junk: React.FC<{x: number; y: number; seed: number}> = ({x, y, seed}) => {
  const R = rng(seed + 5);
  const items: React.ReactNode[] = [];
  for (let k = 0; k < 4; k++) {
    const ix = x - 180 + k * 120;
    const kind = Math.floor(R() * 5);
    if (kind === 0) items.push(<g key={k}><polygon points={`${ix - 30},${y} ${ix + 30},${y} ${ix + 18},${y - 60} ${ix - 18},${y - 60}`} fill="#f2d86a" {...S} /><line x1={ix} y1={y - 60} x2={ix} y2={y - 80} stroke={C.ink} strokeWidth={5} /></g>);
    if (kind === 1) items.push(<g key={k}><rect x={ix - 30} y={y - 50} width={60} height={50} rx={6} fill="#3a7ad8" {...S} /><circle cx={ix} cy={y - 25} r={14} fill="#fff" stroke={C.ink} strokeWidth={4} /></g>);
    if (kind === 2) items.push(<g key={k}><circle cx={ix} cy={y - 30} r={30} fill="#e8503a" {...S} /><circle cx={ix} cy={y - 30} r={8} fill={C.ink} /></g>);
    if (kind === 3) items.push(<g key={k}><path d={`M${ix - 10},${y - 70} L${ix - 10},${y} L${ix + 30},${y}`} fill="none" stroke={C.ink} strokeWidth={22} strokeLinecap="round" /><path d={`M${ix - 10},${y - 70} L${ix - 10},${y} L${ix + 30},${y}`} fill="none" stroke={['#ff8ad8', '#8ae0ff', '#c8f28a'][k % 3]} strokeWidth={14} strokeLinecap="round" /></g>);
    if (kind === 4) items.push(<g key={k}><rect x={ix - 35} y={y - 40} width={70} height={40} fill="#8a5a2b" {...S} /><rect x={ix - 25} y={y - 70} width={50} height={30} fill="#c8a06a" {...S} /></g>);
  }
  return <g>{items}</g>;
};

export const Bedroom: React.FC<{t: number; night?: boolean}> = ({t, night}) => (
  <g>
    <rect x={-1000} y={-600} width={4000} height={1500} fill={night ? '#5a6a9a' : '#bfe0f2'} />
    <rect x={-1000} y={800} width={4000} height={600} fill="#c9925a" stroke={C.ink} strokeWidth={6} />
    {Array.from({length: 30}).map((_, k) => <line key={k} x1={-800 + k * 140} y1={800} x2={-860 + k * 140} y2={1400} stroke="#a8763f" strokeWidth={3} />)}
    <rect x={1260} y={150} width={420} height={330} rx={16} fill={night ? '#22305a' : '#ffe9a0'} {...S} strokeWidth={10} />
    <line x1={1470} y1={150} x2={1470} y2={480} stroke={C.ink} strokeWidth={8} />
    <line x1={1260} y1={315} x2={1680} y2={315} stroke={C.ink} strokeWidth={8} />
    <g transform="translate(420,260) rotate(-3)">
      <rect x={-120} y={-150} width={240} height={300} rx={8} fill="#2a4a7a" {...S} />
      <Txt x={0} y={-100} size={34} color="#ffd84d" outline={0} shadow={false}>HISTORY!</Txt>
      <polygon points="-80,100 0,-40 80,100" fill="#f2d38a" stroke={C.ink} strokeWidth={5} />
    </g>
    <rect x={200} y={560} width={900} height={220} rx={20} fill="#3a6ad6" {...S} />
    <rect x={170} y={420} width={60} height={380} rx={16} fill="#8a5a2b" {...S} />
    <rect x={240} y={500} width={220} height={90} rx={40} fill="#fff" {...S} />
    <rect x={200} y={770} width={900} height={30} fill="#2a3a7a" {...S} />
    <rect x={1700} y={300} width={200} height={500} fill="#a8763f" {...S} />
    <circle cx={1730} cy={560} r={10} fill={C.gold} stroke={C.ink} strokeWidth={3} />
    {/* backpack */}
    <path d="M1240,800 C1230,700 1380,700 1370,800 Z" fill="#e8503a" {...S} />
  </g>
);

export const Vortex: React.FC<{t: number; hue1?: string; hue2?: string}> = ({t, hue1 = '#3a4ad8', hue2 = '#ffd84d'}) => {
  const rings: React.ReactNode[] = [];
  for (let i = 26; i > 0; i--) {
    const r = i * 90 + ((t * 260) % 90);
    const f = Math.min(1, r / 2400);
    const col = mixHex(hue2, hue1, (i % 2) * 0.7 + f * 0.3);
    const wedges: string[] = [];
    for (let j = 0; j < 12; j++) {
      const a0 = (j * 2 * Math.PI) / 12;
      const a1 = a0 + Math.PI / 12;
      wedges.push(`M0,0 L${Math.cos(a0) * r},${Math.sin(a0) * r} A${r},${r} 0 0 1 ${Math.cos(a1) * r},${Math.sin(a1) * r} Z`);
    }
    rings.push(
      <path key={i} d={wedges.join(' ')} fill={col} opacity={0.55 * (1 - f * 0.4)}
        transform={`rotate(${(t * 2 * (i % 2 ? 1 : -0.6) + i * 0.3) * 57.3}) scale(1,0.82)`} />,
    );
  }
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#0d0820" />
      <g transform={`translate(${W / 2},${H / 2})`}>
        {rings}
        <Glow id="vxc" x={0} y={0} r={380} color="#fffbe0" a={1} />
      </g>
    </g>
  );
};

/** open sea with the ship (wide shots) */
export const OpenSea: React.FC<{t: number; night?: boolean; shipX?: number; lights?: boolean; tilt?: number; shipS?: number; shipY?: number}> = ({
  t, night, shipX = 960, lights, tilt = 0, shipS = 0.9, shipY = 760,
}) => (
  <g>
    {night ? (
      <g>
        <rect x={-3000} y={-2000} width={9000} height={4000} fill={C.night} />
        <Stars t={t} n={220} y1={700} />
      </g>
    ) : (
      <Sky t={t} id="osSky" />
    )}
    <Ship x={shipX} y={shipY} s={shipS} t={t} night={night} lights={lights} tilt={tilt} />
    <Waves y={shipY + 30} t={t} color={night ? '#0e1838' : C.sea} dark={night ? '#081028' : C.seaD} amp={night ? 3 : 14} />
  </g>
);

/** boat deck seen from the side: railing in front, white superstructure + funnel bases behind */
export const Deck: React.FC<{t: number; night?: boolean; lights?: boolean; davits?: number}> = ({t, night, lights, davits = 0}) => {
  const wall = night ? '#5a5e78' : '#fbf8f0';
  return (
    <g>
      {night ? (
        <g>
          <rect x={-3000} y={-2000} width={9000} height={4000} fill={C.night} />
          <Stars t={t} n={200} y1={500} />
        </g>
      ) : (
        <Sky t={t} id="dkSky" />
      )}
      {/* funnels */}
      {[-200, 700, 1600, 2500].map((fx) => (
        <g key={fx} transform={`translate(${fx},0) skewX(-6)`}>
          <rect x={-120} y={-500} width={240} height={700} fill={night ? '#8a6a3a' : C.funnel} {...S} />
          <rect x={-120} y={-500} width={240} height={120} fill={C.ink} />
        </g>
      ))}
      {[-200, 700, 1600, 2500].map((fx, k) =>
        [0, 1, 2].map((j) => {
          const ph = (t * 0.2 + j / 3 + k * 0.2) % 1;
          return <circle key={`${k}${j}`} cx={fx - ph * 300} cy={-520 - ph * 300} r={60 + ph * 90} fill={night ? '#4a4a5a' : '#b0b0b8'} opacity={0.45 * (1 - ph)} />;
        }),
      )}
      {/* deckhouse */}
      <rect x={-2000} y={200} width={6000} height={460} fill={wall} {...S} />
      {Array.from({length: 40}).map((_, k) => (
        <g key={k}>
          <rect x={-1900 + k * 150} y={300} width={80} height={140} rx={10} fill={lights ? '#ffd98a' : night ? '#2a3050' : '#4a6a8a'} stroke={C.ink} strokeWidth={5} />
          <line x1={-1860 + k * 150} y1={300} x2={-1860 + k * 150} y2={440} stroke={C.ink} strokeWidth={3} />
        </g>
      ))}
      {/* lifeboats on davits */}
      {[-900, 300, 1500, 2700].map((bx, i) => {
        const drop = davits * (i % 2 === 0 ? 1 : 0.6);
        return (
          <g key={bx}>
            <path d={`M${bx - 160},180 C${bx - 160},60 ${bx - 60},40 ${bx - 60},40`} fill="none" stroke={C.ink} strokeWidth={14} />
            <path d={`M${bx + 160},180 C${bx + 160},60 ${bx + 60},40 ${bx + 60},40`} fill="none" stroke={C.ink} strokeWidth={14} />
            <line x1={bx - 60} y1={40} x2={bx - 120} y2={90 + drop * 400} stroke={C.ink} strokeWidth={3} />
            <line x1={bx + 60} y1={40} x2={bx + 120} y2={90 + drop * 400} stroke={C.ink} strokeWidth={3} />
            <path d={`M${bx - 180},${90 + drop * 400} L${bx + 180},${90 + drop * 400} C${bx + 160},${150 + drop * 400} ${bx - 160},${150 + drop * 400} ${bx - 180},${90 + drop * 400} Z`} fill="#fff" stroke={C.ink} strokeWidth={6} />
          </g>
        );
      })}
      {/* deck floor */}
      <rect x={-2000} y={660} width={6000} height={1000} fill={night ? '#6a5236' : C.deck} {...S} />
      {Array.from({length: 60}).map((_, k) => <line key={k} x1={-2000 + k * 100} y1={660} x2={-2300 + k * 100} y2={1400} stroke={night ? '#4a3a26' : C.deckD} strokeWidth={3} />)}
      {/* railing at the front */}
      <line x1={-2000} y1={900} x2={4000} y2={900} stroke={night ? '#bfc4d0' : '#fff'} strokeWidth={14} />
      <line x1={-2000} y1={900} x2={4000} y2={900} stroke={C.ink} strokeWidth={3} />
      {Array.from({length: 60}).map((_, k) => <line key={k} x1={-2000 + k * 100} y1={900} x2={-2000 + k * 100} y2={1080} stroke={night ? '#bfc4d0' : '#fff'} strokeWidth={8} />)}
    </g>
  );
};

export const GrandStaircase: React.FC<{t: number}> = ({t}) => (
  <g>
    <rect x={-1500} y={-800} width={5000} height={2400} fill="#c99a62" />
    {/* glass dome */}
    <ellipse cx={960} cy={-40} rx={760} ry={260} fill="#dff2fb" {...S} />
    {Array.from({length: 13}).map((_, k) => (
      <line key={k} x1={960} y1={-300} x2={200 + k * 127} y2={180} stroke={C.ink} strokeWidth={4} />
    ))}
    <ellipse cx={960} cy={-40} rx={380} ry={130} fill="none" stroke={C.ink} strokeWidth={4} />
    <rect x={-1500} y={160} width={5000} height={60} fill="#e8c890" {...S} />
    {/* wood panels */}
    {Array.from({length: 18}).map((_, k) => (
      <rect key={k} x={-1300 + k * 280} y={260} width={220} height={360} rx={8} fill="#b8864a" stroke={C.ink} strokeWidth={4} />
    ))}
    <Chandelier x={960} y={340} s={1.1} t={t} />
    {/* clock with the carved figures */}
    <rect x={840} y={360} width={240} height={180} rx={10} fill="#a8763f" {...S} />
    <circle cx={960} cy={440} r={50} fill="#f6efe0" stroke={C.ink} strokeWidth={5} />
    <line x1={960} y1={440} x2={960} y2={404} stroke={C.ink} strokeWidth={5} />
    <line x1={960} y1={440} x2={985} y2={448} stroke={C.ink} strokeWidth={5} />
    {/* stairs */}
    {Array.from({length: 9}).map((_, k) => (
      <rect key={k} x={560 - k * 40} y={640 + k * 40} width={800 + k * 80} height={42} fill={k % 2 ? '#e8d4a8' : '#dcc490'} stroke={C.ink} strokeWidth={4} />
    ))}
    <rect x={-1500} y={1000} width={5000} height={600} fill="#9a2a2a" {...S} />
    {/* banisters */}
    {[-1, 1].map((sd) => (
      <g key={sd}>
        <path d={`M${960 + sd * 420},640 L${960 + sd * 760},1000`} stroke="#6b4428" strokeWidth={26} strokeLinecap="round" />
        <circle cx={960 + sd * 760} cy={980} r={30} fill="#6b4428" stroke={C.ink} strokeWidth={5} />
        <rect x={960 + sd * 760 - 8} y={880} width={16} height={100} fill={C.gold} stroke={C.ink} strokeWidth={4} />
        <circle cx={960 + sd * 760} cy={870} r={22} fill="#fff6c0" stroke={C.ink} strokeWidth={4} />
      </g>
    ))}
  </g>
);

export const Dining: React.FC<{t: number}> = ({t}) => (
  <g>
    <rect x={-1500} y={-800} width={5000} height={2400} fill="#efe2c8" />
    {Array.from({length: 14}).map((_, k) => (
      <g key={k}>
        <rect x={-900 + k * 300} y={120} width={140} height={260} rx={70} fill="#cfe6f2" stroke={C.ink} strokeWidth={6} />
        <line x1={-830 + k * 300} y1={120} x2={-830 + k * 300} y2={380} stroke={C.ink} strokeWidth={3} />
      </g>
    ))}
    {[0, 1, 2].map((k) => <Chandelier key={k} x={300 + k * 660} y={150} s={0.7} t={t + k} />)}
    <rect x={-1500} y={560} width={5000} height={1000} fill="#7a3a2a" {...S} />
    {Array.from({length: 30}).map((_, k) => <line key={k} x1={-1500 + k * 180} y1={560} x2={-1700 + k * 180} y2={1400} stroke="#5a2a1e" strokeWidth={3} />)}
  </g>
);

export const DiningTable: React.FC<{x: number; y: number; w?: number; t: number; plates?: number}> = ({x, y, w = 700, t, plates = 4}) => (
  <g>
    <rect x={x - w / 2} y={y} width={w} height={30} fill="#fff" {...S} />
    <path d={`M${x - w / 2},${y + 30} L${x - w / 2 + 20},${y + 120} L${x + w / 2 - 20},${y + 120} L${x + w / 2},${y + 30} Z`} fill="#fff" {...S} />
    {Array.from({length: plates}).map((_, k) => {
      const px = x - w / 2 + (k + 0.5) * (w / plates);
      return (
        <g key={k}>
          <ellipse cx={px} cy={y + 2} rx={44} ry={12} fill="#f6f6f6" stroke={C.ink} strokeWidth={4} />
          <path d={`M${px + 50},${y} L${px + 46},${y - 60} L${px + 66},${y - 60} L${px + 62},${y} Z`} fill="#e8f6ff" opacity={0.8} stroke={C.ink} strokeWidth={3} />
        </g>
      );
    })}
    <path d={`M${x - 20},${y} L${x - 30},${y - 70} L${x + 30},${y - 70} L${x + 20},${y} Z`} fill="#ff9ad0" stroke={C.ink} strokeWidth={4} />
  </g>
);

export const Bridge: React.FC<{t: number; night?: boolean}> = ({t, night}) => (
  <g>
    <rect x={-1500} y={-800} width={5000} height={2400} fill={night ? '#3a3a4a' : '#e8dcc0'} />
    {/* windows to the sea */}
    {Array.from({length: 8}).map((_, k) => (
      <g key={k}>
        <rect x={-300 + k * 360} y={100} width={300} height={260} rx={10} fill={night ? C.night : '#8fd0f4'} stroke={C.ink} strokeWidth={8} />
        <line x1={-300 + k * 360} y1={290} x2={k * 360} y2={290} stroke={night ? '#1a2850' : '#2f7fc4'} strokeWidth={60} opacity={0.9} />
      </g>
    ))}
    <rect x={-1500} y={700} width={5000} height={900} fill="#a8763f" {...S} />
    {/* ship's wheel */}
    <g transform={`translate(1300,600) rotate(${Math.sin(t * 0.8) * 8})`}>
      {Array.from({length: 8}).map((_, k) => {
        const a = (k * Math.PI) / 4;
        return <line key={k} x1={0} y1={0} x2={Math.cos(a) * 170} y2={Math.sin(a) * 170} stroke="#6b4428" strokeWidth={22} strokeLinecap="round" />;
      })}
      <circle cx={0} cy={0} r={120} fill="none" stroke="#6b4428" strokeWidth={26} />
      <circle cx={0} cy={0} r={120} fill="none" stroke={C.ink} strokeWidth={4} />
      <circle cx={0} cy={0} r={30} fill={C.gold} stroke={C.ink} strokeWidth={6} />
    </g>
    <rect x={1260} y={720} width={80} height={300} fill="#8a5a2b" {...S} />
    {/* engine telegraph */}
    <rect x={460} y={560} width={40} height={460} fill="#c9ccd2" {...S} />
    <circle cx={480} cy={540} r={70} fill="#e3b23a" stroke={C.ink} strokeWidth={7} />
    <circle cx={480} cy={540} r={50} fill="#fff" stroke={C.ink} strokeWidth={4} />
    <line x1={480} y1={540} x2={510} y2={500} stroke={C.red} strokeWidth={6} />
  </g>
);

export const Corridor: React.FC<{t: number; color?: string; label?: string}> = ({t, color = '#e8dcc0', label}) => (
  <g>
    <rect x={-2000} y={-800} width={6000} height={2400} fill={color} />
    {Array.from({length: 30}).map((_, k) => (
      <g key={k}>
        <rect x={-1500 + k * 260} y={260} width={150} height={460} rx={8} fill="#a8763f" stroke={C.ink} strokeWidth={5} />
        <circle cx={-1380 + k * 260} cy={500} r={9} fill={C.gold} stroke={C.ink} strokeWidth={3} />
        <rect x={-1475 + k * 260} y={210} width={100} height={36} fill="#fff" stroke={C.ink} strokeWidth={3} />
        <Txt x={-1425 + k * 260} y={228} size={22} color={C.ink} outline={0} shadow={false}>{String(100 + k * 7 + Math.floor(t * 0))}</Txt>
      </g>
    ))}
    <rect x={-2000} y={720} width={6000} height={800} fill="#9a2a2a" stroke={C.ink} strokeWidth={6} />
    <line x1={-2000} y1={160} x2={4000} y2={160} stroke="#c9a96a" strokeWidth={14} />
    {label && <Txt x={960} y={100} size={50} color={C.ink} outline={0} shadow={false}>{label}</Txt>}
  </g>
);

export const CrowsNest: React.FC<{t: number}> = ({t}) => (
  <g>
    <rect x={-3000} y={-2000} width={9000} height={4000} fill={C.night} />
    <Stars t={t} n={260} y1={900} />
    <rect x={-3000} y={760} width={9000} height={800} fill="#0a1430" />
    <line x1={-3000} y1={760} x2={6000} y2={760} stroke="#2a3a6a" strokeWidth={3} />
    {/* the mast + nest */}
    <rect x={260} y={600} width={60} height={800} fill="#3a2a1e" {...S} />
    <path d="M60,560 L520,560 L480,820 L100,820 Z" fill="#5a3a22" {...S} />
    {Array.from({length: 8}).map((_, k) => <line key={k} x1={80 + k * 55} y1={570} x2={110 + k * 50} y2={810} stroke="#3a2416" strokeWidth={4} />)}
  </g>
);

export const LifeboatSea: React.FC<{t: number; dawn?: number}> = ({t, dawn = 0}) => (
  <g>
    <defs>
      <linearGradient id="lbsky" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor={mixHex(C.night, '#f2a35a', dawn * 0.6)} />
        <stop offset="1" stopColor={mixHex(C.nightB, '#ffd9a0', dawn)} />
      </linearGradient>
    </defs>
    <rect x={-3000} y={-2000} width={9000} height={4000} fill="url(#lbsky)" />
    <Stars t={t} n={140} y1={650} />
    <Waves y={680} t={t} color={mixHex('#0e1838', '#3a6a9a', dawn)} dark="#081028" amp={6} />
  </g>
);

export const PompeiiScreen: React.FC<{t: number}> = ({t}) => (
  <g>
    <defs>
      <linearGradient id="pmp" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stopColor="#ff8a3a" />
        <stop offset="1" stopColor="#ffd98a" />
      </linearGradient>
    </defs>
    <rect x={0} y={0} width={W} height={H} fill="url(#pmp)" />
    {/* Vesuvius with a smoke plume */}
    <polygon points="500,1080 980,380 1100,360 1600,1080" fill="#6a4a3a" stroke={C.ink} strokeWidth={8} />
    <polygon points="980,380 1100,360 1060,440 1010,430" fill="#3a2418" />
    {Array.from({length: 7}).map((_, k) => {
      const ph = (t * 0.25 + k / 7) % 1;
      return <circle key={k} cx={1040 + Math.sin(k * 2 + t) * 40 * ph} cy={340 - ph * 420} r={50 + ph * 140} fill="#5a5050" opacity={0.75 * (1 - ph * 0.6)} />;
    })}
    {/* Roman columns */}
    {[200, 330, 1660, 1790].map((x) => (
      <g key={x}>
        <rect x={x - 35} y={640} width={70} height={440} fill="#f2e6d0" stroke={C.ink} strokeWidth={6} />
        <rect x={x - 50} y={620} width={100} height={30} fill="#e0d4bc" stroke={C.ink} strokeWidth={5} />
      </g>
    ))}
  </g>
);

export const titleFonts = {TITLE, HAND};
