// Vertical (1080x1920) scenes for "I Witnessed the Last Day of Pompeii!".
// Same red-cap hero and comic effects as the other History World episodes; adds Pompeii, Vesuvius and volcanic ash.
import React from 'react';
import {C, blinkAt, clamp, ease, easeIn, easeOut, lerp, prog, rng, backOut, mixHex} from './lib';
import {Doodle, DoodleProps} from './Hero';
import {Burst, Glow, HAND, Pop, Sweat, Txt, Confetti} from './fx';

export const VW = 1080;
export const VH = 1920;
export type Cue = (text: string, frac?: number) => number;
export type ShotProps = {t: number; D: number; cue: Cue};

const feet = (yFeet: number, s: number) => yFeet - 456 * s;
const Hero: React.FC<DoodleProps> = (p) => <Doodle blink={blinkAt(p.x * 0.013 + (p.walk ?? 0))} {...p} />;
const runArms = (t: number, sp = 3): Partial<DoodleProps> => {
  const sw = Math.sin(t * sp * 2 * Math.PI);
  return {walk: t * sp, larm: [0.9 * sw, 0.9], rarm: [0.9 * sw, -0.9]};
};

// ------------------------------------------------------------------ framing helpers
const VCam: React.FC<{cx: number; cy: number; z?: number; shake?: number; t?: number; children: React.ReactNode}> = ({cx, cy, z = 1, shake = 0, t = 0, children}) => {
  const sx = shake * (Math.sin(t * 47) + Math.sin(t * 31)) * 0.5;
  const sy = shake * (Math.cos(t * 53) + Math.sin(t * 37)) * 0.5;
  return <g transform={`translate(${VW / 2 + sx},${VH / 2 + sy}) scale(${z}) translate(${-cx},${-cy})`}>{children}</g>;
};
const Vig: React.FC<{s?: number; color?: string}> = ({s = 0.5, color = '#000'}) => {
  const id = `vg${Math.round(s * 100)}${color.slice(1)}`;
  return (
    <g>
      <defs>
        <radialGradient id={id} cx="50%" cy="42%" r="72%">
          <stop offset="50%" stopColor={color} stopOpacity={0} />
          <stop offset="100%" stopColor={color} stopOpacity={s} />
        </radialGradient>
      </defs>
      <rect x={0} y={0} width={VW} height={VH} fill={`url(#${id})`} />
    </g>
  );
};
const Fill: React.FC<{c: string; a: number}> = ({c, a}) => (a > 0.001 ? <rect x={0} y={0} width={VW} height={VH} fill={c} opacity={clamp(a)} /> : null);

// ------------------------------------------------------------------ sky, Vesuvius, eruption
/** sky that goes from a sunny blue (dark=0) to an ash-black (dark=1) */
const Sky: React.FC<{id: string; dark: number; modern?: boolean}> = ({id, dark, modern}) => {
  const top = mixHex(modern ? '#6ab8f0' : '#7ec0ee', '#1a1414', dark);
  const bot = mixHex(modern ? '#e6f4fc' : '#fde8c0', '#4a3428', dark);
  return (
    <g>
      <defs>
        <linearGradient id={id} x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={top} />
          <stop offset="1" stopColor={bot} />
        </linearGradient>
      </defs>
      <rect x={-3000} y={-3000} width={9000} height={8000} fill={`url(#${id})`} />
      {dark < 0.3 && <circle cx={820} cy={300} r={70} fill="#fff3b0" opacity={1 - dark * 3} />}
    </g>
  );
};

/** Mount Vesuvius: (x, y) = base centre, width ~1400*s */
const Vesuvius: React.FC<{x: number; y: number; s?: number; dark?: number; glow?: number}> = ({x, y, s = 1, dark = 0, glow = 0}) => {
  const body = mixHex('#7a8a5a', '#2a2420', dark);
  const shade = mixHex('#5a6a44', '#1a1614', dark);
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <path d="M-760,0 C-560,-120 -380,-330 -170,-470 L-120,-490 L-60,-450 L40,-460 L110,-500 C300,-360 520,-140 760,0 Z" fill={body} stroke={C.ink} strokeWidth={8} strokeLinejoin="round" />
      <path d="M-120,-490 L-60,-450 L-160,-200 L-300,-80 L-420,0 L-760,0 C-560,-120 -380,-330 -170,-470 Z" fill={shade} opacity={0.6} />
      <path d="M110,-500 C200,-420 260,-320 300,-220 M-170,-470 C-210,-380 -260,-300 -330,-220" fill="none" stroke={C.ink} strokeWidth={4} opacity={0.4} />
      {glow > 0 && <g opacity={glow}>
        <path d="M-60,-450 C-40,-300 -90,-200 -40,-60 M40,-460 C70,-330 30,-230 90,-120" fill="none" stroke="#ff7a1a" strokeWidth={14} strokeLinecap="round" />
        <Glow id={`vg${Math.round(x)}`} x={-10} y={-470} r={260} color="#ff6a1a" a={0.9} />
      </g>}
    </g>
  );
};

