import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Burst, Camera, Dust, Flash, SpeedLines, Stage, Vignette} from '../components/Effects';
import {Glyph, SharedDefs, SideCorridor} from '../components/Environment';
import {Mummy} from '../components/Mummy';
import {backOut, easeOut, FPS, ip, shot} from './helpers';

/** Ancient "restroom" sign, hieroglyph-style. */
const BathroomSign: React.FC<{x: number; y: number; s?: number; glow?: number}> = ({x, y, s = 1, glow = 0}) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}>
    <circle r={180} fill="url(#goldGlow)" opacity={glow} />
    <rect x={-110} y={-90} width={220} height={180} rx={14} fill="#e8cf96" stroke="#141414" strokeWidth={9} />
    <Glyph kind={7} x={-48} y={18} s={1.2} color="#2f5f9a" />
    <g transform="translate(46 18) scale(1.2)" stroke="#a0302a" strokeWidth={6} fill="none" strokeLinecap="round">
      <circle cx={0} cy={-36} r={9} />
      <path d="M0 -26 L-18 20 L18 20 Z M-6 20 L-8 36 M6 20 L8 36" />
    </g>
    <text x={0} y={-52} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={30} fill="#5a3a14">
      WC
    </text>
  </g>
);

/** SCENE 6 — UNEXPECTED ENDING (33.2–39.5s) */
export const Scene6Ending: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.4, 3.2]);
  const skid = ip(t, [0, 0.35], [1, 0], easeOut);

  return (
    <AbsoluteFill>
      <Stage bg="#050302">
        <SharedDefs />
        {s === 0 && (
          <Camera zoom={ip(t, [0, 0.3, 2.4], [1.35, 1.1, 1.2])} focusX={540} focusY={1150} rotate={ip(t, [0, 0.3], [-6, 0])}>
            <SideCorridor scroll={4600 + skid * 120} frame={f} />
            {/* hallway opening on the right with sign */}
            <rect x={790} y={760} width={260} height={740} fill="#0b0704" stroke="#141414" strokeWidth={10} />
            <BathroomSign x={920} y={640} s={0.9} glow={ip(t, [1.9, 2.2], [0, 1])} />
            {/* skid dust */}
            {skid > 0 && <circle cx={360} cy={1660} r={140 * (1 - skid) + 30} fill={`rgba(220,190,140,${skid * 0.8})`} />}
            {/* mummy — stopped, politely asking, knees together */}
            <Mummy
              x={360 - skid * 80}
              y={1690}
              scale={1.05}
              glow={0.9}
              bodyTilt={skid * -18}
              armL={t > 1.9 ? -95 : t > 0.6 ? -150 : -90}
              armR={t > 0.6 && t <= 1.9 ? 10 : 15}
              mouth={t > 0.4 && t < 2.2 ? 'talk' : 'polite'}
              wiggle={t > 0.5 ? 1 : 0}
              sweat={t > 0.8}
              frame={f}
            />
            {/* question bubble with toilet icon */}
            <g transform={`translate(400 650) scale(${0.85 * ip(t, [1.4, 1.65], [0, 1], backOut)})`}>
              <path d="M-170 -110 Q-170 -170 -110 -170 L110 -170 Q170 -170 170 -110 L170 40 Q170 100 110 100 L-20 100 L-80 170 L-60 100 L-110 100 Q-170 100 -170 40 Z" fill="#fff" stroke="#141414" strokeWidth={10} />
              {/* toilet */}
              <g transform="translate(-40 -40)" stroke="#141414" strokeWidth={7} fill="#cfe8ff" strokeLinejoin="round">
                <rect x={-50} y={-70} width={60} height={60} rx={8} />
                <path d="M-60 -10 L60 -10 Q60 40 0 50 L-10 90 L-40 90 L-40 46 Q-60 30 -60 -10 Z" />
              </g>
              <text x={90} y={20} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={150} fill="#e2231a" stroke="#141414" strokeWidth={6}>
                ?
              </text>
            </g>
            <Character
              x={ip(t, [0, 0.3], [960, 720], easeOut)}
              y={1690}
              scale={1.05}
              facing={-1}
              expression={t < 0.5 ? 'scream' : 'confused'}
              lookX={0.6}
              armL={t < 0.5 ? 140 : 10}
              armR={t < 0.5 ? -150 : -10}
              capLift={t < 0.5 ? 40 : 0}
              headTilt={t > 1 ? 10 : 0}
              frame={f}
            />
            {/* pointing arrow toward hallway */}
            {t > 1.9 && (
              <g transform={`translate(${620 + Math.sin(f * 0.6) * 14} 1060)`} opacity={ip(t, [1.9, 2.05], [0, 1])}>
                <path d="M0 -24 L90 -24 L90 -56 L150 0 L90 56 L90 24 L0 24 Z" fill="#ffd400" stroke="#141414" strokeWidth={8} />
              </g>
            )}
          </Camera>
        )}
        {s === 1 && (
          // close-up: hero stares at the camera — "WHAT?!"
          <Camera zoom={ip(t, [2.4, 2.55, 3.2], [2.2, 2.9, 3.0], backOut)} focusX={540} focusY={1330} shake={ip(t, [2.55, 2.9], [14, 0])}>
            <SideCorridor scroll={4600} frame={f} />
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(255,210,0,0.15)" />
            <Character
              x={540}
              y={1700}
              scale={1.2}
              expression={t < 2.55 ? 'confused' : 'shocked'}
              lookX={-0.4}
              lookY={0.2}
              capLift={ip(t, [2.55, 2.7], [0, 60], backOut)}
              armL={150}
              armR={-150}
              headTilt={-8}
              frame={f}
            />
          </Camera>
        )}
        {s === 1 && <SpeedLines opacity={0.9} cy={800} color="rgba(255,255,255,0.9)" />}
        {s === 1 && <Burst x={540} y={420} text="WHAT?!" t={t - 2.55} size={150} />}
        {s === 2 && <EndCard t={t - 3.2} f={f} />}
        <Dust count={18} />
      </Stage>
      {s < 2 && <Vignette strength={0.7} />}
      <Flash at={0} dur={4} peak={0.8} />
      <Flash at={Math.round(3.2 * FPS)} dur={6} peak={1} />
    </AbsoluteFill>
  );
};

