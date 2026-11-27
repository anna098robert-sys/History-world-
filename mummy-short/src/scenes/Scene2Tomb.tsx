import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Camera, Dust, Stage, Vignette} from '../components/Effects';
import {DeepCorridor, GoldenDoor, SharedDefs, SideCorridor} from '../components/Environment';
import {blinkAt, easeOut, FPS, ip, linear, shot} from './helpers';

/** SCENE 2 — THE MYSTERIOUS TOMB (5–12s) */
export const Scene2Tomb: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.0, 3.0, 4.8]);
  const walk = cycle(f, 0.32, 26);

  return (
    <AbsoluteFill>
      <Stage bg="#050302">
        <SharedDefs />
        {s === 0 && (
          // side tracking shot: walking through hieroglyph corridor
          <Camera zoom={ip(t, [0, 2], [1.15, 1.0])} focusX={540} focusY={1100}>
            <SideCorridor scroll={f * 7} frame={f} />
            <Character
              x={430}
              y={1660 - walk.bob}
              scale={1.25}
              expression="curious"
              lookX={0.4}
              lookY={-0.5}
              legL={walk.legL}
              legR={walk.legR}
              armL={walk.armL * 0.6 + 10}
              armR={walk.armR * 0.6 - 10}
              blink={blinkAt(f)}
              frame={f}
            />
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(20,10,0,0.25)" />
          </Camera>
        )}
        {s === 1 && (
          // head-on: corridor stretches into darkness
          <Camera zoom={ip(t, [2, 3], [1.0, 1.12], linear)} focusX={540} focusY={1000}>
            <DeepCorridor frame={f} travel={t * 1.2} vpY={880} />
            <Character
              x={540}
              y={1780 - walk.bob}
              scale={1.35}
              expression="curious"
              lookY={-0.4}
              legL={walk.legL * 0.6}
              legR={walk.legR * 0.6}
              armL={walk.armL * 0.5 + 10}
              armR={walk.armR * 0.5 - 10}
              blink={blinkAt(f, 20)}
              frame={f}
            />
          </Camera>
        )}
        {s >= 2 && (
          // golden door reveal + opening
          <Camera
            zoom={s === 2 ? ip(t, [3, 4.8], [1.35, 1.0], easeOut) : ip(t, [4.8, 7], [1.0, 1.25])}
            focusX={540}
            focusY={s === 2 ? ip(t, [3, 4.8], [600, 1050], easeOut) : ip(t, [4.8, 7], [1050, 900])}
          >
            <SideCorridor scroll={2400} frame={f} />
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(0,0,0,0.35)" />
            <GoldenDoor x={540} y={1500} open={ip(t, [4.9, 6.4], [0, 1], easeOut)} frame={f} s={1.05} />
            {/* sparkles on reveal */}
            {[0, 1, 2, 3, 4, 5, 6, 7].map((k) => {
              const p = ((t - 3 + k * 0.17) % 1.2) / 1.2;
              const x = 260 + ((k * 137) % 560);
              const y = 520 + ((k * 211) % 800);
              return (
                <g key={k} transform={`translate(${x} ${y}) scale(${Math.sin(p * Math.PI) * 1.4}) rotate(${p * 90})`}>
                  <path d="M0 -30 L7 -7 L30 0 L7 7 L0 30 L-7 7 L-30 0 L-7 -7 Z" fill="#fff6c8" />
                </g>
              );
            })}
            <Character
              x={s === 2 ? ip(t, [3, 3.8], [120, 230], easeOut) : ip(t, [4.8, 6.6], [230, 330])}
              y={1740}
              scale={1.2}
              expression={s === 2 ? 'curious' : 'happy'}
              lookX={0.8}
              lookY={-0.8}
              armR={s === 3 ? ip(t, [4.8, 5.2], [-10, -110]) : -10}
              armL={s === 3 ? 30 : 10}
              legL={s === 3 ? Math.sin(f * 0.25) * 10 : 0}
              legR={s === 3 ? -Math.sin(f * 0.25) * 10 : 0}
              blink={blinkAt(f, 40)}
              frame={f}
            />
            {/* warm light washing over hero */}
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(255,210,100,1)" opacity={ip(t, [5.2, 6.6], [0, 0.35])} />
          </Camera>
        )}
        <Dust count={36} />
      </Stage>
      <Vignette strength={0.8} />
    </AbsoluteFill>
  );
};
