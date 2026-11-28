// Vertical (1080x1920) scenes for "I Witnessed the Fall of the Berlin Wall!".
// Reuses the hero, time machine and comic effects from the Titanic project; adds 1989 Berlin.
import React from 'react';
import {C, blinkAt, clamp, ease, easeIn, easeOut, lerp, prog, rng, backOut} from './lib';
import {Doodle, DoodleProps, SlickHair, WoolCap, handPos} from './Hero';
import {Burst, Caption, Glow, HAND, Pop, Sparkle, Sweat, Txt, Confetti} from './fx';
import {TimeMachine} from './props';

export const VW = 1080;
export const VH = 1920;
export type Cue = (text: string, frac?: number) => number;
export type ShotProps = {t: number; D: number; cue: Cue};

const GROUND = 1500;
const feet = (yFeet: number, s: number) => yFeet - 456 * s;
const Hero: React.FC<DoodleProps> = (p) => <Doodle blink={blinkAt(p.x * 0.013 + (p.walk ?? 0))} {...p} />;

// ------------------------------------------------------------------ framing helpers
const VCam: React.FC<{cx: number; cy: number; z?: number; shake?: number; t?: number; children: React.ReactNode}> = ({cx, cy, z = 1, shake = 0, t = 0, children}) => {
  const sx = shake * (Math.sin(t * 47) + Math.sin(t * 31)) * 0.5;
  const sy = shake * (Math.cos(t * 53) + Math.sin(t * 37)) * 0.5;
  return <g transform={`translate(${VW / 2 + sx},${VH / 2 + sy}) scale(${z}) translate(${-cx},${-cy})`}>{children}</g>;
};
const Vig: React.FC<{s?: number; color?: string}> = ({s = 0.5, color = '#000'}) => (
  <g>
    <defs>
      <radialGradient id={`vg${Math.round(s * 100)}${color.slice(1)}`} cx="50%" cy="45%" r="72%">
        <stop offset="50%" stopColor={color} stopOpacity={0} />
        <stop offset="100%" stopColor={color} stopOpacity={s} />
      </radialGradient>
    </defs>
    <rect x={0} y={0} width={VW} height={VH} fill={`url(#vg${Math.round(s * 100)}${color.slice(1)})`} />
  </g>
);
const Fill: React.FC<{c: string; a: number}> = ({c, a}) => (a > 0.001 ? <rect x={0} y={0} width={VW} height={VH} fill={c} opacity={clamp(a)} /> : null);

// ------------------------------------------------------------------ Berlin, night of 9 November 1989
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
      {!warm && Array.from({length: 120}).map((_, i) => (
        <circle key={i} cx={-1200 + R() * 3600} cy={-800 + R() * 1700} r={1.5 + R() * 2.5} fill="#fff" opacity={0.35 + 0.35 * Math.sin(t * 2 + i)} />
      ))}
    </g>
  );
};

