// Vertical (1080x1920) scenes for the Short. Reuses the long-form assets: the hero, cast, ship, time machine,
// bedroom, vortex and comic effects; adds a 1912 harbour background.
import React from 'react';
import {C, blinkAt, clamp, ease, easeIn, easeOut, lerp, prog, rng, backOut} from '../lib';
import {Doodle, DoodleProps, Person} from '../Hero';
import {Burst, DizzyStars, Glow, HAND, Pop, Sparkle, SpeedLines, Sweat, Txt, TITLE} from '../fx';
import {Ship, Stars, TimeMachine, Waves, Iceberg} from '../props';
import {Bedroom, Cloud, Vortex} from '../bg';

export const VW = 1080;
export const VH = 1920;
export type Cue = (text: string, frac?: number) => number;
export type ShotProps = {t: number; D: number; cue: Cue};

const feet = (yFeet: number, s: number) => yFeet - 456 * s;
const Hero: React.FC<DoodleProps> = (p) => <Doodle blink={blinkAt(p.walk ?? p.x * 0.01)} {...p} />;

/** vertical camera */
const VCam: React.FC<{cx: number; cy: number; z?: number; rot?: number; shake?: number; t?: number; children: React.ReactNode}> = ({
  cx, cy, z = 1, rot = 0, shake = 0, t = 0, children,
}) => {
  const sx = shake * (Math.sin(t * 47) + Math.sin(t * 31)) * 0.5;
  const sy = shake * (Math.cos(t * 53) + Math.sin(t * 37)) * 0.5;
  return <g transform={`translate(${VW / 2 + sx},${VH / 2 + sy}) rotate(${rot}) scale(${z}) translate(${-cx},${-cy})`}>{children}</g>;
};

const VVignette: React.FC<{s?: number}> = ({s = 0.5}) => (
  <g>
    <defs>
      <radialGradient id={`vv${Math.round(s * 100)}`} cx="50%" cy="50%" r="70%">
        <stop offset="50%" stopColor="#000" stopOpacity={0} />
        <stop offset="100%" stopColor="#000" stopOpacity={s} />
      </radialGradient>
    </defs>
    <rect x={0} y={0} width={VW} height={VH} fill={`url(#vv${Math.round(s * 100)})`} />
  </g>
);

const Flash: React.FC<{a: number}> = ({a}) => (a > 0 ? <rect x={0} y={0} width={VW} height={VH} fill="#fff" opacity={clamp(a)} /> : null);

/** swirling time portal */
export const Portal: React.FC<{x: number; y: number; r: number; t: number}> = ({x, y, r, t}) => {
  if (r < 2) return null;
  return (
    <g transform={`translate(${x},${y})`}>
      <Glow id={`pg${Math.round(x)}${Math.round(y)}`} x={0} y={0} r={r * 1.9} color="#8ad8ff" a={0.7} />
      {[0, 1, 2, 3, 4, 5].map((k) => {
        const rr = r * (1 - k * 0.13);
        const a0 = t * (3 + k) * (k % 2 ? 1 : -1) * 57.3;
        return (
          <path key={k} transform={`rotate(${a0}) scale(1,1.2)`} d={`M${rr},0 A${rr},${rr} 0 1 1 0,${-rr}`} fill="none"
            stroke={['#6ad0ff', '#ffd84d', '#b88aff'][k % 3]} strokeWidth={20 - k * 2} strokeLinecap="round" />
        );
      })}
      <ellipse cx={0} cy={0} rx={r * 0.36} ry={r * 0.46} fill="#fff" opacity={0.95} />
    </g>
  );
};

