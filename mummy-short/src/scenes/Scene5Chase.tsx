import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Burst, Camera, Dust, MotionStreaks, Stage, Vignette} from '../components/Effects';
import {DeepCorridor, SharedDefs, SideCorridor} from '../components/Environment';
import {Mummy} from '../components/Mummy';
import {easeIn, FPS, ip, linear, shot} from './helpers';

const DustPuffs: React.FC<{x: number; y: number; f: number; dir?: number}> = ({x, y, f, dir = 1}) => (
  <g>
    {[0, 1, 2, 3, 4].map((k) => {
      const p = ((f + k * 4) % 20) / 20;
      return (
        <circle
          key={k}
          cx={x - dir * (40 + p * 220)}
          cy={y - p * 60 - k * 6}
          r={20 + p * 46}
          fill={`rgba(220,190,140,${0.7 * (1 - p)})`}
        />
      );
    })}
  </g>
);

/** SCENE 5 — THE CHASE (26.5–33.2s) */
export const Scene5Chase: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.1, 2.9, 4.5, 5.3]);
  const run = cycle(f, 0.75, 55);
  const mwalk = cycle(f, 0.45, 26);

  return (
    <AbsoluteFill>
      <Stage bg="#050302">
        <SharedDefs />
        {(s === 0 || s === 4) && (
          // side tracking chase
          <Camera zoom={s === 0 ? ip(t, [0, 2.1], [1.2, 1.0]) : 1.05} focusX={540} focusY={1150} rotate={s === 4 ? -4 : 2}>
            <SideCorridor scroll={f * 34} frame={f} />
            <Mummy
              x={s === 0 ? ip(t, [0, 2.1], [-120, 190]) : ip(t, [5.3, 6.7], [160, 330])}
              y={1680 - mwalk.bob}
              scale={1.05}
              glow={1.1}
              armL={-90 + Math.sin(f * 0.45) * 8}
              armR={-90 - Math.sin(f * 0.45) * 8}
              legL={mwalk.legL}
              legR={mwalk.legR}
              mouth="groan"
              frame={f}
            />
            <DustPuffs x={700} y={1660} f={f} />
            <Character
              x={700 + Math.sin(f * 0.3) * 20}
              y={1660 - run.bob * 1.4}
              scale={1.05}
              expression="scream"
              lookX={-0.6}
              legL={run.legL}
              legR={run.legR}
              armL={140 + Math.sin(f * 0.9) * 30}
              armR={-150 - Math.sin(f * 0.9) * 30}
              bodyTilt={-14}
              capLift={30 + Math.abs(Math.sin(f * 0.75)) * 25}
              sweat
              frame={f}
            />
            <MotionStreaks opacity={0.8} />
          </Camera>
        )}
        {s === 1 && (
          // head-on: running straight at the camera
          <Camera zoom={ip(t, [2.1, 2.9], [1.0, 1.2], linear)} focusX={540} focusY={1100} shake={8}>
            <DeepCorridor frame={f} travel={t * 6} vpY={850} />
            <Mummy
              x={540 + Math.sin(f * 0.3) * 30}
              y={1260}
              scale={0.7}
              glow={1.2}
              armL={-90}
              armR={-90}
              legL={mwalk.legL}
              legR={mwalk.legR}
              mouth="groan"
              frame={f}
            />
            <Character
              x={540 + Math.sin(f * 0.4) * 50}
              y={1820 - run.bob}
              scale={ip(t, [2.1, 2.9], [1.3, 1.7], linear)}
              expression="scream"
              legL={run.legL * 0.6}
              legR={run.legR * 0.6}
              armL={150 + Math.sin(f * 0.9) * 25}
              armR={-150 - Math.sin(f * 0.9) * 25}
              capLift={40}
              frame={f}
            />
          </Camera>
        )}
        {s === 2 && (
          // hallway gag: hero zips across, mummy follows… then hero zips BACK the other way
          <Camera zoom={1.1} focusX={540} focusY={1150}>
            <SideCorridor scroll={4000} frame={f} />
            {(() => {
              const lt = t - 2.9;
              const heroX = lt < 0.55 ? ip(lt, [0, 0.55], [-250, 1400], linear) : ip(lt, [0.95, 1.5], [1400, -300], linear);
              const heroDir = lt < 0.55 ? 1 : -1;
              const mumX = ip(lt, [0.3, 1.6], [-250, 1400], linear);
              return (
                <>
                  <Mummy x={mumX} y={1680 - mwalk.bob} scale={1.05} glow={1.1} armL={-90} armR={-90} legL={mwalk.legL} legR={mwalk.legR} mouth="groan" frame={f} />
                  <DustPuffs x={heroX} y={1660} f={f} dir={heroDir} />
                  <Character
                    x={heroX}
                    y={1660 - run.bob}
                    scale={1.05}
                    facing={heroDir as 1 | -1}
                    expression="scream"
                    legL={run.legL}
                    legR={run.legR}
                    armL={140}
                    armR={-150}
                    bodyTilt={-16}
                    capLift={40}
                    frame={f}
                  />
                </>
              );
            })()}
          </Camera>
        )}
        {s === 3 && (
          // low dutch-angle close-up: cartoon wheel legs + boing off a column
          <Camera zoom={1.9} focusX={540} focusY={1450} rotate={-12} shake={6}>
            <SideCorridor scroll={f * 40} frame={f} />
            <g opacity={0.9}>
              {[0, 1].map((k) => (
                <ellipse key={k} cx={500} cy={1560} rx={70} ry={70} fill="none" stroke="rgba(20,20,20,0.5)" strokeWidth={10} strokeDasharray="30 22" transform={`rotate(${f * 60 + k * 40} 500 1560)`} />
              ))}
            </g>
            <Character
              x={500}
              y={1660 - Math.abs(Math.sin(f * 0.5)) * ip(t, [4.6, 4.8, 5.1], [0, 120, 0], easeIn)}
              scale={1.05}
              expression="scream"
              legL={Math.sin(f * 1.6) * 80}
              legR={-Math.sin(f * 1.6) * 80}
              armL={150}
              armR={-150}
              bodyTilt={-18}
              capLift={45}
              frame={f}
            />
            <DustPuffs x={500} y={1660} f={f} />
          </Camera>
        )}
        {s === 3 && <Burst x={760} y={560} text="ZOOM!" t={t - 4.55} size={110} rot={10} />}
        <Dust count={20} />
      </Stage>
      <Vignette strength={0.75} />
    </AbsoluteFill>
  );
};