/** End card: History World channel name + subscribe. */
const EndCard: React.FC<{t: number; f: number}> = ({t, f}) => {
  const logo = ip(t, [0, 0.35], [0, 1], backOut);
  const btn = ip(t, [0.2, 0.5], [0, 1], backOut);
  const clicked = t > 1.3;
  const wave = cycle(f, 0.3, 30);
  const rays = f * 0.4;
  const mumRun = cycle(f, 0.6, 40);
  return (
    <g>
      <rect x={0} y={0} width={1080} height={1920} fill="#f2c230" />
      <g transform={`rotate(${rays} 540 760)`}>
        {new Array(16).fill(0).map((_, i) => (
          <path key={i} d="M540 760 L-600 600 L-600 920 Z" fill={i % 2 ? '#f7d35a' : '#e9b522'} transform={`rotate(${i * 22.5} 540 760)`} />
        ))}
      </g>
      {/* pyramids */}
      <path d="M-60 1500 L300 1000 L660 1500 Z" fill="#d79a3a" stroke="#141414" strokeWidth={10} />
      <path d="M420 1500 L820 940 L1220 1500 Z" fill="#c4862c" stroke="#141414" strokeWidth={10} />
      <rect x={0} y={1500} width={1080} height={420} fill="#e3b462" stroke="#141414" strokeWidth={10} />
      {/* logo */}
      <g transform={`translate(540 560) scale(${logo}) rotate(${Math.sin(f * 0.1) * 2})`}>
        <rect x={-470} y={-170} width={940} height={340} rx={50} fill="#141414" />
        <rect x={-450} y={-150} width={900} height={300} rx={40} fill="#fff" stroke="#141414" strokeWidth={8} />
        <text x={0} y={-10} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={150} fill="#e2231a" stroke="#141414" strokeWidth={8} paintOrder="stroke">
          HISTORY
        </text>
        <text x={0} y={130} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={150} fill="#2f7fa0" stroke="#141414" strokeWidth={8} paintOrder="stroke">
          WORLD
        </text>
      </g>
      {/* subscribe button */}
      <g transform={`translate(540 950) scale(${btn * (clicked && t < 1.45 ? 0.9 : 1)})`}>
        <rect x={-330} y={-80} width={660} height={160} rx={80} fill={clicked ? '#606060' : '#e2231a'} stroke="#141414" strokeWidth={10} />
        <text x={0} y={30} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={84} fill="#fff">
          {clicked ? 'SUBSCRIBED ✓' : 'SUBSCRIBE'}
        </text>
      </g>
      {/* bell */}
      <g transform={`translate(910 950) rotate(${clicked ? Math.sin(f * 1.2) * 20 : 0}) scale(${btn})`}>
        <path d="M-40 30 Q-40 -50 0 -54 Q40 -50 40 30 L54 44 L-54 44 Z" fill="#ffd400" stroke="#141414" strokeWidth={8} />
        <circle cx={0} cy={56} r={12} fill="#ffd400" stroke="#141414" strokeWidth={6} />
      </g>
      {/* hand cursor */}
      {t > 0.6 && t < 2.2 && (
        <g transform={`translate(${ip(t, [0.6, 1.25], [900, 600], easeOut)} ${ip(t, [0.6, 1.25], [1300, 1000], easeOut)}) scale(${clicked && t < 1.45 ? 0.85 : 1})`}>
          <path d="M0 0 L0 90 L22 70 L40 110 L56 102 L38 64 L68 64 Z" fill="#fff" stroke="#141414" strokeWidth={7} strokeLinejoin="round" />
        </g>
      )}
      {/* the mummy dashes into the bathroom in the background */}
      <Mummy
        x={ip(t, [0, 2.3], [-150, 1250], (n) => n)}
        y={1500}
        scale={0.5}
        glow={1}
        armL={-20}
        armR={-30}
        legL={mumRun.legL}
        legR={mumRun.legR}
        bodyTilt={-12}
        mouth="polite"
        frame={f}
        wiggle={0.5}
      />
      {/* hero waving goodbye */}
      <Character
        x={300}
        y={1840}
        scale={1.0}
        expression="happy"
        armR={-150 + wave.armR * 0.8}
        armL={10}
        headTilt={Math.sin(f * 0.2) * 5}
        blink={(f % 60) < 3 ? 1 : 0}
        frame={f}
      />
      <g transform={`translate(760 1760) scale(${ip(t, [0.8, 1.1], [0, 1], backOut)})`}>
        <rect x={-250} y={-60} width={500} height={120} rx={24} fill="#141414" />
        <text x={0} y={22} textAnchor="middle" fontFamily="LuckiestGuy" fontSize={52} fill="#ffd400">
          MORE DISASTERS!
        </text>
      </g>
    </g>
  );
};
