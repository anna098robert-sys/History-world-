import React from 'react';
import {random, useCurrentFrame} from 'remotion';
import {Flame} from './Fire';

export const W = 1080;
export const H = 1920;
const INK = '#141414';

export const LondonDefs: React.FC = () => (
  <defs>
    <linearGradient id="skyDawn" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#2b2340" />
      <stop offset="60%" stopColor="#7a5a6a" />
      <stop offset="100%" stopColor="#d99a6a" />
    </linearGradient>
    <linearGradient id="skyFire" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#1a0b08" />
      <stop offset="45%" stopColor="#6e1f0c" />
      <stop offset="80%" stopColor="#d4541a" />
      <stop offset="100%" stopColor="#ffb347" />
    </linearGradient>
    <linearGradient id="skyAsh" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#57524f" />
      <stop offset="100%" stopColor="#a39a90" />
    </linearGradient>
    <linearGradient id="cobble" x1="0" x2="0" y1="0" y2="1">
      <stop offset="0%" stopColor="#5d544a" />
      <stop offset="100%" stopColor="#2c2622" />
    </linearGradient>
    <pattern id="lattice" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <rect width="16" height="16" fill="none" />
      <path d="M0 0 L0 16 M0 0 L16 0" stroke="#2b2b2b" strokeWidth={2.5} />
    </pattern>
  </defs>
);

/* ------------------------------------------------- timber-framed house */
const PLASTER = ['#efe2c4', '#e8d6ae', '#f2e8d2', '#e3cfa6', '#efdcc0'];
const ROOF = ['#7a3b24', '#6b3220', '#5b4a3a', '#81462a'];

export type HouseProps = {
  x: number; // left edge at ground
  y: number; // ground
  w: number;
  floors?: number;
  seed?: number;
  burn?: number; // 0 none, 0.3 windows glow, 1 fully ablaze
  charred?: number; // 0..1 blackening
  sign?: React.ReactNode;
  lean?: number; // flame wind lean
  fireScale?: number;
};

/**
 * 17th-century London house: timber frame with plaster infill, jettied
 * (overhanging) upper storeys, leaded diamond-pane windows, steep gable.
 */