/** distant skyline: Fernsehturm (East) and Brandenburg Gate silhouettes, Plattenbau blocks with lit windows */
export const Skyline: React.FC<{y: number; t: number; warm?: boolean}> = ({y, t, warm}) => {
  const R = rng(9);
  const sil = warm ? '#7a5a6a' : '#1a2040';
  const win = warm ? '#ffd9a0' : '#f6d98a';
  return (
    <g>
      {/* TV tower */}
      <rect x={1240} y={y - 900} width={26} height={900} fill={sil} />
      <circle cx={1253} cy={y - 760} r={60} fill={sil} />
      <rect x={1249} y={y - 1020} width={8} height={160} fill={sil} />
      <circle cx={1253} cy={y - 1022} r={6} fill="#ff5050" opacity={0.6 + 0.4 * Math.sin(t * 4)} />
      {/* Brandenburg Gate */}
      <g transform={`translate(-300,${y})`}>
        <rect x={-260} y={-300} width={520} height={60} fill={sil} />
        <rect x={-270} y={-330} width={540} height={34} fill={sil} />
        {[0, 1, 2, 3, 4, 5].map((k) => <rect key={k} x={-250 + k * 92} y={-240} width={34} height={240} fill={sil} />)}
        <path d="M-50,-330 L-30,-390 L40,-390 L60,-330 Z" fill={sil} />
      </g>
      {Array.from({length: 14}).map((_, i) => {
        const x = -1300 + i * 260 + R() * 40;
        const h = 260 + R() * 340;
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

const GRAF = ['#ff4a8a', '#ffd84d', '#3ad0ff', '#7ae05a', '#ff8a3a', '#b88aff'];

/** the Wall (Grenzmauer 75): concrete slabs with a round pipe on top, seen from the West (graffiti) or the East (bare) */
export const Wall: React.FC<{x0: number; x1: number; y: number; h?: number; t: number; west?: boolean; shake?: number; crack?: number; night?: boolean}> = ({
  x0, x1, y, h = 420, t, west = true, shake = 0, crack = 0, night = true,
}) => {
  const R = rng(3);
  const n = Math.ceil((x1 - x0) / 120);
  const base = night ? '#9a9a9e' : '#bdbdc0';
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const x = x0 + i * 120;
        const dy = shake * Math.sin(t * 40 + i * 1.7) * 6;
        const col = i % 2 ? base : night ? '#929296' : '#b4b4b8';
        const seed = R();
        return (
          <g key={i} transform={`translate(0,${dy})`}>
            <rect x={x} y={y - h} width={120} height={h} fill={col} stroke={C.ink} strokeWidth={5} />
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
      <rect x={x0 - 10} y={y - h - 40} width={x1 - x0 + 20} height={56} rx={28} fill={night ? '#b4b4b8' : '#d4d4d6'} stroke={C.ink} strokeWidth={6} />
    </g>
  );
};

const Floodlight: React.FC<{x: number; y: number; t: number; a?: number}> = ({x, y, t, a = 1}) => (
  <g>
    <line x1={x} y1={y} x2={x} y2={y - 640} stroke="#2a2a30" strokeWidth={14} />
    <path d={`M${x - 30},${y - 640} L${x + 30},${y - 640} L${x + 420},${y} L${x - 420},${y} Z`} fill="#fff6c0" opacity={0.08 * a * (0.9 + 0.1 * Math.sin(t * 6))} />
    <rect x={x - 34} y={y - 670} width={68} height={34} rx={8} fill="#fff6c0" stroke={C.ink} strokeWidth={5} />
  </g>
);

const Ground: React.FC<{y?: number; night?: boolean; warm?: boolean}> = ({y = GROUND, night = true, warm}) => (
  <g>
    <rect x={-3000} y={y} width={9000} height={2000} fill={warm ? '#b89a8a' : night ? '#3a3a48' : '#8a8a90'} stroke={C.ink} strokeWidth={6} />
    {Array.from({length: 40}).map((_, k) => <line key={k} x1={-2000 + k * 150} y1={y} x2={-2400 + k * 150} y2={y + 700} stroke={warm ? '#a08a7a' : '#2e2e3a'} strokeWidth={4} />)}
  </g>
);

// ------------------------------------------------------------------ 1989 people (same doodle body as the hero, never a red cap)
const HAIR = ['#2a1e14', '#7a4a24', '#d9b05a', '#3a3a3a', '#a03a1a'];
const JACKET = ['#3a6ab8', '#c83a5a', '#2a9a8a', '#7a4ab8', '#e0a030', '#5a6a3a', '#8a8a92', '#d05a2a'];

export const Berliner: React.FC<DoodleProps & {seed?: number}> = ({seed = 0, ...p}) => {
  const style = seed % 5;
  const hair = HAIR[(seed * 3) % HAIR.length];
  let back: React.ReactNode = null;
  let front: React.ReactNode = null;
  if (style === 0) front = <SlickHair color={hair} />;
  if (style === 1) front = <WoolCap color={JACKET[(seed + 3) % JACKET.length]} />;
  if (style === 2) front = <g>{[-80, -40, 0, 40, 80, -60, 60, -20, 20].map((dx, i) => <circle key={i} cx={dx} cy={-70 - (i > 4 ? 40 : 0) - Math.abs(dx) * -0.2} r={36} fill={hair} stroke={C.ink} strokeWidth={5} />)}</g>;
  if (style === 3) {
    back = <path d="M-108,-10 C-130,120 -110,190 -70,200 L70,200 C110,190 130,120 108,-10 Z" fill={hair} stroke={C.ink} strokeWidth={7} />;
    front = <path d="M-100,-20 C-104,-140 104,-150 102,-20 C60,-80 -60,-80 -100,-20 Z" fill={hair} stroke={C.ink} strokeWidth={7} />;
  }
  if (style === 4) front = <g><path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill={hair} stroke={C.ink} strokeWidth={6} />
    {[-30, 32].map((ex) => <circle key={ex} cx={ex + (p.face ?? 0) * 34} cy={-24} r={20} fill="none" stroke={C.ink} strokeWidth={4.5} />)}</g>;
  const scarf = seed % 3 === 0 ? <path d="M-50,76 C-20,96 20,96 50,76 L46,100 C20,116 -20,116 -46,100 Z" fill={JACKET[(seed + 5) % JACKET.length]} stroke={C.ink} strokeWidth={4} /> : null;
  return <Doodle cap={false} body={JACKET[seed % JACKET.length]} blink={blinkAt(seed * 0.9 + p.x * 0.001, seed)} back={back} front={front} bodyExtra={scarf} {...p} />;
};

export const Guard: React.FC<DoodleProps> = (p) => (
  <Doodle cap={false} body="#6a7a5a" blink={blinkAt(2.3, 4)}
    front={<g><path d="M-100,-30 C-110,-120 110,-120 100,-30 Z" fill="#5a6a4a" stroke={C.ink} strokeWidth={7} />
      <rect x={-104} y={-50} width={208} height={24} fill="#3a4430" stroke={C.ink} strokeWidth={5} />
      <path d="M10,-28 C60,-28 120,-30 150,-12 C120,-4 60,-8 10,-12 Z" fill="#222" stroke={C.ink} strokeWidth={4} /></g>}
    bodyExtra={<g>{[150, 200, 250].map((y) => <circle key={y} cx={10} cy={y} r={6} fill="#c9b04a" stroke={C.ink} strokeWidth={2} />)}</g>} {...p} />
);

const Hammer: React.FC<{swing: number}> = ({swing}) => (
  <g transform={`rotate(${-30 + swing * 70})`}>
    <line x1={0} y1={10} x2={0} y2={-120} stroke="#8a5a2b" strokeWidth={14} strokeLinecap="round" />
    <rect x={-40} y={-150} width={80} height={36} rx={6} fill="#6a6a72" stroke={C.ink} strokeWidth={5} />
  </g>
);

const Trabant: React.FC<{x: number; y: number; s?: number; t: number; color?: string}> = ({x, y, s = 1, t, color = '#a8d0c0'}) => (
  <g transform={`translate(${x},${y + Math.sin(t * 20) * 2}) scale(${s})`}>
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

const Heart: React.FC<{x: number; y: number; s?: number; a?: number}> = ({x, y, s = 1, a = 1}) => (
  <path transform={`translate(${x},${y}) scale(${s})`} opacity={a} d="M0,18 C-40,-10 -30,-46 0,-30 C30,-46 40,-10 0,18 Z" fill="#ff4a6a" stroke={C.ink} strokeWidth={4} />
);

const Tear: React.FC<{x: number; y: number; t: number; s?: number}> = ({x, y, t, s = 0.6}) => <Sweat x={x} y={y} t={t} s={s} />;

/** a crowd of Berliners streaming in one direction (dir 1 = right) */
const Crowd: React.FC<{t: number; y: number; n: number; speed?: number; dir?: number; s?: number; seed?: number; x0?: number; span?: number; cheer?: boolean}> = ({
  t, y, n, speed = 140, dir = 1, s = 0.42, seed = 0, x0 = -400, span = 2200, cheer = false,
}) => {
  const R = rng(seed + 11);
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const off = R() * span;
        const x = x0 + (((off + dir * t * speed * (0.8 + R() * 0.4)) % span) + span) % span;
        const yy = y + (i % 3) * 26;
        const sw = Math.sin(t * 7 + i);
        return <Berliner key={i} seed={seed + i} x={x} y={feet(yy, s)} s={s} face={0.85 * dir} walk={t * 1.6 + i * 0.3} expr={cheer ? 'laugh' : i % 3 ? 'happy' : 'o'}
          larm={cheer && i % 2 ? [2.6, 0.2] : [0.3, 0.2]} rarm={cheer ? [-2.5 + 0.3 * sw, 0.3] : i % 4 === 0 ? [-2.4 + 0.3 * sw, 0.4] : [-0.3, -0.2]} />;
      })}
    </g>
  );
};

// ================================================================== SCENES
// 1 — hook: terrified close-up, the Wall shaking behind him, crowd on top
export const BHook: React.FC<ShotProps> = ({t, D, cue}) => {
  const tDestroy = cue('DESTROYING');
  const t1989 = cue('1989');
  const z = lerp(2.3, 1.25, easeOut(prog(t, 0, 2.6)));
  const shake = 0.6 + 0.6 * prog(t, tDestroy, D);
  return (
    <g>
      <VCam cx={540} cy={lerp(1440, 1400, prog(t, 0, 2.6))} z={z} shake={4 + 6 * prog(t, tDestroy, D)} t={t}>
        <NightSky t={t} id="hs" />
        <Skyline y={1060} t={t} />
        <Floodlight x={120} y={1460} t={t} />
        <Floodlight x={980} y={1460} t={t} />
        <Wall x0={-600} x1={1700} y={1460} t={t} shake={shake} crack={prog(t, tDestroy, D)} />
        {/* people up on the wall, cheering */}
        {Array.from({length: 7}).map((_, i) => {
          const x = -40 + i * 190;
          const j = Math.abs(Math.sin(t * 6 + i)) * 18;
          return <Berliner key={i} seed={i + 3} x={x} y={feet(1000 - j, 0.34)} s={0.34} face={0} expr="laugh" larm={[2.6, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 8 + i), 0.3]} />;
        })}
        {/* a sea of heads in the foreground */}
        {Array.from({length: 9}).map((_, i) => (
          <Berliner key={i} seed={i + 20} x={-80 + i * 150} y={1640 + (i % 2) * 30} s={0.4} face={0} look={[0, -1]} expr="o" larm={[2.4, 0.3]} rarm={[-2.5, 0.3]} showLegs={false} />
        ))}
        <Hero x={540} y={feet(1760, 0.8)} s={0.8} expr="scared" face={0} look={[0, 0]} brows="worried" larm={[2.6, 0.3]} rarm={[-2.6, -0.3]} tilt={0.04 * Math.sin(t * 22)} />
        <Sweat x={640} y={feet(1760, 0.8) - 60} t={t} />
        <Sweat x={430} y={feet(1760, 0.8) - 40} s={0.8} t={t + 0.3} />
      </VCam>
      {t > tDestroy && <Burst t={t - tDestroy} x={830} y={360} r={150} label="CRACK!" size={60} hold={1.5} />}
      {t > t1989 && <Pop t={t - t1989} x={540} y={330} size={130} color="#ffd84d" rot={-3}>BERLIN · 1989</Pop>}
      <Vig s={0.55} />
      <Fill c="#fff" a={prog(t, D - 0.25, D)} />
    </g>
  );
};

// 2 — Berlin 1989: thousands rush toward the Wall, the hero pushes through, confused
export const BCrowd: React.FC<ShotProps> = ({t, D, cue}) => {
  const hx = lerp(200, 900, prog(t, 0, D));
  const lookL = Math.sin(t * 3) > 0;
  return (
    <g>
      <VCam cx={lerp(560, 1150, prog(t, 0, D))} cy={1080} z={lerp(1.1, 1.25, ease(prog(t, 0, D)))}>
        <NightSky t={t} id="cs" />
        <Skyline y={1150} t={t} />
        <Floodlight x={1600} y={1500} t={t} />
        <Wall x0={1500} x1={2900} y={1500} t={t} />
        <Ground />
        <Crowd t={t} y={1520} n={14} speed={170} seed={30} x0={-600} span={2500} />
        <Hero x={hx} y={feet(1640, 0.55)} s={0.55} expr={lookL ? 'o' : 'worried'} face={lookL ? -0.8 : 0.8} look={[lookL ? -1 : 1, 0]} walk={t * 1.4}
          larm={[1.4 + 0.3 * Math.sin(t * 6), -1.0]} rarm={[-1.4 - 0.3 * Math.sin(t * 6), 1.0]} tilt={0.06 * Math.sin(t * 5)} />
        <Crowd t={t} y={1700} n={8} speed={200} seed={60} x0={-600} span={2500} s={0.5} />
      </VCam>
      {[0, 1, 2].map((k) => {
        const ph = (t * 0.9 + k / 3) % 1;
        return <Txt key={k} x={460 + k * 80} y={820 - ph * 120} size={80} color="#ffd84d" outline={6} opacity={1 - ph}>?</Txt>;
      })}
      <Pop t={t - 0.3} x={540} y={330} size={84} hold={3.2}>THOUSANDS OF PEOPLE!</Pop>
      <Caption t={t - 0.4} place="BERLIN, GERMANY" date="9 NOVEMBER 1989" dur={D - 1.2} />
      <Vig s={0.45} />
    </g>
  );
};

// 3 — the division: cross-section of the Wall, East on the left, West on the right, families waving over it
export const BDivided: React.FC<ShotProps> = ({t, D, cue}) => {
  const tFam = cue('Families');
  const wave = (k: number) => [-2.6 + 0.35 * Math.sin(t * 3 + k), 0.4] as [number, number];
  const pop = (k: number) => easeOut(prog(t, 0.3 + k * 0.5, 0.8 + k * 0.5));
  return (
    <g>
      <VCam cx={540} cy={lerp(1040, 1080, ease(prog(t, 0, D)))} z={lerp(1.1, 1.2, ease(prog(t, 0, D)))}>
        {/* East: grey, still */}
        <rect x={-600} y={-800} width={1140} height={3500} fill="#3a3e4e" />
        {/* West: colourful */}
        <rect x={540} y={-800} width={1200} height={3500} fill="#2a3466" />
        <g opacity={0.9}>
          {Array.from({length: 4}).map((_, i) => <rect key={i} x={-260 + i * 170} y={860 - (i % 2) * 120} width={150} height={640} fill="#4a4e5e" stroke="#2a2e3a" strokeWidth={4} />)}
          {Array.from({length: 4}).map((_, i) => <rect key={'w' + i} x={700 + i * 160} y={900 - (i % 2) * 90} width={140} height={600} fill="#3a4478" stroke="#222a50" strokeWidth={4} />)}
        </g>
        {/* death strip watchtower */}
        <g transform="translate(250,1500)">
          <rect x={-20} y={-460} width={40} height={460} fill="#7a7a7e" stroke={C.ink} strokeWidth={5} />
          <rect x={-70} y={-560} width={140} height={100} fill="#8a8a8e" stroke={C.ink} strokeWidth={5} />
          <rect x={-56} y={-540} width={112} height={44} fill="#2a2e3a" />
          <path d={`M-30,-520 L-600,${-80 + Math.sin(t * 0.8) * 60} L-500,${40 + Math.sin(t * 0.8) * 60} Z`} fill="#fff6c0" opacity={0.08} />
        </g>
        <Ground y={1500} />
        {/* the Wall seen end-on, with barbed wire */}
        <rect x={500} y={980} width={80} height={520} fill="#a8a8ac" stroke={C.ink} strokeWidth={6} />
        <rect x={486} y={950} width={108} height={50} rx={25} fill="#c4c4c8" stroke={C.ink} strokeWidth={6} />
        {[0, 1, 2, 3, 4].map((k) => <path key={k} d={`M${505 + k * 18},950 l-10,-24 l20,0 Z`} fill="none" stroke="#555" strokeWidth={3} />)}
        <Txt x={250} y={760} size={58} color="#d8d8e0" outline={6}>EAST BERLIN</Txt>
        <Txt x={830} y={760} size={58} color="#ffd84d" outline={6}>WEST BERLIN</Txt>
        {/* families: East side (mother + child), West side on a viewing platform (grandpa + daughter) */}
        <g opacity={pop(0)} transform={`translate(0,${(1 - pop(0)) * 80})`}>
          <Berliner seed={3} x={330} y={feet(1500, 0.5)} s={0.5} face={0.8} look={[1, -0.6]} expr="frown" brows="worried" larm={[0.3, 0.2]} rarm={wave(0)} />
          <Berliner seed={7} x={200} y={feet(1500, 0.34)} s={0.34} face={0.8} look={[1, -0.8]} expr="frown" brows="worried" larm={[0.3, 0.2]} rarm={wave(1)} />
          <Tear x={360} y={feet(1500, 0.5) + 5} t={t} />
        </g>
        <rect x={640} y={1300} width={380} height={30} fill="#8a5a2b" stroke={C.ink} strokeWidth={5} />
        {[660, 1000].map((x) => <line key={x} x1={x} y1={1330} x2={x} y2={1500} stroke="#6b4428" strokeWidth={14} />)}
        <g opacity={pop(1)} transform={`translate(0,${(1 - pop(1)) * 80})`}>
          <Berliner seed={9} x={760} y={feet(1300, 0.5)} s={0.5} face={-0.8} look={[-1, -0.4]} expr="frown" brows="worried" larm={wave(2).map((v) => -v) as [number, number]} rarm={[-0.3, -0.2]} />
          <Berliner seed={13} x={920} y={feet(1300, 0.46)} s={0.46} face={-0.8} look={[-1, -0.4]} expr="frown" brows="worried" larm={wave(3).map((v) => -v) as [number, number]} rarm={[-0.3, -0.2]} />
          <Tear x={720} y={feet(1300, 0.5) + 5} t={t + 0.4} />
        </g>
        <Hero x={940} y={feet(1760, 0.45)} s={0.45} expr="frown" face={-0.6} look={[-1, -0.5]} brows="worried" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </VCam>
      <Pop t={t - 0.3} x={540} y={300} size={120} color="#ffd84d" hold={tFam - 0.4}>28 YEARS</Pop>
      <Txt x={540} y={410} size={52} font={HAND} outline={5} opacity={ease(prog(t, 0.8, 1.2)) * (1 - prog(t, tFam - 0.4, tFam))}>13 August 1961 – 9 November 1989</Txt>
      {t > tFam && <Pop t={t - tFam} x={540} y={320} size={96} color="#d8d8e0">DIVIDED</Pop>}
      <Vig s={0.55} />
    </g>
  );
};

// 4 — 9 November 1989: the barrier opens, people and a Trabant cross the border
export const BCross: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSome = cue('something unbelievable');
  const tCross = cue('People started');
  const lift = easeOut(prog(t, tSome + 0.6, tSome + 1.6));
  const flow = prog(t, tSome + 1.0, D);
  const shock = t > tSome + 1.2;
  return (
    <g>
      <VCam cx={lerp(560, 640, prog(t, 0, D))} cy={lerp(1080, 1110, prog(t, 0, D))} z={lerp(1.15, 1.25, ease(prog(t, 0, D)))} shake={t > tCross ? 3 : 0} t={t}>
        <NightSky t={t} id="xs" />
        <Skyline y={1100} t={t} />
        {/* checkpoint booth + sign */}
        <rect x={-120} y={1180} width={300} height={320} fill="#c8c8c0" stroke={C.ink} strokeWidth={6} />
        <rect x={-90} y={1220} width={240} height={110} fill="#f6d98a" stroke={C.ink} strokeWidth={5} />
        <rect x={-150} y={1150} width={360} height={40} fill="#8a8a82" stroke={C.ink} strokeWidth={5} />
        <g transform="translate(30,1060)">
          <rect x={-260} y={-50} width={520} height={100} rx={10} fill="#f2f2ea" stroke={C.ink} strokeWidth={5} />
          <Txt x={0} y={-16} size={30} color={C.ink} outline={0} shadow={false}>GRENZÜBERGANG</Txt>
          <Txt x={0} y={22} size={30} color={C.ink} outline={0} shadow={false}>BORNHOLMER STRASSE</Txt>
        </g>
        <Floodlight x={420} y={1500} t={t} />
        <Ground />
        {/* barrier */}
        <rect x={240} y={1330} width={50} height={170} fill="#8a8a82" stroke={C.ink} strokeWidth={5} />
        <g transform={`translate(265,1345) rotate(${-80 * lift})`}>
          <rect x={0} y={-16} width={760} height={32} fill="#fff" stroke={C.ink} strokeWidth={5} />
          {Array.from({length: 7}).map((_, k) => <rect key={k} x={20 + k * 110} y={-16} width={55} height={32} fill="#e8303a" />)}
        </g>
        <Guard x={120} y={feet(1520, 0.5)} s={0.5} face={0.6} expr={lift > 0.5 ? 'o' : 'flat'} larm={lift > 0.5 ? [1.4, -0.6] : [0.3, 0.2]} rarm={lift > 0.5 ? [-1.4, 0.6] : [-0.3, -0.2]} />
        {/* crowd waiting, then streaming through */}
        {Array.from({length: 12}).map((_, i) => {
          const R = rng(i + 50);
          const wait = -500 + i * 50 + R() * 30;
          const x = flow > 0 ? wait + flow * 1900 * (0.7 + R() * 0.5) : wait;
          const y = 1540 + (i % 3) * 40;
          const going = flow > 0.02;
          return <Berliner key={i} seed={i + 40} x={x} y={feet(y, 0.46)} s={0.46} face={0.85} walk={going ? t * 1.8 + i : undefined} expr={going ? 'laugh' : 'o'}
            larm={going && i % 2 ? [2.6, 0.2] : [0.3, 0.2]} rarm={going ? [-2.5 + 0.3 * Math.sin(t * 8 + i), 0.3] : [-0.3, -0.2]} />;
        })}
        <Trabant x={lerp(-700, 1900, prog(t, tCross, D + 1.0))} y={1640} s={0.55} t={t} />
        <Hero x={860} y={feet(1760, 0.62)} s={0.62} expr={shock ? 'shock' : 'o'} face={-0.6} look={[-1, 0]} brows={shock ? 'up' : undefined}
          capOff={shock ? Math.sin(prog(t, tSome + 1.2, tSome + 1.9) * Math.PI) * 0.35 : 0} larm={shock ? [1.1, -1.0] : [0.3, 0.2]} rarm={shock ? [-1.1, 1.0] : [-0.3, -0.2]} />
      </VCam>
      <Pop t={t - 0.2} x={540} y={320} size={110} color="#ffd84d" rot={-2} hold={tSome + 1.2}>9 NOVEMBER 1989</Pop>
      {t > tSome + 1.4 && <Pop t={t - tSome - 1.4} x={540} y={320} size={88} color="#7ae05a" rot={-2}>THE BORDER IS OPEN!</Pop>}
      {t > tCross + 0.6 && <Burst t={t - tCross - 0.6} x={820} y={560} r={110} label="HONK!" size={48} hold={1.2} />}
      <Vig s={0.5} />
    </g>
  );
};

