import React from 'react';
import {random} from 'remotion';

const INK = '#141414';
export const W = 1080;
export const H = 1920;

/* ---------------------------------------------------------------- glyphs */
const glyphStroke = {stroke: '#5a3a14', strokeWidth: 6, fill: 'none', strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};

export const Glyph: React.FC<{kind: number; x: number; y: number; s?: number; color?: string}> = ({kind, x, y, s = 1, color}) => {
  const st = {...glyphStroke, stroke: color ?? glyphStroke.stroke};
  let g: React.ReactNode;
  switch (kind % 8) {
    case 0: // ankh
      g = (
        <g {...st}>
          <ellipse cx={0} cy={-34} rx={14} ry={18} />
          <path d="M-24 -12 L24 -12 M0 -16 L0 40" />
        </g>
      );
      break;
    case 1: // eye of Horus
      g = (
        <g {...st}>
          <path d="M-30 -10 Q0 -34 30 -10 Q0 10 -30 -10 Z" />
          <circle cx={0} cy={-12} r={6} fill={st.stroke} />
          <path d="M-6 0 L-10 30 M8 0 Q20 22 34 18" />
          <path d="M-34 -24 Q0 -46 34 -24" />
        </g>
      );
      break;
    case 2: // bird
      g = (
        <g {...st}>
          <circle cx={-12} cy={-26} r={9} />
          <path d="M-22 -26 L-34 -22 M-6 -20 Q20 -10 30 16 L-10 14 Q-14 -4 -6 -20 M0 14 L-4 34 M12 14 L12 34" />
        </g>
      );
      break;
    case 3: // water
      g = (
        <g {...st}>
          <path d="M-32 -20 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8" />
          <path d="M-32 0 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8" />
          <path d="M-32 20 l8 -8 l8 8 l8 -8 l8 8 l8 -8 l8 8 l8 -8" />
        </g>
      );
      break;
    case 4: // scarab
      g = (
        <g {...st}>
          <ellipse cx={0} cy={6} rx={18} ry={24} />
          <circle cx={0} cy={-26} r={9} />
          <path d="M0 -18 L0 30 M-18 -4 L-34 -16 M18 -4 L34 -16 M-18 18 L-32 30 M18 18 L32 30" />
        </g>
      );
      break;
    case 5: // reed
      g = (
        <g {...st}>
          <path d="M0 36 L0 -20 Q14 -34 4 -46 Q-12 -30 0 -20" />
          <path d="M0 10 L14 -2" />
        </g>
      );
      break;
    case 6: // sun disc
      g = (
        <g {...st}>
          <circle cx={0} cy={-6} r={18} />
          <path d="M-36 20 Q-20 0 -14 6 M36 20 Q20 0 14 6" />
        </g>
      );
      break;
    default: // walking figure
      g = (
        <g {...st}>
          <circle cx={0} cy={-36} r={9} />
          <path d="M0 -26 L0 8 M0 8 L-12 36 M0 8 L14 36 M0 -18 L-18 -2 M0 -18 L20 -8" />
        </g>
      );
  }
  return <g transform={`translate(${x} ${y}) scale(${s})`}>{g}</g>;
};

/* ---------------------------------------------------------------- torch */
export const Torch: React.FC<{x: number; y: number; frame: number; s?: number; seed?: number}> = ({x, y, frame, s = 1, seed = 0}) => {
  const fl = Math.sin(frame * 0.7 + seed) * 0.5 + Math.sin(frame * 1.9 + seed * 3) * 0.3;
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <circle cx={0} cy={-70} r={220 + fl * 20} fill="url(#torchGlow)" />
      <path d="M-14 0 L14 0 L22 -40 L-22 -40 Z" fill="#6b4a22" stroke={INK} strokeWidth={6} />
      <rect x={-28} y={-52} width={56} height={14} rx={4} fill="#8a5d2a" stroke={INK} strokeWidth={6} />
      <path
        d={`M-24 -54 Q${-30 + fl * 6} -100 ${fl * 8} ${-150 - fl * 10} Q${30 + fl * 4} -100 24 -54 Z`}
        fill="#ff8a1e"
        stroke={INK}
        strokeWidth={5}
      />
      <path d={`M-12 -56 Q${-14 + fl * 4} -86 ${fl * 5} ${-112 - fl * 6} Q${14} -86 12 -56 Z`} fill="#ffe066" />
    </g>
  );
};

