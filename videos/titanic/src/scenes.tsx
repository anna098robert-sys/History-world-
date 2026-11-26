// Every shot of the film. A shot gets local time t (s), its duration D and cue(text) = start time of the
// narration sentence containing `text` (cue(text, frac) = part-way through that sentence).
import React from 'react';
import {C, W, H, blinkAt, clamp, ease, easeIn, easeOut, lerp, prog, rng, backOut} from './lib';
import {Doodle, DoodleProps, Person, CapShape, LifeJacket} from './Hero';
import {Burst, Caption, Cam, Confetti, DizzyStars, FactCard, Glow, HAND, Pop, Sparkle, SpeedLines, Star, Sweat, TITLE, Txt, Vignette} from './fx';
import {Blanket, Iceberg, Lifeboat, ShipBell, Ship, Stars, TimeMachine, Waves} from './props';
import {Bedroom, Bridge, Corridor, CrowsNest, Deck, Dining, DiningTable, FleaMarket, GrandStaircase, LifeboatSea, OpenSea, PompeiiScreen, Sky, Vortex} from './bg';

export type Cue = (text: string, frac?: number) => number;
export type ShotProps = {t: number; D: number; cue: Cue};

const feet = (yFeet: number, s: number) => yFeet - 456 * s;

/** the hero, with natural blinking */
const Hero: React.FC<DoodleProps> = (p) => <Doodle blink={blinkAt(p.walk ?? 0)} {...p} />;

const runArms = (t: number, sp = 3): Partial<DoodleProps> => {
  const sw = Math.sin(t * sp * 2 * Math.PI);
  return {walk: t * sp, larm: [0.9 * sw, 0.9], rarm: [0.9 * sw, -0.9]};
};

const Bubble: React.FC<{x: number; y: number; w: number; h: number; text: string; size?: number; tail?: [number, number]; a?: number; think?: boolean}> = ({
  x, y, w, h, text, size = 46, tail = [-40, 60], a = 1, think,
}) => {
  if (a <= 0) return null;
  const lines = text.split('\n');
  return (
    <g opacity={a}>
      {think ? (
        <g>
          <ellipse cx={x} cy={y} rx={w / 2} ry={h / 2} fill="#fff" stroke={C.ink} strokeWidth={6} />
          {[18, 12, 8].map((r, i) => (
            <circle key={i} cx={x + tail[0] * ((i + 1) / 3.5) * 1.6} cy={y + h / 2 * 0.8 + tail[1] * ((i + 1) / 3.5)} r={r} fill="#fff" stroke={C.ink} strokeWidth={5} />
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
        <Txt key={i} x={x} y={y + (i - (lines.length - 1) / 2) * size * 1.1} size={size} color={C.ink} font={HAND} outline={0} shadow={false}>{l}</Txt>
      ))}
    </g>
  );
};

const fadeWin = (t: number, a: number, b: number, f = 0.2) => clamp(Math.min((t - a) / f, (b - t) / f));

const PriceTag: React.FC<{x: number; y: number; text: string; rot?: number; s?: number}> = ({x, y, text, rot = -8, s = 1}) => (
  <g transform={`translate(${x},${y}) rotate(${rot}) scale(${s})`}>
    <line x1={-110} y1={-20} x2={-150} y2={-60} stroke={C.ink} strokeWidth={4} />
    <polygon points="-110,-40 110,-40 140,0 110,40 -110,40" fill="#fff6c8" stroke={C.ink} strokeWidth={6} strokeLinejoin="round" />
    <circle cx={-90} cy={0} r={8} fill={C.ink} />
    <Txt x={10} y={0} size={46} color={C.red} outline={0} shadow={false}>{text}</Txt>
  </g>
);

// =================================================================== HOOK + TITLE
export const Hook: React.FC<ShotProps> = ({t, D, cue}) => {
  const t2 = cue('Ten seconds');
  const t3 = cue('Worst purchase');
  if (t < t2) {
    // close-up: hero grins holding the $5 machine at the flea market; it starts shaking
    const k = easeOut(prog(t, 0, 0.8));
    const shake = prog(t, t2 - 1.2, t2);
    return (
      <g>
        <Cam cx={900} cy={lerp(470, 520, k)} z={lerp(2.2, 1.35, k)} shake={10 * shake} t={t}>
          <FleaMarket t={t} />
          <Hero x={760} y={feet(900, 0.7)} s={0.7} expr={shake > 0.3 ? 'shock' : 'grin'} face={0.6} look={[1, 0.6]}
            larm={[0.3, 0.2]} rarm={[-1.5, 0.3]} walk={t} />
          <TimeMachine x={1010} y={790} s={0.55} t={t} screen={shake > 0.4 ? '1912' : '$5'} glow={shake} shake={shake} />
          <PriceTag x={1180} y={600} text="$5" />
        </Cam>
        {t > 0.2 && <Pop t={t - 0.2} x={960} y={140} size={92} color={C.gold}>$5 TIME MACHINE!</Pop>}
        <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={prog(t, t2 - 0.3, t2)} />
        <Vignette strength={0.4} />
      </g>
    );
  }
  if (t < t3) {
    const tt = t - t2;
    const wide = tt > 1.6;
    return (
      <g>
        {!wide ? (
          <Cam cx={900} cy={560} z={lerp(1.6, 1.05, easeOut(prog(tt, 0, 1.4)))}>
            <Deck t={t} />
            <Hero x={900} y={feet(860, 0.7)} s={0.7} expr="shock" face={0} larm={[2.5, 0.3]} rarm={[-2.5, -0.3]} />
            <Person role="gent" seed={0} x={1350} y={feet(860, 0.62)} s={0.62} face={-0.8} expr="o" walk={t} />
          </Cam>
        ) : (
          <Cam cx={lerp(960, 1100, prog(tt, 1.6, t3 - t2))} cy={560} z={lerp(1.15, 0.95, prog(tt, 1.6, t3 - t2))}>
            <OpenSea t={t} />
            <Hero x={1250} y={feet(395, 0.09)} s={0.09} expr="shock" larm={[2.5, 0.3]} rarm={[-2.5, -0.3]} />
          </Cam>
        )}
        <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={1 - prog(tt, 0, 0.35)} />
        <Pop t={tt - 0.4} x={960} y={140} size={96} color="#fff">RMS TITANIC · 1912</Pop>
        <Vignette strength={0.35} />
      </g>
    );
  }
  const tt = t - t3;
  const frozen = t > D - 0.6;
  return (
    <g>
      <Cam cx={900} cy={460} z={lerp(1.5, 1.9, easeOut(prog(tt, 0, 1.2)))} shake={frozen ? 0 : 3} t={Math.min(t, D - 0.6)}>
        <Deck t={Math.min(t, D - 0.6)} />
        <Hero x={900} y={feet(860, 0.7)} s={0.7} expr="worried" brows="worried" face={0} larm={[0.3, 0.2]} rarm={[-2.2, 2.1]} />
        <Sweat x={980} y={330} t={t} />
      </Cam>
      <Pop t={tt} x={960} y={840} size={90} color={C.red} rot={-3}>WORST PURCHASE OF MY LIFE!</Pop>
      {frozen && <rect x={0} y={0} width={W} height={H} fill="#28140a" opacity={0.25} />}
      <Vignette strength={0.45} />
    </g>
  );
};

export const Title: React.FC<ShotProps> = ({t}) => {
  const rows: [string, string, number][] = [['I ACCIDENTALLY', '#fff', 120], ['BOARDED THE', C.gold, 130], ['TITANIC!', C.gold, 180]];
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill={C.night} />
      <Stars t={t} n={160} x0={0} x1={W} y0={0} y1={700} />
      <Ship x={1300} y={820} s={0.55} t={t} night lights />
      <Waves y={835} t={t} color="#0e1838" dark="#081028" amp={4} />
      {rows.map(([w, c, size], ri) => {
        const tt = t - 0.15 - ri * 0.4;
        if (tt < 0) return null;
        const k = tt < 0.45 ? backOut(tt / 0.45, 2.4) : 1;
        return (
          <g key={ri} transform={`translate(600,${190 + ri * 180}) scale(${k})`}>
            <Txt x={0} y={0} size={size} color={c} outline={14} rot={-2 + Math.sin(t * 3 + ri)}>{w}</Txt>
          </g>
        );
      })}
      {t > 1.3 && (
        <g>
          <Hero x={lerp(2200, 1600, easeOut(prog(t, 1.3, 1.9)))} y={feet(1000, 0.6)} s={0.6} expr="worried" brows="worried" face={-0.4}
            larm={[0.3, 0.2]} rarm={[1.1, -1.7]} />
          <TimeMachine x={lerp(2200, 1600, easeOut(prog(t, 1.3, 1.9))) + 120} y={1000} s={0.35} t={t} screen="1912" glow={0.6} />
        </g>
      )}
      <Txt x={600} y={740} size={52} font={HAND} outline={6} opacity={ease(prog(t, 1.6, 2.2))}>HISTORY WORLD</Txt>
    </g>
  );
};

// =================================================================== SCENE 1 — THE MYSTERIOUS TIME MACHINE
export const Market: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSaw = cue('And then I saw it');
  const tBrass = cue('A dusty brass');
  const tSign = cue('Time machine');
  if (t < tSaw) {
    const hx = lerp(-200, 1900, prog(t, 0, tSaw + 1));
    return (
      <g>
        <Cam cx={hx + 200} cy={560} z={0.85}>
          <FleaMarket t={t} />
          <Hero x={hx} y={feet(940, 0.62)} s={0.62} expr="smile" face={0.8} look={[0.6, -0.3]} walk={t * 1.3} />
          <Person role="lady" seed={1} x={hx + 700} y={feet(960, 0.55)} s={0.55} face={-0.7} expr="smile" walk={t * 1.1} />
        </Cam>
        <Caption t={t - 0.6} place="FLEA MARKET" date="SUNDAY, TODAY" dur={4} />
        {t > cue('Old lamps') && <Pop t={t - cue('Old lamps')} x={960} y={140} size={70} hold={2.6}>LAMPS · TOYS · SOCKS?!</Pop>}
        <Vignette strength={0.3} />
      </g>
    );
  }
  const zoom = ease(prog(t, tBrass, tBrass + 1.5));
  return (
    <g>
      <Cam cx={lerp(1000, 1160, zoom)} cy={lerp(620, 700, zoom)} z={lerp(1.2, 2.0, zoom)}>
        <FleaMarket t={t} />
        <Hero x={880} y={feet(940, 0.62)} s={0.62} expr={t > tBrass ? 'happy' : 'shock'} face={0.8} look={[1, 0.3]}
          larm={[2.4, 0.3]} rarm={[-2.4, -0.3]} />
        <TimeMachine x={1180} y={740} s={0.42} t={t} screen="" glow={0.3 + 0.2 * Math.sin(t * 4)} />
        {[0, 1, 2].map((k) => <Sparkle key={k} x={1120 + k * 70} y={600 + Math.sin(t * 3 + k) * 20} r={20} t={t + k} />)}
        <g transform={`translate(1290,640) rotate(${4 + Math.sin(t * 2)})`} opacity={prog(t, tSign - 0.4, tSign)}>
          <rect x={-90} y={-60} width={180} height={120} rx={8} fill="#fff6dc" stroke={C.ink} strokeWidth={5} />
          <Txt x={0} y={-30} size={22} color={C.ink} font={HAND} outline={0} shadow={false}>TIME MACHINE</Txt>
          <Txt x={0} y={4} size={30} color={C.red} outline={0} shadow={false}>$5</Txt>
          <Txt x={0} y={36} size={20} color={C.ink} font={HAND} outline={0} shadow={false}>NO REFUNDS</Txt>
        </g>
      </Cam>
      {t > tSaw && t < tBrass + 0.5 && <Pop t={t - tSaw} x={960} y={160} size={110} color={C.gold}>!!!</Pop>}
      {t > tSign && <Pop t={t - tSign - 0.6} x={960} y={840} size={80} color={C.red} rot={-3}>NO REFUNDS.</Pop>}
      <Vignette strength={0.35} />
    </g>
  );
};