/** Southampton quay, 1912 (world coords: quay edge at y=1240, quay floor down to 2400) */
const Harbour: React.FC<{t: number; ship?: boolean; crowd?: boolean; sunset?: number}> = ({t, ship = true, crowd = true, sunset = 0}) => {
  const top = sunset ? '#ff9a5a' : '#5ab8f0';
  const bot = sunset ? '#ffe0a0' : '#dff3fb';
  const R = rng(7);
  return (
    <g>
      <defs>
        <linearGradient id="hbsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor={top} />
          <stop offset="1" stopColor={bot} />
        </linearGradient>
      </defs>
      <rect x={-3000} y={-3000} width={9000} height={6000} fill="url(#hbsky)" />
      {[0, 1, 2].map((i) => <Cloud key={i} x={((i * 900 + t * 25) % 3600) - 1200} y={-200 + i * 160} s={1.2} />)}
      {/* cranes + warehouses on the far side */}
      {[-900, 2300].map((cx) => (
        <g key={cx}>
          <rect x={cx - 25} y={300} width={50} height={950} fill="#5a4a3a" stroke={C.ink} strokeWidth={6} />
          <line x1={cx} y1={320} x2={cx + (cx < 0 ? 520 : -520)} y2={260} stroke={C.ink} strokeWidth={22} />
          <line x1={cx + (cx < 0 ? 480 : -480)} y1={268} x2={cx + (cx < 0 ? 480 : -480)} y2={520} stroke={C.ink} strokeWidth={4} />
        </g>
      ))}
      {ship && <Ship x={1150} y={1210} s={1.7} t={t} />}
      <Waves y={1200} t={t} amp={8} x0={-3000} x1={5000} />
      {/* quay */}
      <rect x={-3000} y={1240} width={9000} height={1400} fill="#a8a296" stroke={C.ink} strokeWidth={6} />
      {Array.from({length: 40}).map((_, k) => <line key={k} x1={-2000 + k * 160} y1={1240} x2={-2300 + k * 160} y2={2600} stroke="#8e887c" strokeWidth={4} />)}
      <rect x={-3000} y={1240} width={9000} height={40} fill="#7a7468" stroke={C.ink} strokeWidth={5} />
      {[-200, 500, 1300, 2000].map((bx) => (
        <g key={bx}>
          <rect x={bx - 30} y={1250} width={60} height={70} rx={14} fill="#3a3a40" stroke={C.ink} strokeWidth={5} />
          <ellipse cx={bx} cy={1250} rx={44} ry={14} fill="#3a3a40" stroke={C.ink} strokeWidth={5} />
        </g>
      ))}
      {/* gangway */}
      {ship && <polygon points="1500,1240 1660,1240 1760,880 1700,880" fill="#8a5a2b" stroke={C.ink} strokeWidth={6} />}
      {/* luggage + crowd at the back */}
      {crowd && Array.from({length: 9}).map((_, k) => {
        const role = (['gent', 'lady', 'gent', 'mum', 'lady', 'oldman', 'gent', 'lady', 'sailor'] as const)[k];
        const x = -300 + k * 230 + R() * 40;
        return <Person key={k} role={role} seed={k} x={x} y={feet(1520, 0.42)} s={0.42} face={k % 2 ? 0.6 : -0.6}
          expr={k % 3 ? 'smile' : 'happy'} larm={[0.3, 0.2]} rarm={k % 4 === 0 ? [-2.5 + 0.3 * Math.sin(t * 6 + k), 0.3] : [-0.3, -0.2]} showLegs={false} />;
      })}
      {crowd && [[200, 1560], [900, 1580]].map(([lx, ly], k) => (
        <g key={k}>
          <rect x={lx - 70} y={ly - 60} width={140} height={90} rx={10} fill="#8a5a2b" stroke={C.ink} strokeWidth={5} />
          <rect x={lx - 40} y={ly - 80} width={80} height={20} rx={8} fill="#6b4428" stroke={C.ink} strokeWidth={4} />
        </g>
      ))}
    </g>
  );
};

