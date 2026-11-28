// Camera, text and comic effects.
import React from 'react';
import {C, W, H, backOut, clamp, easeIn, easeOut, prog, rng, lerp} from './lib';

export const TITLE = 'Luckiest Guy, Impact, sans-serif';
export const HAND = 'Patrick Hand, Comic Sans MS, sans-serif';

/** camera: looks at (cx, cy) with zoom z, optional rotation (deg) and shake */
export const Cam: React.FC<{cx: number; cy: number; z?: number; rot?: number; shake?: number; t?: number; children: React.ReactNode}> = ({
  cx, cy, z = 1, rot = 0, shake = 0, t = 0, children,
}) => {
  const sx = shake * (Math.sin(t * 47) + Math.sin(t * 31)) * 0.5;
  const sy = shake * (Math.cos(t * 53) + Math.sin(t * 37)) * 0.5;
  return <g transform={`translate(${W / 2 + sx},${H / 2 + sy}) rotate(${rot}) scale(${z}) translate(${-cx},${-cy})`}>{children}</g>;
};

export const Txt: React.FC<{
  x: number; y: number; size: number; children: string; color?: string; font?: string; outline?: number;
  anchor?: 'middle' | 'start' | 'end'; rot?: number; opacity?: number; shadow?: boolean; weight?: number;
}> = ({x, y, size, children, color = '#fff', font = TITLE, outline = 10, anchor = 'middle', rot = 0, opacity = 1, shadow = true}) => (
  <g transform={`translate(${x},${y}) rotate(${rot})`} opacity={opacity}>
    {shadow && outline > 0 && (
      <text x={size * 0.05} y={size * 0.07} fontFamily={font} fontSize={size} textAnchor={anchor} dominantBaseline="central"
        fill="rgba(0,0,0,0.35)" stroke="rgba(0,0,0,0.35)" strokeWidth={outline * 2} strokeLinejoin="round">{children}</text>
    )}
    <text x={0} y={0} fontFamily={font} fontSize={size} textAnchor={anchor} dominantBaseline="central" fill={color}
      stroke={outline > 0 ? C.ink : 'none'} strokeWidth={outline * 2} strokeLinejoin="round" paintOrder="stroke">{children}</text>
  </g>
);

/** text that springs in at local time t=0 and fades after `hold` seconds */
export const Pop: React.FC<{t: number; x: number; y: number; size: number; children: string; color?: string; rot?: number;
  font?: string; outline?: number; hold?: number}> = ({t, x, y, size, children, color = '#fff', rot = 0, font = TITLE, outline = 10, hold = 999}) => {
  if (t < 0) return null;
  const k = t < 0.35 ? backOut(t / 0.35, 2.6) : 1;
  const a = t < hold ? 1 : 1 - prog(t, hold, hold + 0.25);
  if (a <= 0) return null;
  return (
    <g transform={`translate(${x},${y}) scale(${Math.max(k, 0.001)})`} opacity={a}>
      <Txt x={0} y={0} size={size} color={color} rot={rot} font={font} outline={outline}>{children}</Txt>
    </g>
  );
};

/** comic burst bubble with a word inside */
export const Burst: React.FC<{t: number; x: number; y: number; r: number; label: string; color?: string; tcolor?: string; size?: number; hold?: number}> = ({
  t, x, y, r, label, color = '#ffd84d', tcolor = C.red, size, hold = 999,
}) => {
  if (t < 0 || t > hold + 0.3) return null;
  const k = t < 0.25 ? backOut(t / 0.25, 2.2) : 1 + 0.03 * Math.sin(t * 20);
  const a = t < hold ? 1 : 1 - prog(t, hold, hold + 0.3);
  const R = rng(label.length);
  const pts: string[] = [];
  for (let i = 0; i < 28; i++) {
    const ang = (i * Math.PI) / 14;
    const rr = r * (i % 2 === 0 ? 1 : 0.68 + R() * 0.08);
    pts.push(`${Math.cos(ang) * rr * 1.25},${Math.sin(ang) * rr}`);
  }
  return (
    <g transform={`translate(${x},${y}) scale(${k}) rotate(${4.6 * Math.sin(t * 6)})`} opacity={a}>
      <polygon points={pts.join(' ')} fill={color} stroke={C.ink} strokeWidth={8} strokeLinejoin="round" />
      <Txt x={0} y={0} size={size ?? r * 0.5} color={tcolor} outline={7} rot={-4}>{label}</Txt>
    </g>
  );
};

export const Sparkle: React.FC<{x: number; y: number; r: number; t: number; color?: string}> = ({x, y, r, t, color = '#fffbd0'}) => {
  const rr = r * (0.6 + 0.4 * (0.5 + 0.5 * Math.sin(t * 9)));
  const q = rr * 0.12;
  return (
    <path transform={`translate(${x},${y}) rotate(${t * 86})`}
      d={`M0,${-rr} C${q},${-q} ${q},${-q} ${rr},0 C${q},${q} ${q},${q} 0,${rr} C${-q},${q} ${-q},${q} ${-rr},0 C${-q},${-q} ${-q},${-q} 0,${-rr} Z`}
      fill={color} opacity={0.95} />
  );
};

export const Sweat: React.FC<{x: number; y: number; s?: number; t: number}> = ({x, y, s = 1, t}) => (
  <path transform={`translate(${x},${y + ((t * 60) % 40)}) scale(${s})`} d="M0,-22 C10,-6 14,4 0,12 C-14,4 -10,-6 0,-22 Z"
    fill="#8cccff" stroke={C.ink} strokeWidth={4} />
);