/** the Plinian eruption column rising from (x, y); k = 0..1 growth, umbrella cloud at the top */
const Column: React.FC<{x: number; y: number; t: number; k: number; s?: number; spread?: number; h?: number}> = ({x, y, t, k, s = 1, spread = 1, h: h0 = 1500}) => {
  if (k <= 0) return null;
  const R = rng(17);
  const h = h0 * easeOut(k);
  const puffs: React.ReactNode[] = [];
  const N = 30;
  for (let i = 0; i < N; i++) {
    const f = i / (N - 1);
    const show = f <= k * 1.05;
    const yy = -h * f;
    const w = 60 + f * 280;
    for (let j = 0; j < 2; j++) {
      const rx = (R() - 0.5) * w + Math.sin(t * 1.4 + i + j * 2) * 12;
      const r = 55 + f * 85 + R() * 25;
      if (show) puffs.push(<circle key={`${i}${j}`} cx={rx} cy={yy + (R() - 0.5) * 30} r={r * (0.92 + 0.08 * Math.sin(t * 2 + i))}
        fill={['#5a4e48', '#6a5e56', '#4e443e'][(i + j) % 3]} stroke={C.ink} strokeWidth={5} />);
    }
  }
  const top: React.ReactNode[] = [];
  if (k > 0.5) {
    const u = easeOut(prog(k, 0.5, 1)) * spread;
    for (let i = 0; i < 22; i++) {
      const a = (i / 21 - 0.5) * 2;
      const r = 110 + R() * 80;
      top.push(<circle key={i} cx={a * 620 * u + (R() - 0.5) * 60} cy={-h - 60 + a * a * 140 * u + (R() - 0.5) * 80 + Math.sin(t + i) * 10} r={r * (0.55 + 0.45 * u)}
        fill={['#4a403a', '#5a4e48', '#3e3632'][i % 3]} stroke={C.ink} strokeWidth={5} />);
    }
  }
  const flash = Math.sin(t * 9.3) > 0.9 && k > 0.4;
  return (
    <g transform={`translate(${x},${y}) scale(${s})`}>
      <Glow id={`cg${Math.round(x)}${Math.round(y)}`} x={0} y={-40} r={340} color="#ff6a1a" a={0.75} />
      {puffs}
      {top}
      {flash && <path d={`M${-90},${-h * 0.75} l70,90 l-50,14 l90,130`} fill="none" stroke="#fff7a0" strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" />}
      {[0, 1, 2, 3, 4].map((i) => {
        const ph = (t * 0.9 + i / 5) % 1;
        return <circle key={'b' + i} cx={(i - 2) * 60 + ph * (i - 2) * 140} cy={-60 - ph * 260 + ph * ph * 380} r={10} fill="#ff8a2a" stroke={C.ink} strokeWidth={3} opacity={1 - ph} />;
      })}
    </g>
  );
};

/** falling ash flakes + small pumice stones, in screen space */
const AshFall: React.FC<{t: number; n?: number; a?: number; speed?: number; seed?: number; stones?: boolean}> = ({t, n = 140, a = 1, speed = 160, seed = 1, stones}) => {
  if (a <= 0) return null;
  const R = rng(seed);
  return (
    <g opacity={a}>
      {Array.from({length: n}).map((_, i) => {
        const sp = speed * (0.6 + R() * 0.8);
        const x = (R() * VW + Math.sin(t * 1.3 + i) * 30 + t * 40) % VW;
        const y = ((R() * VH + t * sp) % (VH + 40)) - 20;
        const r = 2 + R() * 5;
        const stone = stones && i % 9 === 0;
        return stone
          ? <circle key={i} cx={x} cy={(y * 1.6) % VH} r={r + 4} fill="#c8bca8" stroke={C.ink} strokeWidth={2.5} />
          : <circle key={i} cx={x} cy={y} r={r} fill="#d8d0c8" opacity={0.75} />;
      })}
    </g>
  );
};

// ------------------------------------------------------------------ Pompeii
const WALLS = ['#c8423a', '#e0a24a', '#f0dcb0', '#b85a3a', '#e8c890'];

/** a Roman house/shop front: (x, y) = bottom-left. ash = 0..1 ash layer on roof and ledges */
const RomanHouse: React.FC<{x: number; y: number; w?: number; h?: number; c?: string; shop?: boolean; ash?: number; cols?: boolean; dark?: number}> = ({
  x, y, w = 360, h = 420, c = '#c8423a', shop, ash = 0, cols, dark = 0,
}) => {
  const wall = mixHex(c, '#3a3030', dark * 0.75);
  const roof = mixHex('#b8582e', '#3a2a24', dark * 0.75);
  return (
    <g>
      <rect x={x} y={y - h} width={w} height={h} fill={wall} stroke={C.ink} strokeWidth={6} />
      <rect x={x} y={y - h * 0.32} width={w} height={h * 0.32} fill="rgba(0,0,0,0.12)" />
      <path d={`M${x - 24},${y - h} L${x + w / 2},${y - h - 90} L${x + w + 24},${y - h} Z`} fill={roof} stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
      {Array.from({length: 6}).map((_, i) => <line key={i} x1={x + w / 2} y1={y - h - 90} x2={x - 20 + (i * (w + 40)) / 5} y2={y - h} stroke={C.ink} strokeWidth={2.5} opacity={0.35} />)}
      {ash > 0 && <path d={`M${x - 24},${y - h} L${x + w / 2},${y - h - 90} L${x + w + 24},${y - h} L${x + w + 24},${y - h + 4} L${x + w / 2},${y - h - 90 + 40 * ash + 10} L${x - 24},${y - h + 4} Z`}
        fill="#bcb4ac" stroke={C.ink} strokeWidth={3} transform={`translate(0,${-34 * ash})`} />}
      {cols && [0.18, 0.82].map((f) => (
        <g key={f}>
          <rect x={x + w * f - 18} y={y - h * 0.62} width={36} height={h * 0.62} fill="#f6efe0" stroke={C.ink} strokeWidth={5} />
          <rect x={x + w * f - 28} y={y - h * 0.65} width={56} height={18} fill="#f6efe0" stroke={C.ink} strokeWidth={4} />
        </g>
      ))}
      {shop ? (
        <g>
          <rect x={x + 40} y={y - h * 0.6} width={w - 80} height={h * 0.6} fill={mixHex('#3a2418', '#100c0a', dark)} stroke={C.ink} strokeWidth={5} />
          <rect x={x + 30} y={y - 120} width={w - 60} height={120} fill={mixHex('#f0e4c8', '#5a5048', dark)} stroke={C.ink} strokeWidth={5} />
          {[0, 1, 2].map((k) => <circle key={k} cx={x + 90 + k * ((w - 180) / 2)} cy={y - 120} r={28} fill="#a0582a" stroke={C.ink} strokeWidth={4} />)}
          <path d={`M${x + 20},${y - h * 0.6} L${x + w - 20},${y - h * 0.6} L${x + w + 10},${y - h * 0.6 + 60} L${x - 10},${y - h * 0.6 + 60} Z`}
            fill={mixHex('#e8d8a8', '#4a4038', dark)} stroke={C.ink} strokeWidth={5} />
          {[0, 1, 2, 3].map((k) => <rect key={k} x={x + 10 + k * ((w - 20) / 4)} y={y - h * 0.6} width={(w - 20) / 8} height={60} fill={mixHex('#c8423a', '#3a2a28', dark)} opacity={0.8} />)}
        </g>
      ) : (
        <g>
          <rect x={x + w / 2 - 50} y={y - 190} width={100} height={190} rx={50} fill={mixHex('#5a3420', '#120c0a', dark)} stroke={C.ink} strokeWidth={5} />
          {[0.2, 0.8].map((f) => <rect key={f} x={x + w * f - 26} y={y - h + 70} width={52} height={64} fill={mixHex('#2a1a14', '#0a0808', dark)} stroke={C.ink} strokeWidth={4} />)}
        </g>
      )}
      {ash > 0 && <rect x={x - 4} y={y - h * 0.6 - 6 - 10 * ash} width={w + 8} height={6 + 10 * ash} fill="#bcb4ac" opacity={shop ? 1 : 0} />}
    </g>
  );
};

/** paved Roman street with raised kerbs and the famous stepping stones; ash = depth 0..1 */
const RomanStreet: React.FC<{y: number; x0?: number; x1?: number; ash?: number; dark?: number}> = ({y, x0 = -1200, x1 = 2400, ash = 0, dark = 0}) => {
  const st = mixHex('#8a8478', '#2a2624', dark * 0.8);
  return (
    <g>
      <rect x={x0} y={y} width={x1 - x0} height={40} fill={mixHex('#c8bca0', '#3a3430', dark * 0.8)} stroke={C.ink} strokeWidth={5} />
      <rect x={x0} y={y + 40} width={x1 - x0} height={1600} fill={st} stroke={C.ink} strokeWidth={5} />
      {Array.from({length: 60}).map((_, i) => (
        <path key={i} d={`M${x0 + (i % 20) * 180 + (Math.floor(i / 20) % 2) * 90},${y + 60 + Math.floor(i / 20) * 70} l150,0`} stroke={C.ink} strokeWidth={3} opacity={0.3} />
      ))}
      {[0, 1, 2].map((k) => <ellipse key={k} cx={540 + (k - 1) * 120} cy={y + 150} rx={46} ry={22} fill={mixHex('#b0a898', '#3a3634', dark * 0.8)} stroke={C.ink} strokeWidth={5} />)}
      {ash > 0 && <rect x={x0} y={y + 40 - 70 * ash} width={x1 - x0} height={1600} fill="#b4aca4" stroke={C.ink} strokeWidth={4} opacity={clamp(ash * 3)} />}
    </g>
  );
};

// ------------------------------------------------------------------ Romans (same doodle body as the hero, never a red cap)
const TUNIC = ['#f2ead8', '#e0a24a', '#8a5aa8', '#4a7ab8', '#c86a3a', '#6a9a5a', '#d8c8a0'];
const HAIRC = ['#2a1e14', '#5a3a20', '#1a1a1a', '#8a6a3a'];
const Roman: React.FC<DoodleProps & {seed?: number}> = ({seed = 0, ...p}) => {
  const style = seed % 4;
  const hair = HAIRC[seed % HAIRC.length];
  let front: React.ReactNode = null;
  let back: React.ReactNode = null;
  if (style === 0 || style === 2) {
    front = <g>{Array.from({length: 9}).map((_, i) => <circle key={i} cx={-84 + i * 21} cy={-82 + Math.abs(i - 4) * 6} r={22} fill={hair} stroke={C.ink} strokeWidth={4} />)}</g>;
    if (style === 2) front = <g>{front}<path d="M-96,-40 C-60,-110 60,-110 96,-40" fill="none" stroke="#5a9a3a" strokeWidth={14} strokeDasharray="18 8" strokeLinecap="round" /></g>;
  }
  if (style === 1) {
    const palla = ['#d86a8a', '#6a9ad8', '#e8c86a'][seed % 3];
    back = <path d="M-118,40 C-130,-110 -60,-140 0,-140 C60,-140 130,-110 118,40 L90,120 L-90,120 Z" fill={palla} stroke={C.ink} strokeWidth={6} />;
    front = <path d="M-112,-10 C-110,-120 110,-120 112,-10 C80,-80 -80,-80 -112,-10 Z" fill={palla} stroke={C.ink} strokeWidth={6} />;
  }
  if (style === 3) front = <path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill={hair} stroke={C.ink} strokeWidth={6} />;
  const belt = <rect x={-62} y={196} width={124} height={14} fill="#7a4a22" stroke={C.ink} strokeWidth={3} />;
  return <Doodle cap={false} body={TUNIC[seed % TUNIC.length]} blink={blinkAt(seed * 0.9 + p.x * 0.001, seed)} back={back} front={front} bodyExtra={belt} {...p} />;
};

const Archaeologist: React.FC<DoodleProps & {seed?: number}> = ({seed = 0, ...p}) => (
  <Doodle cap={false} body="#ff8a1a" blink={blinkAt(seed * 1.3, seed)}
    front={<g><path d="M-108,-30 C-110,-140 110,-140 108,-30 Z" fill="#ffd21a" stroke={C.ink} strokeWidth={6} /><rect x={-124} y={-40} width={248} height={20} rx={10} fill="#ffd21a" stroke={C.ink} strokeWidth={5} /></g>}
    bodyExtra={<g>{[150, 250].map((y) => <rect key={y} x={-60} y={y} width={120} height={14} fill="#e8f0f0" stroke={C.ink} strokeWidth={2} />)}</g>} {...p} />
);

const Basket: React.FC = () => (
  <g transform="translate(0,6)">
    <path d="M-40,0 L40,0 L30,50 L-30,50 Z" fill="#c8964a" stroke={C.ink} strokeWidth={4} />
    {[-20, 0, 20].map((x) => <circle key={x} cx={x} cy={-4} r={13} fill={x ? '#e04a3a' : '#7ab04a'} stroke={C.ink} strokeWidth={3} />)}
  </g>
);
const Amphora: React.FC = () => (
  <g transform="translate(0,10)">
    <path d="M-10,-40 L10,-40 L12,-20 C40,0 40,60 0,90 C-40,60 -40,0 -12,-20 Z" fill="#b8642e" stroke={C.ink} strokeWidth={4} />
  </g>
);
const Brush: React.FC = () => <g transform="rotate(30)"><rect x={-5} y={-50} width={10} height={50} fill="#8a5a2b" stroke={C.ink} strokeWidth={3} /><rect x={-12} y={0} width={24} height={26} fill="#e8d8a8" stroke={C.ink} strokeWidth={3} /></g>;

/** the market street (day) — shared by the hook, the city shot and the eruption reaction */
const Market: React.FC<{t: number; dark?: number; ash?: number}> = ({t, dark = 0, ash = 0}) => (
  <g>
    <RomanHouse x={-420} y={1380} w={380} h={480} c={WALLS[1]} dark={dark} ash={ash} />
    <RomanHouse x={-40} y={1380} w={400} h={440} c={WALLS[0]} shop dark={dark} ash={ash} />
    <RomanHouse x={360} y={1380} w={360} h={520} c={WALLS[2]} cols dark={dark} ash={ash} />
    <RomanHouse x={720} y={1380} w={400} h={460} c={WALLS[3]} shop dark={dark} ash={ash} />
    <RomanHouse x={1120} y={1380} w={380} h={500} c={WALLS[4]} dark={dark} ash={ash} />
    <RomanHouse x={1500} y={1380} w={400} h={440} c={WALLS[0]} shop dark={dark} ash={ash} />
    <RomanStreet y={1380} dark={dark} ash={ash} />
    {void t}
  </g>
);

// ================================================================== SCENES
// 1 — HOOK: black sky, the mountain explodes, he points at Vesuvius in terror
export const PHook: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBoom = 0.35;
  const tWhat = cue('WHAT IS');
  const k = prog(t, tBoom, D + 1.5);
  const dark = 0.35 + 0.6 * ease(prog(t, 0, 1.6));
  const zoom = t < tWhat ? lerp(1.55, 1.12, easeOut(prog(t, 0, 1.4))) : lerp(1.12, 1.6, easeOut(prog(t, tWhat, tWhat + 0.4)));
  const hy = feet(1470, 0.62);
  return (
    <g>
      <VCam cx={540} cy={t < tWhat ? 1000 : lerp(1000, 1080, easeOut(prog(t, tWhat, tWhat + 0.4)))} z={zoom} shake={t > tBoom ? lerp(26, 8, prog(t, tBoom, tBoom + 1.5)) : 0} t={t}>
        <Sky id="hks" dark={dark} />
        <Vesuvius x={300} y={1000} s={0.9} dark={dark} glow={prog(t, tBoom, tBoom + 0.4)} />
        <Column x={290} y={570} t={t} k={t > tBoom ? 0.15 + easeOut(k) * 0.8 : 0} s={0.75} />
        <Market t={t} dark={dark * 0.85} />
        <Roman seed={3} x={120} y={feet(1500, 0.5)} s={0.5} face={-0.6} look={[-0.8, -1]} expr="scared" larm={[2.4, 0.3]} rarm={[-2.4, -0.3]} />
        <Roman seed={5} x={950} y={feet(1500, 0.5)} s={0.5} face={-0.6} look={[-0.8, -1]} expr="shock" larm={[1.2, -1.0]} rarm={[-1.2, 1.0]} />
        <Hero x={600} y={hy} s={0.62} expr="scared" face={-0.5} look={[-1, -1]} brows="worried" tilt={0.03 * Math.sin(t * 25)}
          larm={[2.2, 0.0]} rarm={[-1.0, 1.2]} capOff={Math.sin(prog(t, tBoom, tBoom + 0.8) * Math.PI) * 0.3} />
        <Sweat x={690} y={hy - 50} t={t} />
      </VCam>
      <AshFall t={t} n={90} a={prog(t, tBoom + 0.6, tBoom + 1.6)} speed={260} stones />
      <Fill c="#fff2c0" a={(1 - prog(t, tBoom, tBoom + 0.3)) * (t > tBoom ? 0.9 : 0)} />
      {t > tBoom && <Burst t={t - tBoom} x={300} y={330} r={170} label="BOOM!" size={74} color="#ff8a2a" tcolor="#fff" hold={1.6} />}
      {t > tWhat && <Pop t={t - tWhat} x={540} y={300} size={96} color="#ffd84d" rot={-3}>WHAT IS HAPPENING?!</Pop>}
      <Vig s={0.65} />
      <Fill c="#000" a={prog(t, D - 0.2, D)} />
    </g>
  );
};