export const House: React.FC<HouseProps> = ({x, y, w, floors = 3, seed = 0, burn = 0, charred = 0, sign, lean = -70, fireScale = 1}) => {
  const f = useCurrentFrame();
  const fh = 190;
  const jetty = 26; // overhang per floor
  const plaster = PLASTER[seed % PLASTER.length];
  const roof = ROOF[seed % ROOF.length];
  const parts: React.ReactNode[] = [];
  const glow = Math.min(1, burn * 2.2);
  const flick = 0.75 + 0.25 * Math.sin(f * 0.9 + seed);
  for (let i = 0; i < floors; i++) {
    const ox = i * jetty;
    const fx = x - ox;
    const fw = w + ox * 2;
    const fy = y - (i + 1) * fh;
    parts.push(
      <g key={`f${i}`}>
        <rect x={fx} y={fy} width={fw} height={fh} fill={plaster} stroke={INK} strokeWidth={6} />
        {/* timber posts + braces */}
        {[0, 1, 2, 3].map((k) => (
          <rect key={k} x={fx + (fw - 18) * (k / 3)} y={fy} width={18} height={fh} fill="#3a2414" />
        ))}
        <rect x={fx} y={fy} width={fw} height={16} fill="#3a2414" />
        <rect x={fx} y={fy + fh - 16} width={fw} height={16} fill="#3a2414" />
        {(i + seed) % 2 === 0 ? (
          <path d={`M${fx + 9} ${fy + fh} L${fx + fw / 3} ${fy + 16} M${fx + fw - 9} ${fy + fh} L${fx + (2 * fw) / 3} ${fy + 16}`} stroke="#3a2414" strokeWidth={14} />
        ) : (
          <path d={`M${fx + fw / 3} ${fy + fh / 2} L${fx + (2 * fw) / 3} ${fy + fh / 2}`} stroke="#3a2414" strokeWidth={14} />
        )}
        {/* leaded window */}
        {i > 0 || floors === 1 ? (
          <g>
            <rect x={fx + fw * 0.36} y={fy + 50} width={fw * 0.28} height={90} fill={glow > 0 ? `rgba(255,${150 - glow * 60},40,${0.5 + glow * 0.5 * flick})` : '#3d4a55'} stroke="#3a2414" strokeWidth={8} />
            <rect x={fx + fw * 0.36} y={fy + 50} width={fw * 0.28} height={90} fill="url(#lattice)" />
          </g>
        ) : (
          <g>
            {/* ground floor: shop front / door */}
            <rect x={fx + fw * 0.12} y={fy + 60} width={fw * 0.26} height={fh - 60} fill="#4a2c18" stroke={INK} strokeWidth={5} />
            <rect x={fx + fw * 0.5} y={fy + 50} width={fw * 0.38} height={80} fill={glow > 0 ? `rgba(255,130,30,${0.4 + glow * 0.6 * flick})` : '#3d4a55'} stroke="#3a2414" strokeWidth={8} />
            <rect x={fx + fw * 0.5} y={fy + 50} width={fw * 0.38} height={80} fill="url(#lattice)" />
          </g>
        )}
        {/* jetty shadow */}
        {i > 0 && <rect x={fx + jetty} y={fy + fh} width={fw - jetty * 2} height={14} fill="rgba(0,0,0,0.35)" />}
      </g>,
    );
  }
  const topW = w + (floors - 1) * jetty * 2;
  const topX = x - (floors - 1) * jetty;
  const topY = y - floors * fh;
  const peak = topY - topW * 0.62;
  return (
    <g>
      {parts}
      {/* gable roof facing street */}
      <path d={`M${topX - 16} ${topY} L${topX + topW / 2} ${peak} L${topX + topW + 16} ${topY} Z`} fill={roof} stroke={INK} strokeWidth={7} strokeLinejoin="round" />
      <path d={`M${topX + topW * 0.22} ${topY - 4} L${topX + topW / 2} ${peak + 50} L${topX + topW * 0.78} ${topY - 4} Z`} fill={plaster} stroke="#3a2414" strokeWidth={10} />
      <rect x={topX + topW / 2 - 22} y={topY - 110} width={44} height={60} fill={glow > 0 ? `rgba(255,140,40,${glow * flick})` : '#3d4a55'} stroke="#3a2414" strokeWidth={6} />
      {/* chimney */}
      <rect x={topX + topW * 0.72} y={peak + 40} width={38} height={110} fill="#8a4a32" stroke={INK} strokeWidth={6} />
      {sign}
      {charred > 0 && (
        <rect x={topX - 20} y={peak} width={topW + 40} height={y - peak} fill="#120a06" opacity={charred * 0.75} />
      )}
      {burn > 0.25 && (
        <g>
          <Flame x={topX + topW / 2} y={topY + 10} w={topW * 0.9} h={360 * fireScale} seed={`r${seed}`} intensity={Math.min(1, (burn - 0.25) * 1.6)} lean={lean} />
          {floors > 1 && <Flame x={x + w / 2} y={y - fh - 40} w={w * 0.5} h={200 * fireScale} seed={`w${seed}`} intensity={Math.min(1, (burn - 0.45) * 2)} lean={lean} tongues={10} glow={false} />}
        </g>
      )}
    </g>
  );
};