export const Star: React.FC<{x: number; y: number; r: number; color?: string; rot?: number}> = ({x, y, r, color = '#ffd84d', rot = 0}) => {
  const pts: string[] = [];
  for (let i = 0; i < 10; i++) {
    const a = rot - Math.PI / 2 + (i * Math.PI) / 5;
    const rr = i % 2 === 0 ? r : r * 0.45;
    pts.push(`${x + Math.cos(a) * rr},${y + Math.sin(a) * rr}`);
  }
  return <polygon points={pts.join(' ')} fill={color} stroke={C.ink} strokeWidth={4} strokeLinejoin="round" />;
};

export const DizzyStars: React.FC<{x: number; y: number; r: number; t: number}> = ({x, y, r, t}) => (
  <g>
    {[0, 1, 2, 3].map((i) => {
      const a = t * 3 + (i * Math.PI) / 2;
      return <Star key={i} x={x + Math.cos(a) * r} y={y + Math.sin(a) * r * 0.35} r={16} />;
    })}
  </g>
);

export const Vignette: React.FC<{strength?: number}> = ({strength = 0.5}) => (
  <g>
    <defs>
      <radialGradient id={`vig${Math.round(strength * 100)}`} cx="50%" cy="50%" r="75%">
        <stop offset="45%" stopColor="#000" stopOpacity={0} />
        <stop offset="100%" stopColor="#000" stopOpacity={strength} />
      </radialGradient>
    </defs>
    <rect x={0} y={0} width={W} height={H} fill={`url(#vig${Math.round(strength * 100)})`} />
  </g>
);

export const Glow: React.FC<{x: number; y: number; r: number; color?: string; a?: number; id: string}> = ({x, y, r, color = '#ffe08a', a = 0.6, id}) => (
  <g>
    <defs>
      <radialGradient id={id}>
        <stop offset="0%" stopColor={color} stopOpacity={a} />
        <stop offset="100%" stopColor={color} stopOpacity={0} />
      </radialGradient>
    </defs>
    <circle cx={x} cy={y} r={r} fill={`url(#${id})`} />
  </g>
);

export const SpeedLines: React.FC<{x: number; y: number; n?: number; len?: number; color?: string; seed?: number; a?: number}> = ({
  x, y, n = 6, len = 260, color = C.ink, seed = 1, a = 0.6,
}) => {
  const R = rng(seed);
  return (
    <g opacity={a}>
      {Array.from({length: n}).map((_, k) => {
        const yy = y - 120 + k * 45 + (R() - 0.5) * 16;
        const xx = x - R() * 60;
        return <line key={k} x1={xx} y1={yy} x2={xx - len * (0.6 + R() * 0.4)} y2={yy} stroke={color} strokeWidth={5} strokeLinecap="round" />;
      })}
    </g>
  );
};

/** lower-left location card */
export const Caption: React.FC<{t: number; place: string; date: string; dur?: number}> = ({t, place, date, dur = 4.5}) => {
  if (t < 0 || t > dur + 0.6) return null;
  const k = easeOut(prog(t, 0, 0.5)) - easeIn(prog(t, dur, dur + 0.5));
  const x = lerp(-900, 70, k);
  return (
    <g>
      <rect x={x} y={850} width={800} height={150} rx={18} fill="rgba(10,10,20,0.82)" />
      <rect x={x} y={850} width={14} height={150} fill={C.red} />
      <Txt x={x + 40} y={898} size={46} anchor="start" outline={0}>{place}</Txt>
      <Txt x={x + 40} y={958} size={52} anchor="start" outline={0} color={C.gold}>{date}</Txt>
    </g>
  );
};

/** a fact card: pops in at t=0 */
export const FactCard: React.FC<{t: number; x: number; y: number; w: number; h: number; title: string; lines: string[]; hold?: number; color?: string}> = ({
  t, x, y, w, h, title, lines, hold = 999, color = C.navy,
}) => {
  if (t < 0) return null;
  const k = backOut(prog(t, 0, 0.45), 1.6);
  const a = t < hold ? 1 : 1 - prog(t, hold, hold + 0.3);
  if (a <= 0) return null;
  return (
    <g transform={`translate(${x},${y}) scale(${Math.max(k, 0.001)})`} opacity={a}>
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={22} fill="#fbf6e8" stroke={C.ink} strokeWidth={7} />
      <rect x={-w / 2} y={-h / 2} width={w} height={86} rx={22} fill={color} stroke={C.ink} strokeWidth={7} />
      <Txt x={0} y={-h / 2 + 44} size={48} color={C.gold} outline={0} shadow={false}>{title}</Txt>
      {lines.map((l, i) => (
        <Txt key={i} x={0} y={-h / 2 + 140 + i * 62} size={46} color={C.ink} font={HAND} outline={0} shadow={false}
          opacity={clamp((t - 0.4 - i * 0.35) / 0.3)}>{l}</Txt>
      ))}
    </g>
  );
};

export const Confetti: React.FC<{t: number; n?: number; seed?: number}> = ({t, n = 60, seed = 3}) => {
  const R = rng(seed);
  const cols = [C.gold, '#3a7ad8', C.red, '#2bb36b', '#ff8ad8', '#fff'];
  return (
    <g>
      {Array.from({length: n}).map((_, i) => {
        const x = (R() * W + Math.sin(t * 2 + i) * 40) % W;
        const y = ((R() * H + t * (180 + R() * 120)) % (H + 40)) - 20;
        return <rect key={i} x={-8} y={-4} width={16} height={8} fill={cols[i % 6]} transform={`translate(${x},${y}) rotate(${t * 230 + i * 40})`} />;
      })}
    </g>
  );
};