export const Buy: React.FC<ShotProps> = ({t, D, cue}) => {
  const t2 = cue('So, obviously');
  if (t < t2) {
    const wink = (t % 1.6) < 0.25 && t > 1;
    return (
      <g>
        <Cam cx={1000} cy={600} z={1.6}>
          <FleaMarket t={t} />
          <Hero x={760} y={feet(940, 0.62)} s={0.62} expr="o" face={0.8} look={[1, 0]} />
          <TimeMachine x={1000} y={740} s={0.4} t={t} />
          <Person role="vendor" x={1240} y={feet(940, 0.62)} s={0.62} face={-0.7} expr="sly" blink={wink ? 1 : 0}
            larm={[0.3, 0.2]} rarm={[-2.3, 0.7]} />
        </Cam>
        <Bubble x={1400} y={250} w={620} h={130} text={"Don't touch\nthe red lever."} size={50} tail={[-80, 90]} a={prog(t, 0.6, 0.9)} />
        <Vignette strength={0.35} />
      </g>
    );
  }
  const tt = t - t2;
  // pay -> home -> pull the lever
  if (tt < 2.0) {
    return (
      <g>
        <Cam cx={1000} cy={600} z={1.6}>
          <FleaMarket t={t} />
          <Hero x={760} y={feet(940, 0.62)} s={0.62} expr="grin" face={0.8} look={[1, 0]} rarm={[-1.5, 0.3]} />
          <TimeMachine x={1000} y={740} s={0.4} t={t} />
          <Person role="vendor" x={1240} y={feet(940, 0.62)} s={0.62} face={-0.7} expr="grin" />
          <g transform={`translate(${lerp(880, 1170, easeOut(prog(tt, 0.2, 0.9)))},${620 - Math.sin(prog(tt, 0.2, 0.9) * Math.PI) * 120})`}>
            <circle r={26} fill={C.gold} stroke={C.ink} strokeWidth={5} />
            <Txt x={0} y={0} size={26} color={C.ink} outline={0} shadow={false}>$</Txt>
          </g>
        </Cam>
        <Pop t={tt - 0.2} x={960} y={150} size={90} color={C.gold}>SOLD!</Pop>
      </g>
    );
  }
  const pull = easeIn(prog(tt, 3.2, 3.6));
  return (
    <g>
      <Cam cx={1000} cy={600} z={1.35} shake={pull * 6} t={t}>
        <Bedroom t={t} />
        <Hero x={1060} y={feet(900, 0.66)} s={0.66} expr={pull > 0.5 ? 'shock' : 'sly'} face={0.8} look={[1, 0.4]}
          larm={[0.3, 0.2]} rarm={[lerp(-1.75, -1.2, pull), lerp(0.1, 0.5, pull)]} />
        <TimeMachine x={1140} y={900} s={0.5} t={t} lever={pull} glow={pull} shake={pull} screen={pull > 0.5 ? '????' : 'READY'} />
      </Cam>
      {tt > 2.4 && tt < 3.3 && <Pop t={tt - 2.4} x={960} y={160} size={70} font={HAND}>*definitely not touching it*</Pop>}
      {pull > 0 && <Burst t={tt - 3.4} x={1500} y={260} r={140} label="CLUNK!" size={56} />}
      <Vignette strength={0.35} />
    </g>
  );
};

export const Travel: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTunnel = cue('My room turned');
  const tScreen = cue('And a little screen');
  if (t < tTunnel) {
    return (
      <g>
        <Cam cx={1100} cy={700} z={lerp(1.5, 2.3, prog(t, 0, tTunnel))} shake={12} t={t}>
          <Bedroom t={t} />
          <TimeMachine x={1150} y={900} s={0.5} t={t} lever={1} glow={1} shake={1} screen="????" />
          <Hero x={850} y={feet(900, 0.66)} s={0.66} expr="scared" face={0.6} larm={[2.5, 0.3]} rarm={[-2.5, -0.3]} />
        </Cam>
        <Burst t={t - 0.2} x={1450} y={250} r={130} label="RATTLE!" size={46} color="#9ad8ff" tcolor={C.navy} hold={1.4} />
        <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={prog(t, tTunnel - 0.4, tTunnel)} />
      </g>
    );
  }
  const tt = t - tTunnel;
  const R = rng(5);
  const year = Math.round(lerp(2026, 1912, ease(prog(tt, 0.3, Math.max(1, tScreen - tTunnel)))));
  return (
    <g>
      <Vortex t={t} />
      {Array.from({length: 12}).map((_, i) => {
        const ph = (t * 0.35 + i / 12) % 1;
        const a = R() * 6.28 + t * 0.3;
        const r = 60 + ph * ph * 1300;
        const px = W / 2 + Math.cos(a) * r;
        const py = H / 2 + Math.sin(a) * r * 0.7;
        return (
          <g key={i} transform={`translate(${px},${py}) rotate(${t * 120 + i * 40}) scale(${0.2 + ph * 1.2})`}>
            {i % 3 === 0 ? <CapShape /> : i % 3 === 1 ? <circle r={50} fill="#f6efe0" stroke={C.ink} strokeWidth={8} /> : <rect x={-40} y={-50} width={80} height={100} rx={8} fill="#ffd84d" stroke={C.ink} strokeWidth={6} />}
          </g>
        );
      })}
      <g transform={`translate(${W / 2 + 260 * Math.sin(t * 0.9)},${H / 2 + 120 * Math.cos(t * 1.3) - 60}) rotate(${t * 140})`}>
        <Doodle x={0} y={-150} s={0.6} expr="shock" face={0} larm={[2.4, 0.5]} rarm={[-2.4, -0.5]} legs={[0.5, -0.5]} />
      </g>
      <rect x={W / 2 - 260} y={60} width={520} height={130} rx={30} fill="rgba(5,3,16,0.75)" stroke={C.gold} strokeWidth={5} />
      <Txt x={W / 2} y={125} size={90} color={C.gold} outline={0} shadow={false}>{String(year)}</Txt>
      {t > tScreen && <Pop t={t - tScreen - 0.6} x={W / 2} y={840} size={86} color="#7dffb0">14 APRIL 1912</Pop>}
      <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={1 - prog(tt, 0, 0.4) + prog(t, D - 0.3, D)} />
      <Vignette strength={0.55} />
    </g>
  );
};

