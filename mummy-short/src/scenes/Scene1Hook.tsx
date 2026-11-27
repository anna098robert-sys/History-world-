import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character} from '../components/Character';
import {Camera, Dust, Flash, SpeedLines, Stage, Vignette, Burst} from '../components/Effects';
import {Chamber, SharedDefs} from '../components/Environment';
import {Mummy} from '../components/Mummy';
import {backOut, easeOut, FPS, ip, shot} from './helpers';

/** SCENE 1 — SHOCKING HOOK (0–5s) */
export const Scene1Hook: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [1.3, 2.6, 3.4]);

  const eyes = ip(t, [1.45, 1.6], [0, 1], easeOut);
  const glow = eyes * (1 + 0.15 * Math.sin(f * 0.6));
  const mummyRise = ip(t, [3.4, 3.9], [0, 1], backOut);

  // camera per shot
  let cam = {zoom: 2.3, fx: 430, fy: 1340, rot: -4, shake: 3};
  if (s === 0) cam = {zoom: ip(t, [0, 1.3], [2.6, 2.3]), fx: 430, fy: 1340, rot: -4, shake: 3};
  if (s === 1) cam = {zoom: ip(t, [1.3, 2.6], [1.5, 3.4], easeOut), fx: ip(t, [1.3, 2.6], [560, 760]), fy: ip(t, [1.3, 2.6], [1200, 935]), rot: 0, shake: 2};
  if (s === 2) cam = {zoom: ip(t, [2.6, 3.4], [3.0, 2.6]), fx: 430, fy: 1330, rot: 5, shake: 8};
  if (s === 3) cam = {zoom: ip(t, [3.4, 5], [1.25, 1.05], easeOut), fx: 560, fy: 1180, rot: 0, shake: ip(t, [3.4, 4.2], [26, 4])};

  const shocked = s >= 2;

  return (
    <AbsoluteFill>
      <Stage bg="#050302">
        <SharedDefs />
        <Camera zoom={cam.zoom} focusX={cam.fx} focusY={cam.fy} rotate={cam.rot} shake={cam.shake}>
          <Chamber frame={f} flicker={0.55} />
          <rect x={0} y={0} width={1080} height={1920} fill="rgba(10,40,30,0.45)" />
          {/* mummy looming behind */}
          <g opacity={0.35 + eyes * 0.65}>
            <circle cx={760} cy={930} r={420 * glow} fill="url(#greenGlow)" opacity={eyes} />
            <Mummy
              x={760}
              y={1700 - mummyRise * 30}
              scale={1.85}
              facing={-1}
              glow={glow}
              eyesOpen={eyes}
              armL={-90 - mummyRise * 40}
              armR={-90 - mummyRise * 50}
              mouth={s >= 3 ? 'groan' : 'none'}
              frame={f}
              headTilt={s >= 3 ? Math.sin(f * 0.3) * 4 : 0}
            />
          </g>
          {/* hero — terrified, doesn't see it yet (s0) then looks back */}
          <Character
            x={430}
            y={1720}
            scale={1.6}
            expression={s === 0 ? 'scared' : s === 1 ? 'scared' : s === 2 ? 'terrified' : 'terrified'}
            lookX={s === 0 ? -0.6 : 0.8}
            lookY={s === 0 ? 0.2 : -0.2}
            headTilt={s >= 2 ? -6 : 4}
            armL={s >= 3 ? 150 : 20}
            armR={s >= 3 ? -150 : -30}
            sweat
            shiver={shocked ? 5 : 2.5}
            capLift={s === 2 ? ip(t, [2.6, 2.75, 3.3], [0, 70, 30], backOut) : s === 3 ? 20 : 0}
            squash={s === 2 ? ip(t, [2.6, 2.7, 2.9], [1, 1.1, 1]) : 1}
            frame={f}
          />
          <Dust count={30} color="rgba(170,255,210,0.5)" />
        </Camera>
        {s === 2 && <SpeedLines opacity={0.8} />}
        {s === 3 && <Burst x={760} y={430} text="3000 YRS!" t={t - 3.45} size={92} rot={8} />}
      </Stage>
      <Vignette strength={0.85} />
      {/* hook title */}
      <div
        style={{
          position: 'absolute',
          top: 150,
          left: 40,
          right: 40,
          textAlign: 'center',
          fontFamily: 'LuckiestGuy',
          fontSize: 92,
          lineHeight: 1.05,
          color: '#fff',
          WebkitTextStroke: '12px #141414',
          paintOrder: 'stroke fill',
          transform: `scale(${ip(t, [0, 0.25], [0.3, 1], backOut)}) rotate(-2deg)`,
          textShadow: '0 8px 0 rgba(0,0,0,0.5)',
        }}
      >
        I ACCIDENTALLY WOKE UP <span style={{color: '#ffd400'}}>A MUMMY!</span> 💀
      </div>
      <Flash at={Math.round(1.45 * FPS)} dur={6} color="#b6ffd9" peak={0.6} />
      <Flash at={Math.round(3.4 * FPS)} dur={8} peak={0.9} />
      <Flash at={0} dur={6} color="#000" peak={1} />
    </AbsoluteFill>
  );
};