// 2 — Pompeii, 79 AD: an ordinary sunny day at the market
export const PCity: React.FC<ShotProps> = ({t, D, cue}) => {
  const tPeople = cue('People were shopping');
  const hx = lerp(80, 760, prog(t, 0.2, D));
  const lookL = Math.sin(t * 1.7) > 0;
  const walkers: [number, number, number, number][] = [[3, 1420, 90, 1], [8, 1480, -70, -1], [11, 1440, 110, 1], [6, 1500, -60, -1]];
  return (
    <g>
      <VCam cx={lerp(380, 860, ease(prog(t, 0, D)))} cy={1060} z={lerp(1.2, 1.12, prog(t, 0, D))}>
        <Sky id="cys" dark={0} />
        <Vesuvius x={560} y={1000} s={0.9} />
        <Market t={t} />
        {/* vendor at the counter + customers */}
        <Roman seed={4} x={160} y={feet(1300, 0.42)} s={0.42} face={0.6} expr="happy" showLegs={false} larm={[0.3, 0.2]} rarm={[-1.6, 0.6]} hold={<Amphora />} />
        <Roman seed={1} x={340} y={feet(1450, 0.5)} s={0.5} face={-0.7} expr="smile" larm={[0.3, 0.2]} rarm={[-1.4, 0.4]} hold={<Basket />} />
        <Roman seed={9} x={1000} y={feet(1300, 0.42)} s={0.42} face={-0.5} expr="laugh" showLegs={false} larm={[0.3, 0.2]} rarm={[-2.4 + 0.3 * Math.sin(t * 5), 0.3]} />
        <Roman seed={2} x={1160} y={feet(1460, 0.5)} s={0.5} face={-0.8} expr="happy" larm={[0.3, 0.2]} rarm={[-1.6 + 0.2 * Math.sin(t * 4), 1.0]} />
        <Roman seed={7} x={1290} y={feet(1460, 0.5)} s={0.5} face={0.8} expr="laugh" larm={[1.6, -1.0]} rarm={[-0.3, -0.2]} />
        {walkers.map(([seed, y, sp, dir], i) => (
          <Roman key={i} seed={seed} x={(((i * 430 + t * sp) % 1900) + 1900) % 1900 - 300} y={feet(y, 0.48)} s={0.48} face={0.85 * dir} walk={t * 1.4 + i}
            expr="smile" larm={[0.3, 0.2]} rarm={i % 2 ? [-1.4, 0.4] : [-0.3, -0.2]} hold={i % 2 ? <Basket /> : undefined} />
        ))}
        <Hero x={hx} y={feet(1480, 0.56)} s={0.56} expr={t > tPeople ? 'happy' : 'smile'} face={lookL ? -0.6 : 0.8} look={[lookL ? -1 : 1, -0.3]} walk={t * 1.3}
          larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </VCam>
      <g transform={`translate(540,330) scale(${backOut(prog(t, 0.3, 0.75), 2)})`}>
        <rect x={-330} y={-100} width={660} height={200} rx={26} fill="rgba(20,12,8,0.78)" stroke="#e8c070" strokeWidth={5} />
        <Txt x={0} y={-30} size={72} color="#fff" outline={0}>POMPEII</Txt>
        <Txt x={0} y={44} size={64} color="#ffd84d" outline={0}>79 AD</Txt>
      </g>
      <Vig s={0.3} />
    </g>
  );
};

