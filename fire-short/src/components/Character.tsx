import React from 'react';

/**
 * The History World main character — the doodle guy.
 * Round white head, small black dot eyes, small expressive mouth,
 * simple cartoon body and his signature RED BASEBALL CAP.
 *
 * This is the ONE definition used in every scene so design, proportions,
 * face and cap stay identical. Only pose/expression props change.
 */
export type Expression =
  | 'neutral'
  | 'happy'
  | 'curious'
  | 'scared'
  | 'terrified'
  | 'scream'
  | 'shocked'
  | 'confused'
  | 'smug';

export type CharacterProps = {
  x: number;
  y: number; // feet position
  scale?: number;
  expression?: Expression;
  facing?: 1 | -1;
  /** arm angles in degrees (0 = straight down, positive = forward/up) */
  armL?: number;
  armR?: number;
  /** leg angles in degrees */
  legL?: number;
  legR?: number;
  bodyTilt?: number;
  headTilt?: number;
  /** 0..1, 1 = eyes closed */
  blink?: number;
  /** look offset of pupils, -1..1 */
  lookX?: number;
  lookY?: number;
  /** squash & stretch (1 = normal) */
  squash?: number;
  sweat?: boolean;
  capLift?: number; // cap pops up when shocked
  shiver?: number; // px jitter
  frame?: number;
  /** hand-drawn line boil intensity */
  boil?: number;
};

const INK = '#141414';
const LINE = 9;

const Limb: React.FC<{
  x: number;
  y: number;
  angle: number;
  length: number;
  hand?: boolean;
  foot?: boolean;
  facing: number;
}> = ({x, y, angle, length, hand, foot, facing}) => {
  const knee = angle * 0.35;
  return (
    <g transform={`translate(${x} ${y}) rotate(${angle})`}>
      <path
        d={`M0 0 Q ${-knee * 0.4} ${length * 0.5} 0 ${length}`}
        stroke={INK}
        strokeWidth={LINE}
        fill="none"
        strokeLinecap="round"
      />
      {hand && <circle cx={0} cy={length + 4} r={13} fill="#fff" stroke={INK} strokeWidth={7} />}
      {foot && (
        <ellipse
          cx={10 * facing}
          cy={length + 4}
          rx={22}
          ry={11}
          fill={INK}
          transform={`rotate(${-angle} ${10 * facing} ${length + 4})`}
        />
      )}
    </g>
  );
};

const Mouth: React.FC<{expression: Expression; f: number}> = ({expression, f}) => {
  const wob = Math.sin(f * 1.7) * 2;
  switch (expression) {
    case 'happy':
      return <path d="M-26 28 Q0 56 26 28" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" />;
    case 'smug':
      return <path d="M-20 34 Q6 46 28 26" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" />;
    case 'curious':
      return <ellipse cx={4} cy={36} rx={9} ry={9} fill={INK} />;
    case 'scared':
      return (
        <path
          d={`M-24 40 Q-12 ${30 + wob} 0 40 Q12 ${50 - wob} 24 40`}
          stroke={INK}
          strokeWidth={7}
          fill="none"
          strokeLinecap="round"
        />
      );
    case 'terrified':
      return (
        <g>
          <ellipse cx={0} cy={42} rx={20} ry={16 + wob} fill={INK} />
          <rect x={-14} y={28} width={28} height={7} rx={3} fill="#fff" />
        </g>
      );
    case 'scream':
      return (
        <g>
          <ellipse cx={0} cy={48} rx={26 + wob} ry={34 + wob} fill={INK} />
          <ellipse cx={0} cy={66} rx={14} ry={9} fill="#e0525a" />
        </g>
      );
    case 'shocked':
      return <ellipse cx={0} cy={44} rx={14} ry={20} fill={INK} />;
    case 'confused':
      return (
        <path
          d="M-26 40 L-12 32 L0 42 L12 32 L26 40"
          stroke={INK}
          strokeWidth={7}
          fill="none"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      );
    default:
      return <path d="M-18 34 Q0 44 18 34" stroke={INK} strokeWidth={7} fill="none" strokeLinecap="round" />;
  }
};

