// The doodle characters. <Doodle> is the hero from the reference image (round white head, dot eyes,
// red cap, white body, thick black outlines). Other characters reuse the same body with a different
// "hair" (hat, beard, ...) and body colour so the whole cast shares one style.
import React from 'react';
import {C, deg} from './lib';

const LW = 7;
export type Expr =
  | 'smile' | 'happy' | 'grin' | 'laugh' | 'shock' | 'scared' | 'worried' | 'sly' | 'flat' | 'sleep' | 'o' | 'frown';
export type Brows = 'worried' | 'angry' | 'up' | undefined;

export interface DoodleProps {
  x: number;
  y: number; // head centre
  s?: number; // scale: head radius = 100*s, total height ~ 556*s (feet at y + 456*s)
  expr?: Expr;
  face?: number; // -1..1 facial features shift (turn the head)
  look?: [number, number];
  blink?: number;
  larm?: [number, number]; // [angle from down, elbow bend]; positive angle swings left arm outward
  rarm?: [number, number];
  legs?: [number, number];
  walk?: number; // walk phase (seconds * steps/s); overrides legs
  cap?: boolean;
  capOff?: number; // 0 on head .. 1 flown off
  capColor?: string;
  body?: string;
  tilt?: number; // radians
  squash?: number;
  flip?: boolean;
  brows?: Brows;
  blush?: boolean;
  showLegs?: boolean;
  back?: React.ReactNode; // drawn behind the head (hair, hat backs)
  front?: React.ReactNode; // drawn over the face (hats, beards)
  bodyExtra?: React.ReactNode; // drawn on the body (buttons, ties, coats)
  hold?: React.ReactNode; // drawn at the right hand (in local coords, see handR)
  holdL?: React.ReactNode;
}

const arm = (sx: number, sy: number, ang: number, bend: number) => {
  const ex = sx + Math.sin(ang) * 80;
  const ey = sy + Math.cos(ang) * 80;
  const a2 = ang + bend;
  return {ex, ey, hx: ex + Math.sin(a2) * 78, hy: ey + Math.cos(a2) * 78};
};

/** world position of a doodle's right/left hand (ignores tilt) */
export const handPos = (p: DoodleProps, which: 'r' | 'l' = 'r') => {
  const s = p.s ?? 1;
  const a = which === 'r' ? p.rarm ?? [-0.3, -0.2] : p.larm ?? [0.3, 0.2];
  const h = arm(which === 'r' ? 46 : -46, 120, -a[0], -a[1]);
  const m = p.flip ? -1 : 1;
  return [p.x + m * h.hx * s, p.y + h.hy * s];
};

export const CapShape: React.FC<{color?: string}> = ({color = C.red}) => {
  const dark = color === C.red ? C.redD : color;
  const light = color === C.red ? C.redL : color;
  const dome = 'M-104,8 C-122,-95 -40,-150 20,-138 C80,-128 112,-86 108,-52 C60,-60 -30,-42 -104,8 Z';
  return (
    <g>
      <path d={dome} fill={color} stroke={C.ink} strokeWidth={LW} strokeLinejoin="round" />
      <path d="M-104,8 C-122,-95 -40,-150 20,-138 C-50,-120 -84,-60 -88,-2 Z" fill={dark} />
      <path d="M-20,-60 C-10,-110 30,-134 50,-132 C10,-118 -2,-90 -6,-60 Z" fill={light} />
      <path d={dome} fill="none" stroke={C.ink} strokeWidth={LW} strokeLinejoin="round" />
      <ellipse cx={10} cy={-144} rx={12} ry={9} fill={color} stroke={C.ink} strokeWidth={5} />
      <path
        d="M40,-66 C90,-92 150,-100 172,-84 C186,-72 170,-46 140,-38 C120,-34 108,-44 104,-50 C84,-58 60,-62 40,-66 Z"
        fill={dark} stroke={C.ink} strokeWidth={LW} strokeLinejoin="round"
      />
    </g>
  );
};