// =================================================================== SCENE 2 — WELCOME ABOARD
export const Aboard: React.FC<ShotProps> = ({t, D, cue}) => {
  const tChim = cue('Huge chimneys');
  const tCity = cue('A ship so big');
  if (t < tCity) {
    const land = easeIn(prog(t, 0.1, 0.6));
    const sq = t > 0.6 ? -0.18 * Math.exp(-(t - 0.6) * 6) : 0;
    const dizzy = t > 0.6 && t < tChim + 0.4;
    return (
      <g>
        <Cam cx={lerp(900, 1000, prog(t, 0, tCity))} cy={lerp(620, 380, ease(prog(t, tChim - 0.3, tChim + 1.5)))}
          z={lerp(1.35, 0.8, ease(prog(t, tChim - 0.3, tChim + 1.5)))}>
          <Deck t={t} />
          <Hero x={900} y={lerp(-400, feet(860, 0.66), land)} s={0.66} squash={sq} expr={dizzy ? 'worried' : 'o'}
            face={dizzy ? 0 : 0.6} look={dizzy ? [0, 0] : [0.3, -1]} tilt={dizzy ? 0.08 * Math.sin(t * 5) : 0} />
          {dizzy && <DizzyStars x={900} y={feet(860, 0.66) - 90} r={110} t={t} />}
          {[0, 1, 2].map((i) => (
            <Person key={i} role={i === 1 ? 'lady' : 'gent'} seed={i} x={lerp(2200, -400, prog(t, 0.5 + i * 0.8, D + 3))} y={feet(860, 0.6)} s={0.6}
              face={-0.8} expr="smile" walk={t * 1.1 + i} />
          ))}
        </Cam>
        {t > 0.6 && t < 2.2 && <Burst t={t - 0.6} x={500} y={250} r={120} label="BONK!" size={56} />}
        <Caption t={t - 1.2} place="ATLANTIC OCEAN" date="14 APRIL 1912" dur={4.5} />
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tCity;
  return (
    <g>
      <Cam cx={lerp(700, 1200, prog(tt, 0, D - tCity))} cy={520} z={lerp(1.25, 0.85, ease(prog(tt, 0, 2)))}>
        <OpenSea t={t} />
      </Cam>
      <Pop t={tt - 0.5} x={960} y={150} size={86} color="#fff">A FLOATING CITY</Pop>
      <Txt x={960} y={850} size={48} font={HAND} outline={5} opacity={ease(prog(tt, 1.2, 1.6))}>269 metres long · 4 funnels</Txt>
      <Vignette strength={0.3} />
    </g>
  );
};

export const Luxury: React.FC<ShotProps> = ({t, D, cue}) => {
  const tGym = cue('A gym');
  const tRolls = cue('I ate four');
  if (t < tGym) {
    return (
      <g>
        <Cam cx={960} cy={lerp(200, 600, ease(prog(t, 0, tGym)))} z={lerp(0.75, 0.95, ease(prog(t, 0, tGym)))}>
          <GrandStaircase t={t} />
          <Hero x={960} y={feet(1000, 0.55)} s={0.55} expr="happy" face={0} look={[0, -1]} larm={[2.4, 0.3]} rarm={[-2.4, -0.3]} />
        </Cam>
        <Pop t={t - 0.4} x={960} y={110} size={80} color={C.gold}>THE GRAND STAIRCASE</Pop>
        <Vignette strength={0.3} />
      </g>
    );
  }
  if (t < tRolls) {
    const tt = t - tGym;
    const items: [string, string][] = [['GYM', '🏋'], ['SWIMMING POOL', '~'], ['11 COURSES', '🍽']];
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#f3e9d2" />
        {Array.from({length: 33}).map((_, i) => <line key={i} x1={i * 60} y1={0} x2={i * 60} y2={H} stroke="#d8cbb0" strokeWidth={1.5} />)}
        {items.map(([lab], i) => {
          const tc = i * (tRolls - tGym) / 3.2;
          const x = 360 + i * 600;
          if (tt < tc) return null;
          const k = backOut(prog(tt, tc, tc + 0.4), 1.8);
          return (
            <g key={lab} transform={`translate(${x},500) scale(${k})`}>
              <circle r={190} fill="#fff" stroke={C.ink} strokeWidth={8} />
              {i === 0 && <g><rect x={-120} y={-14} width={240} height={28} rx={14} fill="#6a6a7a" stroke={C.ink} strokeWidth={5} />{[-1, 1].map((sd) => <rect key={sd} x={sd * 120 - 25} y={-60} width={50} height={120} rx={10} fill="#3a3a44" stroke={C.ink} strokeWidth={5} />)}</g>}
              {i === 1 && <g><rect x={-130} y={-60} width={260} height={120} rx={20} fill="#7cc8f0" stroke={C.ink} strokeWidth={6} />{[0, 1, 2].map((k2) => <path key={k2} d={`M${-110 + k2 * 80},${-10 + Math.sin(t * 3 + k2) * 8} q20,-20 40,0 t40,0`} fill="none" stroke="#fff" strokeWidth={6} />)}</g>}
              {i === 2 && <g><ellipse cx={0} cy={20} rx={130} ry={40} fill="#f6f6f6" stroke={C.ink} strokeWidth={6} /><path d="M-70,10 C-70,-80 70,-80 70,10 Z" fill="#c9ccd2" stroke={C.ink} strokeWidth={6} /><circle cx={0} cy={-62} r={12} fill="#c9ccd2" stroke={C.ink} strokeWidth={4} /></g>}
              <Txt x={0} y={260} size={60} color={C.navy} outline={0} shadow={false}>{lab}</Txt>
            </g>
          );
        })}
        <Vignette strength={0.25} />
      </g>
    );
  }
  const tt = t - tRolls;
  const n = Math.min(4, Math.floor(tt / 0.7) + 1);
  return (
    <g>
      <Cam cx={900} cy={560} z={1.45}>
        <Dining t={t} />
        <DiningTable x={900} y={760} t={t} plates={3} />
        <Hero x={760} y={feet(780, 0.6)} s={0.6} expr={tt % 0.7 < 0.35 ? 'grin' : 'happy'} face={0.4} rarm={[-1.6, 1.4]} larm={[0.3, 0.2]} showLegs={false} />
        {Array.from({length: 4 - n}).map((_, k) => <ellipse key={k} cx={980 + k * 40} cy={748} rx={22} ry={14} fill="#e0a24f" stroke={C.ink} strokeWidth={4} />)}
        <Person role="waiter" x={1250} y={feet(990, 0.62)} s={0.62} face={-0.8} expr={tt > 2.5 ? 'frown' : 'o'} brows={tt > 2.5 ? 'angry' : 'up'}
          larm={[0.3, 0.2]} rarm={[-1.6, 1.4]} />
      </Cam>
      <rect x={70} y={70} width={380} height={120} rx={20} fill="rgba(10,10,20,0.8)" />
      <Txt x={260} y={130} size={60} color={C.gold} outline={0} shadow={false}>{`ROLLS: ${n}`}</Txt>
      <Vignette strength={0.35} />
    </g>
  );
};

export const Realize: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTop = cue('On the top');
  const tOnce = cue('I read it once');
  const tBrain = cue('And my brain');
  if (t < tBrain) {
    const z = t < tOnce ? lerp(1, 1.15, prog(t, 0, tOnce)) : lerp(1.15, 1.6, ease(prog(t, tOnce, tBrain)));
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#5a2a1e" />
        <Cam cx={960} cy={lerp(560, 330, ease(prog(t, tTop, tTop + 1.5)))} z={z}>
          <g transform="translate(960,560) rotate(-2)">
            <rect x={-420} y={-480} width={840} height={960} rx={14} fill="#fbf6e8" stroke={C.ink} strokeWidth={8} />
            <rect x={-390} y={-450} width={780} height={900} rx={8} fill="none" stroke="#b8892a" strokeWidth={5} />
            <Txt x={0} y={-370} size={40} color="#b8892a" font={HAND} outline={0} shadow={false}>WHITE STAR LINE</Txt>
            <Txt x={0} y={-290} size={86} color="#b8892a" outline={0} shadow={false}>R.M.S. TITANIC</Txt>
            <Txt x={0} y={-215} size={36} color={C.ink} font={HAND} outline={0} shadow={false}>April 14, 1912 · Luncheon</Txt>
            {['Consommé Fermier', 'Cockie Leekie', 'Fillets of Brill', 'Chicken a la Maryland', 'Grilled Mutton Chops', 'Apple Meringue'].map((l, i) => (
              <Txt key={l} x={0} y={-120 + i * 80} size={40} color={C.ink} font={HAND} outline={0} shadow={false}>{l}</Txt>
            ))}
          </g>
        </Cam>
        {t > tOnce && <Pop t={t - tOnce} x={360} y={840} size={70} hold={1.6}>ONCE...</Pop>}
        {t > tOnce + 1.4 && <Pop t={t - tOnce - 1.4} x={1560} y={840} size={70}>TWICE...</Pop>}
        <Vignette strength={0.45} />
      </g>
    );
  }
  const tt = t - tBrain;
  return (
    <g>
      <Cam cx={900} cy={430} z={2.4}>
        <Dining t={t} />
        <Hero x={900} y={feet(860, 0.6)} s={0.6} expr="flat" face={0} look={[0, 0]} blink={0} larm={[1.2, -1.2]} rarm={[-1.2, 1.2]} />
      </Cam>
      <Pop t={tt - 0.6} x={1280} y={260} size={56} font={HAND} outline={6}>...eep.</Pop>
      <Vignette strength={0.5} />
    </g>
  );
};