/** A row of houses packed tightly together, the way London was in 1666. */
export const HouseRow: React.FC<{
  y: number;
  x0?: number;
  count?: number;
  widths?: number[];
  scroll?: number;
  seedBase?: number;
  burnAt?: (i: number, cx: number) => number;
  charred?: number;
  lean?: number;
  floors?: (i: number) => number;
}> = ({y, x0 = -200, count = 8, widths, scroll = 0, seedBase = 0, burnAt, charred = 0, lean = -70, floors}) => {
  const els = [];
  let x = x0 - scroll;
  for (let i = 0; i < count; i++) {
    const w = widths ? widths[i % widths.length] : 220 + ((i * 53 + seedBase * 7) % 80);
    const cx = x + w / 2;
    if (x < W + 400 && x + w > -400) {
      els.push(
        <House
          key={i}
          x={x + 30}
          y={y}
          w={w - 60}
          floors={floors ? floors(i) : 3 + ((i + seedBase) % 2)}
          seed={i + seedBase}
          burn={burnAt ? burnAt(i, cx) : 0}
          charred={charred}
          lean={lean}
        />,
      );
    }
    x += w;
  }
  return <g>{els}</g>;
};

/** Distant skyline silhouette: roofs, church towers and Old St Paul's tower. */
export const Skyline: React.FC<{y: number; color?: string; scroll?: number; withStPauls?: boolean}> = ({y, color = '#2a1712', scroll = 0, withStPauls = true}) => {
  const pts: string[] = [`${-200} ${y + 200}`];
  for (let i = 0; i < 30; i++) {
    const x = -200 + i * 60 - (scroll % 60);
    const hgt = 60 + random(`sk${i + Math.floor(scroll / 60)}`) * 90;
    pts.push(`${x} ${y - hgt * 0.4}`, `${x + 30} ${y - hgt}`, `${x + 60} ${y - hgt * 0.4}`);
  }
  pts.push(`${W + 200} ${y + 200}`);
  return (
    <g fill={color}>
      <polygon points={pts.join(' ')} />
      <rect x={-200} y={y - 20} width={W + 400} height={400} />
      {/* parish church spires */}
      {[140, 470, 880].map((cx, i) => (
        <g key={i} transform={`translate(${cx - scroll * 0.2} ${y - 120})`}>
          <rect x={-18} y={-120} width={36} height={160} />
          <path d="M-22 -120 L0 -230 L22 -120 Z" />
        </g>
      ))}
      {withStPauls && (
        <g transform={`translate(${650 - scroll * 0.2} ${y - 60})`}>
          {/* long nave + square central tower (its spire was lost in 1561) */}
          <rect x={-260} y={-120} width={520} height={160} />
          <path d="M-260 -120 L0 -190 L260 -120 Z" />
          <rect x={-55} y={-330} width={110} height={240} />
          {[-45, -15, 15, 45].map((p) => (
            <rect key={p} x={p - 7} y={-360} width={14} height={34} />
          ))}
        </g>
      )}
    </g>
  );
};

/** Cobbled street with a central gutter (kennel). */
export const Street: React.FC<{y: number; scroll?: number; tint?: string}> = ({y, scroll = 0, tint}) => (
  <g>
    <rect x={0} y={y} width={W} height={H - y} fill="url(#cobble)" />
    {new Array(7).fill(0).map((_, r) => (
      <g key={r}>
        {new Array(16).fill(0).map((__, c) => {
          const rw = 90 + r * 18;
          const cx = ((c * rw + (r % 2) * rw * 0.5 - scroll * (1 + r * 0.15)) % (rw * 14) + rw * 14) % (rw * 14) - rw;
          return <ellipse key={c} cx={cx} cy={y + 30 + r * (40 + r * 8)} rx={rw * 0.42} ry={14 + r * 3} fill="rgba(0,0,0,0.22)" />;
        })}
      </g>
    ))}
    <rect x={0} y={y + 210} width={W} height={10} fill="rgba(0,0,0,0.35)" />
    <line x1={0} x2={W} y1={y} y2={y} stroke={INK} strokeWidth={8} />
    {tint && <rect x={0} y={y} width={W} height={H - y} fill={tint} />}
  </g>
);