// 3 — Vesuvius erupts: fast cuts — the mountain, the crowd freezing, his face
export const PErupt: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBoom = 0.55;
  const tCloud = cue('A giant cloud');
  const tFace = tCloud + 1.7;
  if (t < tCloud) {
    const k = prog(t, tBoom, tCloud + 2.5);
    return (
      <g>
        <VCam cx={540} cy={lerp(820, 700, easeOut(prog(t, tBoom, tCloud)))} z={lerp(1.25, 1.0, easeOut(prog(t, tBoom, tCloud)))} shake={t > tBoom ? 18 * (1 - prog(t, tBoom, tCloud) * 0.6) : 0} t={t}>
          <Sky id="ers" dark={0.25 * prog(t, tBoom, tCloud)} />
          <Column x={540} y={790} t={t} k={easeOut(k)} s={0.85} />
          <Vesuvius x={540} y={1250} s={1.0} glow={prog(t, tBoom, tBoom + 0.3)} dark={0.2 * prog(t, tBoom, tCloud)} />
          <RomanHouse x={-200} y={1500} w={360} h={300} c={WALLS[1]} />
          <RomanHouse x={160} y={1500} w={380} h={260} c={WALLS[2]} cols />
          <RomanHouse x={540} y={1500} w={360} h={320} c={WALLS[0]} />
          <RomanHouse x={900} y={1500} w={380} h={280} c={WALLS[4]} />
          <rect x={-400} y={1500} width={1900} height={600} fill="#8a8478" stroke={C.ink} strokeWidth={5} />
        </VCam>
        <Fill c="#fff2c0" a={t > tBoom ? (1 - prog(t, tBoom, tBoom + 0.35)) * 0.95 : 0} />
        {t > tBoom && <Burst t={t - tBoom} x={790} y={420} r={170} label="KABOOM!" size={62} color="#ff8a2a" tcolor="#fff" hold={1.4} />}
        <Vig s={0.5} />
      </g>
    );
  }
  if (t < tFace) {
    const tt = t - tCloud;
    const freeze = tt > 0.4;
    return (
      <g>
        <VCam cx={540} cy={lerp(1150, 1080, prog(tt, 0, 1.7))} z={1.15} shake={6} t={t}>
          <Sky id="ers2" dark={0.45} />
          <Column x={420} y={1100} t={t} k={0.8 + 0.2 * prog(tt, 0, 1.7)} s={1.0} />
          <Market t={t} dark={0.35} />
          {[[150, 3], [330, 6], [800, 9], [960, 11], [1120, 2]].map(([x, seed], i) => (
            <Roman key={i} seed={seed} x={x} y={feet(1480 + (i % 2) * 20, 0.5)} s={0.5} face={-0.3} look={[-0.3, -1]} expr={freeze ? 'shock' : 'smile'}
              walk={freeze ? undefined : t * 1.3 + i} larm={freeze && i % 2 ? [1.2, -1.0] : [0.3, 0.2]} rarm={freeze && i % 2 ? [-1.2, 1.0] : [-0.3, -0.2]} />
          ))}
          <Hero x={560} y={feet(1500, 0.56)} s={0.56} expr="shock" face={-0.3} look={[-0.4, -1]} brows="up" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        </VCam>
        <Fill c="#000" a={1 - prog(tt, 0, 0.12)} />
        <Pop t={tt - 0.3} x={540} y={300} size={88} color="#ff9a4a" rot={-3}>MOUNT VESUVIUS</Pop>
        <Vig s={0.5} />
      </g>
    );
  }
  const tt = t - tFace;
  return (
    <g>
      <VCam cx={600} cy={1180} z={lerp(2.1, 2.3, prog(tt, 0, 2))} shake={4} t={t}>
        <Sky id="ers3" dark={0.55} />
        <Column x={380} y={1450} t={t} k={1} s={0.8} />
        <Market t={t} dark={0.45} />
        <Hero x={600} y={feet(1500, 0.6)} s={0.6} expr="shock" face={-0.5} look={[-1, -1]} brows="up" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </VCam>
      <Fill c="#000" a={1 - prog(tt, 0, 0.12)} />
      <Glow id="erf" x={300} y={500} r={600} color="#ff6a1a" a={0.25} />
      <Vig s={0.6} />
    </g>
  );
};