export const Fact1: React.FC<ShotProps> = ({t, D, cue}) => {
  const tPaper = cue('Newspapers called');
  const tNight = cue('And on the night');
  const tTonight = cue('That was tonight');
  if (t < tTonight) {
    const route = ease(prog(t, 0.6, tPaper));
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#a8d4f0" />
        <path d="M0,0 L520,0 C480,200 600,320 560,520 C520,700 380,820 300,1080 L0,1080 Z" fill="#b8d08a" stroke={C.ink} strokeWidth={6} />
        <path d="M1920,0 L1560,0 C1600,240 1480,420 1540,640 C1600,840 1720,920 1700,1080 L1920,1080 Z" fill="#b8d08a" stroke={C.ink} strokeWidth={6} />
        <Txt x={260} y={420} size={44} color={C.ink} outline={0} shadow={false}>ENGLAND</Txt>
        <Txt x={1740} y={420} size={44} color={C.ink} outline={0} shadow={false}>NEW YORK</Txt>
        <path d={`M520,450 C900,${520} 1200,${600} 1540,520`} fill="none" stroke={C.red} strokeWidth={8} strokeDasharray="22 16"
          pathLength={1} strokeDashoffset={0} opacity={1} style={{clipPath: `inset(0 ${100 - route * 100}% 0 0)`}} />
        <g transform={`translate(${lerp(520, 1540, route * 0.62)},${lerp(450, 530, route * 0.62) - 20})`}>
          <Ship x={0} y={0} s={0.1} t={t} smoke={false} />
        </g>
        <Pop t={t - 0.3} x={520} y={600} size={54} color={C.navy} outline={0}>10 APRIL 1912</Pop>
        {t > tPaper && (
          <g transform={`translate(1160,240) rotate(${-4})`} opacity={1 - prog(t, tNight - 0.3, tNight)}>
            <rect x={-330} y={-130} width={660} height={260} rx={8} fill="#f6f2e6" stroke={C.ink} strokeWidth={6} />
            <Txt x={0} y={-80} size={34} color={C.ink} font={HAND} outline={0} shadow={false}>THE DAILY HERALD</Txt>
            <Txt x={0} y={10} size={58} color={C.ink} outline={0} shadow={false}>"PRACTICALLY</Txt>
            <Txt x={0} y={80} size={58} color={C.ink} outline={0} shadow={false}>UNSINKABLE"</Txt>
          </g>
        )}
        {t > tNight && (
          <g>
            <Iceberg x={1150} y={600} s={0.35 * backOut(prog(t, tNight + 0.4, tNight + 0.9), 1.6)} />
            <Pop t={t - tNight - 0.8} x={1150} y={760} size={58} color={C.red} outline={0}>14 APRIL · ICEBERG</Pop>
          </g>
        )}
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tTonight;
  return (
    <g>
      <Cam cx={900} cy={520} z={lerp(1.4, 2.0, easeOut(prog(tt, 0, 0.5)))} shake={6} t={t}>
        <Deck t={t} />
        <Hero x={900} y={feet(860, 0.66)} s={0.66} expr="scared" face={0} brows="worried" larm={[2.6, 0.3]} rarm={[-2.6, -0.3]} />
        <Sweat x={990} y={360} t={t} />
        <Sweat x={810} y={370} s={0.8} t={t + 0.3} />
      </Cam>
      <Pop t={tt} x={960} y={150} size={120} color={C.red} rot={-3}>TONIGHT?!</Pop>
      <Vignette strength={0.45} />
    </g>
  );
};

// =================================================================== SCENE 3 — NOBODY BELIEVES ME
const DiningScene: React.FC<{t: number; hero: Partial<DoodleProps>; onTable?: boolean; cam?: [number, number, number]; children?: React.ReactNode}> = ({t, hero, onTable = true, cam = [960, 560, 1.0], children}) => (
  <Cam cx={cam[0]} cy={cam[1]} z={cam[2]}>
    <Dining t={t} />
    <Person role="gent" seed={1} x={560} y={feet(860, 0.6)} s={0.6} face={0.6} expr="smile" showLegs={false} />
    <Person role="lady" seed={0} x={1380} y={feet(860, 0.6)} s={0.6} face={-0.6} expr="smile" showLegs={false} />
    <DiningTable x={960} y={780} w={1000} t={t} plates={4} />
    <Hero x={830} y={onTable ? feet(780, 0.62) : feet(1000, 0.62)} s={0.62} {...hero} />
    {children}
  </Cam>
);

export const Warn1: React.FC<ShotProps> = ({t, D, cue}) => {
  const tShout = cue('I jumped', 0.55);
  const tWaiter = cue('A waiter');
  const jump = easeOut(prog(t, 0.3, 1.0));
  const shouting = t > tShout && t < tWaiter;
  return (
    <g>
      <DiningScene t={t} cam={[lerp(960, 1050, prog(t, tWaiter, D)), lerp(560, 520, prog(t, tWaiter, D)), lerp(0.95, 1.25, ease(prog(t, tWaiter - 0.5, tWaiter + 1)))]}
        hero={{expr: shouting ? 'scared' : t > tWaiter + 2.5 ? 'flat' : 'grin', face: t > tWaiter ? 0.8 : 0, y: lerp(feet(1000, 0.62), feet(780, 0.62), jump) - Math.sin(jump * Math.PI) * 120,
          larm: shouting ? [2.6, 0.2] : [0.3, 0.2], rarm: shouting ? [-2.6, -0.2] : t > tWaiter + 2.2 ? [-1.5, 0.5] : [-0.3, -0.2]}}>
        {t > tWaiter - 0.5 && (
          <g>
            <Person role="waiter" x={lerp(2100, 1240, easeOut(prog(t, tWaiter - 0.5, tWaiter + 0.8)))} y={feet(1000, 0.62)} s={0.62} face={-0.7}
              expr="smile" walk={t < tWaiter + 0.8 ? t * 1.6 : undefined} rarm={[-1.6, 1.4]} />
            <g transform={`translate(${t < tWaiter + 2.2 ? lerp(2100, 1240, easeOut(prog(t, tWaiter - 0.5, tWaiter + 0.8))) - 150 : 1090},${t < tWaiter + 2.2 ? 600 : 590})`}>
              <path d="M-30,-70 L30,-70 L22,10 L-22,10 Z" fill="#cfeeff" stroke={C.ink} strokeWidth={5} opacity={0.9} />
              <rect x={-18} y={-50} width={16} height={16} fill="#fff" stroke={C.ink} strokeWidth={3} transform="rotate(12)" />
              <rect x={2} y={-36} width={16} height={16} fill="#fff" stroke={C.ink} strokeWidth={3} transform="rotate(-10)" />
            </g>
          </g>
        )}
      </DiningScene>
      {shouting && <Burst t={t - tShout} x={960} y={200} r={190} label="ICEBERG!" size={80} />}
      {t > tWaiter + 1.6 && <Pop t={t - tWaiter - 1.6} x={960} y={200} size={84} color="#9ad8ff">...WITH ICE.</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Warn2: React.FC<ShotProps> = ({t, D, cue}) => {
  const tLady = cue('A lady in');
  const shouting = t < tLady;
  return (
    <g>
      <DiningScene t={t} cam={shouting ? [960, 520, lerp(1.1, 1.4, prog(t, 0, tLady))] : [1250, 520, 1.5]}
        hero={{expr: shouting ? 'scared' : 'flat', face: shouting ? 0 : 0.7, look: shouting ? [0, 0] : [1, 0], larm: shouting ? [2.6, 0.2] : [0.3, 0.2], rarm: shouting ? [-2.6, -0.2] : [-0.3, -0.2]}} />
      {shouting && t > 0.5 && <Pop t={t - 0.5} x={960} y={150} size={74} color={C.red} rot={-2}>THIS SHIP IS GOING TO SINK!</Pop>}
      {!shouting && <Bubble x={1300} y={230} w={880} h={150} text={"Oh, yes, dear. The sinks\nin first class are lovely."} size={48} tail={[40, 90]} a={prog(t, tLady + 0.6, tLady + 0.9)} />}
      {!shouting && t > tLady + 3 && <Pop t={t - tLady - 3} x={500} y={840} size={64} font={HAND} outline={6}>*facepalm*</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Warn3: React.FC<ShotProps> = ({t, D, cue}) => {
  const tLaugh = cue('He laughed');
  const laughing = t > tLaugh;
  return (
    <g>
      <Cam cx={lerp(950, 1050, prog(t, 0, D))} cy={540} z={1.45}>
        <Deck t={t} />
        <Hero x={850} y={feet(860, 0.62)} s={0.62} expr={laughing ? 'worried' : 'scared'} face={0.8} look={[1, 0]}
          larm={[0.3, 0.2]} rarm={laughing ? [-0.3, -0.2] : [-1.5, 0.1]} brows="worried" />
        <Person role="gent" seed={0} x={1150} y={feet(860, 0.62)} s={0.62} face={-0.7} expr={laughing ? 'laugh' : 'o'}
          tilt={laughing ? 0.08 * Math.sin(t * 12) : 0} larm={laughing ? [-1.0, 1.6] : [0.3, 0.2]} rarm={laughing ? [1.0, -1.6] : [-0.3, -0.2]} />
      </Cam>
      {!laughing && t > 0.4 && <Pop t={t - 0.4} x={960} y={150} size={80} color={C.red}>NOT ENOUGH LIFEBOATS!</Pop>}
      {laughing && <Bubble x={1350} y={220} w={820} h={150} text={'Young man, this ship\nis unsinkable!'} size={50} tail={[-80, 90]} a={fadeWin(t, tLaugh + 0.6, cue('The lifeboats are') - 0.1)} />}
      {t > cue('The lifeboats are') && <Bubble x={1350} y={220} w={860} h={150} text={'The lifeboats are\nbasically decorations.'} size={50} tail={[-80, 90]} a={prog(t, cue('The lifeboats are'), cue('The lifeboats are') + 0.2)} />}
      {laughing && <Pop t={t - tLaugh} x={480} y={840} size={70} color={C.gold} hold={2.5}>HA HA HA!</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Fact2: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBoats = cue('The Titanic had');
  const tPeople = cue('But there were');
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#f3e9d2" />
      {Array.from({length: 33}).map((_, i) => <line key={i} x1={i * 60} y1={0} x2={i * 60} y2={H} stroke="#d8cbb0" strokeWidth={1.5} />)}
      <Txt x={960} y={90} size={70} color={C.navy} outline={0} shadow={false} opacity={prog(t, 0.3, 0.7)}>THE LIFEBOAT PROBLEM</Txt>
      {t < tBoats + 0.3 && (
        <g opacity={1 - prog(t, tBoats, tBoats + 0.3)}>
          <Hero x={960} y={feet(900, 0.6)} s={0.6} expr="worried" brows="worried" face={0} larm={[1.4, -0.6]} rarm={[-1.4, 0.6]} />
          <Pop t={t - 1.4} x={960} y={300} size={90} color={C.red}>HALF RIGHT...</Pop>
        </g>
      )}
      {t > tBoats &&
        Array.from({length: 20}).map((_, i) => {
          const tc = tBoats + 0.2 + i * 0.08;
          if (t < tc) return null;
          const k = backOut(prog(t, tc, tc + 0.25), 2);
          return (
            <path key={i} transform={`translate(${420 + (i % 10) * 120},${250 + Math.floor(i / 10) * 100}) scale(${k * 1.4})`}
              d="M-36,-12 L36,-12 C32,10 20,16 0,16 C-20,16 -32,10 -36,-12 Z" fill="#fff" stroke={C.ink} strokeWidth={4} />
          );
        })}
      {t > tBoats + 1.6 && <Txt x={960} y={470} size={58} color={C.ink} outline={0} shadow={false}>20 BOATS · ~1,178 SEATS</Txt>}
      {t > tPeople &&
        Array.from({length: 22}).map((_, i) => {
          const tc = tPeople + 0.2 + i * 0.06;
          if (t < tc) return null;
          const seated = i < 11;
          return (
            <g key={i} transform={`translate(${130 + i * 75},700)`} opacity={prog(t, tc, tc + 0.2)}>
              <circle cx={0} cy={-40} r={22} fill={seated ? '#fff' : '#f2c8c8'} stroke={C.ink} strokeWidth={4} />
              <rect x={-18} y={-16} width={36} height={60} rx={14} fill={seated ? '#fff' : '#f2c8c8'} stroke={C.ink} strokeWidth={4} />
            </g>
          );
        })}
      {t > tPeople + 1.8 && <Txt x={960} y={820} size={58} color={C.red} outline={0} shadow={false}>~2,224 PEOPLE ON BOARD</Txt>}
      {t > tPeople + 1.8 && <Txt x={960} y={890} size={44} color={C.ink} font={HAND} outline={0} shadow={false}>each person = 100 · pink = no seat</Txt>}
      <Vignette strength={0.2} />
    </g>
  );
};

export const Napkin: React.FC<ShotProps> = ({t, D, cue}) => {
  const tClap = cue('Everyone clapped');
  const draw = prog(t, 0.3, tClap - 0.2);
  if (t < tClap) {
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#7a3a2a" />
        <g transform="translate(960,540) rotate(3)">
          <rect x={-420} y={-360} width={840} height={720} rx={10} fill="#fff" stroke={C.ink} strokeWidth={6} />
          <path d="M-300,200 L-240,40 L-150,0 L-100,-140 L-20,-100 L40,-220 L130,-80 L210,-100 L280,60 L350,200" fill="none" stroke={C.navy}
            strokeWidth={10} strokeLinecap="round" strokeLinejoin="round" style={{strokeDasharray: 2000, strokeDashoffset: 2000 * (1 - draw)}} />
          <line x1={-380} y1={200} x2={380} y2={200} stroke={C.sea} strokeWidth={8} opacity={draw} />
          <Txt x={0} y={290} size={56} color={C.red} font={HAND} outline={0} shadow={false} opacity={prog(draw, 0.8, 1)}>ICEBERG!!!</Txt>
        </g>
        <Vignette strength={0.4} />
      </g>
    );
  }
  const tt = t - tClap;
  return (
    <g>
      <DiningScene t={t} cam={[960, 520, 1.05]} onTable={false} hero={{expr: 'worried', face: 0, brows: 'worried', rarm: [-2.2, 2.1], y: feet(1000, 0.62)}}>
        <g transform="translate(1180,740)">
          <path d="M-70,0 L-50,-50 L-20,-60 L0,-110 L30,-70 L60,-80 L80,0 Z" fill="#fff6f0" stroke={C.ink} strokeWidth={5} />
          <ellipse cx={5} cy={4} rx={95} ry={18} fill="#e8e8f0" stroke={C.ink} strokeWidth={4} />
          <circle cx={10} cy={-112} r={12} fill={C.red} stroke={C.ink} strokeWidth={3} />
        </g>
      </DiningScene>
      <Pop t={tt} x={960} y={140} size={84} color={C.gold}>*CLAP CLAP CLAP*</Pop>
      <Pop t={tt - 1.2} x={960} y={250} size={64} font={HAND} outline={6}>"Two icebergs for dessert, please!"</Pop>
      <Vignette strength={0.3} />
    </g>
  );
};

// =================================================================== SCENE 4 — MEETING THE CAPTAIN
export const Captain: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTalk = cue('Talk to the captain');
  const tFound = cue('I found Captain');
  if (t < tFound) {
    const hx = lerp(-200, 2000, prog(t, tTalk - 0.2, tFound + 0.6));
    return (
      <g>
        <Cam cx={t < tTalk ? 900 : hx} cy={540} z={t < tTalk ? 1.6 : 0.9}>
          <Corridor t={t} label="A DECK · TO THE BRIDGE →" />
          <Hero x={t < tTalk ? 900 : hx} y={feet(840, 0.62)} s={0.62} expr={t < tTalk ? 'sly' : 'grin'} face={0.9}
            {...(t < tTalk ? {rarm: [-1.1, 1.8] as [number, number]} : runArms(t, 3))} />
          {t > tTalk && <SpeedLines x={hx - 80} y={680} seed={Math.floor(t * 8)} />}
        </Cam>
        {t < tTalk + 0.3 && <Pop t={t - 0.3} x={960} y={150} size={90} color={C.gold}>NEW PLAN!</Pop>}
        <Vignette strength={0.3} />
      </g>
    );
  }
  const tt = t - tFound;
  return (
    <g>
      <Cam cx={lerp(1100, 1250, prog(tt, 0, D - tFound))} cy={520} z={lerp(1.0, 1.25, ease(prog(tt, 0, 2.5)))}>
        <Bridge t={t} />
        <Person role="captain" x={1450} y={feet(960, 0.7)} s={0.7} face={-0.6} expr="flat" blink={blinkAt(t, 3)} larm={[-0.9, 1.9]} rarm={[0.9, -1.9]} />
        <Person role="officer" x={1880} y={feet(960, 0.62)} s={0.62} face={-0.7} expr="flat" blink={blinkAt(t, 5)} />
        <Hero x={lerp(600, 960, easeOut(prog(tt, 0, 1.2)))} y={feet(960, 0.62)} s={0.62} expr="smile" face={0.8} walk={tt < 1.2 ? t * 1.5 : undefined} />
      </Cam>
      <Caption t={tt - 0.5} place="CAPTAIN EDWARD SMITH" date="ON THE BRIDGE" dur={4} />
      <Vignette strength={0.35} />
    </g>
  );
};

/** alternating close-ups between the hero (left) and the captain (right) */
const TwoShot: React.FC<{t: number; who: 'hero' | 'captain' | 'both'; heroP?: Partial<DoodleProps>; capP?: Partial<DoodleProps>; children?: React.ReactNode}> = ({t, who, heroP, capP, children}) => {
  const cam: [number, number, number] = who === 'hero' ? [900, 740, 1.75] : who === 'captain' ? [1420, 720, 1.75] : [1160, 640, 1.15];
  return (
    <g>
      <Cam cx={cam[0]} cy={cam[1]} z={cam[2]}>
        <Bridge t={t} />
        <Hero x={900} y={feet(960, 0.62)} s={0.62} expr="smile" face={0.8} look={[1, 0]} {...heroP} />
        <Person role="captain" x={1450} y={feet(960, 0.7)} s={0.7} face={-0.6} expr="flat" blink={blinkAt(t, 3)} larm={[-0.9, 1.9]} rarm={[0.9, -1.9]} {...capP} />
      </Cam>
      {children}
    </g>
  );
};

export const Conv1: React.FC<ShotProps> = ({t, D, cue}) => {
  const tBrow = cue('He raised');
  const tWhen = cue('When?');
  const tUmm = cue('Umm');
  const tWhere = cue('Where?');
  const tWet = cue('Somewhere');
  let who: 'hero' | 'captain' | 'both' = 'hero';
  if (t > tBrow && t < tUmm) who = 'captain';
  else if (t > tWhere - 0.1 && t < tWet) who = 'captain';
  else if (t > tWet) who = 'both';
  return (
    <TwoShot t={t} who={who}
      heroP={{expr: t < tBrow ? 'scared' : t > tWet ? 'worried' : 'sly', larm: t < tBrow ? [2.6, 0.2] : [0.3, 0.2], rarm: t < tBrow ? [-2.6, -0.2] : [-2.2, 2.0], brows: t > tUmm ? 'worried' : undefined}}
      capP={{brows: t > tBrow ? 'up' : undefined, expr: t > tWet + 0.5 ? 'frown' : 'flat'}}>
      {t < tBrow && <Bubble x={1000} y={170} w={940} h={120} text="Captain! You're going to hit an iceberg!" size={48} tail={[-160, 80]} a={prog(t, 0.2, 0.4)} />}
      {t > tWhen && t < tUmm && <Bubble x={900} y={200} w={300} h={120} text="When?" size={60} tail={[60, 80]} a={1} />}
      {t > tUmm && t < tWhere && <Bubble x={1000} y={200} w={760} h={120} text="Umm... tonight. Midnight. Ish." size={52} tail={[-120, 80]} a={1} />}
      {t > tWhere && t < tWet && <Bubble x={900} y={200} w={320} h={120} text="Where?" size={60} tail={[60, 80]} a={1} />}
      {t > tWet && <Bubble x={760} y={220} w={560} h={120} text="Somewhere... wet." size={56} tail={[-40, 80]} a={1} />}
      {t > tWet + 0.6 && <Pop t={t - tWet - 0.6} x={1500} y={840} size={64} font={HAND} outline={6}>*awkward silence*</Pop>}
      <Vignette strength={0.35} />
    </TwoShot>
  );
};

export const Conv2: React.FC<ShotProps> = ({t, D, cue}) => {
  const tPanic = cue('I panicked');
  const tMovie = cue('I saw it in a movie');
  const tFrown = cue('He frowned');
  const tWhat = cue('What is a movie');
  const tReal = cue('That was when');
  let who: 'hero' | 'captain' | 'both' = 'captain';
  if (t > tPanic && t < tFrown) who = 'hero';
  else if (t > tReal) who = 'both';
  return (
    <TwoShot t={t} who={who}
      heroP={{expr: t < tMovie ? 'worried' : t < tFrown ? 'grin' : 'scared', brows: 'worried', rarm: t > tMovie && t < tFrown ? [-2.5, 0.3] : [-0.3, -0.2]}}
      capP={{expr: t > tFrown ? 'frown' : 'flat', brows: t > tFrown ? 'angry' : 'up'}}>
      {t < tPanic && <Bubble x={1300} y={200} w={760} h={120} text="And how do you know this?" size={52} tail={[100, 80]} a={prog(t, 0.2, 0.4)} />}
      {t > tMovie && t < tFrown && <Bubble x={980} y={200} w={700} h={120} text="I saw it in a MOVIE!" size={56} tail={[-140, 80]} a={1} />}
      {t > tWhat && t < tReal && <Bubble x={1300} y={200} w={600} h={120} text="What is a movie?" size={56} tail={[100, 80]} a={1} />}
      {t > tReal && <Sweat x={980} y={400} t={t} />}
      {t > tReal + 0.8 && <FactCard t={t - tReal - 0.8} x={1430} y={320} w={720} h={250} title="1912" lines={['Silent films only.', 'Talkies arrived in 1927!']} />}
      <Vignette strength={0.35} />
    </TwoShot>
  );
};

export const Binoculars: React.FC<ShotProps> = ({t, D, cue}) => {
  const tKey = cue('The key');
  const tRun = cue('So I ran');
  if (t < tKey) {
    return (
      <g>
        <Cam cx={300} cy={lerp(500, 450, prog(t, 0, tKey))} z={1.5}>
          <rect x={-2000} y={-2000} width={6000} height={4000} fill="#7cc8f0" />
          <Waves y={900} t={t} amp={8} />
          <rect x={260} y={600} width={60} height={800} fill="#3a2a1e" stroke={C.ink} strokeWidth={6} />
          <Person role="lookout" x={210} y={430} s={0.4} face={0.6} expr="flat" larm={[-0.6, 1.9]} rarm={[0.6, -1.9]} showLegs={false} />
          <Person role="lookout" seed={1} x={380} y={430} s={0.4} face={-0.6} expr="frown" larm={[1.6, -0.4]} rarm={[-1.6, 0.4]} showLegs={false} />
          <path d="M60,560 L520,560 L480,820 L100,820 Z" fill="#5a3a22" stroke={C.ink} strokeWidth={6} />
        </Cam>
        <Pop t={t - 0.4} x={960} y={140} size={80}>CROW'S NEST: NO BINOCULARS</Pop>
        <Vignette strength={0.3} />
      </g>
    );
  }
  if (t < tRun) {
    const tt = t - tKey;
    return (
      <g>
        <rect x={0} y={0} width={W} height={H} fill="#2a2440" />
        <Glow id="keyg" x={760} y={540} r={500} a={0.4} />
        <g transform={`translate(760,540) rotate(${-20 + Math.sin(t * 2) * 5}) scale(${backOut(prog(tt, 0, 0.5), 1.6)})`}>
          <circle cx={-160} cy={0} r={90} fill="none" stroke="#e3b23a" strokeWidth={36} />
          <circle cx={-160} cy={0} r={90} fill="none" stroke={C.ink} strokeWidth={4} />
          <rect x={-70} y={-18} width={340} height={36} fill="#e3b23a" stroke={C.ink} strokeWidth={5} />
          <rect x={200} y={18} width={30} height={60} fill="#e3b23a" stroke={C.ink} strokeWidth={5} />
          <rect x={140} y={18} width={30} height={40} fill="#e3b23a" stroke={C.ink} strokeWidth={5} />
        </g>
        <FactCard t={tt - 0.6} x={1400} y={540} w={760} h={330} title="REAL HISTORY" lines={['The key to the', 'binocular locker stayed', 'in England (David Blair).']} />
        <Vignette strength={0.4} />
      </g>
    );
  }
  const tt = t - tRun;
  const hx = lerp(600, 2200, prog(tt, 0, D - tRun));
  return (
    <g>
      <Cam cx={hx} cy={540} z={1.0}>
        <Deck t={t} />
        <Hero x={hx} y={feet(860, 0.62)} s={0.62} expr="grin" face={0.9} {...runArms(t, 3.2)} />
        <SpeedLines x={hx - 80} y={700} seed={Math.floor(t * 8)} />
      </Cam>
      <Pop t={tt} x={960} y={150} size={80} color={C.gold}>OPERATION BINOCULARS!</Pop>
      <Vignette strength={0.3} />
    </g>
  );
};

export const Lost: React.FC<ShotProps> = ({t, D, cue}) => {
  const tNot = cue('I did not');
  const seg = tNot / 4;
  const idx = Math.min(3, Math.floor(t / seg));
  const labels = ['SQUASH COURT', 'MAIL ROOM', 'GALLEY', 'STAIRS...'];
  const cols = ['#d8e8f2', '#e8dcc0', '#f2e2c8', '#d0c4a8'];
  if (t < tNot) {
    const tt = t - idx * seg;
    const hx = lerp(200, 1800, tt / seg);
    return (
      <g>
        {idx < 3 ? (
          <Cam cx={960} cy={540} z={1.0}>
            <Corridor t={t} color={cols[idx]} label={labels[idx]} />
            {idx === 0 && <g><circle cx={1100 + Math.sin(t * 6) * 200} cy={500 + Math.cos(t * 9) * 60} r={18} fill="#2a2a2a" /></g>}
            {idx === 1 && [0, 1, 2, 3, 4].map((k) => <rect key={k} x={900 + k * 60} y={((t * 300 + k * 80) % 400) + 300} width={50} height={34} fill="#fff" stroke={C.ink} strokeWidth={3} transform={`rotate(${t * 100 + k * 30} ${925 + k * 60} 500)`} />)}
            {idx === 2 && <Person role="waiter" x={1300} y={feet(840, 0.62)} s={0.62} face={-0.8} expr="frown" brows="angry" larm={[0.3, 0.2]} rarm={[-2.5 + 0.4 * Math.sin(t * 10), 0.3]} />}
            <Hero x={hx} y={feet(840, 0.62)} s={0.62} expr={idx === 2 ? 'scared' : 'grin'} face={0.9} {...runArms(t, 3)} />
          </Cam>
        ) : (
          <g>
            <rect x={0} y={0} width={W} height={H} fill="#d0c4a8" />
            {Array.from({length: 14}).map((_, k) => <rect key={k} x={-200 + k * 160} y={1000 - k * 80 + ((t * 160) % 80)} width={400} height={80} fill={k % 2 ? '#e8dcc0' : '#dccfaf'} stroke={C.ink} strokeWidth={5} />)}
            <Hero x={960} y={560 - Math.abs(Math.sin(t * 8)) * 30} s={0.6} expr="worried" face={0.6} brows="worried" {...runArms(t, 2.5)} />
            <Sweat x={1040} y={420} t={t} />
          </g>
        )}
        <rect x={60} y={60} width={600} height={110} rx={20} fill="rgba(10,10,20,0.8)" />
        <Txt x={360} y={115} size={52} color={C.gold} outline={0} shadow={false}>{`FOUND: ${labels[idx]}`}</Txt>
        {idx === 2 && <Pop t={t - 2 * seg - 0.3} x={1300} y={200} size={70} color={C.red}>OUT OF MY KITCHEN!</Pop>}
        <Vignette strength={0.3} />
      </g>
    );
  }
  return (
    <g>
      <Cam cx={900} cy={620} z={1.6}>
        <Corridor t={t} color="#d0c4a8" />
        <Hero x={900} y={feet(840, 0.62)} s={0.62} expr="frown" face={0} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
      </Cam>
      <Pop t={t - tNot - 0.4} x={960} y={150} size={90} color={C.red}>BINOCULARS FOUND: 0</Pop>
      <Vignette strength={0.4} />
    </g>
  );
};

// =================================================================== SCENE 5 — THE TERRIFYING NIGHT
export const Night: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSea = cue('The sea was');
  const tStars = cue('Just stars');
  const tTerr = cue('And terrifying');
  if (t < tSea) {
    return (
      <g>
        <Cam cx={960} cy={500} z={lerp(1.5, 1.25, prog(t, 0, tSea))}>
          <Deck t={t} night lights />
          <Hero x={960} y={feet(860, 0.62)} s={0.62} expr="worried" face={0} larm={[-0.9, 1.9]} rarm={[0.9, -1.9]} tilt={0.03 * Math.sin(t * 30)} />
          {[0, 1, 2].map((k) => {
            const ph = (t * 0.7 + k / 3) % 1;
            return <circle key={k} cx={1010 + ph * 60} cy={feet(860, 0.62) + 10 - ph * 60} r={10 + ph * 20} fill="#fff" opacity={0.5 * (1 - ph)} />;
          })}
        </Cam>
        <Pop t={t - 0.6} x={960} y={150} size={80} color="#bfe0ff">BRRRR... -2°C</Pop>
        <Vignette strength={0.55} />
      </g>
    );
  }
  if (t < tStars) {
    return (
      <g>
        <Cam cx={lerp(800, 1100, prog(t, tSea, tStars))} cy={560} z={1.0}>
          <OpenSea t={t} night lights />
        </Cam>
        <Pop t={t - tSea - 0.4} x={960} y={150} size={70} color="#bfe0ff">NO MOON · NO WAVES</Pop>
        <Vignette strength={0.5} />
      </g>
    );
  }
  const tt = t - tStars;
  return (
    <g>
      <Cam cx={960} cy={lerp(200, 520, ease(prog(tt, 0, D - tStars)))} z={lerp(0.8, 1.6, ease(prog(tt, 0, D - tStars)))}>
        <Deck t={t} night lights />
        <Hero x={960} y={feet(860, 0.62)} s={0.62} expr={t > tTerr ? 'scared' : 'o'} face={0} look={[0, -1]} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} brows={t > tTerr ? 'worried' : undefined} />
      </Cam>
      {t > tTerr && <Pop t={t - tTerr} x={960} y={840} size={80} color="#bfe0ff">BEAUTIFUL... AND TERRIFYING.</Pop>}
      <Vignette strength={0.55} />
    </g>
  );
};

export const CrowsNestShot: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSquint = cue('The lookout squinted');
  const tBell = cue('Then he grabbed');
  const tRings = cue('Three rings');
  const tAhead = cue('Iceberg, right ahead');
  const berg = ease(prog(t, tSquint, tAhead + 1));
  const ringN = t > tRings ? Math.min(3, Math.floor((t - tRings) / 0.45) + 1) : 0;
  return (
    <g>
      <Cam cx={lerp(400, 700, ease(prog(t, tSquint, tAhead)))} cy={lerp(440, 560, ease(prog(t, tSquint, tAhead)))} z={lerp(1.6, 1.0, ease(prog(t, tSquint, tAhead)))}
        shake={t > tRings ? 5 : 0} t={t}>
        <CrowsNest t={t} />
        <Iceberg x={lerp(1900, 1400, berg)} y={760} s={lerp(0.2, 0.9, berg)} night />
        <Person role="lookout" x={210} y={430} s={0.4} face={0.8} expr={t > tRings ? 'scared' : 'flat'} blink={t > tSquint && t < tBell ? 0.8 : 0} look={[1, 0]}
          larm={[0.3, 0.2]} rarm={t > tBell ? [-2.4, 0.3] : [-0.3, -0.2]} showLegs={false} />
        <Hero x={380} y={430} s={0.4} expr={t > tRings ? 'scared' : 'o'} face={0.9} look={[1, 0]} rarm={[-1.6, 1.5]} larm={[1.4, -1.5]} showLegs={false} />
        <g transform="translate(445,395)"><circle r={14} fill="#c9a040" stroke={C.ink} strokeWidth={4} /><circle cx={30} r={14} fill="#c9a040" stroke={C.ink} strokeWidth={4} /></g>
        <path d="M60,560 L520,560 L480,820 L100,820 Z" fill="#5a3a22" stroke={C.ink} strokeWidth={6} />
        <ShipBell x={130} y={500} s={0.5} swing={t > tRings ? Math.sin((t - tRings) * 14) : 0} />
      </Cam>
      {ringN > 0 && <Pop t={t - tRings - (ringN - 1) * 0.45} x={460 + ringN * 300} y={170} size={90} color={C.gold}>{'DING!'}</Pop>}
      {t > tAhead && <Burst t={t - tAhead} x={1250} y={300} r={220} label="ICEBERG, RIGHT AHEAD!" size={56} color="#ffd84d" />}
      <Vignette strength={0.55} />
    </g>
  );
};

export const Impact: React.FC<ShotProps> = ({t, D, cue}) => {
  const tShiver = cue("It didn't feel");
  const tIce = cue('Upstairs');
  if (t < tIce) {
    const scrape = ease(prog(t, 0.3, tIce));
    return (
      <g>
        <Cam cx={960} cy={560} z={lerp(1.0, 1.2, prog(t, 0, tIce))} shake={t > tShiver ? 3 : 0} t={t}>
          <rect x={-2000} y={-2000} width={6000} height={4000} fill={C.night} />
          <Stars t={t} n={200} />
          <Ship x={900} y={760} s={0.9} t={t} night lights tilt={t > tShiver ? 0.3 * Math.sin(t * 9) : 0} />
          <Iceberg x={lerp(1900, 120, scrape)} y={790} s={0.85} night />
          <Waves y={790} t={t} color="#0e1838" dark="#081028" amp={3} />
        </Cam>
        <rect x={70} y={70} width={430} height={130} rx={20} fill="rgba(10,10,20,0.8)" />
        <Txt x={285} y={135} size={74} color={C.gold} outline={0} shadow={false}>11:40 PM</Txt>
        {t > tShiver + 0.5 && <Pop t={t - tShiver - 0.5} x={1200} y={150} size={70} font={HAND} outline={6}>*a long, slow shiver*</Pop>}
        <Vignette strength={0.55} />
      </g>
    );
  }
  const tt = t - tIce;
  return (
    <g>
      <Cam cx={960} cy={520} z={1.25}>
        <Deck t={t} night lights />
        {[0, 1, 2, 3, 4, 5, 6].map((k) => (
          <rect key={k} x={700 + k * 90} y={830 + (k % 2) * 20} width={40} height={30} fill="#dff4ff" stroke={C.ink} strokeWidth={3} transform={`rotate(${k * 23} ${720 + k * 90} 845)`} />
        ))}
        <Person role="gent" seed={2} x={620} y={feet(860, 0.6)} s={0.6} face={0.6} expr="laugh" larm={[0.3, 0.2]} rarm={[-2.0 + Math.sin(t * 6) * 0.4, 0.6]} />
        <Person role="girl" x={1250} y={feet(860, 0.45)} s={0.45} face={-0.6} expr="happy" larm={[2.4, 0.3]} rarm={[-2.4, -0.3]} />
        <Hero x={1500} y={feet(860, 0.62)} s={0.62} expr="worried" face={-0.8} brows="worried" />
      </Cam>
      <Pop t={tt - 0.4} x={960} y={150} size={64} font={HAND} outline={6}>Some passengers didn't realise the danger yet</Pop>
      <Vignette strength={0.55} />
    </g>
  );
};

export const Harder: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTV = cue('Changing history is');
  const tHelp = cue('I knew the ending');
  if (t < tHelp) {
    const ch = Math.floor(t * 2.5) % 3;
    return (
      <g>
        <Cam cx={960} cy={440} z={2.1}>
          <Deck t={t} night lights />
          <Hero x={960} y={feet(860, 0.62)} s={0.62} expr="frown" face={0} look={[0, 0.5]} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        </Cam>
        {t > tTV && (
          <g transform={`translate(1480,300) scale(${backOut(prog(t, tTV, tTV + 0.4), 1.6)})`}>
            <rect x={-170} y={-120} width={340} height={240} rx={24} fill="#3a3a44" stroke={C.ink} strokeWidth={8} />
            <rect x={-140} y={-95} width={280} height={190} rx={10} fill={['#ff8a5a', '#5ad8a0', '#8a7aff'][ch]} stroke={C.ink} strokeWidth={5} />
            <Txt x={0} y={0} size={50} color="#fff" outline={5}>{`CH ${ch + 1}`}</Txt>
            <line x1={0} y1={120} x2={-60} y2={180} stroke={C.ink} strokeWidth={8} />
            <line x1={0} y1={120} x2={60} y2={180} stroke={C.ink} strokeWidth={8} />
            <line x1={-200} y1={-150} x2={200} y2={150} stroke={C.red} strokeWidth={18} />
          </g>
        )}
        <Vignette strength={0.55} />
      </g>
    );
  }
  const tt = t - tHelp;
  return (
    <g>
      <Cam cx={960} cy={lerp(440, 520, ease(prog(tt, 0, 2)))} z={lerp(2.1, 1.3, ease(prog(tt, 0, 2)))}>
        <Deck t={t} night lights />
        <Hero x={960} y={feet(860, 0.62)} s={0.62} expr={t > cue('All I could do') ? 'flat' : 'frown'} face={0.4} brows={t > cue('All I could do') ? 'angry' : 'worried'}
          larm={[0.3, 0.2]} rarm={t > cue('All I could do') ? [-2.4, 1.4] : [-0.3, -0.2]} />
      </Cam>
      {t > cue('All I could do') && <Pop t={t - cue('All I could do') - 0.4} x={960} y={840} size={90} color={C.gold}>TIME TO HELP.</Pop>}
      <Vignette strength={0.5} />
    </g>
  );
};

// =================================================================== SCENE 6 — AN UNEXPECTED HERO
export const Help1: React.FC<ShotProps> = ({t, D, cue}) => {
  const tKnock = cue('I knocked');
  const tShow = cue('I showed');
  if (t < tShow) {
    const hx = lerp(300, 1500, prog(t, 0, tShow));
    const knock = Math.sin(t * 14) > 0.3;
    return (
      <g>
        <Cam cx={hx + 100} cy={540} z={1.15}>
          <Corridor t={t} color="#d8ccb0" />
          <Hero x={hx} y={feet(840, 0.62)} s={0.62} expr="flat" brows="angry" face={0.9} walk={t > tKnock ? undefined : t * 1.5}
            rarm={t > tKnock && knock ? [-1.6, 0.2] : [-1.3, 0.4]} bodyExtra={<LifeJacket />} />
          {[0, 1, 2].map((k) => {
            const tc = tKnock + 0.8 + k * 1.1;
            if (t < tc) return null;
            return <Person key={k} role={['mum', 'gent', 'lady'][k] as 'mum'} seed={k} jacket x={hx - 300 - k * 180} y={feet(840, 0.6)} s={0.6}
              face={0.8} expr="worried" walk={t * 1.4} />;
          })}
        </Cam>
        {t > tKnock && <Pop t={t - tKnock} x={960} y={150} size={80} hold={2.5}>KNOCK KNOCK!</Pop>}
        {t > tKnock + 2.5 && <Pop t={t - tKnock - 2.5} x={960} y={250} size={70} color={C.gold}>PUT ON YOUR LIFE JACKETS!</Pop>}
        <Vignette strength={0.4} />
      </g>
    );
  }
  const tt = t - tShow;
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#c99a62" />
      <GrandStaircase t={t} />
      {[0, 1, 2, 3].map((k) => (
        <Person key={k} role={(['mum', 'girl', 'gent', 'oldman'] as const)[k]} seed={k} jacket x={lerp(600 + k * 120, 900 + k * 60, prog(tt, 0, D - tShow))} y={lerp(560, 300, prog(tt, 0, D - tShow)) + k * 30}
          s={k === 1 ? 0.35 : 0.42} face={0.6} expr="worried" walk={t * 1.3 + k} />
      ))}
      <Hero x={1300} y={feet(1000, 0.5)} s={0.5} expr="flat" brows="angry" face={-0.6} larm={[0.3, 0.2]} rarm={[-2.4, 0.9]} bodyExtra={<LifeJacket />} />
      <Pop t={tt - 0.3} x={960} y={140} size={70} color={C.gold}>THIS WAY, TO THE BOAT DECK!</Pop>
      <Vignette strength={0.4} />
    </g>
  );
};

export const Help2: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSay = cue('So I kept');
  const tSeat = cue('Every seat counts');
  return (
    <g>
      <Cam cx={lerp(700, 1000, prog(t, 0, D))} cy={lerp(400, 520, prog(t, 0, D))} z={lerp(0.85, 1.2, prog(t, 0, D))}>
        <Deck t={t} night lights davits={ease(prog(t, 0.5, tSay)) * 0.4} />
        <Person role="officer" x={500} y={feet(860, 0.6)} s={0.6} face={0.6} expr="flat" larm={[0.3, 0.2]} rarm={[-2.0, 0.5]} />
        {[0, 1, 2].map((k) => (
          <Person key={k} role={(['lady', 'mum', 'gent'] as const)[k]} seed={k + 1} jacket x={1200 + k * 170 - ease(prog(t, tSeat + k * 0.6, tSeat + 1.5 + k * 0.6)) * 400} y={feet(860, 0.58)} s={0.58}
            face={-0.6} expr={t > tSeat ? 'worried' : 'o'} walk={t > tSeat ? t * 1.3 : undefined} />
        ))}
        <Hero x={900} y={feet(860, 0.62)} s={0.62} expr="flat" brows="worried" face={0.8} look={[1, 0]} larm={[0.3, 0.2]} rarm={[-1.6 + 0.3 * Math.sin(t * 5), 0.1]} bodyExtra={<LifeJacket />} />
      </Cam>
      {t < tSay && <Pop t={t - 0.6} x={960} y={150} size={66} color="#bfe0ff">LIFEBOAT 7: 28 PEOPLE · 65 SEATS</Pop>}
      {t > tSeat && <Pop t={t - tSeat} x={960} y={840} size={96} color={C.gold}>EVERY SEAT COUNTS.</Pop>}
      <Vignette strength={0.5} />
    </g>
  );
};

