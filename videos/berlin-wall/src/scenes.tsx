// Every shot of the long-form film (16:9). A shot gets local time t (s), its duration D and
// cue(text) = start of the narration sentence containing `text` (cue(text, frac) = part-way through it).
import React from 'react';
import {C, W, H, clamp, ease, easeIn, easeOut, lerp, prog, rng, backOut} from './lib';
import {Doodle, DoodleProps, CapShape} from './Hero';
import {Burst, Cam, Confetti, Glow, HAND, Pop, Sparkle, Star, Sweat, Txt, Vignette} from './fx';
import {TimeMachine} from './props';
import {Bedroom, Vortex} from './bg';
import {
  BarbedWire, Berliner, Bottle, Bouquet, BrandenburgGate, Candle, Chocolate, Crowd, DaySky, Dog, Fill, Floodlight, Flower, GRAF, Girl, Ground, Guard,
  Hammer, HeadRow, Heart, Hero, NightSky, Official, OldLady, OldMan, Papers, Skyline, Speaker, Street, Tear, Trabant, Wall, WallPiece, Watchtower, feet,
} from './berlin';

export type Cue = (text: string, frac?: number) => number;
export type ShotProps = {t: number; D: number; cue: Cue};

// ------------------------------------------------------------------ helpers
/** camera keyframes [tStart, cx, cy, z] with eased transitions of `tr` seconds */
const camAt = (t: number, keys: [number, number, number, number][], tr = 0.9) => {
  let [, cx, cy, z] = keys[0];
  for (let i = 1; i < keys.length; i++) {
    const [ts, x, y, zz] = keys[i];
    const k = ease(prog(t, ts - tr / 2, ts + tr / 2));
    cx = lerp(cx, x, k);
    cy = lerp(cy, y, k);
    z = lerp(z, zz, k);
  }
  return {cx, cy, z};
};
const fadeWin = (t: number, a: number, b: number, f = 0.25) => clamp(Math.min((t - a) / f, (b - t) / f));

const Bubble: React.FC<{x: number; y: number; w: number; h: number; text: string; size?: number; tail?: [number, number]; a?: number; think?: boolean; font?: string; color?: string}> = ({
  x, y, w, h, text, size = 46, tail = [-40, 60], a = 1, think, font = HAND, color = C.ink,
}) => {
  if (a <= 0) return null;
  const lines = text.split('\n');
  const k = backOut(clamp(a), 1.8);
  return (
    <g opacity={clamp(a * 3)} transform={`translate(${x},${y}) scale(${Math.max(0.001, k)}) translate(${-x},${-y})`}>
      {think ? (
        <g>
          <ellipse cx={x} cy={y} rx={w / 2} ry={h / 2} fill="#fff" stroke={C.ink} strokeWidth={6} />
          {[18, 12, 8].map((r, i) => (
            <circle key={i} cx={x + tail[0] * ((i + 1) / 3.5) * 1.6} cy={y + (h / 2) * 0.8 + tail[1] * ((i + 1) / 3.5)} r={r} fill="#fff" stroke={C.ink} strokeWidth={5} />
          ))}
        </g>
      ) : (
        <g>
          <path d={`M${x - 30},${y + h / 2 - 12} L${x + tail[0]},${y + h / 2 + tail[1]} L${x + 25},${y + h / 2 - 12} Z`} fill="#fff" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
          <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={Math.min(h / 2, 40)} fill="#fff" stroke={C.ink} strokeWidth={6} />
          <path d={`M${x - 27},${y + h / 2 - 4} L${x + tail[0] * 0.95},${y + h / 2 + tail[1] * 0.95} L${x + 22},${y + h / 2 - 4} Z`} fill="#fff" />
        </g>
      )}
      {lines.map((l, i) => (
        <Txt key={i} x={x} y={y + (i - (lines.length - 1) / 2) * size * 1.1} size={size} color={color} font={font} outline={0} shadow={false}>{l}</Txt>
      ))}
    </g>
  );
};

/** top-left location / date card */
const LocCard: React.FC<{t: number; place: string; date: string; dur?: number}> = ({t, place, date, dur = 4.5}) => {
  if (t < 0 || t > dur + 0.6) return null;
  const k = easeOut(prog(t, 0, 0.5)) - easeIn(prog(t, dur, dur + 0.5));
  const x = lerp(-820, 50, k);
  return (
    <g>
      <rect x={x} y={44} width={760} height={140} rx={18} fill="rgba(10,10,20,0.82)" />
      <rect x={x} y={44} width={14} height={140} fill={C.red} />
      <Txt x={x + 40} y={90} size={42} anchor="start" outline={0}>{place}</Txt>
      <Txt x={x + 40} y={146} size={50} anchor="start" outline={0} color={C.gold}>{date}</Txt>
    </g>
  );
};

/** a big rubber-stamp year in the top right */
const YearStamp: React.FC<{t: number; year: string; x?: number; y?: number; hold?: number}> = ({t, year, x = 1620, y = 140, hold = 999}) => {
  if (t < 0) return null;
  const k = t < 0.3 ? lerp(2.2, 1, easeOut(t / 0.3)) : 1;
  const a = t < hold ? clamp(t / 0.1) : 1 - prog(t, hold, hold + 0.3);
  if (a <= 0) return null;
  return (
    <g transform={`translate(${x},${y}) rotate(-6) scale(${k})`} opacity={a}>
      <rect x={-210} y={-72} width={420} height={144} rx={16} fill="rgba(255,248,230,0.92)" stroke={C.red} strokeWidth={10} />
      <Txt x={0} y={4} size={110} color={C.red} outline={0} shadow={false}>{year}</Txt>
    </g>
  );
};

const Doughnut: React.FC<{x: number; y: number; s?: number}> = ({x, y, s = 1}) => (
  <g transform={`translate(${x},${y}) scale(${s})`}>
    <ellipse cx={0} cy={10} rx={110} ry={80} fill="#d89a4a" stroke={C.ink} strokeWidth={7} />
    <ellipse cx={0} cy={-4} rx={96} ry={58} fill="#e8b46a" />
    {Array.from({length: 22}).map((_, i) => {
      const R = rng(i + 4);
      return <circle key={i} cx={(R() - 0.5) * 160} cy={(R() - 0.5) * 80 - 6} r={5} fill="#fff" />;
    })}
    <path d="M90,20 C130,30 140,60 120,70 C100,74 96,50 90,20 Z" fill="#c8203a" stroke={C.ink} strokeWidth={5} />
  </g>
);

const Suitcase: React.FC<{c?: string}> = ({c = '#8a5a2b'}) => (
  <g>
    <path d="M-12,4 L-12,-6 L12,-6 L12,4" fill="none" stroke={C.ink} strokeWidth={5} />
    <rect x={-40} y={4} width={80} height={60} rx={8} fill={c} stroke={C.ink} strokeWidth={5} />
  </g>
);

const Briefcase: React.FC = () => <Suitcase c="#3a2a1a" />;

const Clock: React.FC<{x: number; y: number; r?: number; h: number; m: number}> = ({x, y, r = 60, h, m}) => {
  const am = (m / 60) * 2 * Math.PI;
  const ah = ((h % 12) / 12 + m / 720) * 2 * Math.PI;
  return (
    <g transform={`translate(${x},${y})`}>
      <circle r={r} fill="#fbf6e8" stroke={C.ink} strokeWidth={6} />
      {Array.from({length: 12}).map((_, i) => {
        const a = (i / 12) * 2 * Math.PI;
        return <line key={i} x1={Math.sin(a) * r * 0.78} y1={-Math.cos(a) * r * 0.78} x2={Math.sin(a) * r * 0.9} y2={-Math.cos(a) * r * 0.9} stroke={C.ink} strokeWidth={4} />;
      })}
      <line x1={0} y1={0} x2={Math.sin(ah) * r * 0.5} y2={-Math.cos(ah) * r * 0.5} stroke={C.ink} strokeWidth={8} strokeLinecap="round" />
      <line x1={0} y1={0} x2={Math.sin(am) * r * 0.75} y2={-Math.cos(am) * r * 0.75} stroke={C.red} strokeWidth={5} strokeLinecap="round" />
    </g>
  );
};

const Fireworks: React.FC<{t: number; spots: [number, number, number][]; r?: number}> = ({t, spots, r = 160}) => (
  <g>
    {spots.map(([fx, fy, ph], k) => {
      const u = ((t + ph) % 1.8) / 1.8;
      return (
        <g key={k} opacity={1 - u}>
          {Array.from({length: 12}).map((_, j) => {
            const a = (j * Math.PI) / 6;
            return <line key={j} x1={fx + Math.cos(a) * r * 0.25 * u} y1={fy + Math.sin(a) * r * 0.25 * u} x2={fx + Math.cos(a) * r * u} y2={fy + Math.sin(a) * r * u}
              stroke={GRAF[(j + k) % 6]} strokeWidth={8} strokeLinecap="round" />;
          })}
        </g>
      );
    })}
  </g>
);

const Chips: React.FC<{t: number; at: [number, number][]; rate?: number}> = ({t, at, rate = 2.4}) => {
  const R = rng(5);
  const out: React.ReactNode[] = [];
  at.forEach(([hx, hy], k) => {
    const ph = (t * rate + k * 0.33) % 1;
    if (ph < 0.5) {
      for (let c = 0; c < 4; c++) {
        const u = ph * 2;
        out.push(<rect key={`${k}${c}`} x={hx + (R() - 0.3) * 160 * u} y={hy - 200 * u + 300 * u * u} width={14} height={10} fill="#bdbdc0" stroke={C.ink} strokeWidth={2}
          transform={`rotate(${u * 300 + c * 40} ${hx} ${hy})`} />);
      }
    }
  });
  return <g>{out}</g>;
};

/** simplified outline of Germany in a unit box (x east, y south) */
const DE: [number, number][] = [[0.22, 0.12], [0.3, 0.05], [0.38, 0], [0.46, 0.04], [0.5, 0.1], [0.6, 0.07], [0.72, 0.05], [0.84, 0.1], [0.9, 0.2], [0.92, 0.35], [0.98, 0.48],
  [0.88, 0.55], [0.8, 0.6], [0.86, 0.72], [0.92, 0.82], [0.84, 0.9], [0.74, 0.94], [0.6, 0.97], [0.45, 0.96], [0.3, 0.98], [0.22, 0.92], [0.2, 0.8], [0.1, 0.7], [0.04, 0.58],
  [0, 0.46], [0.06, 0.36], [0.08, 0.24], [0.16, 0.18]];
const EAST: [number, number][] = [[0.55, -0.1], [0.55, 0.07], [0.52, 0.2], [0.58, 0.32], [0.5, 0.45], [0.56, 0.55], [0.66, 0.62], [1.1, 0.62], [1.1, -0.1]];
const pts = (p: [number, number][], x: number, y: number, w: number, h: number) => p.map(([u, v]) => `${x + u * w},${y + v * h}`).join(' ');

const GermanyMap: React.FC<{x: number; y: number; w: number; h: number; split: number; unite?: number; labels?: number}> = ({x, y, w, h, split, unite = 0, labels = 0}) => {
  const east = C.red;
  const eastCol = unite > 0 ? `rgba(237,51,56,${0.85 * (1 - unite)})` : 'rgba(237,51,56,0.85)';
  return (
    <g>
      <defs><clipPath id="declip"><polygon points={pts(DE, x, y, w, h)} /></clipPath></defs>
      <polygon points={pts(DE, x + 10, y + 14, w, h)} fill="rgba(0,0,0,0.25)" />
      <polygon points={pts(DE, x, y, w, h)} fill="#5aa0e0" stroke={C.ink} strokeWidth={8} strokeLinejoin="round" />
      {split > 0 && <g clipPath="url(#declip)" opacity={clamp(split * 1.5)}>
        <polygon points={pts(EAST, x, y, w, h)} fill={eastCol} />
        <polyline points={pts(EAST.slice(1, 8), x, y, w, h)} fill="none" stroke={C.ink} strokeWidth={8} strokeDasharray="22 12" opacity={1 - unite} />
      </g>}
      <polygon points={pts(DE, x, y, w, h)} fill="none" stroke={C.ink} strokeWidth={8} strokeLinejoin="round" />
      <circle cx={x + 0.78 * w} cy={y + 0.3 * h} r={14} fill="#fff" stroke={C.ink} strokeWidth={5} />
      {labels > 0 && <g opacity={labels}>
        <Txt x={x + 0.3 * w} y={y + 0.55 * h} size={46} color="#fff" outline={7}>WEST</Txt>
        <Txt x={x + 0.79 * w} y={y + 0.45 * h} size={46} color="#fff" outline={7}>EAST</Txt>
        <Txt x={x + 0.78 * w} y={y + 0.3 * h - 44} size={34} color={C.gold} outline={6}>BERLIN</Txt>
      </g>}
      {void east}
    </g>
  );
};

// ================================================================== HOOK + TITLE
export const Hook: React.FC<ShotProps> = ({t, D, cue}) => {
  const tHam = cue("I'm holding");
  const tThou = cue('Thousands');
  const tGuards = cue('border guards');
  const tWeek = cue('Last week');
  const tBreak = cue('history is breaking');
  const tLit = cue('Literally');
  const cam = camAt(t, [[0, 960, 380, 2.1], [tHam, 1000, 400, 1.75], [tThou, 960, 520, 1.0], [tGuards, 430, 560, 1.55], [tWeek, 960, 420, 1.5], [tBreak, 960, 400, 1.85]], 1.0);
  const swinging = t > tBreak;
  const sw = swinging ? 0.5 + 0.5 * Math.sin((t - tBreak) * 9) : 0.3;
  const hp: DoodleProps = {x: 960, y: 480 - 300 * 0.55 + 10, s: 0.55, expr: swinging ? 'laugh' : t < tThou ? 'grin' : 'happy', face: 0.2, look: [0.3, 0],
    larm: [0.9, -0.5], rarm: [-2.3 - 0.4 * sw, 0.3], legs: [0.15 + 0.1 * Math.sin(t * 3), -0.15 + 0.1 * Math.sin(t * 3 + 1)], hold: <Hammer swing={sw} />};
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z} shake={swinging ? 3 : 0} t={t}>
        <NightSky t={t} id="hk" />
        <Fireworks t={t} spots={[[300, 120, 0], [1600, 80, 0.7], [1150, 40, 1.3]]} />
        <BrandenburgGate x={960} y={830} s={1.35} fill="#3a3a5a" detail />
        <Floodlight x={200} y={830} t={t} />
        <Floodlight x={1720} y={830} t={t} />
        <Ground y={820} />
        <Wall x0={-600} x1={2600} y={820} h={300} t={t} crack={prog(t, tBreak, D) * 0.8} />
        {[-260, -60, 140, 340, 560, 1360, 1560, 1760, 1980, 2180].map((x, i) => {
          const j = Math.abs(Math.sin(t * 6 + i)) * 16;
          return <Berliner key={i} seed={i + 3} x={x} y={feet(484 - j, 0.4)} s={0.4} face={x < 960 ? 0.4 : -0.4} expr="laugh" larm={[2.6, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 8 + i), 0.3]} />;
        })}
        {[0, 1].map((k) => <Guard key={k} x={300 + k * 220} y={feet(905, 0.5)} s={0.5} face={0.5} look={[1, -0.6]} expr={t > tGuards + 1 ? 'o' : 'flat'} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />)}
        <Hero {...hp} />
        {t > tLit && <WallPiece x={1060 + (t - tLit) * 120} y={530 + 600 * (t - tLit) * (t - tLit)} s={0.5} rot={(t - tLit) * 300} />}
        <HeadRow y={1010} t={t} n={14} seed={20} s={0.5} x0={-200} dx={170} />
      </Cam>
      {t > tLit && <Burst t={t - tLit} x={1500} y={260} r={140} label="CRACK!" size={58} />}
      {t > tGuards + 0.6 && t < tWeek && <Pop t={t - tGuards - 0.6} x={960} y={140} size={70} font={HAND} outline={6}>*just watching*</Pop>}
      <LocCard t={t - 0.6} place="BERLIN, GERMANY" date="9 NOVEMBER 1989" dur={tThou + 2} />
      <Vignette strength={0.5} />
      <Fill c="#fff" a={prog(t, D - 0.25, D)} />
    </g>
  );
};