// 4 — people run, ash covers streets, buildings and rooftops; one man calmly sweeps his counter
export const PRun: React.FC<ShotProps> = ({t, D, cue}) => {
  const tAsh = cue('Ash covered');
  const tNob = cue('Nobody understood');
  const ash = ease(prog(t, 0.3, tNob + 0.6)) * 0.85;
  const dark = 0.55 + 0.2 * prog(t, 0, D);
  if (t < tNob) {
    return (
      <g>
        <VCam cx={lerp(700, 380, prog(t, 0, tNob))} cy={1080} z={1.18} shake={5} t={t}>
          <Sky id="rus" dark={dark} />
          <Column x={-200} y={1000} t={t} k={1} s={1.0} />
          <Market t={t} dark={dark * 0.7} ash={ash} />
          {Array.from({length: 9}).map((_, i) => {
            const R = rng(i + 7);
            const x = 1500 - (((t * (330 + R() * 120) + i * 220) % 2100));
            const s = 0.46 + (i % 3) * 0.04;
            return <Roman key={i} seed={i + 2} x={x} y={feet(1450 + (i % 3) * 30, s)} s={s} face={-0.85} look={[-1, 0]} expr={i % 2 ? 'scared' : 'shock'} brows="worried" {...runArms(t + i * 0.2, 3.2)} />;
          })}
          <Hero x={lerp(900, 300, prog(t, 0, tNob))} y={feet(1500, 0.56)} s={0.56} expr="scared" face={-0.8} look={[-1, -0.2]} brows="worried" {...runArms(t, 3)} />
        </VCam>
        <AshFall t={t} n={200} a={1} speed={220} stones />
        {t > tAsh && <Pop t={t - tAsh} x={540} y={300} size={90} color="#e8e0d8" rot={-2} hold={tNob - tAsh - 0.2}>ASH EVERYWHERE!</Pop>}
        <Vig s={0.6} />
      </g>
    );
  }
  const tt = t - tNob;
  const sw = Math.sin(t * 6);
  return (
    <g>
      <VCam cx={430} cy={lerp(1150, 1120, prog(tt, 0, 3))} z={lerp(1.5, 1.6, prog(tt, 0, 3))}>
        <Sky id="rus2" dark={dark} />
        <Market t={t} dark={dark * 0.7} ash={ash} />
        <Roman seed={4} x={170} y={feet(1300, 0.42)} s={0.42} face={0.8} look={[1, 0.6]} expr="smile" showLegs={false} larm={[0.6, 0.6]} rarm={[-1.0 + 0.4 * sw, 1.2]}
          hold={<g transform={`rotate(${20 + 25 * sw})`}><line x1={0} y1={0} x2={60} y2={110} stroke="#8a5a2b" strokeWidth={9} /><path d="M40,100 L90,100 L100,140 L30,140 Z" fill="#c8a85a" stroke={C.ink} strokeWidth={4} /></g>} />
        <Hero x={640} y={feet(1500, 0.56)} s={0.56} expr="worried" face={-0.7} look={[-1, -0.3]} brows="worried" larm={[1.2, -1.0]} rarm={[-1.2, 1.0]} />
      </VCam>
      <AshFall t={t} n={160} a={1} speed={200} stones />
      <Pop t={tt - 0.2} x={540} y={300} size={60} font={HAND} outline={6}>*sweep sweep*</Pop>
      <Fill c="#000" a={1 - prog(tt, 0, 0.12)} />
      <Vig s={0.6} />
    </g>
  );
};