// 5 — up on the Wall: tears, laughter, hammers and chisels
export const BHammer: React.FC<ShotProps> = ({t, D, cue}) => {
  const tClimb = cue('People climbed');
  const climb = easeOut(prog(t, tClimb, tClimb + 1.6));
  const R = rng(5);
  const chips: React.ReactNode[] = [];
  [180, 520, 860].forEach((hx, k) => {
    const ph = (t * 2.4 + k * 0.33) % 1;
    if (ph < 0.5) {
      for (let c = 0; c < 4; c++) {
        const u = ph * 2;
        chips.push(<rect key={`${k}${c}`} x={hx + 70 + (R() - 0.3) * 160 * u} y={1220 - 200 * u + 300 * u * u} width={14} height={10} fill="#bdbdc0" stroke={C.ink} strokeWidth={2}
          transform={`rotate(${u * 300 + c * 40} ${hx + 70} 1220)`} />);
      }
    }
  });
  return (
    <g>
      <VCam cx={540} cy={lerp(1000, 920, ease(prog(t, tClimb, D)))} z={1.2} t={t}>
        <NightSky t={t} id="ms" />
        {/* fireworks */}
        {[[200, 300, 0], [820, 220, 0.6], [520, 140, 1.2]].map(([fx, fy, ph], k) => {
          const u = ((t + ph) % 1.8) / 1.8;
          return (
            <g key={k} opacity={1 - u}>
              {Array.from({length: 12}).map((_, j) => {
                const a = (j * Math.PI) / 6;
                return <line key={j} x1={fx + Math.cos(a) * 40 * u} y1={fy + Math.sin(a) * 40 * u} x2={fx + Math.cos(a) * 160 * u} y2={fy + Math.sin(a) * 160 * u}
                  stroke={GRAF[(j + k) % 6]} strokeWidth={8} strokeLinecap="round" />;
              })}
            </g>
          );
        })}
        <Skyline y={1000} t={t} />
        <Wall x0={-600} x1={1700} y={1460} t={t} crack={0.6} />
        {/* people sitting / standing on top */}
        {[0, 1, 2, 3, 4].map((i) => {
          const x = 60 + i * 230;
          const j = Math.abs(Math.sin(t * 5 + i)) * 14;
          return <Berliner key={i} seed={i + 70} x={x} y={feet(1000 - j, 0.4)} s={0.4} face={i % 2 ? 0.4 : -0.4} expr={i % 2 ? 'laugh' : 'happy'}
            larm={[2.6, 0.2]} rarm={[-2.5 + 0.3 * Math.sin(t * 7 + i), 0.3]} />;
        })}
        <Ground />
        {/* hammering at the base */}
        {[180, 520, 860].map((hx, k) => {
          const ph = (t * 2.4 + k * 0.33) % 1;
          const sw = ph < 0.5 ? 1 - ph * 2 : (ph - 0.5) * 2;
          return <Berliner key={k} seed={k + 90} x={hx} y={feet(1580, 0.5)} s={0.5} face={0.7} expr={k === 1 ? 'happy' : 'grin'} larm={[0.3, 0.2]}
            rarm={[-1.5 - 0.6 * sw, 0.4]} hold={<Hammer swing={sw} />} />;
        })}
        {chips}
        {t > 0.2 && t < tClimb && <Tear x={575} y={feet(1580, 0.5) + 10} t={t} />}
        {/* the hero climbs up and celebrates with a hammer */}
        <Hero x={lerp(980, 900, climb)} y={lerp(feet(1700, 0.5), feet(1000, 0.5), climb)} s={0.5} expr={climb > 0.9 ? 'laugh' : 'grin'} face={-0.3}
          larm={climb > 0.9 ? [2.6, 0.3] : [2.2, 0.4]} rarm={climb > 0.9 ? [-2.6 + 0.3 * Math.sin(t * 9), 0.3] : [-2.2, -0.4]}
          legs={climb > 0 && climb < 1 ? [Math.sin(t * 14) * 0.5, -Math.sin(t * 14) * 0.5] : [0, 0]} hold={climb > 0.9 ? <Hammer swing={0.5 + 0.5 * Math.sin(t * 8)} /> : undefined} />
      </VCam>
      <Pop t={t - 0.3} x={300} y={330} size={84} color="#8ad8ff" hold={tClimb - 0.3} rot={-4}>TEARS</Pop>
      <Pop t={t - 1.2} x={780} y={420} size={84} color="#ffd84d" hold={tClimb - 1.2} rot={4}>LAUGHTER</Pop>
      {t > tClimb + 0.8 && (
        <g>
          <Burst t={t - tClimb - 0.8} x={300} y={360} r={110} label="CLINK!" size={48} />
          <Burst t={t - tClimb - 1.6} x={790} y={470} r={110} label="CHIP!" size={50} color="#8ad8ff" tcolor={C.navy} />
        </g>
      )}
      <Vig s={0.45} />
    </g>
  );
};

