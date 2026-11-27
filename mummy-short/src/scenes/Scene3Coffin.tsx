import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Camera, Dust, Flash, Smoke, Stage, Vignette} from '../components/Effects';
import {Chamber, Sarcophagus, SharedDefs} from '../components/Environment';
import {backOut, blinkAt, easeOut, FPS, ip, shot} from './helpers';

/** SCENE 3 — THE BIG MISTAKE (12–19s) */
export const Scene3Coffin: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.0, 2.6, 4.2, 5.0]);
  const walk = cycle(f, 0.3, 24);

  const lid = ip(t, [2.6, 4.0], [0, 1], easeOut);
  const smoke = ip(t, [3.4, 7], [0, 1], (n) => n);
  // lights flashing at 5.0, 5.7, 6.3
  const flick = [5.0, 5.7, 6.3].some((z) => t >= z && t < z + 0.18) ? 0.15 : t >= 5 ? 0.75 + 0.15 * Math.sin(f * 1.3) : 1;

  const heroX = s === 0 ? ip(t, [0, 2], [-80, 250], easeOut) : 250;
  const walking = s === 0 && t < 1.9;

  let cam = {zoom: 1, fx: 540, fy: 1100, shake: 0};
  if (s === 0) cam = {zoom: ip(t, [0, 2], [1.0, 1.1]), fx: 540, fy: 1100, shake: 0};
  if (s === 1) cam = {zoom: 2.5, fx: 280, fy: 1260, shake: 0}; // close-up: "Naturally…"
  if (s === 2) cam = {zoom: ip(t, [2.6, 4.2], [1.3, 1.1]), fx: 540, fy: 1180, shake: ip(t, [2.6, 4.0], [6, 0])};
  if (s === 3) cam = {zoom: ip(t, [4.2, 5], [2.2, 2.4]), fx: 300, fy: 1240, shake: 0}; // "What could possibly go wrong?"
  if (s === 4) cam = {zoom: ip(t, [5, 7], [1.15, 1.3]), fx: 540, fy: 1150, shake: 5};

  const pulling = s === 2;
  return (
    <AbsoluteFill>
      <Stage bg="#050302">
        <SharedDefs />
        <Camera zoom={cam.zoom} focusX={cam.fx} focusY={cam.fy} shake={cam.shake}>
          <Chamber frame={f} flicker={flick} />
          <Sarcophagus x={640} y={1640} s={0.95} lid={lid} frame={f} shake={t > 4.2 ? 3 : 0}>
            <circle cx={0} cy={-380} r={300 * smoke} fill="url(#greenGlow)" opacity={smoke} />
          </Sarcophagus>
          <Character
            x={heroX}
            y={1720 - (walking ? walk.bob : 0)}
            scale={1.15}
            expression={s === 1 ? 'smug' : s === 2 ? 'happy' : s === 3 ? 'smug' : s === 4 ? 'scared' : 'curious'}
            lookX={s === 3 ? -0.3 : 0.7}
            lookY={s === 1 || s === 3 ? 0 : -0.4}
            legL={walking ? walk.legL : pulling ? -14 : 0}
            legR={walking ? walk.legR : pulling ? 18 : 0}
            armL={walking ? walk.armL * 0.6 : pulling ? -100 + Math.sin(f * 0.8) * 8 : s === 3 ? 30 : 10}
            armR={walking ? walk.armR * 0.6 : pulling ? -120 + Math.sin(f * 0.8) * 8 : s === 3 ? -160 : -10}
            bodyTilt={pulling ? -10 : 0}
            headTilt={s === 3 ? -8 : 0}
            squash={pulling ? 1 + Math.sin(f * 0.9) * 0.03 : 1}
            sweat={s >= 4}
            shiver={s === 4 ? 3 : 0}
            blink={s === 1 ? ip(t, [2.2, 2.3, 2.4], [0, 1, 0]) : blinkAt(f)}
            frame={f}
          />
          <Smoke x={640} y={1290} progress={smoke} spread={650} />
          <Dust count={30} />
          {s === 4 && <rect x={0} y={0} width={1080} height={1920} fill="rgba(80,255,170,0.12)" />}
        </Camera>
        {/* thumbs up "what could go wrong" */}
        {s === 3 && (
          <g transform={`translate(800 520) scale(${ip(t, [4.2, 4.4], [0, 1], backOut)}) rotate(10)`}>
            <circle r={110} fill="#ffd400" stroke="#141414" strokeWidth={10} />
            <path d="M-40 40 L-40 -10 L-10 -10 L10 -60 Q30 -60 26 -20 L50 -20 Q66 -18 60 0 L52 44 Q48 54 36 54 L-10 54 Z" fill="#fff" stroke="#141414" strokeWidth={8} strokeLinejoin="round" />
          </g>
        )}
      </Stage>
      <Vignette strength={0.85} />
      <Flash at={Math.round(5.0 * FPS)} dur={3} color="#b6ffd9" peak={0.5} />
      <Flash at={Math.round(5.7 * FPS)} dur={3} color="#b6ffd9" peak={0.5} />
      <Flash at={Math.round(6.3 * FPS)} dur={3} color="#b6ffd9" peak={0.5} />
    </AbsoluteFill>
  );
};