// 5 — wide shot: the whole city disappears beneath the ash, the sky goes almost black
export const PBury: React.FC<ShotProps> = ({t, D, cue}) => {
  const tReal = cue('I looked up', 0.4);
  const bury = ease(prog(t, 0.6, D - 0.2));
  const dark = 0.75 + 0.22 * prog(t, 0, D);
  const R = rng(31);
  return (
    <g>
      <VCam cx={540} cy={lerp(960, 1000, prog(t, 0, D))} z={lerp(1.08, 0.98, ease(prog(t, 0, D)))} shake={3} t={t}>
        <Sky id="bus" dark={dark} />
        <Vesuvius x={620} y={980} s={0.85} dark={dark} glow={0.8} />
        <Column x={600} y={580} t={t} k={1} s={0.62} spread={1.4} h={800} />
        {/* the city spread over the plain */}
        {Array.from({length: 26}).map((_, i) => {
          const x = -60 + (i % 9) * 140 + (Math.floor(i / 9) % 2) * 60;
          const y = 1100 + Math.floor(i / 9) * 110;
          const w = 110 + R() * 40;
          const h = 60 + R() * 60;
          const c = mixHex(WALLS[i % 5], '#2a2220', dark * 0.8);
          return (
            <g key={i}>
              <rect x={x} y={y - h} width={w} height={h} fill={c} stroke={C.ink} strokeWidth={4} />
              <path d={`M${x - 8},${y - h} L${x + w / 2},${y - h - 30} L${x + w + 8},${y - h} Z`} fill={mixHex('#b8582e', '#2a2018', dark * 0.8)} stroke={C.ink} strokeWidth={4} />
            </g>
          );
        })}
        {/* the rising ash blanket */}
        <path d={`M-400,${lerp(1500, 1010, bury)} C0,${lerp(1500, 990, bury) - 20} 400,${lerp(1500, 1030, bury) + 10} 700,${lerp(1500, 1000, bury)} C900,${lerp(1500, 990, bury)} 1200,${lerp(1500, 1020, bury)} 1500,${lerp(1500, 1000, bury)} L1500,2400 L-400,2400 Z`}
          fill="#8a8078" stroke={C.ink} strokeWidth={5} />
        {/* foreground hill with the hero */}
        <path d="M-300,1500 C0,1420 600,1440 1400,1520 L1400,2400 L-300,2400 Z" fill={mixHex('#6a7a4a', '#1e1a18', dark)} stroke={C.ink} strokeWidth={6} />
        <Hero x={760} y={feet(1470, 0.5)} s={0.5} expr={t > tReal ? 'scared' : 'shock'} face={t > tReal ? Math.sin(t * 3) * 0.8 : -0.4} look={[t > tReal ? Math.sin(t * 3) : -0.4, -0.6]}
          brows="worried" larm={t > tReal ? [2.0, 0.6] : [0.3, 0.2]} rarm={t > tReal ? [-2.0, -0.6] : [-0.3, -0.2]} />
        <Sweat x={830} y={feet(1470, 0.5) - 40} t={t} />
      </VCam>
      <AshFall t={t} n={260} a={1} speed={180} seed={4} />
      <Fill c="#000" a={0.25 * prog(t, 0, D)} />
      <Vig s={0.75} />
    </g>
  );
};