// ------------------------------------------------------------------ scene 1: hook (bedroom -> portal)
export const SHook: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWorst = cue('Worst decision');
  const press = easeIn(prog(t, 0.5, 0.9));
  const pr = 320 * easeOut(prog(t, 1.0, 2.0));
  const pull = easeIn(prog(t, 2.6, 4.4));
  const hx = lerp(960, 1000, pull);
  const hy = lerp(feet(900, 0.66), 520, pull);
  return (
    <g>
      <VCam cx={lerp(1030, 1000, pull)} cy={lerp(660, 560, ease(prog(t, 1, 3)))} z={lerp(1.45, 1.3, prog(t, 0, D))} shake={pr > 50 ? 6 : 0} t={t}>
        <Bedroom t={t} />
        <TimeMachine x={1140} y={900} s={0.5} t={t} glow={press} shake={press * 0.6} screen={press > 0.5 ? '1912' : '$5'} />
        <Portal x={1000} y={500} r={pr} t={t} />
        <g opacity={1 - prog(t, 4.2, 4.6)}>
          <Hero x={hx} y={hy} s={0.66 * (1 - 0.7 * pull)} expr={press < 0.5 ? 'grin' : 'scared'} face={0.6} look={[1, press > 0.5 ? -1 : 0.4]}
            tilt={pull * 6} larm={pull > 0 ? [2.5, 0.3] : [0.3, 0.2]} rarm={pull > 0 ? [-2.5, -0.3] : [lerp(-1.2, -1.45, press), lerp(0.4, 0.6, press)]}
            legs={pull > 0 ? [0.6, -0.6] : [0, 0]} brows={press > 0.5 ? 'worried' : undefined} />
        </g>
        {pull > 0 && <SpeedLines x={1000} y={600} n={6} len={300} color="#fff" seed={Math.floor(t * 10)} />}
      </VCam>
      <Pop t={t - 0.1} x={540} y={330} size={100} color={C.gold} hold={tWorst - 0.2}>$5 TIME MACHINE</Pop>
      {t > 0.75 && t < 1.6 && <Burst t={t - 0.75} x={780} y={560} r={120} label="CLICK!" size={56} />}
      {t > tWorst && <Pop t={t - tWorst} x={540} y={330} size={84} color={C.red} rot={-3}>WORST DECISION EVER!</Pop>}
      <Flash a={prog(t, D - 0.3, D)} />
      <VVignette s={0.45} />
    </g>
  );
};