// 6 — reunited: warm light, families hugging, the hero smiles
const Hug: React.FC<{x: number; y: number; t: number; a: number; b: number; sa?: number; sb?: number; seed?: number}> = ({x, y, t, a, b, sa = 0.52, sb = 0.52}) => {
  const sway = Math.sin(t * 2) * 0.04;
  return (
    <g>
      <Berliner seed={a} x={x - 46} y={feet(y, sa)} s={sa} face={0.9} expr="happy" blush tilt={0.16 + sway} larm={[0.3, 0.2]} rarm={[-1.9, 1.7]} />
      <Berliner seed={b} x={x + 46} y={feet(y, sb)} s={sb} face={-0.9} expr="happy" blush tilt={-0.16 + sway} larm={[1.9, -1.7]} rarm={[-0.3, -0.2]} />
    </g>
  );
};

export const BHug: React.FC<ShotProps> = ({t, D, cue}) => {
  const tHug = cue('people could finally');
  const together = easeOut(prog(t, 0.3, 1.6));
  return (
    <g>
      <VCam cx={540} cy={lerp(1330, 1360, prog(t, 0, D))} z={lerp(1.2, 1.3, ease(prog(t, 0, D)))}>
        <NightSky t={t} id="us" warm={1} />
        <Glow id="sunrise" x={540} y={1150} r={900} color="#ffd9a0" a={0.7} />
        <Skyline y={1200} t={t} warm />
        <Wall x0={-600} x1={180} y={1480} t={t} night={false} />
        <Wall x0={900} x1={1700} y={1480} t={t} night={false} />
        <Ground warm />
        {/* through the gap: two families run into each other's arms */}
        {together < 1 ? (
          <g>
            <Berliner seed={14} x={lerp(240, 494, together)} y={feet(1620, 0.52)} s={0.52} face={0.9} expr="o" walk={t * 2} larm={[1.6, -0.4]} rarm={[-1.6, 0.4]} />
            <Berliner seed={21} x={lerp(840, 586, together)} y={feet(1620, 0.52)} s={0.52} face={-0.9} expr="o" walk={t * 2} larm={[1.6, -0.4]} rarm={[-1.6, 0.4]} />
          </g>
        ) : (
          <Hug x={540} y={1620} t={t} a={14} b={21} />
        )}
        <Hug x={230} y={1700} t={t + 1} a={33} b={8} sa={0.5} sb={0.36} />
        <Hug x={850} y={1700} t={t + 2} a={4} b={27} sa={0.44} sb={0.5} />
        {Array.from({length: 7}).map((_, k) => {
          const ph = (t * 0.45 + k / 7) % 1;
          return <Heart key={k} x={160 + k * 130 + Math.sin(t * 2 + k) * 20} y={1450 - ph * 520} s={0.9 + (k % 3) * 0.2} a={Math.sin(ph * Math.PI) * prog(t, 1.4, 2)} />;
        })}
        <Hero x={385} y={feet(1880, 0.5)} s={0.5} expr="smile" face={0} look={[0, -0.6]} blush larm={[0.3, 0.2]} rarm={[-2.2, 2.0]} />
        <Tear x={435} y={feet(1880, 0.5) - 10} t={t} s={0.5} />
      </VCam>
      {t > tHug && <Pop t={t - tHug} x={540} y={330} size={104} color="#fff">TOGETHER AGAIN</Pop>}
      <Vig s={0.35} color="#6a2a1a" />
    </g>
  );
};