export const Title: React.FC<ShotProps> = ({t}) => {
  const rows: [string, string, number][] = [['I WITNESSED', '#fff', 110], ['THE FALL OF THE', C.gold, 110], ['BERLIN WALL!', C.gold, 170]];
  return (
    <g>
      <NightSky t={t} id="tt" />
      <Fireworks t={t} spots={[[260, 160, 0], [1700, 120, 0.6], [1500, 380, 1.2]]} />
      <Ground y={900} />
      <Wall x0={-60} x1={2000} y={900} h={260} t={t} />
      {rows.map(([w, c, size], ri) => {
        const tt = t - 0.15 - ri * 0.4;
        if (tt < 0) return null;
        const k = tt < 0.45 ? backOut(tt / 0.45, 2.4) : 1;
        return (
          <g key={ri} transform={`translate(700,${170 + ri * 160}) scale(${k})`}>
            <Txt x={0} y={0} size={size} color={c} outline={14} rot={-2 + Math.sin(t * 3 + ri)}>{w}</Txt>
          </g>
        );
      })}
      {t > 1.3 && (
        <g>
          <Hero x={lerp(2200, 1560, easeOut(prog(t, 1.3, 1.9)))} y={feet(630, 0.55)} s={0.55} expr="grin" face={-0.4} larm={[0.3, 0.2]}
            rarm={[-2.4 + 0.3 * Math.sin(t * 8), 0.3]} hold={<Hammer swing={0.5 + 0.5 * Math.sin(t * 8)} />} />
        </g>
      )}
      <Txt x={700} y={700} size={52} font={HAND} outline={6} opacity={ease(prog(t, 1.6, 2.2))}>HISTORY WORLD</Txt>
      <Vignette strength={0.45} />
    </g>
  );
};

// ================================================================== 1961
export const Glitch: React.FC<ShotProps> = ({t, D, cue}) => {
  const tPress = cue('I pressed');
  const tNot = cue('Not in 1989');
  const t61 = cue('In 1961');
  if (t < tPress + 1.4) {
    const shake = prog(t, cue('My five dollar'), tPress) * 0.5 + (t > tPress ? 1 : 0);
    const press = t > tPress + 0.3;
    return (
      <g>
        <Cam cx={1000} cy={lerp(600, 640, prog(t, 0, tPress))} z={lerp(1.4, 1.6, prog(t, 0, tPress))} shake={press ? 10 : 0} t={t}>
          <Bedroom t={t} />
          <Hero x={820} y={feet(900, 0.62)} s={0.62} expr={press ? 'scared' : shake > 0.2 ? 'worried' : 'smile'} face={0.6} look={[1, 0.6]} brows={shake > 0.2 ? 'worried' : undefined}
            larm={[0.3, 0.2]} rarm={press ? [-1.4, 0.2] : [-0.8, 0.4]} />
          <TimeMachine x={1130} y={900} s={0.45} t={t} screen={press ? '????' : '$5'} glow={press ? 1 : shake} shake={shake} lever={press ? 1 : 0} />
        </Cam>
        {t < tPress && <Pop t={t - 0.3} x={960} y={140} size={80} color={C.gold}>$5 TIME MACHINE</Pop>}
        {press && <Burst t={t - tPress - 0.3} x={1450} y={250} r={130} label="CLICK!" size={52} />}
        <Fill c="#fff" a={prog(t, tPress + 1.0, tPress + 1.4)} />
        <Vignette strength={0.35} />
      </g>
    );
  }
  if (t < t61 + 0.5) {
    const tt = t - tPress - 1.4;
    const yr = t < tNot ? Math.round(lerp(2026, 1989, ease(prog(t, tPress + 1.5, tNot)))) : Math.round(lerp(1989, 1961, easeIn(prog(t, tNot + 0.4, t61))));
    const glitch = t > tNot + 0.3 && Math.sin(t * 40) > 0.6;
    return (
      <g>
        <Vortex t={t} hue1={glitch ? '#d83a3a' : '#3a4ad8'} />
        <g transform={`translate(${W / 2 + 240 * Math.sin(t * 0.9)},${H / 2 + 100 * Math.cos(t * 1.3) - 60}) rotate(${t * 140})`}>
          <Doodle x={0} y={-150} s={0.6} expr="shock" face={0} larm={[2.4, 0.5]} rarm={[-2.4, -0.5]} legs={[0.5, -0.5]} />
        </g>
        <g transform={`translate(${glitch ? 12 : 0},0)`}>
          <rect x={W / 2 - 260} y={60} width={520} height={130} rx={30} fill="rgba(5,3,16,0.75)" stroke={glitch ? '#ff4a4a' : C.gold} strokeWidth={5} />
          <Txt x={W / 2} y={125} size={90} color={yr === 1989 ? '#7dffb0' : glitch ? '#ff4a4a' : C.gold} outline={0} shadow={false}>{String(yr)}</Txt>
        </g>
        {t > tNot && t < tNot + 1.6 && <Pop t={t - tNot} x={W / 2} y={300} size={70} color="#7dffb0">1989? ALMOST...</Pop>}
        {t > tNot + 1.2 && <Burst t={t - tNot - 1.2} x={1500} y={760} r={120} label="ERROR!" size={46} color="#ff8a8a" tcolor="#fff" />}
        <Fill c="#fff" a={1 - prog(tt, 0, 0.4) + prog(t, t61 + 0.1, t61 + 0.5)} />
        <Vignette strength={0.55} />
      </g>
    );
  }
  const tt = t - t61 - 0.5;
  const land = easeOut(prog(tt, 0, 0.4));
  return (
    <g>
      <Cam cx={960} cy={540} z={lerp(1.0, 1.1, prog(tt, 0, 3))}>
        <DaySky id="g61" />
        <Street y={820} x0={-300} seed={4} />
        <Ground y={820} night={false} />
        <rect x={-300} y={860} width={2600} height={10} fill="#e8e8e0" />
        <Hero x={900} y={lerp(-300, feet(950, 0.62), land)} s={0.62} expr="shock" face={0} brows="up" squash={tt > 0.4 ? -0.15 * Math.exp(-(tt - 0.4) * 6) : 0}
          larm={[1.2, -0.4]} rarm={[-1.2, 0.4]} />
        <TimeMachine x={1180} y={950} s={0.32} t={t} screen="1961" screenColor="#ff8a3a" />
      </Cam>
      <Fill c="#fff" a={1 - prog(tt, 0, 0.35)} />
      <YearStamp t={tt - 0.3} year="1961" />
      <Vignette strength={0.3} />
    </g>
  );
};

export const MapShot: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWW = cue('After World War');
  const tWE = cue('West Germany, and');
  const tBer = cue('And Berlin');
  const tFree = cue('Half the city');
  const tNot = cue('The other half');
  const mapK = backOut(prog(t, tWW - 0.2, tWW + 0.4), 1.4);
  const zoom = ease(prog(t, tBer - 0.2, tBer + 1.4));
  const bx = 560 + 0.78 * 640;
  const by = 120 + 0.3 * 800;
  const inset = prog(t, tBer + 1.0, tBer + 1.5);
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#f2e6c8" />
      {Array.from({length: 14}).map((_, i) => <line key={i} x1={0} y1={i * 80} x2={W} y2={i * 80} stroke="#e4d4b0" strokeWidth={3} />)}
      <g transform={`translate(${lerp(0, 960 - bx * 4, zoom)},${lerp(0, 520 - by * 4, zoom)}) scale(${lerp(1, 4, zoom)})`} opacity={1 - inset}>
        <g transform={`translate(860,520) scale(${Math.max(0.001, mapK)}) translate(-860,-520)`}>
          <GermanyMap x={560} y={120} w={640} h={800} split={prog(t, tWE - 0.3, tWE + 0.6)} labels={prog(t, tWE + 0.3, tWE + 0.8)} />
        </g>
      </g>
      {inset > 0 && (
        <g opacity={inset}>
          <rect x={0} y={0} width={W} height={H} fill="#c86a6a" />
          {Array.from({length: 14}).map((_, i) => <line key={i} x1={0} y1={i * 80} x2={W} y2={i * 80} stroke="#b85a5a" strokeWidth={3} />)}
          <Txt x={1660} y={170} size={44} color="#fff" outline={6}>EAST GERMANY</Txt>
          <defs><clipPath id="berclip"><path d="M960,170 C1200,160 1360,300 1340,520 C1330,740 1160,880 940,870 C720,860 560,720 580,500 C600,300 740,180 960,170 Z" /></clipPath></defs>
          <path d="M960,170 C1200,160 1360,300 1340,520 C1330,740 1160,880 940,870 C720,860 560,720 580,500 C600,300 740,180 960,170 Z" fill="#a8a8b0" stroke={C.ink} strokeWidth={8} />
          <g clipPath="url(#berclip)">
            <path d="M0,0 L1010,0 C990,200 1060,320 990,460 C940,560 1030,700 990,1080 L0,1080 Z" fill="#6ac06a" />
          </g>
          <path d="M1010,170 C990,300 1060,320 990,460 C940,560 1030,700 990,870" fill="none" stroke={C.ink} strokeWidth={10} strokeDasharray="24 12" />
          <path d="M960,170 C1200,160 1360,300 1340,520 C1330,740 1160,880 940,870 C720,860 560,720 580,500 C600,300 740,180 960,170 Z" fill="none" stroke={C.ink} strokeWidth={8} />
          <Txt x={780} y={420} size={50} color="#fff" outline={7}>WEST</Txt>
          <Txt x={780} y={480} size={50} color="#fff" outline={7}>BERLIN</Txt>
          <Txt x={1170} y={420} size={50} color="#fff" outline={7}>EAST</Txt>
          <Txt x={1170} y={480} size={50} color="#fff" outline={7}>BERLIN</Txt>
          {t > tFree && <g>
            <Pop t={t - tFree} x={780} y={620} size={64} color={C.gold}>FREE</Pop>
            {[0, 1, 2].map((k) => <Sparkle key={k} x={700 + k * 80} y={300 + (k % 2) * 40} r={26} t={t + k} />)}
          </g>}
          {t > tNot && <Pop t={t - tNot} x={1170} y={620} size={56} color="#ddd">NOT FREE</Pop>}
        </g>
      )}
      {(() => {
        const hx = lerp(260, 280, inset);
        const point = t > tWW && t < tBer + 1 ? 1 : t > tFree ? 1 : 0;
        return <Hero x={hx} y={feet(900, 0.6)} s={0.6} expr={t > tNot ? 'frown' : 'smile'} face={0.6} look={[1, -0.3]} larm={[0.3, 0.2]}
          rarm={point ? [-2.0, 0.1] : [-0.3, -0.2]} hold={point ? <line x1={0} y1={0} x2={0} y2={-220} stroke="#8a5a2b" strokeWidth={10} strokeLinecap="round" transform="rotate(30)" /> : undefined} />;
      })()}
      {t < tWW && <Pop t={t - 0.2} x={960} y={130} size={84} color={C.red}>QUICK HISTORY LESSON!</Pop>}
      <YearStamp t={t - tWW - 0.5} year="1945" x={1620} y={130} hold={tBer - tWW - 0.6} />
      <Vignette strength={0.3} />
    </g>
  );
};