// 6 — escaping through a dark, ash-filled street; pull back to the silent buried city (no graphic content)
export const PEscape: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBur = cue('Pompeii would remain');
  if (t < tBur) {
    const hx = lerp(260, 640, prog(t, 0, tBur));
    return (
      <g>
        <VCam cx={lerp(480, 620, prog(t, 0, tBur))} cy={lerp(1150, 1180, prog(t, 0, tBur))} z={lerp(1.45, 1.6, prog(t, 0, tBur))} shake={3} t={t}>
          <Sky id="ess" dark={0.97} />
          <Market t={t} dark={0.92} ash={1} />
          <Glow id="esg" x={1200} y={900} r={700} color="#ff5a1a" a={0.18} />
          <Hero x={hx} y={feet(1470, 0.56)} s={0.56} expr="worried" face={0.8} look={[1, 0.3]} brows="worried" walk={t * 1.1} tilt={0.12}
            larm={[0.3, 0.2]} rarm={[-2.2, 2.2]} />
        </VCam>
        <AshFall t={t} n={280} a={1} speed={240} seed={6} stones />
        <Fill c="#000" a={0.35 + 0.25 * prog(t, 0, tBur)} />
        <Vig s={0.85} />
      </g>
    );
  }
  const tt = t - tBur;
  const back = ease(prog(tt, 0, D - tBur));
  return (
    <g>
      <VCam cx={540} cy={lerp(1150, 960, back)} z={lerp(1.8, 0.95, back)}>
        <Sky id="ess2" dark={0.9} />
        <Vesuvius x={620} y={980} s={0.85} dark={0.85} glow={0.4} />
        <path d="M300,560 C200,300 500,180 640,120 C760,200 900,300 820,560 Z" fill="#3a3230" opacity={0.85} />
        <path d="M-400,1000 C0,980 400,1020 700,995 C900,985 1200,1010 1500,1000 L1500,2400 L-400,2400 Z" fill="#7a7068" stroke={C.ink} strokeWidth={5} />
        {[[-40, 990, 140], [180, 1000, 120], [420, 985, 160], [700, 995, 130], [940, 990, 150]].map(([x, y, w], i) => (
          <path key={i} d={`M${x},${y} l${w / 2},-24 l${w / 2},24`} fill="none" stroke={C.ink} strokeWidth={4} opacity={0.5} />
        ))}
        <Hero x={540} y={feet(1180, 0.3)} s={0.3} expr="frown" face={0} look={[0, -0.4]} brows="worried" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </VCam>
      <AshFall t={t} n={120} a={1 - back * 0.6} speed={120} seed={8} />
      <Txt x={540} y={330} size={64} color="#e8e0d8" outline={7} opacity={ease(prog(tt, 0.6, 1.2))}>BURIED FOR CENTURIES</Txt>
      <Fill c="#000" a={0.3 + prog(t, D - 0.4, D) * 0.7} />
      <Vig s={0.75} />
    </g>
  );
};