export const SharedDefs: React.FC = () => (
  <defs>
    <radialGradient id="torchGlow">
      <stop offset="0%" stopColor="rgba(255,170,60,0.55)" />
      <stop offset="60%" stopColor="rgba(255,120,30,0.12)" />
      <stop offset="100%" stopColor="rgba(255,120,30,0)" />
    </radialGradient>
    <radialGradient id="greenGlow">
      <stop offset="0%" stopColor="rgba(120,255,190,0.6)" />
      <stop offset="100%" stopColor="rgba(120,255,190,0)" />
    </radialGradient>
    <radialGradient id="goldGlow">
      <stop offset="0%" stopColor="rgba(255,215,90,0.8)" />
      <stop offset="100%" stopColor="rgba(255,215,90,0)" />
    </radialGradient>
    <linearGradient id="gold" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0%" stopColor="#ffe9a0" />
      <stop offset="40%" stopColor="#f2c230" />
      <stop offset="100%" stopColor="#a8740c" />
    </linearGradient>
    <linearGradient id="wallGrad" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#3a2a1a" />
      <stop offset="55%" stopColor="#8a6436" />
      <stop offset="100%" stopColor="#6e4c26" />
    </linearGradient>
    <linearGradient id="floorGrad" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#5a3e20" />
      <stop offset="100%" stopColor="#2a1c0e" />
    </linearGradient>
  </defs>
);

/* -------------------------------------------------- side-view corridor */
export const SideCorridor: React.FC<{scroll: number; frame: number; floorY?: number; tint?: string}> = ({
  scroll,
  frame,
  floorY = 1500,
  tint,
}) => {
  const panel = 540;
  const start = Math.floor(scroll / panel) - 1;
  const panels = [];
  for (let i = start; i < start + 5; i++) {
    const px = i * panel - scroll;
    const r = (k: number) => random(`p${i}-${k}`);
    panels.push(
      <g key={i} transform={`translate(${px} 0)`}>
        {/* blocks */}
        {[0, 1, 2, 3, 4, 5, 6].map((row) => (
          <g key={row}>
            <line x1={0} x2={panel} y1={200 + row * 190} y2={200 + row * 190} stroke="rgba(40,24,10,0.5)" strokeWidth={5} />
            <line
              x1={(row % 2) * 270 + 100}
              x2={(row % 2) * 270 + 100}
              y1={200 + row * 190}
              y2={390 + row * 190}
              stroke="rgba(40,24,10,0.45)"
              strokeWidth={5}
            />
          </g>
        ))}
        {/* painted hieroglyph panel */}
        <rect x={60} y={420} width={420} height={640} rx={8} fill="rgba(230,190,120,0.35)" stroke="#5a3a14" strokeWidth={6} />
        <rect x={60} y={420} width={420} height={60} fill="rgba(40,110,140,0.55)" />
        <rect x={60} y={1000} width={420} height={60} fill="rgba(170,50,30,0.5)" />
        {[0, 1, 2].map((c) =>
          [0, 1, 2, 3].map((rr) => (
            <Glyph key={`${c}-${rr}`} kind={Math.floor(r(c * 4 + rr) * 8)} x={140 + c * 130} y={560 + rr * 120} s={0.95} />
          )),
        )}
        {/* column */}
        <rect x={500} y={160} width={80} height={floorY - 160} fill="#9c7444" stroke={INK} strokeWidth={7} />
        <rect x={490} y={150} width={100} height={40} fill="#b48a52" stroke={INK} strokeWidth={7} />
        <path d={`M515 220 L515 ${floorY - 30} M565 220 L565 ${floorY - 30}`} stroke="rgba(60,36,12,0.5)" strokeWidth={5} />
        <Torch x={540} y={700} frame={frame} seed={i * 1.7} s={0.9} />
      </g>,
    );
  }
  return (
    <g>
      <rect x={0} y={0} width={W} height={floorY} fill="url(#wallGrad)" />
      {panels}
      {/* ceiling beam */}
      <rect x={0} y={0} width={W} height={150} fill="#24180c" />
      <rect x={0} y={130} width={W} height={30} fill="#3b2914" stroke={INK} strokeWidth={6} />
      {/* floor */}
      <rect x={0} y={floorY} width={W} height={H - floorY} fill="url(#floorGrad)" />
      <line x1={0} x2={W} y1={floorY} y2={floorY} stroke={INK} strokeWidth={8} />
      {[0, 1, 2, 3, 4, 5].map((k) => {
        const fx = ((k * 260 - scroll * 1.25) % 1560 + 1560) % 1560 - 240;
        return <path key={k} d={`M${fx} ${floorY} L${fx - 160} ${H}`} stroke="rgba(0,0,0,0.35)" strokeWidth={5} />;
      })}
      {tint && <rect x={0} y={0} width={W} height={H} fill={tint} />}
    </g>
  );
};