export const Help3: React.FC<ShotProps> = ({t, D, cue}) => {
  const tCoat = cue('I gave my coat');
  const tBand = cue('And all around us');
  if (t < tCoat) {
    const meet = ease(prog(t, 1.2, tCoat - 0.5));
    return (
      <g>
        <Cam cx={960} cy={520} z={1.3}>
          <Deck t={t} night lights />
          <Person role="girl" x={lerp(900, 1180, meet)} y={feet(860, 0.42)} s={0.42} face={0.8} expr={meet > 0.95 ? 'happy' : 'worried'} brows={meet > 0.95 ? undefined : 'worried'}
            walk={meet > 0 && meet < 1 ? t * 1.6 : undefined} larm={meet > 0.95 ? [2.4, 0.3] : [0.3, 0.2]} rarm={meet > 0.95 ? [-2.4, -0.3] : [-0.3, -0.2]} jacket />
          <Person role="mum" x={1400} y={feet(860, 0.6)} s={0.6} face={-0.8} expr={meet > 0.9 ? 'happy' : 'worried'} larm={[0.3, 0.2]} rarm={meet > 0.9 ? [-1.5, 0.4] : [-0.3, -0.2]} jacket />
          <Hero x={720} y={feet(860, 0.62)} s={0.62} expr="smile" face={0.8} larm={[0.3, 0.2]} rarm={[-1.4, 0.2]} bodyExtra={<LifeJacket />} />
          {meet > 0.95 && <Txt x={1300} y={300} size={70} color={C.red} font={HAND} outline={4}>♥</Txt>}
        </Cam>
        <Vignette strength={0.5} />
      </g>
    );
  }
  if (t < tBand) {
    return (
      <g>
        <Cam cx={960} cy={480} z={1.6}>
          <Deck t={t} night lights />
          <Person role="oldman" x={1120} y={feet(860, 0.6)} s={0.6} face={-0.7} expr="smile" larm={[-0.9, 1.9]} rarm={[0.9, -1.9]} body="#7a5a3a" />
          <Hero x={820} y={feet(860, 0.62)} s={0.62} expr="smile" face={0.8} rarm={[-1.5, 0.3]} />
        </Cam>
        <Vignette strength={0.5} />
      </g>
    );
  }
  const tt = t - tBand;
  return (
    <g>
      <Cam cx={960} cy={500} z={1.15}>
        <Deck t={t} night lights />
        {[0, 1, 2, 3].map((k) => (
          <g key={k}>
            <Person role="band" seed={k} x={600 + k * 240} y={feet(860, 0.55)} s={0.55} face={0.3} expr="sleep" blink={1}
              larm={[-0.8 + Math.sin(t * 4 + k) * 0.1, 1.9]} rarm={[0.6 + Math.sin(t * 6 + k) * 0.3, -1.5]} />
            <path d={`M${600 + k * 240 - 60},${feet(860, 0.55) + 120} l40,-20 l12,40 Z`} fill="#8a4a1a" stroke={C.ink} strokeWidth={3} />
          </g>
        ))}
        {[0, 1, 2, 3, 4].map((k) => {
          const ph = (t * 0.5 + k / 5) % 1;
          return <Txt key={k} x={600 + k * 200 + ph * 40} y={400 - ph * 200} size={60} color="#fff" font="DejaVu Sans, sans-serif" outline={4} opacity={1 - ph}>♪</Txt>;
        })}
      </Cam>
      <Pop t={tt - 0.5} x={960} y={840} size={60} font={HAND} outline={6}>The ship's band played to keep everyone calm.</Pop>
      <Vignette strength={0.5} />
    </g>
  );
};