export const Character: React.FC<CharacterProps> = ({
  x,
  y,
  scale = 1,
  expression = 'neutral',
  facing = 1,
  armL = 8,
  armR = -8,
  legL = 4,
  legR = -4,
  bodyTilt = 0,
  headTilt = 0,
  blink = 0,
  lookX = 0,
  lookY = 0,
  squash = 1,
  sweat = false,
  capLift = 0,
  shiver = 0,
  frame = 0,
  boil = 1,
}) => {
  const jx = shiver ? Math.sin(frame * 2.3) * shiver : 0;
  const jy = shiver ? Math.cos(frame * 3.1) * shiver * 0.5 : 0;
  // subtle "line boil" so the drawing feels hand-animated
  const b = Math.floor(frame / 3);
  const bx = (((b * 37) % 7) - 3) * 0.25 * boil;
  const by = (((b * 53) % 5) - 2) * 0.25 * boil;

  const big = expression === 'terrified' || expression === 'scream' || expression === 'shocked';
  const eyeR = big ? 9 : 8;
  const eyeY = big ? -14 : -8;
  const eyeOpen = Math.max(0.08, 1 - blink);
  const confusedBrow = expression === 'confused';

  return (
    <g transform={`translate(${x + jx} ${y + jy}) scale(${scale * facing} ${scale})`}>
      <g transform={`scale(${1 / squash} ${squash})`}>
        {/* shadow */}
        <ellipse cx={0} cy={4} rx={70} ry={12} fill="rgba(0,0,0,0.35)" />
        {/* legs */}
        <Limb x={-18} y={-120} angle={legL} length={110} foot facing={1} />
        <Limb x={18} y={-120} angle={legR} length={110} foot facing={1} />
        <g transform={`rotate(${bodyTilt} 0 -120)`}>
          {/* back arm */}
          <Limb x={-34} y={-238} angle={armL} length={100} hand facing={1} />
          {/* body */}
          <path
            d={`M${-46 + bx} -250 Q${-56} -180 ${-44} -122 Q0 ${-108 + by} 44 -122 Q56 -180 ${46 - bx} -250 Q0 ${-268 + by} ${-46 + bx} -250 Z`}
            fill="#ffffff"
            stroke={INK}
            strokeWidth={LINE}
            strokeLinejoin="round"
          />
          {/* front arm */}
          <Limb x={34} y={-238} angle={armR} length={100} hand facing={1} />
          {/* head */}
          <g transform={`translate(0 -340) rotate(${headTilt})`}>
            <circle cx={bx} cy={by} r={92} fill="#ffffff" stroke={INK} strokeWidth={LINE} />
            {/* eyes */}
            <g transform={`translate(${10 + lookX * 12} ${eyeY + lookY * 8})`}>
              <ellipse cx={-28} cy={0} rx={eyeR} ry={eyeR * eyeOpen * (confusedBrow ? 0.9 : 1)} fill={INK} />
              <ellipse cx={26} cy={confusedBrow ? -6 : 0} rx={eyeR} ry={eyeR * eyeOpen} fill={INK} />
            </g>
            {/* brows for strong emotions */}
            {(expression === 'terrified' || expression === 'scared' || expression === 'scream') && (
              <g stroke={INK} strokeWidth={6} strokeLinecap="round">
                <path d="M-36 -40 L-10 -32" />
                <path d="M48 -40 L22 -32" />
              </g>
            )}
            {confusedBrow && (
              <g stroke={INK} strokeWidth={6} strokeLinecap="round" fill="none">
                <path d="M-34 -30 L-8 -26" />
                <path d="M22 -40 Q36 -50 50 -38" />
              </g>
            )}
            {expression === 'smug' && (
              <path d="M-36 -26 L-10 -22" stroke={INK} strokeWidth={6} strokeLinecap="round" />
            )}
            <g transform={`translate(${6 + lookX * 6} 0)`}>
              <Mouth expression={expression} f={frame} />
            </g>
            {/* signature red baseball cap */}
            <g transform={`translate(0 ${-capLift})`}>
              <path
                d="M-86 -34 Q-90 -112 0 -116 Q86 -112 88 -34 Q0 -50 -86 -34 Z"
                fill="#e2231a"
                stroke={INK}
                strokeWidth={LINE}
                strokeLinejoin="round"
              />
              <path d="M-30 -110 Q-12 -70 -6 -42" stroke="#b01810" strokeWidth={5} fill="none" />
              <path d="M30 -110 Q16 -70 12 -42" stroke="#b01810" strokeWidth={5} fill="none" />
              {/* brim pointing forward */}
              <path
                d="M40 -44 Q120 -52 150 -30 Q120 -16 40 -30 Z"
                fill="#c41b13"
                stroke={INK}
                strokeWidth={LINE}
                strokeLinejoin="round"
              />
              <circle cx={0} cy={-114} r={9} fill="#c41b13" stroke={INK} strokeWidth={5} />
              <path d="M-70 -70 Q-40 -96 -10 -100" stroke="rgba(255,255,255,0.45)" strokeWidth={8} fill="none" strokeLinecap="round" />
            </g>
            {sweat && (
              <g transform={`translate(-80 ${-20 + (frame % 20) * 2})`} opacity={1 - (frame % 20) / 22}>
                <path d="M0 0 Q-14 22 0 30 Q14 22 0 0 Z" fill="#7fd3ff" stroke={INK} strokeWidth={4} />
              </g>
            )}
          </g>
        </g>
      </g>
    </g>
  );
};

/** Walk/run cycle helper — returns limb angles for a given phase. */
export const cycle = (frame: number, speed: number, amp: number) => {
  const p = Math.sin(frame * speed);
  return {
    legL: p * amp,
    legR: -p * amp,
    armL: -p * amp * 1.1,
    armR: p * amp * 1.1,
    bob: Math.abs(Math.cos(frame * speed)) * amp * 0.5,
  };
};