/* -------------------------------------------- perspective (head-on) corridor */
export const DeepCorridor: React.FC<{frame: number; travel?: number; vpY?: number}> = ({frame, travel = 0, vpY = 900}) => {
  const vx = W / 2;
  const rings = [];
  // receding door frames give a strong sense of depth
  for (let i = 0; i < 9; i++) {
    let z = ((i + travel) % 9) / 9; // 0 near .. 1 far
    z = 1 - z;
    const sc = Math.pow(0.32, z * 3);
    const w = 1400 * sc;
    const h = 2200 * sc;
    const x0 = vx - w / 2;
    const y0 = vpY - h * 0.45;
    const shade = Math.max(0, 1 - z * 1.1);
    rings.push({z, el: (
      <g key={i} opacity={Math.min(1, shade + 0.15)}>
        <rect x={x0} y={y0} width={w} height={h} fill="none" stroke="#2a1a0a" strokeWidth={Math.max(2, 40 * sc)} />
        <rect x={x0 + 10 * sc} y={y0 + 10 * sc} width={w - 20 * sc} height={60 * sc} fill="#7a5530" />
        {[0, 1, 2].map((g) => (
          <Glyph key={g} kind={i + g * 3} x={x0 + w * 0.08} y={y0 + h * (0.3 + g * 0.2)} s={sc * 2.4} />
        ))}
        {[0, 1, 2].map((g) => (
          <Glyph key={`r${g}`} kind={i * 2 + g} x={x0 + w * 0.92} y={y0 + h * (0.3 + g * 0.2)} s={sc * 2.4} />
        ))}
        {i % 2 === 0 && <Torch x={x0 + w * 0.06} y={y0 + h * 0.42} frame={frame} s={sc * 2.2} seed={i} />}
        {i % 2 === 1 && <Torch x={x0 + w * 0.94} y={y0 + h * 0.42} frame={frame} s={sc * 2.2} seed={i} />}
      </g>
    )});
  }
  rings.sort((a, b) => b.z - a.z);
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#5e4122" />
      {/* walls */}
      <path d={`M0 0 L${vx - 40} ${vpY - 60} L${vx - 40} ${vpY + 60} L0 ${H} Z`} fill="#8a6234" />
      <path d={`M${W} 0 L${vx + 40} ${vpY - 60} L${vx + 40} ${vpY + 60} L${W} ${H} Z`} fill="#7a5530" />
      <path d={`M0 0 L${W} 0 L${vx + 40} ${vpY - 60} L${vx - 40} ${vpY - 60} Z`} fill="#2a1c0e" />
      <path d={`M0 ${H} L${W} ${H} L${vx + 40} ${vpY + 60} L${vx - 40} ${vpY + 60} Z`} fill="#4a321a" />
      <rect x={vx - 40} y={vpY - 60} width={80} height={120} fill="#0b0704" />
      {rings.map((r) => r.el)}
    </g>
  );
};