export const Escape: React.FC<ShotProps> = ({t, D, cue}) => {
  const tMil = cue('Almost three');
  const tDoc = cue('Doctors');
  const tGov = cue('The East German government');
  if (t < tGov - 0.2) {
    const count = Math.round(lerp(0, 3000000, easeOut(prog(t, 0.4, tMil + 1.2))) / 1000) * 1000;
    return (
      <g>
        <Cam cx={960} cy={560} z={1.05}>
          <DaySky id="esc" />
          <Street y={800} x0={-500} n={6} seed={7} grey />
          <Street y={800} x0={1300} n={5} seed={8} />
          <Ground y={800} night={false} />
          <g transform="translate(1180,800)">
            <line x1={0} y1={0} x2={0} y2={-300} stroke="#5a5a5a" strokeWidth={12} />
            <rect x={-200} y={-330} width={400} height={110} rx={8} fill="#fff" stroke={C.ink} strokeWidth={6} />
            <Txt x={0} y={-296} size={30} color={C.ink} outline={0} shadow={false}>YOU ARE ENTERING</Txt>
            <Txt x={0} y={-252} size={34} color={C.red} outline={0} shadow={false}>THE WEST</Txt>
          </g>
          <rect x={1170} y={800} width={20} height={300} fill="#fff" opacity={0.7} />
          <Txt x={420} y={300} size={60} color="#e0e0e8" outline={7}>EAST</Txt>
          <Txt x={1600} y={300} size={60} color={C.gold} outline={7}>WEST</Txt>
          {Array.from({length: 11}).map((_, i) => {
            const R = rng(i + 3);
            const sp = 120 + R() * 60;
            const x = -300 + ((R() * 2400 + t * sp) % 2400);
            const y = 900 + (i % 3) * 36;
            const s = 0.4 + (i % 3) * 0.03;
            const g = x < 1180;
            return <Berliner key={i} seed={i + 4} grey={g} x={x} y={feet(y, s)} s={s} face={0.85} walk={t * 1.6 + i * 0.4} expr={g ? 'flat' : 'happy'}
              larm={[0.3, 0.2]} rarm={[-0.2, -0.1]} hold={i % 2 === 0 ? <Suitcase c={['#8a5a2b', '#3a6ab8', '#a03a1a'][i % 3]} /> : undefined} />;
          })}
        </Cam>
        <g>
          <rect x={660} y={50} width={600} height={130} rx={24} fill="rgba(10,10,20,0.82)" />
          <Txt x={960} y={115} size={84} color={C.gold} outline={0}>{count.toLocaleString('en-US')}</Txt>
        </g>
        {t > tMil && <Pop t={t - tMil} x={960} y={230} size={46} font={HAND} outline={5} hold={tDoc - tMil}>people left East Germany (1949–1961)</Pop>}
        {[['DOCTORS', 420, 0], ['ENGINEERS', 960, 0.8], ['FAMILIES', 1500, 1.6]].map(([w, x, d]) => (
          <Pop key={w as string} t={t - tDoc - (d as number)} x={x as number} y={250} size={64} color="#fff" rot={-3}>{w as string}</Pop>
        ))}
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tGov + 0.2;
  const arrow = ease(prog(tt, 0.4, 2.2));
  return (
    <g>
      <Cam cx={960} cy={540} z={lerp(1.0, 1.12, prog(tt, 0, 3))}>
        <rect x={-200} y={-200} width={2400} height={1500} fill="#c8c0a8" />
        <rect x={-200} y={760} width={2400} height={600} fill="#8a6a4a" stroke={C.ink} strokeWidth={6} />
        <g transform="translate(1250,180)">
          <rect x={-300} y={0} width={600} height={420} fill="#fbf6e8" stroke={C.ink} strokeWidth={7} />
          <Txt x={0} y={44} size={40} color={C.ink} outline={0} shadow={false}>POPULATION</Txt>
          <polyline points={`-250,120 ${-250 + 500 * arrow},${120 + 250 * arrow}`} fill="none" stroke={C.red} strokeWidth={14} strokeLinecap="round" />
          <polygon transform={`translate(${-250 + 500 * arrow},${120 + 250 * arrow}) rotate(27)`} points="0,-24 40,0 0,24" fill={C.red} stroke={C.ink} strokeWidth={4} />
        </g>
        <rect x={420} y={640} width={700} height={40} fill="#6a4a2a" stroke={C.ink} strokeWidth={6} />
        <Official x={760} y={feet(770, 0.6)} s={0.6} face={0.5} look={[1, -0.5]} expr="worried" brows="worried" larm={[0.6, 0.6]} rarm={[-2.2, 2.0]} />
        <Sweat x={850} y={feet(770, 0.6) - 40} t={t} />
        <rect x={420} y={680} width={700} height={240} fill="#7a5a3a" stroke={C.ink} strokeWidth={6} />
      </Cam>
      <Pop t={tt - 0.3} x={600} y={160} size={76} color={C.red} rot={-3}>UH-OH.</Pop>
      <Vignette strength={0.35} />
    </g>
  );
};

export const Night61: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSt = cue('Streets, parks');
  const tOver = cue('Overnight');
  const k = ease(prog(t, 0.6, tSt - 0.2));
  const xe = lerp(-200, 2200, k);
  return (
    <g>
      <Cam cx={lerp(800, 1100, prog(t, 0, D))} cy={560} z={1.08}>
        <NightSky t={t} id="n61" />
        <Street y={760} x0={-400} n={9} seed={11} lit />
        <Ground y={760} />
        <BarbedWire x0={-200} x1={2200} y={860} k={k} />
        {[0, 1, 2].map((i) => {
          const gx = xe - 60 - i * 260;
          return <Guard key={i} x={gx} y={feet(930 + (i % 2) * 20, 0.5)} s={0.5} face={0.7} walk={t * 1.2 + i} expr="flat" larm={[1.1, -0.6]} rarm={[-1.1, 0.6]} />;
        })}
        <g transform={`translate(${xe},860)`}>
          <circle r={70} fill="#5a4a3a" stroke={C.ink} strokeWidth={6} />
          <circle r={30} fill="#3a2a1a" stroke={C.ink} strokeWidth={4} />
        </g>
        <Floodlight x={300} y={760} t={t} />
        <Floodlight x={1500} y={760} t={t} />
        <Hero x={1650} y={feet(800, 0.42)} s={0.42} expr="scared" face={-0.7} look={[-1, 0.4]} brows="worried" larm={[0.3, 0.2]} rarm={[-2.0, 2.2]} />
      </Cam>
      <LocCard t={t - 0.3} place="BERLIN" date="13 AUGUST 1961" dur={tSt - 1} />
      {t > tSt && [['STREETS', 480], ['PARKS', 960], ['CEMETERIES', 1440]].map(([w, x], i) => {
        const tt = t - tSt - i * 0.9;
        if (tt < 0) return null;
        const cut = ease(prog(tt, 0.4, 0.8));
        return (
          <g key={w as string} transform={`translate(${x},220) scale(${backOut(prog(tt, 0, 0.35), 2)})`}>
            <rect x={-200} y={-90} width={400} height={180} rx={20} fill="#fbf6e8" stroke={C.ink} strokeWidth={6} />
            <Txt x={0} y={0} size={52} color={C.ink} outline={0} shadow={false}>{w as string}</Txt>
            <line x1={-220 * cut} y1={-110 * cut} x2={220 * cut} y2={110 * cut} stroke={C.red} strokeWidth={14} strokeLinecap="round" />
          </g>
        );
      })}
      {t > tOver && <Pop t={t - tOver} x={960} y={440} size={110} color={C.gold} rot={-3}>OVERNIGHT!</Pop>}
      <Vignette strength={0.5} />
    </g>
  );
};

export const Morning: React.FC<ShotProps> = ({t, D, cue}) => {
  const tGirl = cue('A girl');
  const tMan = cue('A man');
  const tMe = cue('I tried');
  const cam = camAt(t, [[0, 960, 540, 1.0], [tGirl, 760, 600, 1.45], [tMan, 1300, 600, 1.45], [tMe, 960, 600, 1.5]]);
  const step = prog(t, tMe + 0.3, tMe + 1.3);
  const glare = t > tMe + 1.6;
  const manX = lerp(1700, 1380, prog(t, tMan - 0.4, tMan + 1.2));
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>
        <DaySky id="mrn" top="#b8d8ee" bot="#f2e8d0" />
        <Street y={740} x0={-300} n={9} seed={12} />
        <Ground y={740} night={false} />
        <OldLady x={680} y={feet(790, 0.4)} s={0.4} face={-0.4} look={[-0.6, 0.6]} expr="frown" brows="worried" larm={[0.3, 0.2]} rarm={[-2.5 + 0.3 * Math.sin(t * 3), 0.3]} />
        <BarbedWire x0={-300} x1={2300} y={850} h={100} />
        <Girl x={560} y={feet(960, 0.34)} s={0.34} face={0.6} look={[0.6, -0.8]} expr="frown" brows="worried" larm={[0.3, 0.2]} rarm={[-2.5 + 0.3 * Math.sin(t * 3 + 1), 0.3]} />
        {t > tGirl + 0.5 && <Tear x={590} y={feet(960, 0.34) + 5} t={t} s={0.45} />}
        <Berliner seed={6} x={manX} y={feet(960, 0.5)} s={0.5} face={-0.7} look={[-0.6, -0.3]} walk={t < tMan + 1.2 ? t * 1.5 : undefined} expr={t > tMan + 1.2 ? 'frown' : 'flat'}
          brows={t > tMan + 1.2 ? 'worried' : undefined} larm={[0.3, 0.2]} rarm={[-0.2, -0.1]} hold={<Briefcase />} />
        <Guard x={1220} y={feet(780, 0.46)} s={0.46} face={glare ? -0.5 : 0} look={glare ? [-1, 0.4] : [0, 0]} expr="flat" brows={glare ? 'angry' : undefined} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        <Hero x={lerp(980, 1010, step)} y={feet(960, 0.55) - 30 * Math.sin(step * Math.PI) * (glare ? 0 : 1)} s={0.55} expr={glare ? 'scared' : step > 0 ? 'o' : 'worried'} face={0.6} look={[1, -0.4]}
          brows={glare ? 'worried' : undefined} legs={step > 0 && !glare ? [0.7 * Math.sin(step * Math.PI), 0] : glare ? [0.35, 0] : [0, 0]} larm={[0.9, -0.3]} rarm={[-0.9, 0.3]} />
        {glare && <Sweat x={1070} y={feet(960, 0.55) - 50} t={t} />}
      </Cam>
      {t < tGirl && <Pop t={t - 0.3} x={960} y={140} size={80} color="#fff">14 AUGUST 1961</Pop>}
      {glare && <Pop t={t - tMe - 1.6} x={1450} y={170} size={74} color={C.red} rot={3}>NOPE.</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Schumann: React.FC<ShotProps> = ({t, D, cue}) => {
  const tName = cue('A young border guard');
  const tPhoto = cue('A photographer');
  const tFamous = cue('It became');
  const tJ = tPhoto + 0.1;
  const scene = (tt: number) => {
    const run = prog(tt, tJ - 2.0, tJ - 0.55);
    const jump = prog(tt, tJ - 0.55, tJ + 0.55);
    const gx = tt < tJ - 2.0 ? 640 + 30 * Math.sin(tt * 2) : tt < tJ - 0.55 ? lerp(640, 860, run) : lerp(860, 1120, jump);
    const gy = feet(900, 0.5) - Math.sin(jump * Math.PI) * 230;
    const air = jump > 0 && jump < 1;
    return (
      <g>
        <DaySky id="sch" />
        <Street y={720} x0={-300} n={9} seed={14} />
        <Ground y={720} night={false} />
        <BarbedWire x0={-300} x1={2300} y={880} h={80} />
        <Guard x={gx} y={gy} s={0.5} face={0.9} look={[1, -0.3]} expr={air ? 'shock' : tt > tName + 2 ? 'worried' : 'flat'} brows={tt > tName + 2 && !air ? 'worried' : undefined}
          walk={run > 0 && run < 1 ? tt * 3 : tt < tJ - 2.0 ? tt * 0.8 : undefined} legs={air ? [0.9, -0.6] : undefined} larm={air ? [1.6, -0.4] : [0.4, 0.2]} rarm={air ? [-1.8, 0.4] : [-0.4, -0.2]} />
        <Berliner seed={9} x={1450} y={feet(960, 0.48)} s={0.48} face={-0.8} look={[-1, -0.3]} expr="o" larm={[0.3, 0.2]} rarm={[-1.9, 2.2]}
          hold={<g transform="translate(-20,-40)"><rect x={-40} y={-30} width={80} height={60} rx={8} fill="#2a2a30" stroke={C.ink} strokeWidth={4} /><circle cx={-6} cy={0} r={18} fill="#6a8ab8" stroke={C.ink} strokeWidth={4} /></g>} />
        <Hero x={1700} y={feet(980, 0.55)} s={0.55} expr={tt > tJ - 0.6 ? 'shock' : 'o'} face={-0.7} look={[-1, -0.3]} brows={tt > tJ - 0.6 ? 'up' : undefined} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </g>
    );
  };
  if (t < tJ) {
    const cam = camAt(t, [[0, 1100, 580, 1.15], [tName, 900, 600, 1.35], [tJ - 1.8, 1050, 560, 1.1]]);
    return (
      <g>
        <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>{scene(t)}</Cam>
        <LocCard t={t - 0.3} place="BERNAUER STRASSE" date="15 AUGUST 1961" dur={tName + 1} />
        <Txt x={460} y={150} size={52} font={HAND} outline={6} opacity={fadeWin(t, tName + 2.2, tJ - 2.2)}>Conrad Schumann, 19</Txt>
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tJ;
  const k = easeOut(prog(tt, 0.3, 1.0));
  const fz = lerp(1, 0.62, k);
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#2a2420" />
      {t > tFamous && [0, 1, 2, 3, 4, 5].map((i) => <Star key={i} x={260 + i * 280} y={140 + (i % 2) * 800} r={30 + 8 * Math.sin(t * 5 + i)} rot={t + i} />)}
      <g transform={`translate(960,${lerp(540, 590, k)}) scale(${fz}) rotate(${-3 * k}) translate(-960,-540)`}>
        <rect x={-40} y={-40} width={W + 80} height={H + 80} fill="#fbf6e8" stroke={C.ink} strokeWidth={8} />
        <defs><clipPath id="photo"><rect x={0} y={0} width={W} height={H} /></clipPath></defs>
        <g clipPath="url(#photo)">
          <Cam cx={1050} cy={560} z={1.1}>{scene(tJ)}</Cam>
          <rect x={0} y={0} width={W} height={H} fill="#8a6a3a" opacity={0.45} style={{mixBlendMode: 'multiply'}} />
        </g>
      </g>
      <Fill c="#fff" a={1 - prog(tt, 0, 0.35)} />
      {t > tFamous && <Pop t={t - tFamous} x={960} y={110} size={60} color={C.gold}>ONE OF THE MOST FAMOUS PHOTOS EVER</Pop>}
      <Pop t={tt - 0.1} x={1650} y={150} size={80} color="#fff" rot={6} hold={2}>CLICK!</Pop>
    </g>
  );
};

export const Concrete: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTwo = cue('Then two walls');
  const tTow = cue('Watchtowers');
  const tFl = cue('Floodlights');
  const tDog = cue('Dogs');
  const tKm = cue('One hundred');
  if (t < tKm - 0.2) {
    const rise = easeOut(prog(t, 0.4, 1.8));
    const rise2 = easeOut(prog(t, tTwo + 0.2, tTwo + 1.4));
    const cam = camAt(t, [[0, 1250, 560, 1.25], [tTwo, 960, 540, 1.0], [tTow, 820, 470, 1.25], [tFl, 1050, 470, 1.2], [tDog, 900, 640, 1.4]]);
    return (
      <g>
        <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>
          <NightSky t={t} id="con" />
          <Skyline y={720} t={t} gate={false} />
          <Ground y={720} />
          <rect x={360} y={720} width={1000} height={400} fill="#c8b48a" stroke={C.ink} strokeWidth={5} />
          {Array.from({length: 30}).map((_, i) => <circle key={i} cx={380 + ((i * 97) % 960)} cy={760 + ((i * 53) % 280)} r={4} fill="#a8946a" />)}
          {rise2 > 0 && <g transform={`translate(0,${(1 - rise2) * 300})`}><Wall x0={240} x1={360} y={900} h={260 * rise2 + 1} t={t} west={false} /></g>}
          {t > tTow - 0.3 && <g opacity={prog(t, tTow - 0.3, tTow)}><Watchtower x={720} y={830} s={0.9} t={t} /></g>}
          {t > tFl - 0.3 && <g opacity={prog(t, tFl - 0.3, tFl)}><Floodlight x={1050} y={830} t={t} h={560} a={2} /></g>}
          {t > tDog - 0.3 && <g opacity={prog(t, tDog - 0.3, tDog)}>
            <line x1={400} y1={960} x2={1320} y2={960} stroke="#555" strokeWidth={4} />
            <Dog x={lerp(600, 1000, (Math.sin(t * 0.9) + 1) / 2)} y={980} s={0.7} t={t} flip={Math.cos(t * 0.9) < 0} />
          </g>}
          {Array.from({length: 4}).map((_, i) => (
            <g key={i} transform={`translate(${480 + i * 240},${900 + (i % 2) * 70})`}>
              <path d="M-40,0 L40,-60 M-40,-60 L40,0 M0,10 L0,-70" stroke="#4a4a50" strokeWidth={10} strokeLinecap="round" />
            </g>
          ))}
          {rise < 1 && <g opacity={1 - rise}><BarbedWire x0={1360} x1={1500} y={1000} h={110} /></g>}
          <g transform={`translate(0,${(1 - rise) * 400})`}><Wall x0={1360} x1={1480} y={1000} h={rise * 360 + 1} t={t} /></g>
          <Hero x={1640} y={feet(1040, 0.5)} s={0.5} expr="worried" face={-0.7} look={[-1, -0.5]} brows="worried" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        </Cam>
        <Pop t={t - tTwo - 0.6} x={960} y={130} size={76} color={C.gold} hold={tTow - tTwo - 0.7}>THE DEATH STRIP</Pop>
        <Pop t={t - tTow} x={460} y={140} size={64} color="#fff" rot={-3} hold={tKm - tTow - 0.4}>WATCHTOWERS</Pop>
        <Pop t={t - tFl} x={960} y={250} size={64} color="#fff6a0" rot={2} hold={tKm - tFl - 0.4}>FLOODLIGHTS</Pop>
        <Pop t={t - tDog} x={1460} y={140} size={64} color="#ffb08a" rot={-2} hold={tKm - tDog - 0.4}>DOGS</Pop>
        <Vignette strength={0.5} />
      </g>
    );
  }
  const tt = t - tKm + 0.2;
  const draw = ease(prog(tt, 0.3, 3.4));
  const ring = 'M960,190 C1250,170 1450,330 1420,560 C1400,780 1200,900 960,880 C700,870 520,760 520,540 C520,320 680,210 960,190 Z';
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#c86a6a" />
      <Txt x={260} y={160} size={40} color="#fff" outline={6}>EAST GERMANY</Txt>
      <path d={ring} fill="#6ac06a" stroke="none" />
      <Txt x={960} y={500} size={64} color="#fff" outline={8}>WEST BERLIN</Txt>
      <path d={ring} fill="none" stroke="#e8e8ec" strokeWidth={22} strokeDasharray={`${draw * 3000} 3000`} strokeLinecap="round" />
      <path d={ring} fill="none" stroke={C.ink} strokeWidth={6} strokeDasharray={`${draw * 3000} 3000`} />
      {tt > 1.0 && <Pop t={tt - 1.0} x={960} y={640} size={110} color={C.gold}>155 KM</Pop>}
      <Hero x={1650} y={feet(980, 0.55)} s={0.55} expr="o" face={-0.6} look={[-1, -0.5]} larm={[0.3, 0.2]} rarm={[-2.0, 0.1]} />
      <Fill c="#fff" a={1 - prog(tt, 0, 0.3)} />
    </g>
  );
};

export const Jump: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWh = cue('Whoosh');
  const tEv = cue('Every time');
  if (t < tWh) {
    const blink = Math.sin(t * 14) > 0 ? 1 : 0;
    const hp = {x: 900, y: feet(950, 0.62), s: 0.62, larm: [0.3, 0.2] as [number, number], rarm: [-1.5, 0.6] as [number, number]};
    return (
      <g>
        <Cam cx={960} cy={560} z={lerp(1.3, 1.6, prog(t, 0, tWh))} shake={6} t={t}>
          <NightSky t={t} id="jmp" />
          <Skyline y={760} t={t} />
          <Ground y={760} />
          <Wall x0={-300} x1={2300} y={800} h={260} t={t} west={false} />
          <Hero {...hp} expr="shock" face={0.4} look={[0.6, 0.8]} brows="up" />
          <Glow id="jg" x={hp.x + 160} y={hp.y + 110} r={300} color="#ff2020" a={0.6 * blink} />
          <TimeMachine x={hp.x + 160} y={hp.y + 170} s={0.24} t={t} shake={1} screen="!!!" screenColor="#ff4a4a" glow={0} />
        </Cam>
        <Pop t={t - 0.2} x={960} y={140} size={100} color="#ff4a4a" rot={-3}>BEEP! BEEP!</Pop>
        <Fill c="#fff" a={prog(t, tWh - 0.3, tWh)} />
      </g>
    );
  }
  const tt = t - tWh;
  const yr = Math.round(lerp(1961, 1963, ease(prog(tt, 0.3, D - tWh - 0.4))));
  const icons = [0, 1, 2, 3, 4, 5];
  return (
    <g>
      <Vortex t={t} />
      {t > tEv && icons.map((i) => {
        const ph = ((t - tEv) * 0.45 + i / 6) % 1;
        const a = i * 1.05 + t * 0.4;
        const r = 80 + ph * 900;
        return (
          <g key={i} transform={`translate(${W / 2 + Math.cos(a) * r * 1.3},${H / 2 + Math.sin(a) * r * 0.7}) rotate(${-8 + i * 5}) scale(${0.3 + ph})`} opacity={Math.sin(ph * Math.PI)}>
            <rect x={-130} y={-110} width={260} height={230} fill="#fbf6e8" stroke={C.ink} strokeWidth={6} />
            <rect x={-110} y={-90} width={220} height={150} fill={['#3a4466', '#8ec8ee', '#3a4466', '#c8b48a', '#8ec8ee', '#3a4466'][i]} />
            {i % 2 === 0 ? <rect x={-110} y={0} width={220} height={60} fill="#9a9a9e" stroke={C.ink} strokeWidth={4} /> : <circle cx={0} cy={-20} r={40} fill="#ffd84d" stroke={C.ink} strokeWidth={4} />}
          </g>
        );
      })}
      <g transform={`translate(${W / 2 + 240 * Math.sin(t * 0.9)},${H / 2 + 100 * Math.cos(t * 1.3) - 60}) rotate(${t * 140})`}>
        <Doodle x={0} y={-150} s={0.55} expr="grin" face={0} larm={[2.4, 0.5]} rarm={[-2.4, -0.5]} legs={[0.5, -0.5]} />
      </g>
      <rect x={W / 2 - 260} y={60} width={520} height={130} rx={30} fill="rgba(5,3,16,0.75)" stroke={C.gold} strokeWidth={5} />
      <Txt x={W / 2} y={125} size={90} color={C.gold} outline={0} shadow={false}>{String(yr)}</Txt>
      <Fill c="#fff" a={1 - prog(tt, 0, 0.35) + prog(t, D - 0.3, D)} />
      <Vignette strength={0.5} />
    </g>
  );
};

// ================================================================== LIFE WITH THE WALL
export const Kennedy: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSaid = cue('Kennedy came');
  const tJoke = cue('Some people');
  const tKnew = cue('But Berliners');
  const tIch = tSaid + 1.6;
  const cam = camAt(t, [[0, 960, 520, 1.0], [tSaid, 900, 470, 1.35], [tJoke, 1250, 520, 1.3], [tKnew, 960, 540, 1.0]]);
  const wild = t > tKnew + 1.2;
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z} shake={wild ? 2 : 0} t={t}>
        <DaySky id="ken" />
        <g transform="translate(960,700)">
          <rect x={-420} y={-520} width={840} height={520} fill="#c89a6a" stroke={C.ink} strokeWidth={7} />
          {[-300, -100, 100, 300].map((x) => <rect key={x} x={x - 50} y={-440} width={100} height={180} rx={50} fill="#9a7048" stroke={C.ink} strokeWidth={5} />)}
          <rect x={-500} y={-560} width={1000} height={50} fill="#b88a5a" stroke={C.ink} strokeWidth={6} />
          <rect x={-480} y={-140} width={960} height={140} fill="#e8e0d0" stroke={C.ink} strokeWidth={6} />
          {[-360, -120, 120, 360].map((x) => <path key={x} d={`M${x - 70},-140 C${x - 40},-100 ${x + 40},-100 ${x + 70},-140`} fill="none" stroke={C.red} strokeWidth={10} />)}
        </g>
        <Speaker x={900} y={feet(580, 0.5)} s={0.5} face={0.2} look={[0, 0.2]} expr={t > tIch ? 'grin' : 'smile'} hair="#a0582a"
          larm={[0.4, 0.3]} rarm={t > tIch && t < tJoke ? [-2.2 + 0.2 * Math.sin(t * 4), 0.4] : [-0.6, 0.6]} />
        <rect x={830} y={480} width={140} height={110} fill="#7a5a3a" stroke={C.ink} strokeWidth={5} />
        {[870, 930].map((x) => <line key={x} x1={x} y1={480} x2={x - 20} y2={430} stroke={C.ink} strokeWidth={5} />)}
        <HeadRow y={830} t={t} n={13} seed={40} s={0.42} x0={-120} dx={180} cheer={t > tIch} />
        <Hero x={1380} y={870 - (wild ? Math.abs(Math.sin(t * 6)) * 14 : 0)} s={0.48} expr={t > tJoke && t < tKnew ? 'sly' : t > tIch ? 'grin' : 'smile'} face={-0.3} look={[-0.6, -0.6]}
          showLegs={false} larm={wild ? [2.6, 0.2] : [0.3, 0.2]} rarm={wild ? [-2.6 + 0.3 * Math.sin(t * 8), 0.3] : [-0.3, -0.2]} />
        <HeadRow y={950} t={t} n={12} seed={60} s={0.5} x0={-60} dx={190} cheer={t > tIch} />
        {t > tIch && t < tJoke + 0.5 && <Bubble x={560} y={250} w={560} h={130} text="Ich bin ein Berliner!" size={56} tail={[260, 110]} a={prog(t, tIch, tIch + 0.4) * (1 - prog(t, tJoke, tJoke + 0.4))} />}
        {t > tJoke + 0.4 && t < tKnew && (
          <g opacity={fadeWin(t, tJoke + 0.4, tKnew)}>
            <Bubble x={1280} y={300} w={460} h={300} text="" think tail={[60, 120]} a={1} />
            <Doughnut x={1280} y={290} s={0.95} />
            <Txt x={1280} y={420} size={34} color={C.ink} font={HAND} outline={0} shadow={false}>a "Berliner" = jelly doughnut</Txt>
          </g>
        )}
        {wild && <Confetti t={t - tKnew} n={40} />}
      </Cam>
      <LocCard t={t - 0.3} place="WEST BERLIN" date="26 JUNE 1963" dur={tSaid + 0.8} />
      <YearStamp t={t - 0.1} year="1963" hold={tSaid} />
      {t > tKnew && <Pop t={t - tKnew} x={1450} y={170} size={64} color="#7ae05a" rot={3}>THEY GOT IT!</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

const crawlPose = (t: number, i: number): Partial<DoodleProps> => {
  const sw = Math.sin(t * 6 + i);
  return {tilt: 1.25, legs: [0.9 + 0.4 * sw, 0.9 - 0.4 * sw], larm: [0.9 - 0.5 * sw, 0.2], rarm: [0.9 + 0.5 * sw, 0.2]};
};

export const Tunnel: React.FC<ShotProps> = ({t, D, cue}) => {
  const tIn = cue('In two nights');
  const tCalled = cue("It's still called");
  const n = Math.round(lerp(0, 57, ease(prog(t, tIn, tIn + 3.0))));
  return (
    <g>
      <Cam cx={lerp(900, 1050, prog(t, 0, D))} cy={620} z={1.45}>
        <DaySky id="tun" top="#2a3466" bot="#4a5a8a" />
        <Skyline y={300} t={t} gate={false} />
        <rect x={-400} y={300} width={2800} height={1000} fill="#8a5a34" stroke={C.ink} strokeWidth={6} />
        {Array.from({length: 60}).map((_, i) => <circle key={i} cx={-300 + ((i * 137) % 2600)} cy={340 + ((i * 71) % 700)} r={6 + (i % 3) * 4} fill="#7a4c2a" />)}
        <Wall x0={900} x1={1020} y={300} h={220} t={t} />
        <Txt x={600} y={520} size={50} color="#e0e0e8" outline={6}>EAST</Txt>
        <Txt x={1250} y={520} size={50} color={C.gold} outline={6}>WEST</Txt>
        <rect x={1780} y={300} width={60} height={420} fill="#5a3a20" stroke={C.ink} strokeWidth={5} />
        <rect x={-100} y={620} width={1940} height={170} rx={30} fill="#4a2e18" stroke={C.ink} strokeWidth={6} />
        {[0, 1, 2, 3, 4, 5, 6].map((k) => (
          <g key={k}>
            <line x1={k * 280} y1={620} x2={k * 280} y2={790} stroke="#a07a4a" strokeWidth={14} />
            <circle cx={k * 280 + 140} cy={650} r={12} fill="#ffe08a" />
            <Glow id={`tl${k}`} x={k * 280 + 140} y={660} r={120} color="#ffe08a" a={0.35} />
          </g>
        ))}
        <path d="M-100,640 C400,630 1300,650 1840,640" fill="none" stroke="#2a2a2a" strokeWidth={3} />
        {Array.from({length: 5}).map((_, i) => {
          const x = ((i * 380 + t * 90) % 1900) - 50;
          const s = 0.26;
          return <Berliner key={i} seed={i + 30} x={x} y={735} s={s} face={0.9} look={[1, 0]} expr="worried" {...crawlPose(t, i)} />;
        })}
        <Hero x={((2 * 380 + 190 + t * 90) % 1900) - 50} y={735} s={0.27} face={0.9} look={[1, 0]} expr="grin" {...crawlPose(t, 7)} />
      </Cam>
      <YearStamp t={t - 0.1} year="1964" />
      {t > tIn && <g>
        <rect x={680} y={60} width={560} height={130} rx={24} fill="rgba(10,10,20,0.82)" />
        <Txt x={960} y={125} size={78} color={C.gold} outline={0}>{`${n} PEOPLE`}</Txt>
      </g>}
      {t > tCalled && <g transform={`translate(1500,${880}) scale(${backOut(prog(t, tCalled, tCalled + 0.4), 2)})`}>
        <rect x={-240} y={-60} width={480} height={120} rx={12} fill="#fbf6e8" stroke={C.ink} strokeWidth={6} />
        <Txt x={0} y={4} size={60} color={C.red} outline={0} shadow={false}>TUNNEL 57</Txt>
      </g>}
      <Vignette strength={0.45} />
    </g>
  );
};

const Balloon: React.FC<{x: number; y: number; s?: number; t: number}> = ({x, y, s = 1, t}) => {
  const cols = ['#e05a3a', '#f2d06a', '#5a8ad8', '#e8e0d0', '#c84a8a', '#6ac06a'];
  return (
    <g transform={`translate(${x},${y}) scale(${s}) rotate(${3 * Math.sin(t * 1.3)})`}>
      {cols.map((c, i) => {
        const x0 = -200 + i * 66.7;
        return <path key={i} d={`M0,180 C${x0 * 1.4},120 ${x0 * 1.3},-220 ${x0 * 0.3},-260 L${(x0 + 66.7) * 0.3},-260 C${(x0 + 66.7) * 1.3},-220 ${(x0 + 66.7) * 1.4},120 0,180 Z`}
          fill={c} stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />;
      })}
      {[[-60, -120], [40, -40], [-20, 60], [80, -160]].map(([px, py], i) => <rect key={i} x={px} y={py} width={40} height={30} fill={cols[(i + 3) % 6]} stroke={C.ink} strokeWidth={3} />)}
      {[-40, 40].map((lx) => <line key={lx} x1={lx * 0.6} y1={170} x2={lx} y2={290} stroke={C.ink} strokeWidth={4} />)}
      <Glow id="bflame" x={0} y={250} r={80} color="#ffb03a" a={0.8 + 0.2 * Math.sin(t * 20)} />
      <rect x={-70} y={290} width={140} height={80} rx={8} fill="#a07a4a" stroke={C.ink} strokeWidth={5} />
      {Array.from({length: 8}).map((_, i) => (
        <g key={i}>
          <circle cx={-56 + (i % 4) * 37} cy={i < 4 ? 270 : 284} r={17} fill="#fff" stroke={C.ink} strokeWidth={4} />
          <circle cx={-56 + (i % 4) * 37 + 4} cy={(i < 4 ? 270 : 284) - 2} r={2.5} fill={C.ink} />
        </g>
      ))}
      <rect x={-70} y={290} width={140} height={80} rx={8} fill="#a07a4a" stroke={C.ink} strokeWidth={5} />
      {[0, 1, 2].map((k) => <line key={k} x1={-60} y1={310 + k * 20} x2={60} y2={310 + k * 20} stroke="#7a5a2a" strokeWidth={3} />)}
    </g>
  );
};

export const BalloonShot: React.FC<ShotProps> = ({t, D, cue}) => {
  const t8 = cue('Eight people');
  const t1 = cue('One homemade');
  const tLeg = cue('Total legends');
  const bx = lerp(300, 1500, ease(prog(t, 0.5, D)));
  const by = lerp(760, 380, easeOut(prog(t, 0.5, D * 0.7)));
  return (
    <g>
      <Cam cx={lerp(700, 1250, ease(prog(t, 0.5, D)))} cy={lerp(540, 520, prog(t, 0, D))} z={1.0}>
        <NightSky t={t} id="bal" />
        <circle cx={1700} cy={180} r={70} fill="#fff6d0" stroke={C.ink} strokeWidth={5} />
        <Skyline y={880} t={t} gate={false} tower={false} />
        <Ground y={880} />
        <Watchtower x={900} y={900} s={0.55} t={t} />
        <Floodlight x={500} y={900} t={t} h={420} />
        <Wall x0={-400} x1={2400} y={960} h={180} t={t} west={false} />
        <Balloon x={bx} y={by} s={0.75} t={t} />
        <Hero x={1950} y={feet(1040, 0.42)} s={0.42} expr="grin" face={-0.6} look={[-0.8, -1]} larm={[0.3, 0.2]} rarm={[-2.5 + 0.3 * Math.sin(t * 7), 0.3]} />
      </Cam>
      <YearStamp t={t - 0.1} year="1979" />
      <LocCard t={t - 0.5} place="CURTAINS + BED SHEETS" date="16 SEPTEMBER 1979" dur={t8 - 1.2} />
      <Pop t={t - t8} x={500} y={170} size={66} color="#fff" rot={-3} hold={tLeg - t8}>8 PEOPLE</Pop>
      <Pop t={t - t1} x={960} y={280} size={66} color={C.gold} rot={2} hold={tLeg - t1}>1 HOMEMADE BALLOON</Pop>
      {t > tLeg && <Burst t={t - tLeg} x={960} y={220} r={170} label="LEGENDS!" size={64} />}
      <Vignette strength={0.45} />
    </g>
  );
};

export const Memorial: React.FC<ShotProps> = ({t, D, cue}) => {
  const tAt = cue('At least');
  const tToday = cue('Today, their names');
  const place = prog(t, tAt + 1.0, tAt + 2.6);
  return (
    <g>
      <Cam cx={lerp(960, 900, ease(prog(t, 0, D)))} cy={lerp(540, 560, ease(prog(t, 0, D)))} z={lerp(1.0, 1.15, ease(prog(t, 0, D)))}>
        <DaySky id="mem" top="#3a3a5a" bot="#c8a8a0" />
        <Ground y={820} color="#6a6a72" />
        {Array.from({length: 22}).map((_, i) => <rect key={i} x={-200 + i * 110} y={260} width={20} height={560} fill="#8a4a2a" stroke={C.ink} strokeWidth={4} />)}
        <g transform="translate(960,500)">
          <rect x={-420} y={-220} width={840} height={440} fill="#7a4a30" stroke={C.ink} strokeWidth={7} />
          {Array.from({length: 40}).map((_, i) => {
            const cx = -370 + (i % 10) * 82;
            const cy = -175 + Math.floor(i / 10) * 100;
            return (
              <g key={i}>
                <rect x={cx - 30} y={cy - 38} width={60} height={76} fill="#e8e0d0" stroke={C.ink} strokeWidth={3} />
                <circle cx={cx} cy={cy - 10} r={14} fill="#b8b0a0" />
                <path d={`M${cx - 22},${cy + 34} C${cx - 20},${cy + 6} ${cx + 20},${cy + 6} ${cx + 22},${cy + 34} Z`} fill="#b8b0a0" />
              </g>
            );
          })}
        </g>
        {Array.from({length: 9}).map((_, i) => <Candle key={i} x={600 + i * 90} y={790 + (i % 2) * 14} s={0.9} t={t} seed={i} />)}
        {[640, 820, 1100, 1290].map((x, i) => <Flower key={x} x={x} y={770} s={0.7} color={['#ff6a8a', '#fff', '#ffd84d', '#b88aff'][i]} rot={-20 + i * 12} />)}
        {place > 0.95 && <Flower x={1180} y={760} s={0.8} color="#ff4a4a" rot={10} />}
        <Hero x={lerp(1500, 1300, ease(prog(t, 0.3, tAt + 1.0)))} y={feet(960, 0.55) + 20 * Math.sin(place * Math.PI)} s={0.55} expr="flat" face={-0.6} look={[-0.6, 0.7]} blink={0}
          walk={t > 0.3 && t < tAt + 1.0 ? t * 1.0 : undefined} larm={[0.3, 0.2]} rarm={place > 0 && place < 0.95 ? [-1.2 + 0.4 * place, 0.6] : [-0.3, -0.2]}
          hold={place < 0.95 ? <Flower x={0} y={-10} s={0.7} color="#ff4a4a" rot={-60 + place * 50} /> : undefined} />
      </Cam>
      <Txt x={960} y={120} size={50} color="#fff" outline={6} opacity={fadeWin(t, tAt + 0.4, D - 0.4, 0.6)}>AT LEAST 140 PEOPLE DIED AT THE BERLIN WALL</Txt>
      <Txt x={960} y={185} size={44} font={HAND} color="#f2e6c8" outline={5} opacity={fadeWin(t, tToday, D - 0.4, 0.6)}>Berlin Wall Memorial, Bernauer Strasse</Txt>
      <Vignette strength={0.55} />
      <Fill c="#000" a={prog(t, D - 0.5, D) * 0.6} />
    </g>
  );
};

export const Reagan: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSp = cue('U S President');
  const tEv = cue('Everyone thought');
  const tLife = cue('Not in our');
  const tTear = lerp(tSp, tEv, 0.55);
  const cam = camAt(t, [[0, 960, 500, 1.0], [tSp + 0.6, 860, 470, 1.3], [tEv, 960, 540, 1.0]]);
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>
        <DaySky id="rea" />
        <BrandenburgGate x={960} y={720} s={1.25} fill="#d8c8a0" detail />
        <Ground y={720} night={false} />
        <Wall x0={-400} x1={2400} y={780} h={220} t={t} west night={false} />
        <rect x={560} y={600} width={600} height={220} fill="#2a3a6a" stroke={C.ink} strokeWidth={6} />
        <Speaker x={860} y={feet(720, 0.5)} s={0.5} face={0.1} hair="#4a2e1a" expr={t > tTear ? 'flat' : 'smile'} brows={t > tTear ? 'angry' : undefined}
          larm={[0.3, 0.2]} rarm={t > tTear && t < tEv ? [-2.3, 0.5] : [-0.6, 0.6]} />
        {[700, 1020].map((x) => <rect key={x} x={x - 6} y={380} width={150} height={260} fill="#cfe6f2" opacity={0.35} stroke="#8aa8c8" strokeWidth={4} />)}
        <rect x={800} y={540} width={120} height={120} fill="#5a4a3a" stroke={C.ink} strokeWidth={5} />
        <HeadRow y={900} t={t} n={13} seed={80} s={0.45} x0={-120} dx={180} cheer={t > tTear && t < tEv} />
        <Hero x={1500} y={feet(980, 0.5)} s={0.5} expr={t > tEv ? 'sly' : 'o'} face={t > tEv ? 0 : -0.5} look={t > tEv ? [0, 0] : [-1, -0.6]} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </Cam>
      <LocCard t={t - 0.3} place="BRANDENBURG GATE" date="12 JUNE 1987" dur={tSp + 1.2} />
      <YearStamp t={t - 0.1} year="1987" hold={tSp + 1} />
      {t > tTear && t < tEv + 0.3 && <Bubble x={560} y={210} w={760} h={160} text={'"Mr. Gorbachev,\ntear down this wall!"'} size={54} tail={[180, 90]} a={prog(t, tTear, tTear + 0.4) * (1 - prog(t, tEv, tEv + 0.3))} />}
      {t > tEv && <Pop t={t - tEv} x={700} y={190} size={70} color="#ddd" rot={-2} hold={tLife - tEv}>"NEVER GONNA HAPPEN."</Pop>}
      {t > tLife && <Pop t={t - tLife} x={1300} y={300} size={56} font={HAND} outline={6}>*I know something you don't*</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

// ================================================================== 1989
export const Leipzig: React.FC<ShotProps> = ({t, D, cue}) => {
  const tHun = cue('Hungary');
  const tLei = cue('In Leipzig');
  const tShot = cue('Nobody fired');
  if (t < tHun) {
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#2a3466" />
        {Array.from({length: 10}).map((_, i) => {
          const ph = (t * 1.6 + i / 10) % 1;
          return <rect key={i} x={-200 + ph * 2400} y={100 + i * 90} width={300} height={8} fill="#fff" opacity={0.25} />;
        })}
        <g transform={`translate(960,480) scale(${backOut(prog(t, 0, 0.4), 2)}) rotate(${-4 + 2 * Math.sin(t * 6)})`}>
          <rect x={-330} y={-200} width={660} height={400} rx={30} fill="#fbf6e8" stroke={C.ink} strokeWidth={9} />
          <rect x={-330} y={-200} width={660} height={110} rx={30} fill={C.red} stroke={C.ink} strokeWidth={9} />
          <Txt x={0} y={-145} size={56} color="#fff" outline={0} shadow={false}>CALENDAR</Txt>
          <Txt x={0} y={60} size={190} color={C.ink} outline={0} shadow={false}>1989</Txt>
        </g>
        <Pop t={t - 1.4} x={960} y={850} size={84} color={C.gold}>⏩ FAST FORWARD ⏩</Pop>
      </g>
    );
  }
  if (t < tLei) {
    const tt = t - tHun;
    const cut = prog(tt, 0.6, 1.6);
    return (
      <g>
        <Cam cx={960} cy={560} z={lerp(1.0, 1.1, prog(tt, 0, 4))}>
          <DaySky id="hun" top="#9ad0f0" bot="#e8f4e0" />
          <rect x={-300} y={720} width={2600} height={600} fill="#7ab05a" stroke={C.ink} strokeWidth={6} />
          <BarbedWire x0={-200} x1={800} y={860} h={150} />
          <BarbedWire x0={1120} x1={2200} y={860} h={150} />
          {cut < 1 && <g opacity={1 - cut}><BarbedWire x0={800} x1={1120} y={860} h={150} /></g>}
          <Txt x={460} y={400} size={56} color="#fff" outline={7}>HUNGARY</Txt>
          <Txt x={1500} y={400} size={56} color={C.gold} outline={7}>AUSTRIA</Txt>
          {cut > 0 && Array.from({length: 7}).map((_, i) => {
            const x = lerp(300 - i * 120, 1700 - i * 120, prog(tt, 1.6 + i * 0.1, 4.6 + i * 0.1));
            return <Berliner key={i} seed={i + 12} x={x} y={feet(940 + (i % 2) * 30, 0.42)} s={0.42} face={0.85} walk={tt * 1.6 + i} expr="happy" larm={[0.3, 0.2]} rarm={[-0.2, -0.1]}
              hold={i % 2 ? <Suitcase /> : undefined} />;
          })}
          {cut > 0 && cut < 1 && <g transform="translate(960,700)"><path d="M-80,-40 L80,40 M-80,40 L80,-40" stroke="#c8203a" strokeWidth={22} strokeLinecap="round" /><circle r={18} fill="#666" stroke={C.ink} strokeWidth={4} /></g>}
        </Cam>
        {cut > 0.5 && <Burst t={tt - 1.1} x={1450} y={200} r={130} label="SNIP!" size={56} hold={1.4} />}
        <Pop t={tt - 0.2} x={700} y={140} size={60} color="#fff">SUMMER 1989</Pop>
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tLei;
  return (
    <g>
      <Cam cx={960} cy={lerp(520, 560, prog(tt, 0, 6))} z={lerp(1.05, 1.15, prog(tt, 0, 6))}>
        <NightSky t={t} id="lei" />
        <g transform="translate(1450,760)">
          <rect x={-200} y={-420} width={400} height={420} fill="#4a4a66" stroke={C.ink} strokeWidth={6} />
          <rect x={-70} y={-680} width={140} height={260} fill="#4a4a66" stroke={C.ink} strokeWidth={6} />
          <path d="M-80,-680 L0,-820 L80,-680 Z" fill="#3a6a5a" stroke={C.ink} strokeWidth={6} />
          {[-120, 0, 120].map((x) => <path key={x} d={`M${x - 36},-140 L${x - 36},-280 C${x - 36},-330 ${x + 36},-330 ${x + 36},-280 L${x + 36},-140 Z`} fill="#ffe08a" stroke={C.ink} strokeWidth={5} />)}
        </g>
        <Street y={760} x0={-500} n={5} seed={15} grey lit />
        <Ground y={760} />
        <g transform={`translate(700,${520 + 6 * Math.sin(t * 2)})`}>
          {[-300, 300].map((x) => <line key={x} x1={x} y1={0} x2={x} y2={260} stroke="#6b4428" strokeWidth={10} />)}
          <rect x={-330} y={-50} width={660} height={110} fill="#fbf6e8" stroke={C.ink} strokeWidth={6} />
          <Txt x={0} y={6} size={58} color={C.ink} font={HAND} outline={0} shadow={false}>WIR SIND DAS VOLK!</Txt>
        </g>
        <HeadRow y={800} t={t} n={14} seed={100} s={0.42} x0={-160} dx={170} cheer={false} candles grey />
        <Hero x={1180} y={860} s={0.46} expr="smile" face={0.2} look={[0, -0.6]} showLegs={false} larm={[0.3, 0.2]} rarm={[-1.2, 1.1]} hold={<Candle x={0} y={0} s={1.3} t={t} seed={3} />} />
        <HeadRow y={930} t={t} n={12} seed={130} s={0.5} x0={-60} dx={190} cheer={false} candles grey />
      </Cam>
      <LocCard t={tt - 0.2} place="LEIPZIG, EAST GERMANY" date="9 OCTOBER 1989" dur={tShot - tLei - 1} />
      {tt > 2.2 && <Pop t={tt - 2.2} x={1400} y={190} size={60} color={C.gold} hold={tShot - tLei - 2.4}>"WE ARE THE PEOPLE!"</Pop>}
      <Pop t={tt - 0.6} x={1400} y={300} size={52} color="#fff" hold={tShot - tLei - 0.8}>70,000 PEOPLE</Pop>
      {t > tShot && <Pop t={t - tShot} x={960} y={200} size={90} color="#ffe08a">PEACEFUL.</Pop>}
      <Vignette strength={0.5} />
    </g>
  );
};

const PressRoom: React.FC<{t: number; paper?: number; shuffle?: number; expr?: DoodleProps['expr']; brows?: DoodleProps['brows']; look?: [number, number]; clock?: number}> = ({
  t, shuffle = 0, expr = 'flat', brows, look = [0, 0.6], clock = 0,
}) => (
  <g>
    <rect x={-400} y={-300} width={2800} height={1700} fill="#b8c4cc" />
    {Array.from({length: 18}).map((_, i) => <rect key={i} x={-400 + i * 160} y={-300} width={70} height={1700} fill="#aebac2" />)}
    <Clock x={1500} y={220} r={64} h={18} m={53 + clock} />
    <rect x={300} y={140} width={500} height={130} rx={8} fill="#e8e0d0" stroke={C.ink} strokeWidth={5} />
    <Txt x={550} y={205} size={34} color={C.ink} outline={0} shadow={false}>PRESSEKONFERENZ</Txt>
    <Doodle cap={false} x={620} y={feet(620, 0.46)} s={0.46} body="#3a3e4a" face={0.4} expr="flat" front={<path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill="#5a4a3a" stroke={C.ink} strokeWidth={6} />} />
    <Doodle cap={false} x={1300} y={feet(620, 0.46)} s={0.46} body="#3a3e4a" face={-0.4} expr="flat" front={<path d="M-100,-30 C-100,-120 100,-130 100,-30 C60,-70 -60,-70 -100,-30 Z" fill="#3a3a3a" stroke={C.ink} strokeWidth={6} />} />
    <Official x={960} y={feet(620, 0.5)} s={0.5} face={0} look={look} expr={expr} brows={brows} larm={[0.6, 0.8]} rarm={[-0.9, 1.2]} hold={<Papers shuffle={shuffle} />} />
    <rect x={380} y={560} width={1160} height={60} fill="#7a5a3a" stroke={C.ink} strokeWidth={6} />
    <rect x={380} y={620} width={1160} height={260} fill="#8a6a4a" stroke={C.ink} strokeWidth={6} />
    {[820, 900, 1020, 1100].map((x, i) => <g key={x}><line x1={x} y1={560} x2={x + (i < 2 ? 30 : -30)} y2={470} stroke={C.ink} strokeWidth={6} /><rect x={x + (i < 2 ? 18 : -42)} y={448} width={24} height={34} rx={8} fill="#2a2a30" /></g>)}
    {void t}
  </g>
);

const Journalists: React.FC<{t: number; heroExpr?: DoodleProps['expr']; flash?: boolean}> = ({t, heroExpr = 'o', flash = true}) => (
  <g>
    {[180, 470, 760, 1250, 1530, 1800].map((x, i) => {
      const R = rng(i + 2);
      const fl = flash && Math.sin(t * (3 + R() * 2) + i * 2) > 0.97;
      return (
        <g key={x}>
          <Berliner seed={i * 2 + 1} x={x} y={920 + (i % 2) * 30} s={0.5} face={(960 - x) / 1200} look={[(960 - x) / 900, -1]} expr="flat" showLegs={false}
            larm={[0.3, 0.2]} rarm={i % 2 ? [-1.6, 1.4] : [-0.3, -0.2]}
            hold={i % 2 ? <g transform="translate(-10,-50)"><rect x={-40} y={-30} width={80} height={60} rx={8} fill="#2a2a30" stroke={C.ink} strokeWidth={4} /><circle cx={-6} cy={0} r={18} fill="#6a8ab8" stroke={C.ink} strokeWidth={4} /></g> : undefined} />
          {fl && <Glow id={`jf${i}`} x={x - 40} y={820} r={200} color="#fff" a={0.9} />}
        </g>
      );
    })}
    <Hero x={1030} y={930} s={0.5} expr={heroExpr} face={-0.1} look={[0, -1]} showLegs={false} larm={[0.3, 0.2]} rarm={[-1.4, 1.5]}
      hold={<g transform="translate(-10,-30)"><rect x={-30} y={-40} width={60} height={80} fill="#fbf6e8" stroke={C.ink} strokeWidth={4} /></g>} />
  </g>
);

export const Press: React.FC<ShotProps> = ({t, D, cue}) => {
  const tStand = cue('I was standing');
  const tRead = cue('He was reading');
  const tNob = cue('Nobody had told');
  const cam = camAt(t, [[0, 960, 560, 1.0], [tStand + 1.5, 960, 600, 1.05], [tRead, 960, 480, 1.6], [tNob, 960, 460, 1.9]]);
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>
        <PressRoom t={t} clock={t * 0.3} shuffle={t > tRead ? 0.2 * Math.sin(t * 3) : 0} expr={t > tNob ? 'worried' : 'flat'} brows={t > tNob ? 'worried' : undefined} />
        <Journalists t={t} />
      </Cam>
      <LocCard t={t - 0.3} place="EAST BERLIN · PRESS CONFERENCE" date="9 NOVEMBER 1989, 18:53" dur={tRead - 0.8} />
      <Txt x={1250} y={300} size={44} font={HAND} outline={6} opacity={fadeWin(t, tStand + 3.2, tRead - 0.2)}>Günter Schabowski, government spokesman</Txt>
      {t > tNob && <g>
        {[0, 1, 2].map((k) => {
          const ph = (t * 0.9 + k / 3) % 1;
          return <Txt key={k} x={880 + k * 80} y={260 - ph * 100} size={80} color={C.gold} outline={6} opacity={1 - ph}>?</Txt>;
        })}
      </g>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const When: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSh = cue('He shuffled');
  const tConf = cue('He looked confused');
  const tSaid = cue('And then he said');
  const tFroze = cue('The whole room');
  const tOops = cue('Oops');
  if (t < tOops) {
    const frozen = t > tFroze;
    const tf = frozen ? tFroze : t;
    const cam = camAt(tf, [[0, 960, 640, 1.05], [tSh, 960, 420, 1.9], [tSaid, 960, 400, 2.2]]);
    return (
      <g>
        <Cam cx={cam.cx} cy={cam.cy + (frozen ? 0 : 0)} z={frozen ? cam.z * (1 + 0.04 * prog(t, tFroze, tOops)) : cam.z}>
          <PressRoom t={tf} clock={tf * 0.3} shuffle={tf > tSh && tf < tConf ? Math.sin(tf * 14) : 0} expr={tf > tSaid ? 'flat' : tf > tConf ? 'worried' : 'o'} brows={tf > tConf && tf < tSaid ? 'worried' : undefined}
            look={tf > tConf && tf < tSaid ? [Math.sin(tf * 4), 0.2] : [0, 0.6]} />
          <Journalists t={tf} heroExpr={frozen ? 'shock' : 'o'} flash={!frozen} />
        </Cam>
        {t < tSh + 0.2 && <Bubble x={500} y={200} w={600} h={120} text='"When does this start?"' size={50} tail={[120, 90]} a={prog(t, 0.1, 0.5) * (1 - prog(t, tSh, tSh + 0.2))} />}
        {t > tSh && t < tConf + 0.2 && <Pop t={t - tSh} x={1450} y={180} size={64} font={HAND} outline={6} color="#fff">*shuffle shuffle*</Pop>}
        {t > tConf && t < tSaid && [0, 1, 2].map((k) => {
          const ph = (t * 0.9 + k / 3) % 1;
          return <Txt key={k} x={880 + k * 80} y={200 - ph * 100} size={80} color={C.gold} outline={6} opacity={1 - ph}>?</Txt>;
        })}
        {t > tSaid + 0.6 && <Bubble x={1340} y={210} w={760} h={190} text={'"As far as I know...\nimmediately. Without delay."'} size={50} tail={[-260, 110]} a={prog(t, tSaid + 0.6, tSaid + 1.0)} />}
        {t > tSaid + 1.0 && <Txt x={1340} y={360} size={36} font={HAND} outline={5} color={C.gold} opacity={prog(t, tSaid + 1.0, tSaid + 1.4)}>(German: "sofort, unverzüglich")</Txt>}
        {frozen && <g>
          <rect x={0} y={0} width={W} height={H} fill="#1a2a4a" opacity={0.25} />
          <Pop t={t - tFroze} x={500} y={500} size={70} color="#8ad8ff" rot={-4}>*FROZEN*</Pop>
        </g>}
        <Vignette strength={0.35} />
      </g>
    );
  }
  const tt = t - tOops;
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#ffd84d" />
      {Array.from({length: 16}).map((_, i) => (
        <path key={i} transform={`translate(960,560) rotate(${t * 15 + i * 22.5})`} d="M0,0 L1400,-140 L1400,140 Z" fill="#ffe680" />
      ))}
      <Cam cx={960} cy={560} z={lerp(1.6, 1.4, easeOut(prog(tt, 0, 0.3)))}>
        <Hero x={960} y={feet(1000, 0.75)} s={0.75} expr="grin" face={0} look={[0, 0]} brows="up" larm={[0.3, 0.2]} rarm={[-2.2, 2.1]} />
        <Sweat x={1060} y={feet(1000, 0.75) - 60} t={t} />
      </Cam>
      <Pop t={tt} x={960} y={160} size={170} color={C.red} rot={-4}>OOPS.</Pop>
    </g>
  );
};

export const TV: React.FC<ShotProps> = ({t, D, cue}) => {
  const tLook = cue('East Berliners');
  const tGo = cue('Can we just go');
  const tWent = cue('So they went');
  const tThou = cue('Thousands of them');
  if (t < tThou - 0.1) {
    const leave = prog(t, tWent + 0.2, tThou);
    const lookSide = t > tLook && t < tWent;
    const ppl: [React.FC<DoodleProps & {seed?: number}>, number, number][] = [[Berliner, 1, 700], [OldLady as React.FC<DoodleProps & {seed?: number}>, 0, 900], [Berliner, 3, 1100]];
    return (
      <g>
        <Cam cx={960} cy={560} z={lerp(1.1, 1.0, prog(t, 0, tWent))}>
          <rect x={-200} y={-200} width={2400} height={1500} fill="#d8b07a" />
          {Array.from({length: 24}).map((_, i) => <circle key={i} cx={-100 + (i % 8) * 300} cy={60 + Math.floor(i / 8) * 260} r={50} fill="#c89a62" />)}
          <rect x={-200} y={820} width={2400} height={500} fill="#8a5a3a" stroke={C.ink} strokeWidth={6} />
          <rect x={1650} y={260} width={240} height={560} fill="#9a6a3a" stroke={C.ink} strokeWidth={6} />
          <circle cx={1680} cy={560} r={12} fill={C.gold} stroke={C.ink} strokeWidth={3} />
          <g transform="translate(260,560)">
            <rect x={-30} y={180} width={20} height={80} fill="#4a3018" />
            <rect x={170} y={180} width={20} height={80} fill="#4a3018" />
            <rect x={-80} y={-150} width={320} height={330} rx={26} fill="#6a4a2a" stroke={C.ink} strokeWidth={7} />
            <rect x={-56} y={-126} width={230} height={200} rx={30} fill="#9ab8c8" stroke={C.ink} strokeWidth={6} />
            <g transform="translate(59,-20)">
              <Official x={0} y={-10} s={0.32} face={0} look={[0, 0.5]} expr="flat" showLegs={false} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
              <rect x={-110} y={50} width={220} height={40} fill="#c8203a" />
              <Txt x={0} y={70} size={24} color="#fff" outline={0} shadow={false}>BORDER OPEN?!</Txt>
            </g>
            {[200, 210].map((x, i) => <circle key={x} cx={x} cy={-60 + i * 60} r={16} fill="#d8c8a0" stroke={C.ink} strokeWidth={4} />)}
            <line x1={40} y1={-150} x2={-20} y2={-260} stroke={C.ink} strokeWidth={5} />
            <line x1={80} y1={-150} x2={140} y2={-260} stroke={C.ink} strokeWidth={5} />
          </g>
          <path d="M600,840 L600,640 C600,600 1300,600 1300,640 L1300,840 Z" fill="#5a7a5a" stroke={C.ink} strokeWidth={7} />
          {ppl.map(([P, seed, x], i) => {
            const lx = leave > 0 ? lerp(x, 1900 + i * 160, ease(prog(leave, i * 0.12, 0.7 + i * 0.12))) : x;
            const standing = leave > 0;
            const ly = standing ? feet(900, 0.46) : 650;
            return <P key={i} seed={seed} x={lx} y={ly} s={0.46} face={lookSide ? (i === 1 ? (Math.sin(t * 3) > 0 ? 0.9 : -0.9) : i === 0 ? 0.9 : -0.9) : standing ? 0.9 : -0.8}
              look={lookSide ? [i === 0 ? 1 : i === 2 ? -1 : Math.sin(t * 3), 0] : [-1, -0.2]} expr={t > tGo ? 'o' : lookSide ? 'o' : 'flat'} brows={t > tGo && !standing ? 'up' : undefined}
              walk={standing ? t * 1.8 + i : undefined} legs={standing ? undefined : [-1.2, -1.2]} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />;
          })}
          <rect x={560} y={760} width={780} height={90} rx={30} fill="#4a6a4a" stroke={C.ink} strokeWidth={7} />
        </Cam>
        {t > tGo && t < tWent + 0.4 && <Bubble x={960} y={220} w={560} h={130} text='"Wait. Can we just... go?"' size={50} tail={[0, 100]} a={prog(t, tGo, tGo + 0.3)} />}
        <Pop t={t - 0.3} x={1300} y={140} size={60} color="#fff" hold={tLook - 0.5}>ON TV, MINUTES LATER</Pop>
        <Vignette strength={0.35} />
      </g>
    );
  }
  const tt = t - tThou + 0.1;
  return (
    <g>
      <Cam cx={lerp(800, 1150, prog(tt, 0, D - tThou))} cy={560} z={1.05}>
        <NightSky t={t} id="tvn" />
        <Skyline y={760} t={t} gate={false} />
        <Ground y={760} />
        <Crowd t={t} y={860} n={18} speed={180} seed={150} x0={-600} span={3000} s={0.4} />
        <g transform="translate(1700,760)">
          <line x1={0} y1={0} x2={0} y2={-340} stroke="#5a5a5a" strokeWidth={12} />
          <rect x={-200} y={-400} width={400} height={100} rx={8} fill="#fff" stroke={C.ink} strokeWidth={6} />
          <Txt x={0} y={-350} size={40} color={C.ink} outline={0} shadow={false}>GRENZÜBERGANG →</Txt>
        </g>
        <Crowd t={t} y={980} n={10} speed={210} seed={170} x0={-600} span={3000} s={0.48} />
      </Cam>
      <Fill c="#fff" a={1 - prog(tt, 0, 0.25)} />
      <Pop t={tt - 0.3} x={960} y={150} size={90} color={C.gold}>THOUSANDS!</Pop>
      <Vignette strength={0.45} />
    </g>
  );
};

export const Bornholmer: React.FC<ShotProps> = ({t, D, cue}) => {
  const tNo = cue('The guards had no');
  const tCh = cue('The crowd chanted');
  const tFin = cue('Finally');
  const tOpen = cue('He opened');
  const lift = easeOut(prog(t, tOpen - 0.1, tOpen + 0.9));
  const flow = prog(t, tOpen + 0.6, D + 2);
  const cam = camAt(t, [[0, 900, 560, 1.0], [tNo, 600, 520, 1.45], [tCh, 960, 560, 1.0], [tFin + 1.5, 520, 500, 1.6], [tOpen - 0.3, 960, 540, 1.05]]);
  const chant = t > tCh && t < tOpen;
  const n = Math.round(lerp(12, 22, prog(t, 0, tCh)));
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z} shake={t > tOpen ? 3 : 0} t={t}>
        <NightSky t={t} id="bor" />
        <Skyline y={700} t={t} gate={false} />
        <g transform="translate(560,0)">
          <rect x={-560} y={360} width={900} height={60} fill="#5a5a62" stroke={C.ink} strokeWidth={6} />
          {[-520, -120, 280].map((x) => <rect key={x} x={x} y={420} width={40} height={300} fill="#6a6a72" stroke={C.ink} strokeWidth={5} />)}
          <g transform="translate(-110,300)">
            <rect x={-300} y={-50} width={600} height={100} rx={10} fill="#f2f2ea" stroke={C.ink} strokeWidth={5} />
            <Txt x={0} y={-16} size={32} color={C.ink} outline={0} shadow={false}>GRENZÜBERGANG</Txt>
            <Txt x={0} y={22} size={32} color={C.ink} outline={0} shadow={false}>BORNHOLMER STRASSE</Txt>
          </g>
        </g>
        <rect x={120} y={500} width={260} height={220} fill="#c8c8c0" stroke={C.ink} strokeWidth={6} />
        <rect x={150} y={530} width={200} height={90} fill="#f6d98a" stroke={C.ink} strokeWidth={5} />
        <Floodlight x={900} y={720} t={t} h={500} />
        <Ground y={720} />
        <Guard x={340} y={feet(800, 0.5)} s={0.5} face={0.6} look={[1, 0]} expr={t > tFin + 1.5 ? 'flat' : t > tNo ? 'worried' : 'flat'} brows={t > tNo && t < tFin + 1.5 ? 'worried' : undefined}
          larm={t > tNo && t < tFin ? [1.6, -0.9] : [0.3, 0.2]} rarm={t > tNo && t < tFin ? [-1.6, 0.9] : t > tOpen - 0.4 ? [-2.0, 0.2] : [-0.3, -0.2]} />
        <Guard x={540} y={feet(810, 0.46)} s={0.46} face={0.7} expr={t > tNo ? 'o' : 'flat'} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        {Array.from({length: n}).map((_, i) => {
          const R = rng(i + 50);
          const wait = 900 + (i % 8) * 130 + R() * 40;
          const x = flow > 0 ? wait - flow * 1700 * (0.7 + R() * 0.5) : wait;
          const y = 830 + Math.floor(i / 8) * 60 + (i % 2) * 14;
          const going = flow > 0.02;
          const s = 0.4 + Math.floor(i / 8) * 0.04;
          const j = chant ? Math.abs(Math.sin(t * 5 + i)) * 10 : 0;
          return <Berliner key={i} seed={i + 40} grey x={x} y={feet(y, s) - j} s={s} face={-0.85} look={[-1, -0.2]} walk={going ? t * 1.8 + i : undefined} expr={going ? 'laugh' : chant ? 'grin' : 'o'}
            larm={(going || chant) && i % 2 ? [2.6, 0.2] : [0.3, 0.2]} rarm={going || chant ? [-2.5 + 0.3 * Math.sin(t * 8 + i), 0.3] : [-0.3, -0.2]} />;
        })}
        <rect x={780} y={690} width={46} height={150} fill="#8a8a82" stroke={C.ink} strokeWidth={5} />
        <g transform={`translate(803,705) rotate(${-80 * lift})`}>
          <rect x={0} y={-16} width={760} height={32} fill="#fff" stroke={C.ink} strokeWidth={5} />
          {Array.from({length: 7}).map((_, k) => <rect key={k} x={20 + k * 110} y={-16} width={55} height={32} fill="#e8303a" />)}
        </g>
        <Hero x={flow > 0 ? 1160 - flow * 1500 : 1160} y={feet(990, 0.5)} s={0.5} expr={t > tOpen ? 'laugh' : chant ? 'grin' : 'o'} face={-0.6} look={[-1, -0.2]} walk={flow > 0 ? t * 1.8 : undefined}
          larm={chant || t > tOpen ? [2.6, 0.2] : [0.3, 0.2]} rarm={chant || t > tOpen ? [-2.6 + 0.3 * Math.sin(t * 8), 0.3] : [-0.3, -0.2]} />
      </Cam>
      {chant && <g>
        <Pop t={t - tCh - 0.3} x={1350} y={170} size={84} color={C.gold} rot={-3}>"TOR AUF!"</Pop>
        <Txt x={1350} y={260} size={44} font={HAND} outline={5} opacity={prog(t, tCh + 0.6, tCh + 1)}>= "Open the gate!"</Txt>
      </g>}
      {t > tFin && t < tOpen && <g transform={`translate(400,180) scale(${backOut(prog(t, tFin, tFin + 0.4), 2)})`}>
        <rect x={-180} y={-80} width={360} height={160} rx={20} fill="rgba(10,10,20,0.85)" stroke={C.gold} strokeWidth={5} />
        <Txt x={0} y={0} size={100} color={C.gold} outline={0}>23:30</Txt>
      </g>}
      <Txt x={560} y={870} size={44} font={HAND} outline={5} opacity={fadeWin(t, tFin + 2.0, tOpen - 0.2)}>Lt. Col. Harald Jäger</Txt>
      {t > tOpen + 0.5 && <Pop t={t - tOpen - 0.5} x={960} y={160} size={110} color="#7ae05a" rot={-2}>OPEN!</Pop>}
      <Vignette strength={0.5} />
    </g>
  );
};

export const Flood: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWalk = cue('Walking');
  const tRun = cue('Running');
  const tTrab = cue('Driving');
  const tStr = cue('Strangers');
  const tHug = cue('People who had');
  const gifts = [<Bouquet key="b" />, <Chocolate key="c" />, <Bottle key="o" />];
  return (
    <g>
      <Cam cx={lerp(900, 1100, prog(t, 0, D))} cy={560} z={t > tStr ? lerp(1.0, 1.25, ease(prog(t, tStr, tStr + 1))) : 1.0}>
        <NightSky t={t} id="fld" />
        <Skyline y={720} t={t} />
        <Ground y={720} />
        <Wall x0={-600} x1={300} y={760} h={260} t={t} />
        <Wall x0={700} x1={900} y={760} h={260} t={t} />
        <Crowd t={t} y={800} n={14} speed={t > tRun ? 230 : 130} seed={200} x0={-600} span={3200} s={0.36} />
        {t > tTrab - 0.5 && <Trabant x={lerp(-500, 2500, prog(t, tTrab - 0.5, tTrab + 5))} y={900} s={0.55} t={t} />}
        {t > tTrab + 1.2 && <Trabant x={lerp(-500, 2500, prog(t, tTrab + 1.2, tTrab + 6.6))} y={940} s={0.6} t={t} color="#e8c87a" />}
        {[1300, 1520, 1760].map((x, i) => (
          <Berliner key={i} seed={i + 60} x={x} y={feet(990, 0.5)} s={0.5} face={-0.8} look={[-1, -0.2]} expr="laugh" larm={[0.3, 0.2]}
            rarm={t > tStr + i * 0.5 ? [-1.6, 0.3] : [-0.3, -0.2]} hold={t > tStr + i * 0.5 ? gifts[i] : undefined} />
        ))}
        {t > tHug && [[1150, 61], [560, 63]].map(([x, s0], k) => (
          <g key={k}>
            <Berliner seed={s0} grey x={x - 46} y={feet(1000, 0.5)} s={0.5} face={0.9} expr="happy" blush tilt={0.16} larm={[0.3, 0.2]} rarm={[-1.9, 1.7]} />
            <Berliner seed={s0 + 7} x={x + 46} y={feet(1000, 0.5)} s={0.5} face={-0.9} expr="happy" blush tilt={-0.16} larm={[1.9, -1.7]} rarm={[-0.3, -0.2]} />
            <Tear x={x - 20} y={feet(1000, 0.5) + 10} t={t + k} s={0.5} />
          </g>
        ))}
        <Hero x={t < tHug ? lerp(200, 900, prog(t, 0, tHug)) : 860} y={feet(1010, 0.5)} s={0.5} expr="laugh" face={0.8} walk={t < tHug ? t * 2 : undefined}
          larm={t < tWalk ? [0.3, 0.2] : [2.6, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 8), 0.3]} />
        {t > tHug && Array.from({length: 6}).map((_, k) => {
          const ph = (t * 0.45 + k / 6) % 1;
          return <Heart key={k} x={400 + k * 220 + Math.sin(t * 2 + k) * 20} y={850 - ph * 500} s={1 + (k % 3) * 0.2} a={Math.sin(ph * Math.PI) * prog(t, tHug, tHug + 0.6)} />;
        })}
      </Cam>
      <Pop t={t - tWalk} x={500} y={150} size={70} color="#fff" rot={-3} hold={tStr - tWalk}>WALKING</Pop>
      <Pop t={t - tRun} x={960} y={230} size={70} color={C.gold} rot={2} hold={tStr - tRun}>RUNNING</Pop>
      {t > tTrab + 0.8 && t < tStr && <Burst t={t - tTrab - 0.8} x={1450} y={170} r={130} label="HONK HONK!" size={40} />}
      {t > tStr && t < tHug && <Pop t={t - tStr} x={960} y={150} size={64} color="#ffb0c8">FLOWERS · CHOCOLATE · BUBBLY</Pop>}
      <Vignette strength={0.45} />
    </g>
  );
};