/* ------------------------------------------------------ Londoners 1666 */
export type PersonKind = 'man' | 'woman' | 'boy' | 'merchant';
const CLOTH: Record<PersonKind, {coat: string; hat: string; skin: string}> = {
  man: {coat: '#5a3d2b', hat: '#222', skin: '#e6b994'},
  woman: {coat: '#6b4f7a', hat: '#f2ece0', skin: '#f0c9a6'},
  boy: {coat: '#3f5a3c', hat: '#5a4030', skin: '#d9a57f'},
  merchant: {coat: '#7a2a24', hat: '#1b1b1b', skin: '#e9be9a'},
};

/**
 * A 17th-century Londoner: men in doublet, breeches, stockings, falling-band
 * collar and wide-brimmed hat; women in long skirt, apron, shawl and coif.
 */
export const Person: React.FC<{
  x: number;
  y: number;
  kind?: PersonKind;
  s?: number;
  facing?: 1 | -1;
  run?: number; // phase in radians; NaN = standing
  panic?: boolean;
  bundle?: boolean;
  silhouette?: string;
}> = ({x, y, kind = 'man', s = 1, facing = 1, run, panic = false, bundle = false, silhouette}) => {
  const c = CLOTH[kind];
  const isRun = run !== undefined && !Number.isNaN(run);
  const sw = isRun ? Math.sin(run!) : 0;
  const bob = isRun ? Math.abs(Math.cos(run!)) * 10 : 0;
  const ink = silhouette ? silhouette : INK;
  const fill = (col: string) => silhouette ?? col;
  const legs =
    kind === 'woman' ? null : (
      <g stroke={ink} strokeWidth={12} strokeLinecap="round">
        <line x1={-10} y1={-110} x2={-10 + sw * 40} y2={-10} stroke={fill('#d8d0c0')} />
        <line x1={10} y1={-110} x2={10 - sw * 40} y2={-10} stroke={fill('#d8d0c0')} />
        <ellipse cx={-10 + sw * 40 + 8} cy={-6} rx={16} ry={8} fill={ink} stroke="none" />
        <ellipse cx={10 - sw * 40 + 8} cy={-6} rx={16} ry={8} fill={ink} stroke="none" />
      </g>
    );
  const armA = panic ? -150 + Math.sin((run ?? 0) * 2) * 20 : isRun ? -sw * 50 : 10;
  const armB = panic ? 150 - Math.sin((run ?? 0) * 2) * 20 : isRun ? sw * 50 : -10;
  return (
    <g transform={`translate(${x} ${y - bob * s}) scale(${s * facing} ${s})`}>
      {!silhouette && <ellipse cx={0} cy={0} rx={50} ry={9} fill="rgba(0,0,0,0.35)" />}
      {legs}
      {kind === 'woman' ? (
        <g>
          <path d={`M-30 -150 L-48 ${-4 + sw * 3} L48 ${-4 - sw * 3} L30 -150 Z`} fill={fill(c.coat)} stroke={ink} strokeWidth={6} />
          <path d="M-18 -140 L-24 -20 L24 -20 L18 -140 Z" fill={fill('#efe6d6')} stroke={ink} strokeWidth={4} />
          <path d="M-30 -200 L-34 -140 L34 -140 L30 -200 Z" fill={fill('#3c2f45')} stroke={ink} strokeWidth={6} />
        </g>
      ) : (
        <g>
          <path d="M-30 -205 L-36 -110 L36 -110 L30 -205 Z" fill={fill(c.coat)} stroke={ink} strokeWidth={6} />
          <rect x={-34} y={-120} width={68} height={22} fill={fill('#2d2620')} stroke={ink} strokeWidth={5} />
          <path d="M-22 -205 L0 -186 L22 -205 Z" fill={fill('#f4efe4')} stroke={ink} strokeWidth={4} />
        </g>
      )}
      {/* arms */}
      <g transform={`translate(-26 -195) rotate(${armA})`}>
        <line x1={0} y1={0} x2={0} y2={70} stroke={fill(c.coat)} strokeWidth={14} strokeLinecap="round" />
        <circle cx={0} cy={76} r={9} fill={fill(c.skin)} stroke={ink} strokeWidth={3} />
      </g>
      <g transform={`translate(26 -195) rotate(${armB})`}>
        <line x1={0} y1={0} x2={0} y2={70} stroke={fill(c.coat)} strokeWidth={14} strokeLinecap="round" />
        <circle cx={0} cy={76} r={9} fill={fill(c.skin)} stroke={ink} strokeWidth={3} />
      </g>
      {bundle && (
        <g transform="translate(-40 -150)">
          <circle r={32} fill={fill('#b9a27a')} stroke={ink} strokeWidth={5} />
          <path d="M-10 -30 Q0 -46 10 -30" stroke={ink} strokeWidth={5} fill="none" />
        </g>
      )}
      {/* head */}
      <circle cx={0} cy={-232} r={30} fill={fill(c.skin)} stroke={ink} strokeWidth={5} />
      {!silhouette && (
        <g>
          <circle cx={10} cy={-236} r={3.5} fill={INK} />
          {panic ? <ellipse cx={14} cy={-218} rx={6} ry={8} fill={INK} /> : <path d="M6 -220 Q14 -216 20 -222" stroke={INK} strokeWidth={3} fill="none" />}
          {kind === 'man' || kind === 'merchant' ? <path d="M-28 -240 Q-34 -206 -22 -200" stroke="#4a3020" strokeWidth={10} fill="none" /> : null}
        </g>
      )}
      {/* headwear */}
      {kind === 'woman' ? (
        <path d="M-34 -230 Q-36 -268 0 -270 Q36 -268 34 -230 Q20 -246 -34 -230 Z" fill={fill(c.hat)} stroke={ink} strokeWidth={5} />
      ) : kind === 'boy' ? (
        <path d="M-30 -246 Q0 -276 30 -246 Z" fill={fill(c.hat)} stroke={ink} strokeWidth={5} />
      ) : (
        <g>
          <ellipse cx={0} cy={-252} rx={56} ry={10} fill={fill(c.hat)} stroke={ink} strokeWidth={5} />
          <path d="M-26 -252 L-22 -300 L22 -300 L26 -252 Z" fill={fill(c.hat)} stroke={ink} strokeWidth={5} />
        </g>
      )}
    </g>
  );
};