export const Respect: React.FC<ShotProps> = ({t, D, cue}) => {
  const tLost = cue('More than fifteen');
  const tCarp = cue('The ship Carpathia');
  const tSad = cue("It's one of");
  const tRule = cue('After the Titanic');
  const dawn = prog(t, tCarp, tCarp + 4);
  const textCol = '#f2f2f2';
  // camera beats: wide -> lifeboat close-up -> Carpathia -> wreath close-up -> wide dawn
  const seg = t < tLost ? 0 : t < tCarp ? 1 : t < tSad ? 2 : t < tRule ? 3 : 4;
  const targets: [number, number, number][] = [[960, 560, 1.0], [520, 700, 2.0], [1500, 640, 1.6], [1000, 860, 2.4], [960, 560, 1.0]];
  const starts = [0, tLost, tCarp, tSad, tRule];
  const prev = targets[Math.max(0, seg - 1)];
  const k = ease(prog(t, starts[seg], starts[seg] + 1.6));
  const cam = seg === 0 ? targets[0] : ([0, 1, 2].map((i2) => lerp(prev[i2], targets[seg][i2], k)) as [number, number, number]);
  const drift = (t - starts[seg]) * 6;
  const carpX = lerp(2300, 1650, ease(prog(t, tCarp, tSad)));
  return (
    <g>
      <Cam cx={cam[0] + drift} cy={cam[1]} z={cam[2]}>
        <LifeboatSea t={t} dawn={dawn} />
        {t < tLost && <Ship x={1500} y={680} s={0.25 * (1 - prog(t, 0.5, tLost))} t={t} night lights={false} smoke={false} tilt={-8 * prog(t, 0.5, tLost)} />}
        {t > tCarp - 0.5 && (
          <g opacity={prog(t, tCarp - 0.5, tCarp + 1)}>
            <Ship x={carpX} y={690} s={0.22} t={t} lights smoke />
            <Txt x={carpX} y={540} size={40} color={C.gold} outline={5}>RMS CARPATHIA</Txt>
          </g>
        )}
        {[0, 1, 2].map((kk) => (
          <Lifeboat key={kk} x={300 + kk * 520} y={760 + (kk % 2) * 40} s={0.35} t={t + kk}>
            {[0, 1, 2].map((p2) => (
              <Doodle key={p2} x={-150 + p2 * 150} y={-200} s={0.32} cap={false} expr="sleep" blink={1} face={0} showLegs={false}
                body="#9a6a4a" larm={[-0.9, 1.9]} rarm={[0.9, -1.9]} />
            ))}
          </Lifeboat>
        ))}
        {/* memorial wreath on the water */}
        <g transform={`translate(1000,${880 + Math.sin(t * 1.4) * 5}) scale(1,0.45)`} opacity={prog(t, tSad - 1, tSad)}>
          {Array.from({length: 14}).map((_, l) => {
            const a = (l * Math.PI * 2) / 14;
            return <ellipse key={l} cx={Math.cos(a) * 80} cy={Math.sin(a) * 80} rx={26} ry={14} fill="#4e8a3e" stroke={C.ink} strokeWidth={4}
              transform={`rotate(${(a * 180) / Math.PI + 90} ${Math.cos(a) * 80} ${Math.sin(a) * 80})`} />;
          })}
          {[0, 1, 2, 3, 4, 5].map((l) => {
            const a = (l * Math.PI * 2) / 6 + 0.3;
            return <circle key={l} cx={Math.cos(a) * 80} cy={Math.sin(a) * 80} r={16} fill="#f2f2f2" stroke={C.ink} strokeWidth={4} />;
          })}
        </g>
      </Cam>
      <rect x={0} y={0} width={W} height={H} fill="#000" opacity={0.22} />
      <Txt x={960} y={180} size={64} color={textCol} outline={0} opacity={fadeWin(t, 0.5, tLost - 0.2, 0.5)}>2:20 AM · 15 APRIL 1912</Txt>
      <Txt x={960} y={180} size={64} color={textCol} outline={0} opacity={fadeWin(t, tLost, tCarp - 0.2, 0.5)}>MORE THAN 1,500 LIVES LOST</Txt>
      <Txt x={960} y={180} size={60} color={textCol} outline={0} opacity={fadeWin(t, tCarp, tSad - 0.2, 0.5)}>ABOUT 705 SURVIVORS RESCUED</Txt>
      <Txt x={960} y={180} size={56} color={textCol} outline={0} opacity={fadeWin(t, tSad, tRule - 0.2, 0.5)}>IN MEMORY OF ALL WHO WERE ON BOARD</Txt>
      <Txt x={960} y={180} size={52} color={C.gold} outline={0} opacity={fadeWin(t, tRule, D + 1, 0.5)}>1914: LIFEBOATS FOR EVERYONE ON BOARD</Txt>
      <Vignette strength={0.5} />
    </g>
  );
};

