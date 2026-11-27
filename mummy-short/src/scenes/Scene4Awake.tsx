import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character} from '../components/Character';
import {Burst, Camera, Dust, Flash, Smoke, SpeedLines, Stage, Vignette} from '../components/Effects';
import {Chamber, Sarcophagus, SharedDefs} from '../components/Environment';
import {Mummy} from '../components/Mummy';
import {backOut, easeIn, easeOut, FPS, ip, shot} from './helpers';

/** SCENE 4 — THE MUMMY AWAKENS (19–26.5s) */
export const Scene4Awake: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.0, 3.2, 4.4, 5.2]);

  const eyes = ip(t, [0.9, 1.3], [0, 1], easeOut);
  const glow = eyes * (1 + 0.2 * Math.sin(f * 0.5));
  const rise = ip(t, [2.0, 3.3], [0, 1], easeIn);

  return (
    <AbsoluteFill>
      <Stage bg="#000">
        <SharedDefs />
        {s === 0 && (
          // total darkness — just two glowing eyes
          <Camera zoom={ip(t, [0, 2], [1, 1.35])} focusX={540} focusY={900}>
            <rect x={0} y={0} width={1080} height={1920} fill="#020302" />
            <Smoke x={540} y={1500} progress={0.6 + t * 0.1} color="60,140,100" spread={300} count={14} />
            <circle cx={540} cy={900} r={500 * glow} fill="url(#greenGlow)" opacity={eyes * 0.8} />
            {[-1, 1].map((d) => (
              <g key={d}>
                <ellipse cx={540 + d * 110} cy={900} rx={60} ry={44 * eyes} fill="#b6ffd9" />
                <ellipse cx={540 + d * 110} cy={900} rx={22} ry={18 * eyes} fill="#fff" />
              </g>
            ))}
          </Camera>
        )}
        {s >= 1 && s <= 2 && (
          // low angle: mummy rises out of the sarcophagus
          <Camera
            zoom={s === 1 ? ip(t, [2, 3.2], [1.5, 1.25]) : 1.15}
            focusX={600}
            focusY={s === 1 ? 1050 : 1000}
            shake={s === 2 ? ip(t, [3.2, 4.0], [30, 6]) : 3}
          >
            <Chamber frame={f} flicker={0.35} />
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(20,80,60,0.35)" />
            <circle cx={620} cy={800} r={600} fill="url(#greenGlow)" opacity={0.6} />
            <Sarcophagus x={620} y={1720} s={1} lid={1} frame={f}>
              <g transform={`translate(0 ${-380 + (1 - rise) * 420})`}>
                <Mummy
                  x={0}
                  y={0}
                  scale={1.15}
                  noLegs
                  glow={1 + 0.2 * Math.sin(f * 0.5)}
                  armL={s === 2 ? -150 + Math.sin(f * 0.4) * 10 : -90}
                  armR={s === 2 ? -160 - Math.sin(f * 0.4) * 10 : -90}
                  mouth="groan"
                  headTilt={Math.sin(f * 0.2) * 5}
                  frame={f}
                />
              </g>
            </Sarcophagus>
            <Smoke x={620} y={1420} progress={ip(t, [2, 4.4], [0.55, 1], (n) => n)} spread={420} count={14} color="150,230,190" />
            <Dust count={30} color="rgba(170,255,210,0.5)" />
          </Camera>
        )}
        {s === 2 && <SpeedLines opacity={ip(t, [3.2, 3.5, 4.4], [0, 0.9, 0.3])} cy={800} />}
        {s === 2 && <Burst x={540} y={380} text="ALIVE!" t={t - 3.25} size={130} />}
        {s >= 3 && (
          // hero freezes … then SCREAMS
          <Camera
            zoom={s === 3 ? ip(t, [4.4, 5.2], [2.0, 2.2]) : ip(t, [5.2, 5.5], [1.6, 2.1], backOut)}
            focusX={s === 4 && t > 6.9 ? ip(t, [6.9, 7.5], [560, 820], easeIn) : 560}
            focusY={1300}
            shake={s === 4 ? 14 : 0}
            rotate={s === 4 ? Math.sin(f * 0.8) * 3 : 0}
          >
            <Chamber frame={f} flicker={0.45} />
            <rect x={0} y={0} width={1080} height={1920} fill="rgba(20,80,60,0.35)" />
            <Mummy x={110} y={1760} scale={1.5} facing={1} glow={1.1} armL={-110} armR={-120} mouth="groan" frame={f} />
            <Character
              x={s === 4 && t > 6.9 ? ip(t, [6.9, 7.5], [600, 1500], easeIn) : 600}
              y={1740}
              scale={1.3}
              facing={s === 4 && t > 6.9 ? 1 : -1}
              expression={s === 3 ? 'shocked' : 'scream'}
              lookX={s === 3 ? 0.9 : 0}
              armL={s === 3 ? 4 : 160 + Math.sin(f * 1.5) * 15}
              armR={s === 3 ? -4 : -160 - Math.sin(f * 1.5) * 15}
              capLift={s === 3 ? ip(t, [4.6, 4.75], [0, 90], backOut) : 40 + Math.abs(Math.sin(f * 0.9)) * 30}
              squash={s === 3 ? ip(t, [4.6, 4.7, 4.85], [1, 1.12, 1]) : 1.05}
              shiver={s === 4 ? 6 : 0}
              boil={s === 3 ? 0 : 1}
              frame={f}
            />
          </Camera>
        )}
        {s === 4 && <SpeedLines opacity={0.9} cx={540} cy={900} color="rgba(255,240,180,0.8)" />}
        {s === 3 && <rect x={0} y={0} width={1080} height={1920} fill="rgba(255,255,255,0.06)" />}
      </Stage>
      <Vignette strength={0.9} />
      {/* freeze-frame look: desaturate during shock */}
      {s === 3 && <AbsoluteFill style={{backdropFilter: 'grayscale(0.7) contrast(1.2)'}} />}
      <Flash at={Math.round(3.2 * FPS)} dur={8} color="#c8ffe6" peak={0.95} />
      <Flash at={Math.round(5.2 * FPS)} dur={5} color="#fff" peak={0.7} />
    </AbsoluteFill>
  );
};