/** A crowd of fleeing Londoners crossing the frame. */
export const FleeingCrowd: React.FC<{
  y: number;
  count?: number;
  dir?: 1 | -1;
  speed?: number;
  s?: number;
  seed?: string;
  silhouette?: string;
  start?: number; // frame offset
}> = ({y, count = 8, dir = -1, speed = 14, s = 1, seed = 'c', silhouette, start = 0}) => {
  const f = useCurrentFrame() - start;
  const kinds: PersonKind[] = ['man', 'woman', 'boy', 'merchant'];
  const span = W + 600;
  return (
    <g>
      {new Array(count).fill(0).map((_, i) => {
        const off = random(`${seed}o${i}`) * span;
        const sp = speed * (0.8 + random(`${seed}s${i}`) * 0.5);
        let x = off + f * sp;
        x = ((x % span) + span) % span - 300;
        if (dir === -1) x = W - x;
        return (
          <Person
            key={i}
            x={x}
            y={y + random(`${seed}y${i}`) * 40 * s}
            s={s * (0.9 + random(`${seed}z${i}`) * 0.2)}
            kind={kinds[Math.floor(random(`${seed}k${i}`) * 4)]}
            facing={dir}
            run={f * 0.55 + i}
            panic={random(`${seed}p${i}`) > 0.55}
            bundle={random(`${seed}b${i}`) > 0.6}
            silhouette={silhouette}
          />
        );
      })}
    </g>
  );
};