export const Party: React.FC<ShotProps> = ({t, D, cue}) => {
  const tUp = cue('I climbed');
  const tHand = cue('Somebody handed');
  const tHere = cue("That's how");
  const climb = easeOut(prog(t, tUp, tUp + 1.4));
  const has = t > tHand + 0.6;
  const cam = camAt(t, [[0, 960, 500, 1.0], [tUp, 1100, 470, 1.35], [tHere, 1100, 400, 1.7]]);
  return (
    <g>
      <Cam cx={cam.cx} cy={cam.cy} z={cam.z}>
        <NightSky t={t} id="pty" />
        <Fireworks t={t} spots={[[300, 120, 0], [1600, 100, 0.6], [1000, 40, 1.2], [600, 200, 0.9]]} />
        <BrandenburgGate x={960} y={820} s={1.35} fill="#4a4a6a" detail />
        <Floodlight x={250} y={820} t={t} />
        <Ground y={820} />
        <Wall x0={-600} x1={2600} y={820} h={300} t={t} />
        {[-200, 0, 200, 400, 600, 800, 1450, 1650, 1850, 2050].map((x, i) => {
          const j = Math.abs(Math.sin(t * 6 + i)) * 20;
          return <Berliner key={i} seed={i + 210} x={x} y={feet(484 - j, 0.42)} s={0.42} face={Math.sin(t * 2 + i) * 0.6} expr="laugh"
            larm={[2.6 + 0.2 * Math.sin(t * 7 + i), 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 8 + i), 0.3]} legs={[0.3 * Math.sin(t * 9 + i), -0.3 * Math.sin(t * 9 + i)]} />;
        })}
        <Berliner seed={233} x={1240} y={feet(484, 0.42)} s={0.42} face={-0.7} expr="laugh" larm={[0.3, 0.2]} rarm={has ? [-0.3, -0.2] : t > tHand ? [-1.4, 0.3] : [-2.5, 0.3]}
          hold={t > tHand - 0.5 && !has ? <Hammer swing={0.4} /> : undefined} flip />
        <Hero x={lerp(1080, 1080, climb)} y={lerp(feet(900, 0.42), feet(484, 0.42), climb)} s={0.42} expr={has ? 'laugh' : climb > 0.9 ? 'happy' : 'grin'} face={0.4}
          larm={climb > 0 && climb < 1 ? [2.6, 0.2] : [0.6, 0.2]} rarm={has ? [-2.4 + 0.3 * Math.sin(t * 8), 0.3] : climb > 0 && climb < 1 ? [-2.6, -0.2] : [-1.2, 0.3]}
          legs={climb > 0 && climb < 1 ? [Math.sin(t * 14) * 0.5, -Math.sin(t * 14) * 0.5] : [0, 0]} hold={has ? <Hammer swing={0.5 + 0.5 * Math.sin(t * 8)} /> : undefined} />
        <HeadRow y={1010} t={t} n={14} seed={240} s={0.5} x0={-200} dx={170} />
      </Cam>
      <Pop t={t - 0.3} x={1400} y={140} size={70} color={C.gold} hold={tUp - 0.4}>MIDNIGHT</Pop>
      {t > tHere && <Pop t={t - tHere} x={960} y={150} size={70} color="#fff">...AND THAT'S WHERE WE STARTED!</Pop>}
      <Vignette strength={0.45} />
    </g>
  );
};