/* ------------------------------------------------------------ golden door */
export const GoldenDoor: React.FC<{x: number; y: number; open: number; frame: number; s?: number}> = ({x, y, open, frame, s = 1}) => {
  const shine = (frame * 14) % 900 - 300;
  const leaf = (side: -1 | 1) => (
    <g transform={`translate(${side * 260} 0) scale(${1 - open * 0.85} 1) translate(${-side * 260} 0)`}>
      <rect
        x={side === -1 ? -260 : 0}
        y={-900}
        width={260}
        height={900}
        fill="url(#gold)"
        stroke={INK}
        strokeWidth={10}
      />
      <rect x={side === -1 ? -230 : 30} y={-860} width={200} height={380} fill="none" stroke="#8a5e08" strokeWidth={8} />
      <rect x={side === -1 ? -230 : 30} y={-440} width={200} height={380} fill="none" stroke="#8a5e08" strokeWidth={8} />
      <Glyph kind={side === -1 ? 1 : 0} x={side * 130} y={-680} s={2.2} color="#7a4e04" />
      <Glyph kind={side === -1 ? 4 : 6} x={side * 130} y={-260} s={2.2} color="#7a4e04" />
      <circle cx={side * 30} cy={-450} r={18} fill="#ffe9a0" stroke={INK} strokeWidth={6} />
    </g>
  );
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <circle cx={0} cy={-450} r={720} fill="url(#goldGlow)" opacity={0.45 + Math.sin(frame * 0.15) * 0.1} />
      {/* frame */}
      <path d="M-330 0 L-330 -980 L330 -980 L330 0" fill="#3a2810" stroke={INK} strokeWidth={12} />
      <rect x={-380} y={-1060} width={760} height={110} fill="#c99a2e" stroke={INK} strokeWidth={10} />
      <g transform="translate(0 -1005)">
        <circle cx={0} cy={0} r={34} fill="#e2231a" stroke={INK} strokeWidth={6} />
        <path d="M-40 0 Q-120 -30 -200 0 Q-120 20 -40 0 M40 0 Q120 -30 200 0 Q120 20 40 0" fill="#2f7fa0" stroke={INK} strokeWidth={6} />
      </g>
      {/* darkness behind / light spilling */}
      <rect x={-260} y={-900} width={520} height={900} fill="#070402" />
      <rect x={-260 * open} y={-900} width={520 * open} height={900} fill="rgba(255,220,120,0.55)" />
      {leaf(-1)}
      {leaf(1)}
      {/* moving shine */}
      <g clipPath="url(#doorClip)" opacity={0.6 * (1 - open)}>
        <rect x={shine - 300} y={-900} width={80} height={900} fill="rgba(255,255,255,0.55)" transform={`skewX(-20)`} />
      </g>
      <clipPath id="doorClip">
        <rect x={-260} y={-900} width={520} height={900} />
      </clipPath>
    </g>
  );
};

/* ------------------------------------------------------------- chamber */
export const Chamber: React.FC<{frame: number; floorY?: number; flicker?: number}> = ({frame, floorY = 1450, flicker = 1}) => (
  <g>
    <rect x={0} y={0} width={W} height={floorY} fill="#4a321a" />
    <rect x={0} y={0} width={W} height={floorY} fill="url(#wallGrad)" opacity={0.7} />
    {/* wall painting: procession */}
    <rect x={80} y={300} width={920} height={360} fill="rgba(230,190,120,0.3)" stroke="#5a3a14" strokeWidth={6} />
    {[0, 1, 2, 3, 4, 5, 6].map((k) => (
      <Glyph key={k} kind={7} x={170 + k * 125} y={500} s={2.1} color="#4e2f0e" />
    ))}
    <rect x={80} y={300} width={920} height={50} fill="rgba(40,110,140,0.6)" />
    <rect x={80} y={610} width={920} height={50} fill="rgba(170,50,30,0.55)" />
    {[0, 1, 2, 3, 4, 5, 6, 7].map((k) => (
      <Glyph key={`g${k}`} kind={k} x={130 + k * 115} y={780} s={1.1} />
    ))}
    {/* columns */}
    {[60, 1020].map((cx) => (
      <g key={cx}>
        <rect x={cx - 55} y={120} width={110} height={floorY - 120} fill="#a07848" stroke={INK} strokeWidth={8} />
        <path d={`M${cx - 75} 120 Q${cx} 40 ${cx + 75} 120 Z`} fill="#3f8f6a" stroke={INK} strokeWidth={8} />
      </g>
    ))}
    {/* gold treasure piles */}
    {[
      [170, floorY + 10, 1],
      [930, floorY + 20, 1.2],
    ].map(([tx, ty, ts], i) => (
      <g key={i} transform={`translate(${tx} ${ty}) scale(${ts})`}>
        <path d="M-150 0 Q-100 -90 0 -110 Q100 -90 150 0 Z" fill="url(#gold)" stroke={INK} strokeWidth={7} />
        {[-80, -30, 30, 80, 0].map((c, j) => (
          <ellipse key={j} cx={c} cy={-40 - (j % 2) * 30} rx={22} ry={9} fill="#ffe27a" stroke="#8a5e08" strokeWidth={4} />
        ))}
        <path d="M60 -110 L90 -170 L120 -110 Z" fill="#2f7fa0" stroke={INK} strokeWidth={6} />
        <circle cx={-60} cy={-100} r={8} fill="#fff" opacity={0.5 + 0.5 * Math.sin(frame * 0.3 + i)} />
      </g>
    ))}
    <Torch x={250} y={1080} frame={frame} seed={2} />
    <Torch x={830} y={1080} frame={frame} seed={5} />
    <rect x={0} y={floorY} width={W} height={H - floorY} fill="url(#floorGrad)" />
    <line x1={0} x2={W} y1={floorY} y2={floorY} stroke={INK} strokeWidth={8} />
    <rect x={0} y={0} width={W} height={H} fill="#000" opacity={1 - flicker} />
  </g>
);