// ------------------------------------------------------------------ scene 2: time travel -> harbour, ticket
export const STravel: React.FC<ShotProps> = ({t, D, cue}) => {
  const tTen = cue('Ten seconds');
  if (t < 1.4) {
    return (
      <g>
        <g transform={`translate(${VW / 2 - 960 * 1.8},${VH / 2 - 540 * 1.8}) scale(1.8)`}>
          <Vortex t={t + 3} />
        </g>
        <g transform={`translate(${540 + 160 * Math.sin(t * 2)},${900}) rotate(${t * 300})`}>
          <Doodle x={0} y={-150} s={0.7} expr="shock" face={0} larm={[2.4, 0.5]} rarm={[-2.4, -0.5]} legs={[0.5, -0.5]} />
        </g>
        <rect x={VW / 2 - 230} y={240} width={460} height={130} rx={30} fill="rgba(5,3,16,0.75)" stroke={C.gold} strokeWidth={5} />
        <Txt x={VW / 2} y={305} size={90} color={C.gold} outline={0} shadow={false}>{String(Math.round(lerp(2026, 1912, ease(prog(t, 0.1, 1.3)))))}</Txt>
        <Flash a={1 - prog(t, 0, 0.25)} />
        <VVignette s={0.6} />
      </g>
    );
  }
  const tt = t - 1.4;
  const fall = easeIn(prog(tt, 0.15, 0.75));
  const landed = tt > 0.75;
  const sq = landed ? -0.2 * Math.exp(-(tt - 0.75) * 6) : 0;
  const tTicket = 3.9;
  const give = ease(prog(tt, 2.2, 3.0));
  const showTicket = tt > tTicket;
  return (
    <g>
      <VCam cx={showTicket ? 640 : lerp(560, 700, prog(tt, 0, tTicket))} cy={showTicket ? 1260 : lerp(1180, 1300, prog(tt, 0, 1.5))} z={showTicket ? 1.6 : 0.95}>
        <Harbour t={t} />
        <Portal x={560} y={900} r={260 * (1 - prog(tt, 0.9, 1.4))} t={t} />
        <Hero x={560} y={lerp(900, feet(1760, 0.62), fall)} s={0.62} squash={sq} expr={landed && tt < 2.2 ? 'worried' : landed ? 'o' : 'shock'}
          face={landed && tt > 2.0 ? 0.8 : 0} look={tt > 2.0 ? [1, 0] : [0, 0]} tilt={landed ? 0 : tt * 4} larm={[0.3, 0.2]}
          rarm={give > 0.8 ? [-1.5, 0.3] : [-0.3, -0.2]} />
        {landed && tt < 2.2 && <DizzyStars x={560} y={feet(1760, 0.62) - 100} r={110} t={t} />}
        <Person role="sailor" x={lerp(1300, 820, easeOut(prog(tt, 1.4, 2.4)))} y={feet(1760, 0.62)} s={0.62} face={-0.7} expr="smile"
          walk={tt > 1.4 && tt < 2.4 ? t * 1.6 : undefined} rarm={give > 0 ? [-1.5, 0.3] : [-0.3, -0.2]} />
        {give > 0 && (
          <g transform={`translate(${lerp(790, 700, give)},${feet(1760, 0.62) + 170}) rotate(-8)`}>
            <rect x={-40} y={-26} width={80} height={52} rx={4} fill="#f1dfa8" stroke={C.ink} strokeWidth={4} />
          </g>
        )}
      </VCam>
      {landed && tt < 1.8 && <Burst t={tt - 0.75} x={300} y={520} r={120} label="BONK!" size={56} />}
      {t > tTen && <Pop t={t - tTen} x={540} y={330} size={110} color={C.gold} hold={tTicket + 1.4 - (t - tt) - tTen + 1.4}>1912!</Pop>}
      {showTicket && (
        <g transform={`translate(540,620) rotate(${-4 + Math.sin(t * 3)}) scale(${backOut(prog(tt, tTicket, tTicket + 0.4), 1.7)})`}>
          <rect x={-380} y={-200} width={760} height={400} rx={18} fill="#f1dfa8" stroke={C.ink} strokeWidth={8} />
          <rect x={-350} y={-170} width={700} height={340} rx={10} fill="none" stroke="#8a6a3a" strokeWidth={4} />
          <Txt x={0} y={-110} size={46} color="#8a2a1a" outline={0} shadow={false}>WHITE STAR LINE</Txt>
          <Txt x={0} y={-35} size={40} color={C.ink} font={HAND} outline={0} shadow={false}>PASSENGER TICKET</Txt>
          <Txt x={0} y={35} size={40} color={C.ink} font={HAND} outline={0} shadow={false}>Southampton → New York</Txt>
          <Txt x={0} y={110} size={52} color={C.red} outline={0} shadow={false}>10 APRIL 1912</Txt>
        </g>
      )}
      <VVignette s={0.4} />
    </g>
  );
};