const Woodpecker: React.FC<{x: number; y: number; s?: number; t: number}> = ({x, y, s = 1, t}) => {
  const peck = Math.max(0, Math.sin(t * 16)) * 14;
  return (
    <g transform={`translate(${x - peck},${y}) scale(${s})`}>
      <path d="M20,-40 C80,-50 110,10 90,70 L60,120 L40,70 C10,40 0,0 20,-40 Z" fill="#2a2a30" stroke={C.ink} strokeWidth={5} />
      <circle cx={10} cy={-40} r={38} fill="#fff" stroke={C.ink} strokeWidth={5} />
      <path d="M-10,-78 C10,-90 40,-80 40,-56 C20,-64 0,-66 -10,-78 Z" fill={C.red} stroke={C.ink} strokeWidth={4} />
      <path d="M-24,-46 L-80,-40 L-24,-30 Z" fill="#e8b43a" stroke={C.ink} strokeWidth={4} />
      <circle cx={0} cy={-46} r={5} fill={C.ink} />
    </g>
  );
};

export const Woodpeckers: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWp = cue('Wall woodpeckers');
  const tTap = cue('Tap tap');
  const tPiece = cue('Everyone wanted');
  const hold = t > tPiece + 0.3;
  return (
    <g>
      <Cam cx={lerp(900, 1000, prog(t, 0, D))} cy={540} z={lerp(1.05, 1.15, prog(t, 0, D))}>
        <DaySky id="wdp" top="#c8d0d8" bot="#eef0f2" />
        <Ground y={860} night={false} />
        <Wall x0={-400} x1={2400} y={860} h={560} t={t} night={false} crack={0.7} />
        {[[260, 0], [700, 1], [1180, 2]].map(([hx, k]) => {
          const ph = (t * 2.4 + k * 0.33) % 1;
          const sw = ph < 0.5 ? 1 - ph * 2 : (ph - 0.5) * 2;
          return <Berliner key={k} seed={k + 90} x={hx} y={feet(990, 0.55)} s={0.55} face={-0.8} look={[-1, -0.3]} expr={k === 1 ? 'happy' : 'grin'} larm={[0.3, 0.2]}
            rarm={[-1.5 - 0.6 * sw, 0.4]} hold={<Hammer swing={sw} />} flip />;
        })}
        <Chips t={t} at={[[200, 700], [640, 700], [1120, 700]]} />
        {t > tWp - 0.3 && <Woodpecker x={1500} y={480} s={0.9} t={t} />}
        <Hero x={1650} y={feet(1000, 0.55)} s={0.55} expr={hold ? 'happy' : 'grin'} face={-0.5} look={hold ? [0, -0.4] : [-1, -0.3]} larm={[0.3, 0.2]}
          rarm={hold ? [-2.3, 0.5] : [-0.3, -0.2]} hold={hold ? <WallPiece x={0} y={-30} s={0.6} /> : undefined} />
        {hold && <Sparkle x={1580} y={feet(1000, 0.55) - 120} r={30} t={t} />}
      </Cam>
      {t > tWp && <g transform={`translate(960,170) scale(${backOut(prog(t, tWp, tWp + 0.4), 2)})`}>
        <rect x={-480} y={-90} width={960} height={180} rx={24} fill="#fbf6e8" stroke={C.ink} strokeWidth={7} />
        <Txt x={0} y={-30} size={64} color={C.red} outline={0} shadow={false}>MAUERSPECHTE</Txt>
        <Txt x={0} y={40} size={46} color={C.ink} font={HAND} outline={0} shadow={false}>= "wall woodpeckers"</Txt>
      </g>}
      {t > tTap && t < tPiece + 0.3 && ['TAP!', 'TAP!', 'TAP!'].map((w, i) => (
        <Pop key={i} t={t - tTap - i * 0.4} x={500 + i * 420} y={420 + (i % 2) * 60} size={70} color={C.gold} rot={-6 + i * 6}>{w}</Pop>
      ))}
      {!(t > tWp) && <Pop t={t - 0.3} x={960} y={150} size={64} color="#fff">NOVEMBER 1989</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Reunite: React.FC<ShotProps> = ({t, D, cue}) => {
  const tOld = cue('It was an old man');
  const tSil = cue("They didn't say");
  const meet = easeOut(prog(t, tOld - 0.5, tOld + 2.5));
  const hug = meet >= 1;
  const sway = Math.sin(t * 1.4) * 0.04;
  return (
    <g>
      <Cam cx={960} cy={lerp(540, 570, prog(t, 0, D))} z={lerp(1.0, 1.3, ease(prog(t, tOld, D)))}>
        <NightSky t={t} id="reu" warm={1} />
        <Glow id="sunr" x={960} y={700} r={900} color="#ffd9a0" a={0.7} />
        <Skyline y={720} t={t} warm />
        <Wall x0={-600} x1={760} y={780} h={300} t={t} night={false} />
        <Wall x0={1160} x1={2600} y={780} h={300} t={t} night={false} />
        <Ground y={780} warm />
        {[[300, 4, 27], [1600, 33, 8]].map(([x, a, b], k) => (
          <g key={k} opacity={0.9}>
            <Berliner seed={a} x={x - 40} y={feet(900, 0.42)} s={0.42} face={0.9} expr="happy" blush tilt={0.16} larm={[0.3, 0.2]} rarm={[-1.9, 1.7]} />
            <Berliner seed={b} x={x + 40} y={feet(900, 0.42)} s={0.42} face={-0.9} expr="happy" blush tilt={-0.16} larm={[1.9, -1.7]} rarm={[-0.3, -0.2]} />
          </g>
        ))}
        {!hug ? (
          <g>
            <OldMan x={lerp(600, 912, meet)} y={feet(960, 0.52)} s={0.52} face={0.9} look={[1, 0]} expr="o" walk={t * 0.9} larm={[1.2, -0.4]} rarm={[-1.2, 0.4]} />
            <OldLady x={lerp(1320, 1008, meet)} y={feet(960, 0.5)} s={0.5} face={-0.9} look={[-1, 0]} expr="o" walk={t * 0.9} larm={[1.2, -0.4]} rarm={[-1.2, 0.4]} />
          </g>
        ) : (
          <g>
            <OldMan x={912} y={feet(960, 0.52)} s={0.52} face={0.9} expr="happy" blush tilt={0.16 + sway} larm={[0.3, 0.2]} rarm={[-1.9, 1.7]} />
            <OldLady x={1008} y={feet(960, 0.5)} s={0.5} face={-0.9} expr="happy" blush tilt={-0.16 + sway} larm={[1.9, -1.7]} rarm={[-0.3, -0.2]} />
            <Tear x={940} y={feet(960, 0.52) + 10} t={t} s={0.5} />
            <Tear x={990} y={feet(960, 0.5) + 10} t={t + 0.5} s={0.5} />
          </g>
        )}
        {hug && Array.from({length: 5}).map((_, k) => {
          const ph = (t * 0.3 + k / 5) % 1;
          return <Heart key={k} x={780 + k * 90 + Math.sin(t * 2 + k) * 20} y={620 - ph * 360} s={0.8 + (k % 3) * 0.2} a={Math.sin(ph * Math.PI) * prog(t, tSil - 1, tSil)} />;
        })}
        <Hero x={1400} y={feet(1010, 0.48)} s={0.48} expr="smile" face={-0.6} look={[-1, -0.3]} blush larm={[0.3, 0.2]} rarm={[-2.2, 2.0]} />
        {t > tSil && <Tear x={1360} y={feet(1010, 0.48) - 10} t={t} s={0.5} />}
      </Cam>
      <Txt x={960} y={140} size={72} color="#fff" outline={8} opacity={fadeWin(t, tOld + 1.5, D - 0.6, 0.6)}>28 YEARS</Txt>
      <Vignette strength={0.35} />
    </g>
  );
};

// ================================================================== AFTER, HOME, LESSON, OUTRO
export const After: React.FC<ShotProps> = ({t, D, cue}) => {
  const tToday = cue('Today, pieces');
  const tLine = cue('And in Berlin');
  if (t < tToday - 0.1) {
    const unite = ease(prog(t, 2.2, 4.4));
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#f2e6c8" />
        {unite > 0.6 && <Fireworks t={t} spots={[[300, 220, 0], [1600, 200, 0.6], [1500, 700, 1.2], [360, 760, 0.3]]} r={200} />}
        <GermanyMap x={640} y={120} w={640} h={800} split={1} unite={unite} />
        <g transform={`translate(400,200) scale(${backOut(prog(t, 0.2, 0.6), 2)}) rotate(-4)`}>
          <rect x={-230} y={-130} width={460} height={260} rx={24} fill="#fbf6e8" stroke={C.ink} strokeWidth={8} />
          <rect x={-230} y={-130} width={460} height={80} rx={24} fill={C.red} stroke={C.ink} strokeWidth={8} />
          <Txt x={0} y={-90} size={40} color="#fff" outline={0} shadow={false}>3 OCTOBER</Txt>
          <Txt x={0} y={30} size={110} color={C.ink} outline={0} shadow={false}>1990</Txt>
        </g>
        {unite > 0.9 && <Pop t={t - 4.4} x={1500} y={480} size={70} color={C.red} rot={4}>ONE COUNTRY</Pop>}
        <Hero x={1560} y={feet(960, 0.5)} s={0.5} expr={unite > 0.5 ? 'laugh' : 'smile'} face={-0.6} look={[-1, -0.4]} larm={[0.3, 0.2]} rarm={unite > 0.5 ? [-2.6 + 0.3 * Math.sin(t * 8), 0.3] : [-0.3, -0.2]} />
        <Vignette strength={0.25} />
      </g>
    );
  }
  if (t < tLine - 0.1) {
    const tt = t - tToday + 0.1;
    const spots: [number, number][] = [[-250, -100], [-120, 150], [60, -190], [200, 80], [-30, 20], [300, -60]];
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#1a2a5a" />
        <Glow id="glob" x={960} y={540} r={500} color="#5aa0e0" a={0.4} />
        <g transform={`translate(960,540) rotate(${tt * 8})`}>
          <circle r={360} fill="#3a7ad8" stroke={C.ink} strokeWidth={8} />
          <path d="M-280,-120 C-200,-200 -100,-150 -120,-60 C-140,20 -240,40 -280,-20 Z" fill="#6ac06a" stroke={C.ink} strokeWidth={5} />
          <path d="M20,-260 C120,-280 220,-180 160,-90 C100,-20 40,-120 20,-260 Z" fill="#6ac06a" stroke={C.ink} strokeWidth={5} />
          <path d="M-60,60 C40,30 140,100 100,220 C60,300 -60,260 -60,60 Z" fill="#6ac06a" stroke={C.ink} strokeWidth={5} />
          <path d="M180,60 C260,40 320,120 280,180 C240,200 180,140 180,60 Z" fill="#6ac06a" stroke={C.ink} strokeWidth={5} />
        </g>
        {spots.map(([x, y], i) => {
          const k = backOut(prog(tt, 0.3 + i * 0.35, 0.65 + i * 0.35), 2);
          return (
            <g key={i} transform={`translate(${960 + x},${540 + y}) scale(${Math.max(0.001, k) * 0.7})`}>
              <rect x={-36} y={-100} width={72} height={140} fill="#bdbdc0" stroke={C.ink} strokeWidth={6} />
              <path d={`M-30,-60 C-10,-90 20,-40 30,-70`} fill="none" stroke={GRAF[i]} strokeWidth={10} strokeLinecap="round" />
              <ellipse cx={0} cy={44} rx={50} ry={12} fill="rgba(0,0,0,0.3)" />
            </g>
          );
        })}
        <Pop t={tt - 0.2} x={960} y={110} size={64} color={C.gold}>PIECES OF THE WALL, ALL OVER THE WORLD</Pop>
        <Fill c="#fff" a={1 - prog(tt, 0, 0.3)} />
      </g>
    );
  }
  const tt = t - tLine + 0.1;
  const hx = lerp(500, 1400, prog(tt, 0.5, 4.5));
  return (
    <g>
      <Cam cx={960} cy={560} z={1.05}>
        <DaySky id="aft" />
        <Street y={640} x0={-300} n={9} seed={20} />
        <rect x={-300} y={640} width={2600} height={600} fill="#a8a8b0" stroke={C.ink} strokeWidth={6} />
        {Array.from({length: 26}).map((_, i) => (
          <g key={i}>
            <rect x={900 + (i % 2) * 52} y={640 + Math.floor(i / 2) * 36} width={50} height={34} rx={6} fill="#7a7a84" stroke={C.ink} strokeWidth={3} />
          </g>
        ))}
        <rect x={860} y={830} width={200} height={50} rx={6} fill="#6a6a52" stroke={C.ink} strokeWidth={4} />
        <Txt x={960} y={846} size={18} color="#e8e0b0" outline={0} shadow={false}>BERLINER MAUER</Txt>
        <Txt x={960} y={868} size={18} color="#e8e0b0" outline={0} shadow={false}>1961–1989</Txt>
        <Berliner seed={5} x={lerp(1700, 200, prog(tt, 0, 4.4))} y={feet(800, 0.4)} s={0.4} face={-0.85} walk={tt * 1.6} expr="smile" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        <Girl x={lerp(1800, 300, prog(tt, 0.4, 4.6))} y={feet(800, 0.3)} s={0.3} face={-0.85} walk={tt * 2} expr="happy" larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        <Hero x={hx} y={feet(960, 0.55)} s={0.55} expr="smile" face={0.8} look={[0.6, 0.6]} walk={tt * 1.4} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </Cam>
      <Pop t={tt - 0.4} x={960} y={150} size={60} color="#fff">WHERE THE WALL USED TO BE</Pop>
      <Fill c="#fff" a={1 - prog(tt, 0, 0.3)} />
      <Vignette strength={0.25} />
    </g>
  );
};