// =================================================================== SCENE 7 — THE FINAL TWIST
export const Return: React.FC<ShotProps> = ({t, D, cue}) => {
  const tSpin = cue('The dials spun');
  const tHome = cue('Sitting on my bedroom');
  if (t < tSpin + 1.2) {
    const buzz = prog(t, cue('I felt', 0.5), tSpin);
    return (
      <g>
        <Cam cx={960} cy={560} z={1.4} shake={buzz * 4} t={t}>
          <LifeboatSea t={t} dawn={0.8} />
          <Lifeboat x={960} y={820} s={1.0} t={t}>
            <Person role="oldman" x={-180} y={-150} s={0.4} face={0.6} expr="sleep" blink={1} showLegs={false} body="#7a5a3a" />
            <Hero x={80} y={-160} s={0.42} expr={buzz > 0.3 ? 'shock' : 'flat'} face={0.3} showLegs={false} bodyExtra={<Blanket />} />
            <TimeMachine x={200} y={-50} s={0.2} t={t} glow={buzz} shake={buzz} screen="2026" />
          </Lifeboat>
        </Cam>
        {buzz > 0.2 && <Pop t={t - cue('I felt', 0.5)} x={1450} y={200} size={80} color={C.gold}>BZZZZ!</Pop>}
        <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={prog(t, tSpin + 0.6, tSpin + 1.2)} />
      </g>
    );
  }
  const tt = t - tSpin - 1.2;
  const land = easeOut(prog(tt, 0, 0.4));
  return (
    <g>
      <Cam cx={960} cy={560} z={1.1}>
        <Bedroom t={t} />
        <ellipse cx={900} cy={905} rx={lerp(60, 200, prog(tt, 0.4, 3))} ry={lerp(12, 34, prog(tt, 0.4, 3))} fill="#8ad0ff" opacity={0.7} stroke={C.ink} strokeWidth={3} />
        <Hero x={900} y={lerp(-300, feet(900, 0.62), land)} s={0.62} expr="o" face={0} squash={tt > 0.4 ? -0.15 * Math.exp(-(tt - 0.4) * 6) : 0}
          larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        {[0, 1, 2].map((k) => <Sweat key={k} x={850 + k * 50} y={feet(900, 0.62) - 40 + k * 15} s={0.7} t={t + k * 0.4} />)}
        <TimeMachine x={1250} y={900} s={0.45} t={t} screen="HOME" />
      </Cam>
      <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={1 - prog(tt, 0, 0.4)} />
      {t > tHome && <Pop t={t - tHome - 0.5} x={960} y={150} size={84} color="#8ad0ff">*SOAKING WET*</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Promise: React.FC<ShotProps> = ({t, D, cue}) => {
  const tNo = cue('No more time travel');
  const tCloset = cue("I'm putting you");
  return (
    <g>
      <Cam cx={t < tCloset ? 1000 : lerp(1000, 1500, ease(prog(t, tCloset, D)))} cy={520} z={t < tNo ? 1.6 : 1.3}>
        <Bedroom t={t} />
        <Hero x={t < tCloset ? 900 : lerp(900, 1450, prog(t, tCloset, D))} y={feet(900, 0.62)} s={0.62} expr={t > tNo ? 'flat' : 'frown'} brows="angry" face={t < tCloset ? 0.4 : 0.9}
          walk={t > tCloset ? t * 1.3 : undefined} larm={t > tNo && t < tCloset ? [2.6, 0.1] : [-1.1, 1.7]} rarm={[1.1, -1.7]} />
        <TimeMachine x={t < tCloset ? 1010 : lerp(1010, 1560, prog(t, tCloset, D))} y={feet(900, 0.62) + 260} s={0.28} t={t} screen="..." />
      </Cam>
      {t > tNo && <Pop t={t - tNo} x={960} y={150} size={96} color={C.gold} hold={tCloset - tNo}>NEVER. AGAIN.</Pop>}
      {t > tCloset && <Pop t={t - tCloset} x={960} y={150} size={70} font={HAND} outline={6}>*solemn promise*</Pop>}
      <Vignette strength={0.3} />
    </g>
  );
};

export const Click: React.FC<ShotProps> = ({t, D, cue}) => {
  const tScreen = cue('The screen lit up');
  const tClick = cue('And then I tripped', 0.85);
  if (t < tScreen) {
    const trip = prog(t, 1.0, 2.4);
    return (
      <g>
        <Cam cx={1350} cy={600} z={1.3}>
          <Bedroom t={t} />
          <Hero x={lerp(1150, 1380, trip)} y={feet(900, 0.62) + 260 * easeIn(trip)} s={0.62} expr={trip > 0.2 ? 'scared' : 'smile'} face={0.9}
            tilt={1.4 * easeIn(trip)} walk={trip < 0.2 ? t * 1.3 : undefined} larm={trip > 0.2 ? [2.4, 0.4] : [0.3, 0.2]} rarm={trip > 0.2 ? [-2.4, -0.4] : [-0.3, -0.2]} />
          <TimeMachine x={1500} y={900} s={0.35} t={t} screen={t > tClick ? '!!!' : ''} />
        </Cam>
        {t > tClick && <Pop t={t - tClick} x={1200} y={250} size={70} font={HAND} outline={6}>*click*</Pop>}
        <Vignette strength={0.35} />
      </g>
    );
  }
  const tt = t - tScreen;
  return (
    <g>
      <rect x={0} y={0} width={W} height={H} fill="#1a1020" />
      <g transform={`translate(${W / 2},${H / 2 + 100}) scale(${lerp(1.6, 2.6, ease(prog(tt, 0, 2)))})`}>
        <TimeMachine x={0} y={130} s={1} t={t} screen="POMPEII AD 79" screenColor="#ff8a3a" glow={1} shake={0.3} />
      </g>
      <Pop t={tt - 1.0} x={960} y={140} size={110} color="#ff8a3a">POMPEII — AD 79</Pop>
      <Vignette strength={0.5} />
    </g>
  );
};

export const Scream: React.FC<ShotProps> = ({t, D}) => (
  <g>
    <PompeiiScreen t={t} />
    <Cam cx={960} cy={780} z={lerp(1.15, 1.35, easeOut(prog(t, 0, 0.4)))} shake={14} t={t}>
      <Hero x={960} y={feet(1100, 0.8)} s={0.8} expr="scared" face={0} brows="worried" larm={[2.7, 0.2]} rarm={[-2.7, -0.2]} capOff={Math.sin(prog(t, 0.1, 1.6) * Math.PI) * 1.4} />
    </Cam>
    <Pop t={t} x={960} y={150} size={120} color={C.red} rot={-3}>ARE YOU KIDDING ME?!</Pop>
    <Vignette strength={0.45} />
  </g>
);

export const Outro: React.FC<ShotProps> = ({t, D}) => (
  <g>
    <Spiral t={t} />
    <Hero x={960} y={lerp(1400, 420, easeOut(prog(t, 0, 0.5)))} s={1.05} expr="grin" face={0} larm={[0.3, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 7), 0.4]} />
    <Pop t={t - 0.3} x={960} y={110} size={78}>SUBSCRIBE TO HISTORY WORLD</Pop>
    <Pop t={t - 1.4} x={960} y={840} size={64} color={C.gold}>TO SEE WHAT HAPPENS NEXT!</Pop>
  </g>
);

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

export const EndCard: React.FC<ShotProps> = ({t, D}) => {
  const tb = t - 1.0;
  const kk = tb > 0 ? backOut(clamp(tb / 0.4), 2) * (1 + 0.05 * Math.sin(t * 6)) : 0;
  const u = ease(prog(tb, 1.0, 1.6));
  return (
    <g>
      <Spiral t={t} />
      <Confetti t={t} n={60} />
      <Hero x={420} y={lerp(1400, 470, easeOut(prog(t, 0, 0.6)))} s={0.85} expr="grin" face={0.4} larm={[0.3, 0.2]} rarm={[-2.6 + 0.3 * Math.sin(t * 7), 0.5]} />
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
      <Txt x={1150} y={830} size={52} font={HAND} outline={5} opacity={ease(prog(t, 1.8, 2.4))}>Next time: Pompeii, AD 79. What could go wrong?</Txt>
      <rect x={0} y={0} width={W} height={H} fill="#000" opacity={prog(t, D - 0.8, D)} />
    </g>
  );
};

export const SHOTS: Record<string, React.FC<ShotProps>> = {
  hook: Hook, title: Title, market: Market, buy: Buy, travel: Travel, aboard: Aboard, luxury: Luxury, realize: Realize, fact1: Fact1,
  warn1: Warn1, warn2: Warn2, warn3: Warn3, fact2: Fact2, napkin: Napkin, captain: Captain, conv1: Conv1, conv2: Conv2,
  binoculars: Binoculars, lost: Lost, night: Night, crowsnest: CrowsNestShot, impact: Impact, harder: Harder, help1: Help1,
  help2: Help2, help3: Help3, respect: Respect, return: Return, promise: Promise, click: Click, scream: Scream, outro: Outro,
  endcard: EndCard,
};

// silence unused-import lint for helpers kept for future scenes
void [Star, TITLE, Sky, Confetti];