/* --------------------------------------------------------- sarcophagus */
export const Sarcophagus: React.FC<{
  x: number;
  y: number;
  s?: number;
  lid: number; // 0 closed, 1 fully slid off
  frame: number;
  shake?: number;
  children?: React.ReactNode;
}> = ({x, y, s = 1, lid, frame, shake = 0, children}) => {
  const sx = shake ? Math.sin(frame * 2.2) * shake : 0;
  return (
    <g transform={`translate(${x + sx} ${y}) scale(${s})`}>
      <circle cx={0} cy={-260} r={560} fill="url(#goldGlow)" opacity={0.35} />
      {/* box (open top, seen from front-high angle) */}
      <path d="M-300 0 L-330 -340 L330 -340 L300 0 Z" fill="url(#gold)" stroke={INK} strokeWidth={10} />
      <rect x={-260} y={-300} width={520} height={60} fill="#2f7fa0" stroke={INK} strokeWidth={6} />
      {[0, 1, 2, 3, 4, 5].map((k) => (
        <Glyph key={k} kind={k + 1} x={-210 + k * 84} y={-140} s={1.1} color="#7a4e04" />
      ))}
      <rect x={-260} y={-70} width={520} height={30} fill="#b0301e" stroke={INK} strokeWidth={6} />
      {/* interior */}
      <path d="M-310 -340 L-270 -420 L270 -420 L310 -340 Z" fill="#120a04" stroke={INK} strokeWidth={8} />
      {children}
      {/* lid: pharaoh face, slides up and away */}
      <g transform={`translate(${lid * 620} ${-lid * 260}) rotate(${lid * 24} 0 -380)`}>
        <path d="M-320 -340 L-280 -430 L280 -430 L320 -340 Z" fill="url(#gold)" stroke={INK} strokeWidth={10} />
        <g transform="translate(0 -560)">
          {/* nemes headdress stripes */}
          <path d="M-170 140 L-120 -80 Q0 -150 120 -80 L170 140 Z" fill="#2f7fa0" stroke={INK} strokeWidth={9} />
          {[-90, -45, 0, 45, 90].map((c) => (
            <path key={c} d={`M${c * 1.2} 140 L${c * 0.8} -90`} stroke="#f2c230" strokeWidth={14} />
          ))}
          <ellipse cx={0} cy={0} rx={92} ry={110} fill="url(#gold)" stroke={INK} strokeWidth={9} />
          <path d="M-56 -14 Q-36 -30 -14 -14" stroke={INK} strokeWidth={8} fill="#fff" />
          <path d="M14 -14 Q36 -30 56 -14" stroke={INK} strokeWidth={8} fill="#fff" />
          <circle cx={-34} cy={-16} r={7} fill={INK} />
          <circle cx={34} cy={-16} r={7} fill={INK} />
          <path d="M-60 -30 L-80 -10 M60 -30 L80 -10" stroke={INK} strokeWidth={7} />
          <path d="M-20 40 Q0 50 20 40" stroke={INK} strokeWidth={7} fill="none" />
          <rect x={-14} y={98} width={28} height={70} fill="#2f7fa0" stroke={INK} strokeWidth={6} />
          <path d="M-14 -102 Q0 -130 14 -102" fill="#e2231a" stroke={INK} strokeWidth={6} />
        </g>
        <circle cx={-120} cy={-600} r={10} fill="#fff" opacity={0.4 + 0.6 * Math.abs(Math.sin(frame * 0.2))} />
      </g>
    </g>
  );
};