export const Home: React.FC<ShotProps> = ({t, D, cue}) => {
  const tPiece = cue('A little piece');
  const tOwn = cue('My own piece');
  const land = easeOut(prog(t, 0.6, 1.0));
  const show = t > tPiece - 0.2;
  return (
    <g>
      <Cam cx={show ? lerp(960, 1000, ease(prog(t, tPiece - 0.2, tPiece + 0.8))) : 960} cy={show ? lerp(560, 470, ease(prog(t, tPiece - 0.2, tPiece + 0.8))) : 560}
        z={show ? lerp(1.1, 1.9, ease(prog(t, tPiece - 0.2, tPiece + 0.8))) : 1.1}>
        <Bedroom t={t} />
        <Hero x={900} y={lerp(-300, feet(900, 0.62), land)} s={0.62} expr={show ? 'happy' : t > 1.6 ? 'o' : 'shock'} face={0.2} look={show ? [0.6, -0.4] : [0, 0]}
          squash={t > 1.0 ? -0.15 * Math.exp(-(t - 1.0) * 6) : 0} larm={[0.3, 0.2]} rarm={show ? [-2.3, 0.6] : t > 2.4 ? [-0.6, 1.4] : [-0.3, -0.2]}
          hold={show ? <WallPiece x={0} y={-30} s={0.7} /> : undefined} />
        <TimeMachine x={1250} y={900} s={0.42} t={t} screen="HOME" />
        {show && [0, 1, 2].map((k) => <Sparkle key={k} x={1000 + k * 60} y={250 + (k % 2) * 60} r={24} t={t + k} />)}
      </Cam>
      <Fill c="#fff" a={1 - prog(t, 0, 0.35)} />
      {t > 2.4 && t < tPiece && <Pop t={t - 2.4} x={960} y={150} size={70} font={HAND} outline={6}>*something heavy in my pocket...*</Pop>}
      {t > tOwn && <Pop t={t - tOwn} x={960} y={150} size={84} color={C.gold}>MY OWN PIECE OF HISTORY</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Lesson: React.FC<ShotProps> = ({t, D, cue}) => {
  const t28 = cue('This one lasted');
  const tOrd = cue('But it was brought');
  const tHam = cue('And a few');
  const fall = prog(t, tOrd + 3.0, tOrd + 4.4);
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#22284a" />
      <Glow id="lglow" x={960} y={600} r={800} color="#ffd86a" a={0.25 + 0.3 * prog(t, tOrd, tOrd + 2)} />
      <Ground y={820} />
      {Array.from({length: 14}).map((_, i) => {
        const x = 120 + i * 120;
        const dir = i % 2 ? 1 : -1;
        const f = clamp(fall * 1.6 - (i % 5) * 0.12);
        return (
          <g key={i} transform={`rotate(${dir * 80 * easeIn(f)} ${x + (dir > 0 ? 120 : 0)} 820)`}>
            <rect x={x} y={420} width={120} height={400} fill={i % 2 ? '#9a9a9e' : '#929296'} stroke={C.ink} strokeWidth={5} />
            <rect x={x} y={380} width={120} height={56} fill="#b4b4b8" stroke={C.ink} strokeWidth={5} />
          </g>
        );
      })}
      {t > t28 && t < tOrd + 0.3 && <g opacity={fadeWin(t, t28, tOrd + 0.3)}>
        <rect x={360} y={200} width={1200} height={20} rx={10} fill="#fff" opacity={0.3} />
        <rect x={360} y={200} width={1200 * ease(prog(t, t28, t28 + 1.6))} height={20} rx={10} fill={C.gold} />
        <Txt x={360} y={150} size={50} outline={6}>1961</Txt>
        <Txt x={1560} y={150} size={50} outline={6}>1989</Txt>
        <Txt x={960} y={290} size={80} color={C.gold} outline={8}>28 YEARS</Txt>
      </g>}
      {t > tOrd && <HeadRow y={960} t={t} n={13} seed={300} s={0.5} x0={-40} dx={170} cheer={fall > 0.3} candles={fall < 0.3} />}
      {t > tOrd + 1.2 && fall < 0.2 && <Pop t={t - tOrd - 1.2} x={960} y={200} size={64} color="#ffe08a">CANDLES · CHANTS · COURAGE</Pop>}
      {fall > 0.3 && <Pop t={t - tOrd - 3.4} x={960} y={200} size={84} color="#fff">ORDINARY PEOPLE DID THIS</Pop>}
      {t > tHam && (
        <g>
          <Hero x={lerp(2200, 1620, easeOut(prog(t, tHam, tHam + 0.5)))} y={feet(1000, 0.6)} s={0.6} expr="sly" face={-0.3} larm={[0.3, 0.2]}
            rarm={[-2.4 + 0.3 * Math.sin(t * 8), 0.3]} hold={<Hammer swing={0.5 + 0.5 * Math.sin(t * 8)} />} />
          <Pop t={t - tHam - 0.4} x={1500} y={360} size={56} font={HAND} outline={6}>*and a few hammers*</Pop>
        </g>
      )}
      <Vignette strength={0.5} />
    </g>
  );
};

const Spiral: React.FC<{t: number}> = ({t}) => {
  let d = 'M0,0';
  for (let i = 0; i < 900; i++) {
    const a = i * 0.035;
    const r = 6 + a * 52;
    d += ` L${Math.cos(a) * r},${Math.sin(a) * r}`;
  }
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#b82126" />
      <path transform={`translate(${W / 2},${H / 2}) rotate(${t * 14})`} d={d} fill="none" stroke="#cc2e30" strokeWidth={60} />
    </g>
  );
};

export const Outro: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBeep = cue('Because my time machine');
  const alarm = t > tBeep + 0.6;
  const blink = alarm && Math.sin(t * 14) > 0 ? 1 : 0;
  const hp = {x: 960, y: lerp(1400, 470, easeOut(prog(t, 0, 0.5))), s: 0.85, larm: [0.3, 0.2] as [number, number], rarm: alarm ? [-1.5, 0.6] as [number, number] : [-2.6 + 0.3 * Math.sin(t * 7), 0.4] as [number, number]};
  return (
    <g>
      <Spiral t={t} />
      <Hero {...hp} expr={alarm ? 'shock' : 'grin'} face={0} brows={alarm ? 'up' : undefined} look={alarm ? [0.6, 0.8] : [0, 0]} />
      {alarm && <g>
        <Glow id="ob" x={hp.x + 200} y={hp.y + 260} r={300} color="#ff2020" a={0.7 * blink} />
        <TimeMachine x={hp.x + 210} y={hp.y + 340} s={0.36} t={t} shake={1} screen="???" screenColor="#ff4a4a" />
      </g>}
      <Pop t={t - 0.3} x={960} y={110} size={78}>SUBSCRIBE TO HISTORY WORLD</Pop>
      {alarm && <Pop t={t - tBeep - 0.6} x={480} y={500} size={80} color={C.gold} rot={-4}>BEEP! BEEP!</Pop>}
    </g>
  );
};