// ------------------------------------------------------------------ scene 3: the reveal
export const SReveal: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWait = cue('Wait');
  const tTit = cue('TITANIC');
  if (t < tWait) {
    const k = ease(prog(t, 0.2, tWait));
    return (
      <g>
        <VCam cx={lerp(560, 1150, k)} cy={lerp(1450, 900, k)} z={lerp(1.15, 0.55, k)}>
          <Harbour t={t} />
          <Hero x={560} y={feet(1760, 0.62)} s={0.62} expr="o" face={0.6} look={[0.6, -1]} larm={[0.3, 0.2]} rarm={[-0.3, -0.2]} />
        </VCam>
        <Pop t={t - 1.4} x={540} y={330} size={90}>ENORMOUS...</Pop>
        <VVignette s={0.35} />
      </g>
    );
  }
  if (t < tTit) {
    const tt = t - tWait;
    return (
      <g>
        <VCam cx={2120} cy={970} z={lerp(1.9, 2.2, prog(tt, 0, tTit - tWait))}>
          <Harbour t={t} crowd={false} />
        </VCam>
        <Sparkle x={620} y={900} r={50} t={t} />
        <VVignette s={0.5} />
      </g>
    );
  }
  const tt = t - tTit;
  const jump = Math.sin(prog(tt, 0, 0.7) * Math.PI) * 0.35;
  return (
    <g>
      <VCam cx={560} cy={lerp(1500, 1540, prog(tt, 0, 2))} z={lerp(2.7, 2.4, easeOut(prog(tt, 0, 0.4)))} shake={tt < 1.2 ? 12 : 3} t={t}>
        <Harbour t={t} crowd={false} />
        <Hero x={560} y={feet(1760, 0.62)} s={0.62} expr="shock" face={0} look={[0, -0.6]} squash={tt < 0.15 ? 0.15 : 0.04}
          brows="up" capOff={jump} larm={[1.0, -1.0]} rarm={[-1.0, 1.0]} />
      </VCam>
      {Array.from({length: 18}).map((_, k) => {
        const a = (k * Math.PI) / 9;
        return <line key={k} x1={540 + Math.cos(a) * 520} y1={960 + Math.sin(a) * 820} x2={540 + Math.cos(a) * 1200} y2={960 + Math.sin(a) * 1600}
          stroke="#fff" strokeWidth={10} opacity={0.35} />;
      })}
      <Pop t={tt} x={540} y={330} size={150} color={C.red} rot={-4}>TITANIC?!</Pop>
      <VVignette s={0.5} />
    </g>
  );
};

// ------------------------------------------------------------------ scene 4: panic
export const SPanic: React.FC<ShotProps> = ({t, D, cue}) => {
  const tExcept = cue('Except me');
  const tKnew = cue('Because I');
  const hx = 520 + Math.sin(t * 2.4) * 260;
  return (
    <g>
      <VCam cx={t < tExcept ? 900 : lerp(700, 640, prog(t, tExcept, D))} cy={t < tExcept ? 1250 : 1400} z={t < tExcept ? 0.85 : t < tKnew ? 1.25 : 1.05}>
        <Harbour t={t} crowd={false} />
        {[0, 1, 2, 3, 4].map((k) => {
          const role = (['lady', 'gent', 'mum', 'gent', 'lady'] as const)[k];
          const x = ((t * 140 + k * 330) % 1700) - 300;
          return <Person key={k} role={role} seed={k + 1} x={x} y={feet(1760 - (k % 2) * 90, 0.55)} s={0.55} face={0.8} expr={t > tKnew ? 'laugh' : 'happy'}
            walk={t * 1.2 + k} larm={[0.3, 0.2]} rarm={[-2.4 + 0.3 * Math.sin(t * 6 + k), 0.3]} />;
        })}
        {t > tExcept && (
          <Hero x={hx} y={feet(1820, 0.62)} s={0.62} expr="scared" face={Math.cos(t * 2.4) > 0 ? 0.8 : -0.8} brows="worried" walk={t * 3}
            larm={[2.6 + 0.3 * Math.sin(t * 9), 0.3]} rarm={[-2.6 - 0.3 * Math.sin(t * 9), -0.3]} />
        )}
        {t > tExcept && <Sweat x={hx + 60} y={feet(1820, 0.62) - 60} t={t} />}
      </VCam>
      {t < tExcept && <Pop t={t - 0.4} x={540} y={330} size={90} color={C.gold}>ALL ABOARD!</Pop>}
      {t > tExcept && t < tKnew && <Pop t={t - tExcept} x={540} y={330} size={110} color={C.red}>EXCEPT ME.</Pop>}
      {t > tKnew && (
        <g transform={`translate(540,420) scale(${backOut(prog(t, tKnew, tKnew + 0.4), 1.6)})`}>
          <ellipse cx={0} cy={0} rx={330} ry={210} fill="#fff" stroke={C.ink} strokeWidth={7} />
          {[16, 11, 7].map((r, i) => <circle key={i} cx={-60 - i * 40} cy={230 + i * 50} r={r} fill="#fff" stroke={C.ink} strokeWidth={5} />)}
          <rect x={-250} y={20} width={500} height={110} fill="#2f7fc4" />
          <Iceberg x={60} y={60} s={0.42} />
          <Txt x={0} y={-130} size={44} color={C.ink} font={HAND} outline={0} shadow={false}>14 April, 11:40 pm...</Txt>
        </g>
      )}
      {t > tExcept && t < tKnew && (
        <g>
          <rect x={140} y={460} width={800} height={120} rx={40} fill="#fff" stroke={C.ink} strokeWidth={6} />
          <Txt x={540} y={520} size={64} color={C.ink} font={HAND} outline={0} shadow={false}>WAIT! DON'T GO!</Txt>
        </g>
      )}
      <VVignette s={0.4} />
    </g>
  );
};