// 7 — the time machine flashes red; he turns to the camera; subscribe
export const BEnd: React.FC<ShotProps> = ({t, D, cue}) => {
  const tFlash = cue('until my time machine');
  const tSub = cue('SUBSCRIBE');
  const alarm = prog(t, tFlash, tFlash + 0.3);
  const blink = alarm > 0 ? 0.5 + 0.5 * Math.sign(Math.sin(t * 14)) : 0;
  if (t < tSub) {
    const turned = t > tFlash + 1.2;
    const hp = {x: 540, y: feet(1650, 0.62), s: 0.62, larm: [0.3, 0.2] as [number, number], rarm: [-1.5, 0.6] as [number, number]};
    const [hx, hy] = handPos(hp, 'r');
    return (
      <g>
        <VCam cx={540} cy={lerp(1250, 1180, prog(t, 0, D))} z={turned ? lerp(1.4, 2.1, easeOut(prog(t, tFlash + 1.2, tFlash + 1.8))) : 1.15} shake={turned ? 8 : 0} t={t}>
          <NightSky t={t} id="es" />
          <Skyline y={1150} t={t} />
          <Wall x0={-600} x1={1700} y={1480} t={t} crack={0.8} />
          <Ground />
          <Crowd t={t} y={1520} n={10} speed={60} seed={110} cheer />
          <Hero {...hp} expr={turned ? 'shock' : alarm > 0 ? 'o' : 'smile'} face={turned ? 0 : 0.6} look={turned ? [0, 0] : [0.6, 0.8]} brows={turned ? 'up' : undefined} />
          {alarm > 0 && <Glow id="alarm" x={hx + 40} y={hy - 40} r={360} color="#ff2020" a={0.75 * blink} />}
          <TimeMachine x={hx + 40} y={hy + 40} s={0.22} t={t} glow={0} shake={alarm} screen={alarm > 0 ? '!!!' : '1989'} screenColor={alarm > 0 ? '#ff4a4a' : '#7dffb0'} />
        </VCam>
        <Fill c="#ff1a1a" a={0.22 * blink} />
        {t < tFlash && <Pop t={t - 0.2} x={540} y={330} size={84} font={HAND}>History... done!</Pop>}
        {alarm > 0 && <Pop t={t - tFlash} x={540} y={330} size={110} color="#ff4a4a" rot={-3}>BEEP! BEEP!</Pop>}
        <Vig s={0.55} />
        <Fill c="#fff" a={prog(t, tSub - 0.25, tSub)} />
      </g>
    );
  }
  const tt = t - tSub;
  const k = backOut(prog(tt, 0, 0.45), 2) * (1 + 0.05 * Math.sin(t * 7));
  return (
    <g>
      <rect x={0} y={0} width={VW} height={VH} fill="#b82126" />
      {Array.from({length: 16}).map((_, i) => (
        <path key={i} transform={`translate(540,960) rotate(${t * 20 + i * 22.5})`} d="M0,0 L1400,-140 L1400,140 Z" fill="#cc2e30" />
      ))}
      <Confetti t={tt} n={50} />
      <Hero x={540} y={lerp(2200, 1180, easeOut(prog(tt, 0, 0.5)))} s={0.95} expr="grin" face={0} larm={[0.3, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 9), 0.4]} />
      <g transform={`translate(540,420) scale(${Math.max(k, 0.001)})`}>
        <rect x={-430} y={-110} width={860} height={220} rx={50} fill="#ff2a2a" stroke={C.ink} strokeWidth={9} />
        <polygon points="-340,-50 -340,50 -260,0" fill="#fff" />
        <Txt x={60} y={0} size={110} outline={8}>SUBSCRIBE</Txt>
      </g>
      <Pop t={tt - 0.3} x={540} y={640} size={96} color="#ffd84d">HISTORY WORLD</Pop>
      <Fill c="#000" a={prog(t, D - 0.35, D)} />
    </g>
  );
};

export const SHOTS: Record<string, React.FC<ShotProps>> = {
  b_hook: BHook, b_crowd: BCrowd, b_divided: BDivided, b_cross: BCross, b_hammer: BHammer, b_hug: BHug, b_end: BEnd,
};
void [easeIn, Sparkle];