const Face: React.FC<{expr: Expr; face: number; look: [number, number]; blink: number; brows?: Brows; blush?: boolean}> = ({
  expr, face, look, blink, brows, blush,
}) => {
  const fx = face * 34;
  const lx = look[0] * 8;
  const ly = look[1] * 7;
  const eyes: [number, number][] = [[-30 + fx + lx, -22 + ly], [32 + fx + lx, -25 + ly]];
  const mx = 8 + fx + lx * 0.6;
  const my = 14 + ly * 0.6;
  const els: React.ReactNode[] = [];
  if (blush) eyes.forEach(([ex, ey], i) => els.push(<ellipse key={'b' + i} cx={ex + (i ? 8 : -6)} cy={ey + 30} rx={16} ry={8} fill="#ff8080" opacity={0.5} />));
  if (expr === 'shock' || expr === 'scared') {
    eyes.forEach(([ex, ey], i) => {
      els.push(<ellipse key={'e' + i} cx={ex} cy={ey} rx={15} ry={18} fill="#fff" stroke={C.ink} strokeWidth={4.5} />);
      els.push(<circle key={'p' + i} cx={ex + lx * 0.6} cy={ey + ly * 0.6} r={6} fill={C.ink} />);
    });
  } else if (expr === 'happy' || expr === 'laugh' || (blink >= 0.98 && expr !== 'sleep')) {
    eyes.forEach(([ex, ey], i) =>
      blink >= 0.98 && expr !== 'happy' && expr !== 'laugh'
        ? els.push(<line key={'e' + i} x1={ex - 10} y1={ey} x2={ex + 10} y2={ey} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />)
        : els.push(<path key={'e' + i} d={`M${ex - 11},${ey + 4} C${ex - 6},${ey - 9} ${ex + 6},${ey - 9} ${ex + 11},${ey + 4}`} fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" />),
    );
  } else if (expr === 'sleep') {
    eyes.forEach(([ex, ey], i) => els.push(<line key={'e' + i} x1={ex - 10} y1={ey} x2={ex + 10} y2={ey} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />));
  } else if (expr === 'sly') {
    eyes.forEach(([ex, ey], i) => {
      els.push(<ellipse key={'e' + i} cx={ex} cy={ey + 2} rx={10} ry={5} fill={C.ink} />);
      els.push(<line key={'l' + i} x1={ex - 13} y1={ey - 5} x2={ex + 13} y2={ey - 3} stroke={C.ink} strokeWidth={4.5} strokeLinecap="round" />);
    });
  } else {
    eyes.forEach(([ex, ey], i) => els.push(<ellipse key={'e' + i} cx={ex} cy={ey} rx={9.5} ry={Math.max(0.5, 10.5 * (1 - blink * 0.9))} fill={C.ink} />));
  }
  if (brows) {
    eyes.forEach(([ex, ey], i) => {
      const sg = i === 0 ? -1 : 1;
      if (brows === 'worried') els.push(<line key={'w' + i} x1={ex - 12} y1={ey - 22 + sg * 6} x2={ex + 12} y2={ey - 22 - sg * 6} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />);
      if (brows === 'angry') els.push(<line key={'w' + i} x1={ex - 12} y1={ey - 26 + sg * 6} x2={ex + 12} y2={ey - 26 - sg * 6} stroke={C.ink} strokeWidth={5} strokeLinecap="round" />);
      if (brows === 'up') els.push(<path key={'w' + i} d={`M${ex - 12},${ey - 26} C${ex - 4},${ey - 34} ${ex + 4},${ey - 34} ${ex + 12},${ey - 26}`} fill="none" stroke={C.ink} strokeWidth={5} strokeLinecap="round" />);
    });
  }
  const st = {fill: 'none', stroke: C.ink, strokeWidth: 5.5, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const};
  switch (expr) {
    case 'smile':
    case 'happy':
      els.push(<path key="m" d={`M${mx - 17},${my - 3} C${mx - 9},${my + 11} ${mx + 9},${my + 11} ${mx + 17},${my - 3}`} {...st} />);
      break;
    case 'grin':
    case 'laugh':
      els.push(<path key="m" d={`M${mx - 24},${my - 4} C${mx - 18},${my + 30} ${mx + 18},${my + 30} ${mx + 24},${my - 4} Z`} fill="#40141a" stroke={C.ink} strokeWidth={5} strokeLinejoin="round" />);
      els.push(<ellipse key="t" cx={mx} cy={my + 13} rx={10} ry={5} fill="#f26673" />);
      break;
    case 'shock':
    case 'scared':
      els.push(<ellipse key="m" cx={mx} cy={my + 8} rx={13} ry={18} fill="#40141a" stroke={C.ink} strokeWidth={5} />);
      break;
    case 'worried':
      els.push(<path key="m" d={`M${mx - 20},${my + 6} C${mx - 10},${my - 4} ${mx - 4},${my + 12} ${mx + 4},${my + 4} C${mx + 10},${my - 4} ${mx + 14},${my + 8} ${mx + 20},${my + 2}`} {...st} />);
      break;
    case 'sly':
      els.push(<path key="m" d={`M${mx - 16},${my + 4} C${mx - 2},${my + 10} ${mx + 12},${my + 6} ${mx + 20},${my - 6}`} {...st} />);
      break;
    case 'flat':
    case 'sleep':
      els.push(<line key="m" x1={mx - 14} y1={my + 4} x2={mx + 14} y2={my + 4} {...st} />);
      break;
    case 'o':
      els.push(<ellipse key="m" cx={mx} cy={my + 4} rx={7} ry={9} fill="#40141a" stroke={C.ink} strokeWidth={4.5} />);
      break;
    case 'frown':
      els.push(<path key="m" d={`M${mx - 17},${my + 10} C${mx - 9},${my - 2} ${mx + 9},${my - 2} ${mx + 17},${my + 10}`} {...st} />);
      break;
  }
  return <g>{els}</g>;
};

let clipId = 0;

export const Doodle: React.FC<DoodleProps> = (p) => {
  const s = p.s ?? 1;
  const expr = p.expr ?? 'smile';
  const face = p.face ?? 0.9;
  const look = p.look ?? [0, 0];
  const blink = p.blink ?? 0;
  const larm = p.larm ?? [0.3, 0.2];
  const rarm = p.rarm ?? [-0.3, -0.2];
  let legs = p.legs ?? [0, 0];
  let bob = 0;
  if (p.walk !== undefined) {
    const sw = Math.sin(p.walk * 2 * Math.PI);
    legs = [sw * 0.45, -sw * 0.45];
    bob = Math.abs(Math.cos(p.walk * 2 * Math.PI)) * 6;
  }
  const sq = 1 + (p.squash ?? 0);
  const body = p.body ?? '#ffffff';
  const hl = arm(-46, 120, -larm[0], -larm[1]);
  const hr = arm(46, 120, -rarm[0], -rarm[1]);
  const id = `hc${(clipId = (clipId + 1) % 100000)}`;
  const capOff = p.capOff ?? 0;
  return (
    <g transform={`translate(${p.x},${p.y}) scale(${s}) ${p.flip ? 'scale(-1,1)' : ''} rotate(${deg(p.tilt ?? 0)}) scale(${1 / Math.sqrt(sq)},${sq}) translate(0,${-bob})`}>
      {p.showLegs !== false &&
        [-1, 1].map((side, i) => {
          const a = legs[i];
          const hx = side * 30;
          const fx = hx + Math.sin(a) * 120;
          const fy = 318 + Math.cos(a) * 120;
          return (
            <g key={side}>
              <line x1={hx} y1={318} x2={fx} y2={fy} stroke={C.ink} strokeWidth={9} strokeLinecap="round" />
              <ellipse cx={fx + 10} cy={fy + 4} rx={22} ry={11} fill={C.ink} />
            </g>
          );
        })}
      <path
        d="M-48,70 C-58,170 -70,260 -66,300 C-64,332 -40,336 0,336 C40,336 64,332 66,300 C70,260 58,170 48,70 Z"
        fill={body} stroke={C.ink} strokeWidth={LW} strokeLinejoin="round"
      />
      {body === '#ffffff' && <path d="M-48,90 C-58,170 -70,260 -66,300 C-52,250 -44,170 -38,95 Z" fill={C.shade} />}
      {p.bodyExtra}
      {[hl, hr].map((h, i) => (
        <g key={i}>
          <polyline points={`${i ? 46 : -46},120 ${h.ex},${h.ey} ${h.hx},${h.hy}`} fill="none" stroke={C.ink} strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" />
          <circle cx={h.hx} cy={h.hy} r={11} fill="#fff" stroke={C.ink} strokeWidth={5} />
        </g>
      ))}
      {p.hold && <g transform={`translate(${hr.hx},${hr.hy})`}>{p.hold}</g>}
      {p.holdL && <g transform={`translate(${hl.hx},${hl.hy})`}>{p.holdL}</g>}
      {p.back}
      <defs>
        <clipPath id={id}>
          <circle cx={0} cy={0} r={100} />
        </clipPath>
      </defs>
      <circle cx={0} cy={0} r={100} fill="#fff" />
      <g clipPath={`url(#${id})`}>
        <circle cx={0} cy={0} r={100} fill={C.shade} />
        <circle cx={16} cy={-6} r={97} fill="#fff" />
      </g>
      <circle cx={0} cy={0} r={100} fill="none" stroke={C.ink} strokeWidth={LW} />
      <Face expr={expr} face={face} look={look} blink={blink} brows={p.brows} blush={p.blush} />
      {p.front}
      {p.cap !== false && (
        <g transform={`translate(0,${-capOff * 260}) rotate(${deg(-capOff * 0.9)})`}>
          <CapShape color={p.capColor} />
        </g>
      )}
    </g>
  );
};

// ------------------------------------------------------------------ cast (same body, different hats)
const S = {stroke: C.ink, strokeWidth: LW, strokeLinejoin: 'round' as const};

export const TopHat: React.FC<{band?: string}> = ({band = '#6a2a2a'}) => (
  <g>
    <rect x={-66} y={-240} width={132} height={170} fill="#1c1c22" {...S} />
    <rect x={-66} y={-110} width={132} height={20} fill={band} stroke={C.ink} strokeWidth={4} />
    <ellipse cx={0} cy={-72} rx={118} ry={20} fill="#1c1c22" {...S} />
  </g>
);

export const BigHat: React.FC<{color: string; flower?: string}> = ({color, flower = C.red}) => (
  <g>
    <path d="M-100,0 C-100,-110 100,-110 100,0" fill="#5a3a22" {...S} />
    <ellipse cx={0} cy={-70} rx={210} ry={40} fill={color} {...S} />
    <ellipse cx={0} cy={-100} rx={90} ry={50} fill={color} {...S} />
    {[0, 1, 2].map((k) => (
      <circle key={k} cx={-60 + k * 40} cy={-120} r={18} fill={[flower, '#fff', '#ff9ad0'][k]} stroke={C.ink} strokeWidth={3} />
    ))}
    <path d="M80,-110 C160,-170 200,-120 220,-160" fill="none" stroke="#fff" strokeWidth={14} strokeLinecap="round" />
  </g>
);

export const Moustache: React.FC<{face?: number; color?: string; big?: boolean}> = ({face = 0, color = '#2a2420', big}) => {
  const mx = 8 + face * 34;
  const k = big ? 1.4 : 1;
  return (
    <path
      d={`M${mx},2 C${mx - 20 * k},-6 ${mx - 44 * k},4 ${mx - 52 * k},28 C${mx - 30 * k},12 ${mx - 14},12 ${mx},12 C${mx + 14},12 ${mx + 30 * k},12 ${mx + 52 * k},28 C${mx + 44 * k},4 ${mx + 20 * k},-6 ${mx},2 Z`}
      fill={color} stroke={C.ink} strokeWidth={3}
    />
  );
};

export const CaptainHat: React.FC = () => (
  <g>
    <path d="M-104,-30 C-110,-130 110,-130 104,-30 Z" fill="#fff" {...S} />
    <rect x={-106} y={-50} width={212} height={26} fill="#1c2a48" {...S} />
    <path d="M10,-26 C60,-26 120,-30 150,-12 C120,-4 60,-8 10,-10 Z" fill="#111" stroke={C.ink} strokeWidth={4} />
    <circle cx={0} cy={-62} r={14} fill={C.gold} stroke={C.ink} strokeWidth={3} />
  </g>
);

export const WhiteBeard: React.FC<{face?: number}> = ({face = 0}) => {
  const mx = 8 + face * 34;
  return (
    <g>
      <path d={`M${mx - 78},0 C${mx - 80},100 ${mx - 30},150 ${mx},150 C${mx + 30},150 ${mx + 82},100 ${mx + 80},0 C${mx + 50},40 ${mx - 50},40 ${mx - 78},0 Z`} fill="#f2f2f2" stroke={C.ink} strokeWidth={5} />
      <Moustache face={face} color="#f2f2f2" big />
    </g>
  );
};

export const SlickHair: React.FC<{color?: string}> = ({color = '#2a1e14'}) => (
  <path d="M-100,-20 C-104,-140 104,-150 102,-20 C70,-70 20,-90 -20,-70 C-50,-80 -80,-60 -100,-20 Z" fill={color} {...S} />
);

export const WoolCap: React.FC<{color?: string}> = ({color = '#4a5a6a'}) => (
  <g>
    <path d="M-104,-10 C-110,-150 110,-150 104,-10 Z" fill={color} {...S} />
    <rect x={-108} y={-34} width={216} height={30} rx={10} fill={color} {...S} />
    <circle cx={0} cy={-138} r={20} fill={color} {...S} />
  </g>
);

export const Pigtails: React.FC = () => (
  <g>
    {[-1, 1].map((sx) => (
      <g key={sx}>
        <ellipse cx={sx * 112} cy={30} rx={30} ry={46} fill="#c9853a" {...S} />
        <circle cx={sx * 100} cy={-14} r={16} fill={C.red} stroke={C.ink} strokeWidth={4} />
      </g>
    ))}
    <path d="M-100,-10 C-100,-140 100,-140 100,-10 C70,-60 -70,-60 -100,-10 Z" fill="#c9853a" {...S} />
  </g>
);

export const BowTie: React.FC<{color?: string}> = ({color = '#1c1c22'}) => (
  <g>
    <polygon points="0,100 -26,86 -26,116" fill={color} stroke={C.ink} strokeWidth={4} />
    <polygon points="0,100 26,86 26,116" fill={color} stroke={C.ink} strokeWidth={4} />
    <circle cx={0} cy={100} r={7} fill={color} stroke={C.ink} strokeWidth={4} />
  </g>
);

export const Buttons: React.FC<{color?: string}> = ({color = C.gold}) => (
  <g>
    {[150, 200, 250].map((y) => (
      <circle key={y} cx={10} cy={y} r={7} fill={color} stroke={C.ink} strokeWidth={2.5} />
    ))}
  </g>
);

export const LifeJacket: React.FC = () => (
  <g>
    <path d="M-62,96 L-30,90 L-26,250 L-66,250 Z" fill="#f2f2ea" stroke={C.ink} strokeWidth={5} />
    <path d="M62,96 L30,90 L26,250 L66,250 Z" fill="#f2f2ea" stroke={C.ink} strokeWidth={5} />
    {[140, 190, 230].map((y) => (
      <line key={y} x1={-64} y1={y} x2={64} y2={y} stroke="#c9b48a" strokeWidth={6} />
    ))}
  </g>
);

export type Role = 'gent' | 'lady' | 'waiter' | 'captain' | 'officer' | 'lookout' | 'vendor' | 'girl' | 'mum' | 'oldman' | 'band' | 'sailor';

/** a passenger/crew member built on the same doodle body */
export const Person: React.FC<DoodleProps & {role: Role; seed?: number; jacket?: boolean}> = ({role, seed = 0, jacket, ...p}) => {
  const f = p.face ?? 0;
  const ladyCols = ['#f2c8d8', '#c8e0f2', '#f2e2c8', '#d8f2c8'];
  const base: Partial<DoodleProps> = {cap: false};
  let back: React.ReactNode = null;
  let front: React.ReactNode = null;
  let extra: React.ReactNode = null;
  switch (role) {
    case 'gent':
      Object.assign(base, {body: ['#2a2a33', '#3a2a2a', '#2a3340'][seed % 3]});
      front = <g><TopHat />{seed % 2 === 0 && <Moustache face={f} />}</g>;
      extra = <BowTie color="#fff" />;
      break;
    case 'lady':
      Object.assign(base, {body: ['#d8a8c8', '#a8c8e0', '#e8d0a0', '#b8d8a8'][seed % 4]});
      front = <BigHat color={ladyCols[seed % 4]} />;
      break;
    case 'waiter':
      Object.assign(base, {body: '#ffffff'});
      front = <SlickHair />;
      extra = <g><BowTie /><path d="M-58,200 L58,200 L50,330 L-50,330 Z" fill="#fff" stroke={C.ink} strokeWidth={4} /></g>;
      break;
    case 'captain':
      Object.assign(base, {body: '#1c2a48'});
      front = <g><WhiteBeard face={f} /><CaptainHat /></g>;
      extra = <Buttons />;
      break;
    case 'officer':
      Object.assign(base, {body: '#1c2a48'});
      front = <g><Moustache face={f} /><CaptainHat /></g>;
      extra = <Buttons />;
      break;
    case 'sailor':
      Object.assign(base, {body: '#2a3a5a'});
      front = <WoolCap color="#1c2a48" />;
      break;
    case 'lookout':
      Object.assign(base, {body: '#2a3a5a'});
      front = <WoolCap />;
      break;
    case 'vendor':
      Object.assign(base, {body: '#7a5a3a'});
      front = <g><path d="M-96,-10 C-110,-90 -70,-60 -60,-90 M96,-10 C110,-90 70,-60 60,-90" fill="none" stroke="#d8d8d8" strokeWidth={22} strokeLinecap="round" /><WhiteBeard face={f} /></g>;
      break;
    case 'oldman':
      Object.assign(base, {body: '#4a4a52'});
      front = <g><path d="M-96,-10 C-110,-90 -70,-60 -60,-90 M96,-10 C110,-90 70,-60 60,-90" fill="none" stroke="#d8d8d8" strokeWidth={22} strokeLinecap="round" /><Moustache face={f} color="#e0e0e0" big /></g>;
      break;
    case 'girl':
      Object.assign(base, {body: '#f2a3c8'});
      back = <Pigtails />;
      break;
    case 'mum':
      Object.assign(base, {body: '#8aa8c8'});
      front = <BigHat color="#e0e8f2" flower="#6a8ad8" />;
      break;
    case 'band':
      Object.assign(base, {body: '#1c1c22'});
      front = <g><SlickHair color="#3a2a1a" /><Moustache face={f} /></g>;
      extra = <BowTie color="#fff" />;
      break;
  }
  return (
    <Doodle
      {...base}
      {...p}
      back={back}
      front={front}
      bodyExtra={<g>{extra}{jacket && <LifeJacket />}</g>}
    />
  );
};