/* ------------------------------------------------------- the bakery */
export const Bakery: React.FC<{x: number; y: number; burn: number; s?: number}> = ({x, y, burn, s = 1}) => {
  const f = useCurrentFrame();
  const oven = 0.6 + 0.4 * Math.sin(f * 0.5);
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <House
        x={-210}
        y={0}
        w={420}
        floors={3}
        seed={3}
        burn={burn}
        fireScale={1.3}
        sign={
          <g transform="translate(250 -330)">
            <line x1={-40} y1={0} x2={60} y2={0} stroke="#2a1a0e" strokeWidth={10} />
            <g transform={`rotate(${Math.sin(f * 0.08) * 5} 50 0)`}>
              <line x1={50} y1={0} x2={50} y2={20} stroke="#2a1a0e" strokeWidth={4} />
              <rect x={-10} y={20} width={120} height={84} rx={10} fill="#d9b25a" stroke={INK} strokeWidth={6} />
              {/* loaf emblem */}
              <ellipse cx={50} cy={62} rx={40} ry={22} fill="#b9772e" stroke={INK} strokeWidth={5} />
              <path d="M28 52 L36 72 M46 48 L54 72 M64 50 L70 70" stroke="#7a4a1a" strokeWidth={4} />
            </g>
          </g>
        }
      />
      {/* oven glow from the shop window */}
      <rect x={-210 + 420 * 0.5} y={-140} width={420 * 0.38} height={80} fill={`rgba(255,120,30,${0.35 * oven})`} />
      {/* loaves on the shop counter */}
      <rect x={-120} y={-60} width={250} height={22} fill="#6b4220" stroke={INK} strokeWidth={5} />
      {[-90, -40, 10, 60, 100].map((lx, i) => (
        <ellipse key={i} cx={lx} cy={-68} rx={22} ry={12} fill="#c98a3c" stroke={INK} strokeWidth={4} />
      ))}
      {/* firewood stacked by the door (bakers kept fuel close) */}
      {[0, 1, 2].map((r) => (
        <g key={r}>
          {[0, 1, 2, 3].map((k) => (
            <circle key={k} cx={-250 + k * 26 + (r % 2) * 13} cy={-14 - r * 24} r={13} fill="#8a5a2e" stroke={INK} strokeWidth={4} />
          ))}
        </g>
      ))}
    </g>
  );
};