// ------------------------------------------------------------------ scene 5: cliffhanger
export const SCliff: React.FC<ShotProps> = ({t, D, cue}) => {
  const tWatch = cue('Watch the full');
  if (t < tWatch) {
    return (
      <g>
        <VCam cx={560} cy={lerp(1300, 1530, prog(t, 0, tWatch))} z={lerp(1.3, 2.8, easeIn(prog(t, 0, tWatch)))}>
          <Harbour t={t} crowd={false} />
          <Hero x={560} y={feet(1760, 0.62)} s={0.62} expr="worried" brows="worried" face={0} look={[0, 0]} larm={[0.3, 0.2]} rarm={[-2.2, 2.1]} />
        </VCam>
        <rect x={0} y={0} width={VW} height={VH} fill="#000" opacity={0.25 * prog(t, 0, tWatch)} />
        <Pop t={t - 0.1} x={540} y={330} size={84}>COULD I CHANGE</Pop>
        <Pop t={t - 0.4} x={540} y={440} size={104} color={C.gold}>HISTORY?</Pop>
        <VVignette s={0.6} />
      </g>
    );
  }
  const tt = t - tWatch;
  const sx = lerp(300, 820, prog(tt, 0, D - tWatch));
  const pulse = 1 + 0.06 * Math.sin(t * 7);
  return (
    <g>
      <defs>
        <linearGradient id="clsky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" stopColor="#ff8a4a" />
          <stop offset="1" stopColor="#ffd9a0" />
        </linearGradient>
      </defs>
      <rect x={0} y={0} width={VW} height={VH} fill="url(#clsky)" />
      <Glow id="clsun" x={540} y={1040} r={420} color="#fff2a0" a={0.8} />
      <circle cx={540} cy={1040} r={130} fill="#ffe066" stroke={C.ink} strokeWidth={6} />
      <Ship x={sx} y={1110} s={0.5} t={t} />
      <Waves y={1110} t={t} color="#3a6a9a" dark="#24507a" amp={6} x0={-200} x1={1300} />
      <g transform={`translate(540,420) scale(${backOut(prog(tt, 0, 0.5), 2) * pulse})`}>
        <rect x={-480} y={-120} width={960} height={240} rx={40} fill="#ff2a2a" stroke={C.ink} strokeWidth={9} />
        <Txt x={0} y={-30} size={78} outline={7}>WATCH THE</Txt>
        <Txt x={0} y={50} size={90} color={C.gold} outline={8}>FULL STORY!</Txt>
      </g>
      <Pop t={tt - 0.5} x={540} y={640} size={70} font={TITLE}>HISTORY WORLD</Pop>
      <VVignette s={0.4} />
      <rect x={0} y={0} width={VW} height={VH} fill="#000" opacity={prog(t, D - 0.4, D)} />
    </g>
  );
};

export const SHORT_SHOTS: Record<string, React.FC<ShotProps>> = {
  s_hook: SHook, s_travel: STravel, s_reveal: SReveal, s_panic: SPanic, s_cliff: SCliff,
};

void [Stars, Sparkle];