// 7 — almost 2,000 years later: archaeologists uncover the streets; he is amazed; subscribe
export const PDig: React.FC<ShotProps> = ({t, D, cue}) => {
  const tAlm = cue('Almost 2,000');
  const tSub = cue('SUBSCRIBE');
  const sub = t > tSub - 0.1;
  const brush = (k: number) => Math.sin(t * 9 + k * 2) * 0.35;
  return (
    <g>
      <VCam cx={540} cy={lerp(1080, 1120, prog(t, 0, D))} z={sub ? lerp(1.1, 1.0, easeOut(prog(t, tSub, tSub + 0.6))) : lerp(1.15, 1.1, prog(t, 0, D))}>
        <Sky id="dgs" dark={0} modern />
        <Vesuvius x={560} y={980} s={0.9} />
        <rect x={-400} y={980} width={1900} height={140} fill="#c8b48a" stroke={C.ink} strokeWidth={5} />
        {/* excavated ruins: broken walls and columns */}
        {[[-60, 1240, 240, 150], [250, 1240, 160, 210], [700, 1240, 200, 170], [960, 1240, 220, 130]].map(([x, y, w, h], i) => (
          <path key={i} d={`M${x},${y} L${x},${y - h} L${x + w * 0.3},${y - h + 26} L${x + w * 0.55},${y - h - 10} L${x + w * 0.8},${y - h + 30} L${x + w},${y - h + 6} L${x + w},${y} Z`}
            fill={WALLS[i % 5]} opacity={0.85} stroke={C.ink} strokeWidth={5} />
        ))}
        {[470, 560, 650].map((x, i) => (
          <g key={x}>
            <rect x={x - 22} y={1240 - (i === 1 ? 300 : 230)} width={44} height={i === 1 ? 300 : 230} fill="#f2ead8" stroke={C.ink} strokeWidth={5} />
            <rect x={x - 32} y={1240 - (i === 1 ? 300 : 230) - 16} width={64} height={18} fill="#f2ead8" stroke={C.ink} strokeWidth={4} />
          </g>
        ))}
        <RomanStreet y={1240} />
        {/* dig-site strings and a bucket */}
        <line x1={-100} y1={1300} x2={1200} y2={1300} stroke="#fff" strokeWidth={3} strokeDasharray="14 10" />
        {[60, 380, 700, 1020].map((x) => <rect key={x} x={x - 6} y={1280} width={12} height={40} fill="#8a5a2b" />)}
        <path d="M900,1420 L980,1420 L970,1490 L910,1490 Z" fill="#3a7ad8" stroke={C.ink} strokeWidth={4} />
        <Archaeologist seed={1} x={200} y={feet(1430, 0.44) + 70} s={0.44} face={0.6} look={[1, 0.9]} expr="happy" tilt={0.25} showLegs={false} larm={[0.6, 0.6]} rarm={[0.2 + brush(0), 0.5]} hold={<Brush />} />
        <Archaeologist seed={2} x={820} y={feet(1400, 0.44) + 70} s={0.44} face={-0.6} look={[-1, 0.9]} expr="smile" tilt={-0.25} showLegs={false} larm={[-0.2 - brush(1), -0.5]} rarm={[-0.6, -0.6]} />
        <Archaeologist seed={3} x={1000} y={feet(1300, 0.36)} s={0.36} face={-0.7} expr="happy" larm={[0.3, 0.2]} rarm={[-1.6, 0.4]}
          hold={<g transform="translate(0,-30)"><rect x={-30} y={-40} width={60} height={80} fill="#fbf6e8" stroke={C.ink} strokeWidth={4} /></g>} />
        <Hero x={520} y={feet(1500, 0.64)} s={0.64} expr={sub ? 'grin' : t > tAlm ? 'shock' : 'o'} face={sub ? 0 : -0.3} look={sub ? [0, 0] : [-0.5, -0.3]} brows={t > tAlm && !sub ? 'up' : undefined}
          larm={sub ? [0.3, 0.2] : [1.1, -1.0]} rarm={sub ? [-2.6 + 0.3 * Math.sin(t * 8), 0.4] : [-1.1, 1.0]} />
      </VCam>
      <Fill c="#000" a={1 - prog(t, 0, 0.35)} />
      {t > tAlm && !sub && <g transform={`translate(540,320) scale(${backOut(prog(t, tAlm, tAlm + 0.4), 2)})`}>
        <rect x={-380} y={-100} width={760} height={200} rx={26} fill="rgba(20,20,30,0.8)" stroke={C.gold} strokeWidth={5} />
        <Txt x={0} y={-32} size={66} color="#fff" outline={0}>REDISCOVERED!</Txt>
        <Txt x={0} y={40} size={46} color={C.gold} outline={0}>excavations since 1748</Txt>
      </g>}
      {sub && (() => {
        const tt = t - tSub + 0.1;
        const k = backOut(prog(tt, 0, 0.45), 2) * (1 + 0.05 * Math.sin(t * 7));
        return (
          <g>
            <Confetti t={tt} n={40} />
            <g transform={`translate(540,300) scale(${Math.max(k, 0.001)})`}>
              <rect x={-430} y={-110} width={860} height={220} rx={50} fill="#ff2a2a" stroke={C.ink} strokeWidth={9} />
              <polygon points="-340,-50 -340,50 -260,0" fill="#fff" />
              <Txt x={60} y={0} size={110} outline={8}>SUBSCRIBE</Txt>
            </g>
            <Pop t={tt - 0.3} x={540} y={510} size={90} color="#ffd84d">HISTORY WORLD</Pop>
          </g>
        );
      })()}
      <Vig s={0.3} />
      <Fill c="#000" a={prog(t, D - 0.3, D)} />
    </g>
  );
};

export const SHOTS: Record<string, React.FC<ShotProps>> = {
  p_hook: PHook, p_city: PCity, p_erupt: PErupt, p_run: PRun, p_bury: PBury, p_escape: PEscape, p_dig: PDig,
};
void [easeIn, HAND];