/* -------------------------------------------------- Old St Paul's */
export const OldStPauls: React.FC<{x: number; y: number; s?: number; burn?: number; ruin?: number; collapse?: number}> = ({
  x,
  y,
  s = 1,
  burn = 0,
  ruin = 0,
  collapse = 0,
}) => {
  const stone = ruin > 0 ? '#6f6760' : '#b9ad98';
  const dark = ruin > 0 ? '#4a4440' : '#8f8370';
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      {/* nave */}
      <rect x={-460} y={-330} width={920} height={330} fill={stone} stroke={INK} strokeWidth={8} />
      {/* roof (collapses) */}
      {ruin < 0.5 && (
        <g transform={`translate(0 ${collapse * 120}) rotate(${collapse * 6})`} opacity={1 - collapse * 0.7}>
          <path d="M-470 -330 L0 -470 L470 -330 Z" fill="#5d6a72" stroke={INK} strokeWidth={8} />
        </g>
      )}
      {/* buttresses + pointed gothic windows */}
      {new Array(9).fill(0).map((_, i) => {
        const bx = -420 + i * 105;
        return (
          <g key={i}>
            <rect x={bx - 14} y={-320} width={28} height={320} fill={dark} stroke={INK} strokeWidth={5} />
            {i < 8 && (
              <path
                d={`M${bx + 30} -60 L${bx + 30} -210 Q${bx + 52} -270 ${bx + 74} -210 L${bx + 74} -60 Z`}
                fill={burn > 0 ? `rgba(255,${160 - burn * 80},40,${0.5 + burn * 0.5})` : ruin > 0 ? '#1d1916' : '#33414d'}
                stroke={INK}
                strokeWidth={5}
              />
            )}
          </g>
        );
      })}
      {/* square central tower — no spire after the 1561 lightning strike */}
      <g>
        <rect x={-110} y={-760} width={220} height={440} fill={stone} stroke={INK} strokeWidth={8} />
        {ruin === 0 && [-80, -27, 27, 80].map((p) => <rect key={p} x={p - 16} y={-800} width={32} height={44} fill={stone} stroke={INK} strokeWidth={6} />)}
        {ruin > 0 && <path d="M-110 -760 L-70 -800 L-20 -770 L30 -820 L80 -780 L110 -760 Z" fill={stone} stroke={INK} strokeWidth={6} />}
        {[-50, 50].map((p) => (
          <path key={p} d={`M${p - 22} -460 L${p - 22} -640 Q${p} -700 ${p + 22} -640 L${p + 22} -460 Z`} fill={burn > 0 ? 'rgba(255,140,40,0.85)' : ruin > 0 ? '#1d1916' : '#33414d'} stroke={INK} strokeWidth={5} />
        ))}
      </g>
      {/* Inigo Jones's classical west portico (1630s) */}
      <g transform="translate(-560 0)">
        <rect x={-110} y={-280} width={220} height={280} fill={stone} stroke={INK} strokeWidth={7} />
        <path d="M-130 -280 L0 -360 L130 -280 Z" fill={stone} stroke={INK} strokeWidth={7} />
        {[-80, -40, 0, 40, 80].map((p) => (
          <rect key={p} x={p - 10} y={-270} width={20} height={270} fill="#d6ccb8" stroke={INK} strokeWidth={4} />
        ))}
      </g>
      {ruin > 0 && (
        <g fill="#2b2622">
          <path d="M-460 -330 L-380 -380 L-300 -320 L-200 -360 L-120 -330 Z" />
          <path d="M120 -330 L220 -370 L300 -320 L400 -350 L460 -330 Z" />
        </g>
      )}
      {burn > 0 && (
        <g>
          {[-380, -230, -80, 80, 230, 380].map((fx, i) => (
            <Flame key={i} x={fx} y={-330 + collapse * 60} w={240} h={420} seed={`sp${i}`} intensity={burn} lean={-90} tongues={12} glow={i % 2 === 0} />
          ))}
          <Flame x={0} y={-760} w={200} h={380} seed="spt" intensity={burn * 0.9} lean={-80} />
        </g>
      )}
    </g>
  );
};

/* --------------------------------------------------------- ruins */
export const Ruins: React.FC<{y: number; seed?: string}> = ({y, seed = 'ru'}) => {
  const els = [];
  for (let i = 0; i < 7; i++) {
    const x = -60 + i * 180 + random(`${seed}x${i}`) * 40;
    const h = 160 + random(`${seed}h${i}`) * 260;
    els.push(
      <g key={i}>
        {/* broken wall stub */}
        <path d={`M${x} ${y} L${x} ${y - h} L${x + 40} ${y - h + 30} L${x + 80} ${y - h - 20} L${x + 120} ${y - h + 50} L${x + 140} ${y}`} fill="#4b4540" stroke={INK} strokeWidth={6} />
        {/* surviving brick chimney stack */}
        {i % 2 === 0 && <rect x={x + 50} y={y - h - 160} width={44} height={160} fill="#6d3d2c" stroke={INK} strokeWidth={6} />}
        {/* charred beams */}
        <line x1={x + 10} y1={y - 20} x2={x + 150} y2={y - 90 - random(`${seed}b${i}`) * 60} stroke="#1b1410" strokeWidth={16} strokeLinecap="round" />
      </g>,
    );
  }
  return (
    <g>
      {els}
      {/* rubble */}
      {new Array(40).fill(0).map((_, i) => (
        <ellipse key={i} cx={random(`${seed}rx${i}`) * W} cy={y + random(`${seed}ry${i}`) * 60} rx={20 + random(`${seed}rr${i}`) * 40} ry={10 + random(`${seed}rh${i}`) * 14} fill={i % 3 ? '#3b3632' : '#5a524b'} />
      ))}
    </g>
  );
};