export const EndCard: React.FC<ShotProps> = ({t, D}) => {
  const tb = t - 1.0;
  const kk = tb > 0 ? backOut(clamp(tb / 0.4), 2) * (1 + 0.05 * Math.sin(t * 6)) : 0;
  const u = ease(prog(tb, 1.0, 1.6));
  return (
    <g>
      <Spiral t={t} />
      <Confetti t={t} n={60} />
      <Hero x={420} y={lerp(1400, 470, easeOut(prog(t, 0, 0.6)))} s={0.85} expr="grin" face={0.4} larm={[0.3, 0.2]} rarm={[-2.4, 0.5]} hold={<WallPiece x={0} y={-30} s={0.8} />} />
      <Pop t={t - 0.3} x={1150} y={260} size={150} color={C.gold}>HISTORY WORLD</Pop>
      {tb > 0 && (
        <g>
          <g transform={`translate(1150,540) scale(${Math.max(kk, 0.001)})`}>
            <rect x={-300} y={-80} width={600} height={160} rx={40} fill="#ff2a2a" stroke={C.ink} strokeWidth={8} />
            <polygon points="-220,-40 -220,40 -160,0" fill="#fff" />
            <Txt x={40} y={0} size={80} outline={6}>SUBSCRIBE</Txt>
          </g>
          <g transform={`translate(${lerp(1500, 1180, u)},${lerp(950, 560, u)})`}>
            <polygon points="0,0 0,60 16,46 30,74 40,68 26,42 46,40" fill="#fff" stroke={C.ink} strokeWidth={4} />
          </g>
          {tb > 1.6 && <Pop t={tb - 1.6} x={1150} y={690} size={50} color="#6aff8a">SUBSCRIBED!</Pop>}
        </g>
      )}
      <Txt x={1150} y={830} size={52} font={HAND} outline={5} opacity={ease(prog(t, 1.8, 2.4))}>Next time: where will the time machine take me?</Txt>
      <rect x={0} y={0} width={W} height={H} fill="#000" opacity={prog(t, D - 0.8, D)} />
    </g>
  );
};

export const SHOTS: Record<string, React.FC<ShotProps>> = {
  hook: Hook, title: Title, glitch: Glitch, map: MapShot, escape: Escape, night61: Night61, morning: Morning, schumann: Schumann, concrete: Concrete,
  jump: Jump, kennedy: Kennedy, tunnel: Tunnel, balloon: BalloonShot, memorial: Memorial, reagan: Reagan, leipzig: Leipzig, press: Press, when: When,
  tv: TV, bornholmer: Bornholmer, flood: Flood, party: Party, woodpeckers: Woodpeckers, reunite: Reunite, after: After, home: Home, lesson: Lesson,
  outro: Outro, endcard: EndCard,
};
void [CapShape, Dog, Watchtower];
