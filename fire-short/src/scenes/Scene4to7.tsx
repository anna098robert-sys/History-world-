import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Burst, Camera, Flash, SpeedLines, Vignette} from '../components/Effects';
import {Embers, Flame, FireWall, SmokeColumn, SmokeHaze} from '../components/Fire';
import {FleeingCrowd, House, HouseRow, OldStPauls, Ruins, Skyline, Street} from '../components/London';
import {Portal, TimeMachine} from '../components/TimeMachine';
import {Caption, FireLight, Scene} from './common';
import {backOut, blinkAt, easeIn, easeOut, FPS, ip, linear, shot} from './helpers';

/* ============================== SCENE 4 — THE CITY BURNS (18–27s) */
export const Scene4Burns: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0, 7.0]);
  const run = cycle(f, 0.75, 52);
  // wind from the east pushes the fire west (right → left on screen)
  const spread = (cx: number, delay = 0) => ip(t, [delay + (1080 - cx) / 520, delay + (1080 - cx) / 520 + 0.5], [0, 1], linear);
  return (
    <Scene overlay={<><Vignette strength={0.8} color="30,5,0" /><Flash at={Math.round(2.5 * FPS)} dur={4} color="#ffcf6a" peak={0.5} /></>}>
      {s === 0 && (
        // high view over packed rooftops — the fire marches west row by row
        <Camera zoom={ip(t, [0, 2.5], [1.1, 1.0])} focusX={ip(t, [0, 2.5], [640, 480])} focusY={1050}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <SmokeHaze y={380} opacity={0.9} color="35,18,14" speed={-4} />
          <Skyline y={760} color="#2a120c" />
          <g transform="translate(0 -40) scale(0.55)">
            <HouseRow y={1700} x0={-300} count={12} seedBase={5} burnAt={(i, cx) => spread(cx * 0.55, -0.4)} lean={-120} />
          </g>
          <g transform="translate(0 260) scale(0.75)">
            <HouseRow y={1700} x0={-300} count={10} seedBase={9} burnAt={(i, cx) => spread(cx * 0.75, 0.1)} lean={-120} />
          </g>
          <HouseRow y={1900} x0={-250} count={7} seedBase={1} burnAt={(i, cx) => spread(cx, 0.7)} lean={-120} />
          <SmokeColumn x={950} y={900} height={1300} width={320} drift={-800} seed="b1" />
          <SmokeColumn x={600} y={1000} height={1200} width={260} drift={-800} seed="b2" opacity={ip(t, [0.5, 1.5], [0, 1])} />
          <Embers count={90} wind={-14} rise={6} seed="b0" />
          <FireLight strength={0.25} />
        </Camera>
      )}
      {s === 1 && (
        // side tracking: hero sprints west, dodges a falling burning beam
        <Camera zoom={1.05} focusX={540} focusY={1200} rotate={-2} shake={t > 3.6 && t < 4.0 ? 18 : 4}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <Skyline y={1000} color="#2a120c" scroll={-f * 4} />
          <HouseRow y={1560} x0={-2600} count={20} seedBase={3} scroll={-f * 22} burnAt={() => 1} charred={0.3} lean={-110} />
          <Street y={1560} scroll={-f * 22} tint="rgba(255,90,20,0.15)" />
          {/* falling beam */}
          {(() => {
            const bt = ip(t, [3.0, 3.6], [0, 1], easeIn);
            const bx = 380 + (t - 3.0) * 22 * FPS * 0.3;
            return t > 2.9 ? (
              <g transform={`translate(${bx} ${ip(bt, [0, 1], [700, 1640], linear)}) rotate(${bt * 70 - 20})`}>
                <rect x={-160} y={-22} width={320} height={44} fill="#3a2414" stroke="#141414" strokeWidth={6} />
                <Flame x={0} y={-10} w={260} h={180} seed="beam" lean={-60} tongues={10} />
              </g>
            ) : null;
          })()}
          <Character
            x={540}
            y={1700 - run.bob * 1.3 - (t > 3.35 && t < 3.95 ? Math.sin(((t - 3.35) / 0.6) * Math.PI) * 220 : 0)}
            scale={1.1}
            facing={-1}
            expression="terrified"
            lookX={-0.3}
            legL={run.legL}
            legR={run.legR}
            armL={run.armL}
            armR={run.armR}
            bodyTilt={-12}
            capLift={20}
            sweat
            frame={f}
          />
          <Embers count={70} wind={-10} rise={-6} seed="b1e" />
          <FireLight strength={0.3} />
        </Camera>
      )}
      {s === 1 && <Burst x={760} y={600} text="CRASH!" t={t - 3.6} size={110} color="#ff9a2a" />}
      {s === 2 && (
        // low angle: running at camera under burning overhanging (jettied) houses
        <Camera zoom={ip(t, [5, 7], [1.0, 1.15], linear)} focusX={540} focusY={1100} shake={6}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <SmokeHaze y={600} opacity={1} color="30,15,10" speed={-6} />
          <Skyline y={1150} color="#2a120c" />
          <g transform="translate(-520 300) scale(1.5)">
            <House x={0} y={1100} w={300} floors={4} seed={7} burn={1} charred={0.3} lean={-80} />
          </g>
          <g transform="translate(1080 300) scale(-1.5 1.5)">
            <House x={0} y={1100} w={300} floors={4} seed={2} burn={1} charred={0.3} lean={80} />
          </g>
          <Street y={1500} tint="rgba(255,90,20,0.2)" />
          <FleeingCrowd y={1560} count={5} dir={1} speed={8} s={0.55} seed="lr" silhouette="#2a1410" />
          <Character
            x={540 + Math.sin(f * 0.37) * 40}
            y={1830 - run.bob}
            scale={ip(t, [5, 7], [1.1, 1.5], linear)}
            expression="scream"
            legL={run.legL * 0.6}
            legR={run.legR * 0.6}
            armL={150 + Math.sin(f * 0.9) * 20}
            armR={-150 - Math.sin(f * 0.9) * 20}
            capLift={25}
            frame={f}
          />
          <Embers count={80} wind={-4} rise={-9} seed="b2e" size={1.2} />
          <FireLight strength={0.3} />
        </Camera>
      )}
      {s === 3 && (
        // the wind gust: flames sweep sideways, ember storm, hero holds his cap
        <Camera zoom={ip(t, [7, 9], [1.2, 1.05])} focusX={540} focusY={1250} rotate={ip(t, [7, 9], [3, -3])} shake={10}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <SmokeHaze y={500} opacity={1} color="40,18,12" speed={-22} />
          <Skyline y={1050} color="#2a120c" />
          <FireWall x0={-200} x1={1300} y={1250} h={700} seed="gust" lean={ip(t, [6.8, 7.4], [-80, -260])} step={170} />
          <HouseRow y={1580} count={7} seedBase={6} burnAt={() => 1} charred={0.5} lean={-200} />
          <Street y={1580} tint="rgba(255,90,20,0.2)" />
          <Character
            x={560}
            y={1820}
            scale={1.25}
            facing={1}
            expression="scared"
            lookX={-0.4}
            bodyTilt={-14}
            headTilt={-12}
            armR={-175}
            armL={-60}
            legL={-12}
            legR={16}
            sweat
            shiver={3}
            frame={f}
          />
          <Embers count={140} wind={-30} rise={2} seed="g" size={1.1} />
          <FireLight strength={0.32} />
        </Camera>
      )}
    </Scene>
  );
};

/* ============================== SCENE 5 — THE CATASTROPHE (27–36s) */
export const Scene5Catastrophe: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.6, 4.4]);
  const collapse = ip(t, [7.4, 8.2], [0, 1], easeIn);
  return (
    <Scene
      overlay={
        <>
          <Vignette strength={0.85} color="30,5,0" />
          {s === 2 && <Caption text="OLD ST PAUL'S CATHEDRAL" sub="destroyed by the fire, 4 September 1666" show={ip(t, [4.8, 5.1, 7.2, 7.4], [0, 1, 1, 0])} top={300} />}
          <Flash at={Math.round(7.4 * FPS)} dur={8} color="#ffd27a" peak={0.85} />
        </>
      }
    >
      {s === 0 && (
        // trapped: wall of fire at both ends of the street, whip pans left/right
        <Camera
          zoom={1.35}
          focusX={ip(t, [0, 0.8, 1.0, 1.6, 1.8, 2.6], [540, 540, 280, 280, 800, 540], easeOut)}
          focusY={1300}
          shake={5}
        >
          <rect x={-400} y={-200} width={1880} height={2400} fill="url(#skyFire)" />
          <Skyline y={1050} color="#2a120c" />
          <HouseRow y={1580} x0={-500} count={9} seedBase={4} burnAt={() => 1} charred={0.45} lean={-100} />
          <Street y={1580} tint="rgba(255,90,20,0.2)" />
          <FireWall x0={-400} x1={160} y={1700} h={1100} seed="wl" lean={-40} step={140} />
          <FireWall x0={920} x1={1480} y={1700} h={1100} seed="wr" lean={-60} step={140} />
          <Character
            x={540}
            y={1760}
            scale={1.2}
            facing={t > 1.6 ? 1 : -1}
            expression="terrified"
            lookX={0.8}
            armL={30}
            armR={-40}
            sweat
            shiver={3}
            frame={f}
          />
          <Embers count={80} wind={-6} rise={8} seed="c0" />
          <FireLight strength={0.32} />
        </Camera>
      )}
      {s === 1 && (
        // close-up: face lit by the inferno
        <Camera zoom={ip(t, [2.6, 4.4], [2.3, 2.6], linear)} focusX={540} focusY={1280} shake={3}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <FireWall x0={-200} x1={1300} y={1500} h={900} seed="cu" lean={-70} step={170} />
          <Character x={540} y={1760} scale={1.2} expression="scared" lookX={0} sweat shiver={2} blink={blinkAt(f)} frame={f} />
          <Embers count={50} wind={-5} rise={7} seed="c1" />
          <FireLight strength={0.38} />
        </Camera>
      )}
      {s === 2 && (
        // Old St Paul's engulfed; hero watches in shock
        <Camera zoom={ip(t, [4.4, 9], [0.95, 1.12], linear)} focusX={560} focusY={1150} shake={t > 7.4 && t < 8.2 ? 20 : 2}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <SmokeHaze y={350} opacity={1} color="30,14,10" speed={-4} />
          <SmokeColumn x={620} y={700} height={1100} width={380} drift={-700} seed="p1" />
          <g transform="translate(0 790) scale(0.45)">
            <HouseRow y={1700} x0={-300} count={14} seedBase={8} burnAt={() => 1} charred={0.5} lean={-120} />
          </g>
          <OldStPauls x={660} y={1520} s={0.78} burn={ip(t, [4.4, 6], [0.5, 1])} collapse={collapse} />
          <Street y={1560} tint="rgba(255,90,20,0.25)" />
          <FleeingCrowd y={1620} count={5} dir={-1} speed={12} s={0.6} seed="sp" silhouette="#1c0c08" />
          <Character x={200} y={1880} scale={1.25} facing={1} expression="shocked" lookX={0.6} lookY={-0.7} headTilt={-6} armL={10} armR={-10} capLift={t > 7.4 ? ip(t, [7.4, 7.6], [0, 40], backOut) : 0} frame={f} />
          <Embers count={110} wind={-9} rise={8} seed="c2" />
          {collapse > 0 && collapse < 1 && <Embers count={60} wind={-2} rise={18} seed="cb" size={1.6} area={{x: 300, y: 600, w: 700, h: 900}} />}
          <FireLight strength={0.3} />
        </Camera>
      )}
    </Scene>
  );
};

/* ============================== SCENE 6 — HISTORICAL AFTERMATH (36–44s) */
export const Scene6Aftermath: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [1.2, 4.0, 6.0]);
  const walk = cycle(f, 0.18, 14);
  const fade = ip(t, [0, 1.2], [0, 1], linear);
  return (
    <Scene
      bg="#57524f"
      overlay={
        <>
          <Vignette strength={0.6} color="20,18,16" />
          <Caption text="6 SEPTEMBER 1666" sub="About 13,200 houses and 87 parish churches lost" show={ip(t, [1.4, 1.8, 3.8, 4.0], [0, 1, 1, 0])} top={300} />
        </>
      }
    >
      {s === 0 && (
        // the fire burns itself out — inferno dissolves to ash
        <Camera zoom={1.05} focusX={560} focusY={1150}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyAsh)" opacity={fade} />
          <OldStPauls x={640} y={1380} s={0.62} burn={1 - fade} ruin={fade > 0.6 ? 1 : 0} />
          <g transform="translate(0 260) scale(0.7)">
            <HouseRow y={1700} x0={-300} count={10} seedBase={8} burnAt={() => 1 - fade} charred={0.5 + fade * 0.5} lean={-120} />
          </g>
          <Street y={1560} />
          <SmokeHaze y={700} opacity={0.4 + fade * 0.6} color="120,115,110" speed={-1} />
        </Camera>
      )}
      {s >= 1 && (
        <Camera
          zoom={s === 1 ? ip(t, [1.2, 4], [1.0, 1.08]) : s === 2 ? 1.25 : ip(t, [6, 8], [1.6, 1.75])}
          focusX={s === 1 ? ip(t, [1.2, 4], [460, 620]) : s === 2 ? 540 : 520}
          focusY={s === 3 ? 1400 : 1250}
        >
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyAsh)" />
          <SmokeHaze y={500} opacity={0.6} color="140,135,128" speed={-1} />
          <OldStPauls x={700} y={1250} s={0.45} ruin={1} />
          <SmokeColumn x={300} y={1300} height={800} width={120} drift={-200} dark={0.2} seed="a1" lit={0} opacity={0.7} />
          <SmokeColumn x={850} y={1350} height={800} width={140} drift={-200} dark={0.25} seed="a2" lit={0} opacity={0.7} />
          <Ruins y={1560} />
          <rect x={0} y={1600} width={1080} height={320} fill="#4a443f" />
          <Ruins y={1700} seed="r2" />
          {s >= 2 && (
            <Character
              x={s === 2 ? ip(t, [4, 6], [300, 520], linear) : 520}
              y={1840 - (s === 2 ? walk.bob : 0)}
              scale={1.2}
              facing={1}
              expression={s === 2 ? 'neutral' : 'happy'}
              blink={s === 2 ? 0.55 : blinkAt(f)}
              headTilt={s === 2 ? 14 : 0}
              bodyTilt={s === 2 ? 8 : 0}
              legL={s === 2 ? walk.legL : 0}
              legR={s === 2 ? walk.legR : 0}
              armL={s === 2 ? 4 : 10}
              armR={s === 2 ? -4 : t > 6.3 && t < 7.3 ? -165 : -10}
              lookX={s === 3 ? -0.3 : 0.2}
              frame={f}
            />
          )}
          {/* a few last embers dying out */}
          <Embers count={12} wind={-2} rise={2} seed="ad" size={0.7} />
        </Camera>
      )}
    </Scene>
  );
};

/* ============================== SCENE 7 — UNEXPECTED TWIST (44–50s) */
export const Scene7Twist: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [1.3, 3.3, 4.4]);
  const portal = ip(t, [3.4, 3.9], [0, 1], backOut);
  const suck = ip(t, [3.75, 4.4], [0, 1], easeIn);
  return (
    <Scene
      bg="#57524f"
      overlay={
        <>
          {s < 3 && <Vignette strength={0.6} color="20,18,16" />}
          {s === 3 && <EndCard t={t - 4.4} />}
          <Flash at={Math.round(3.3 * FPS)} dur={5} color="#c8f6ff" peak={0.8} />
          <Flash at={Math.round(4.4 * FPS)} dur={7} peak={1} />
        </>
      }
    >
      {s === 0 && (
        <Camera zoom={ip(t, [0, 1.3], [1.5, 1.8])} focusX={540} focusY={1400}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyAsh)" />
          <OldStPauls x={700} y={1250} s={0.45} ruin={1} />
          <Ruins y={1560} />
          <rect x={0} y={1600} width={1080} height={320} fill="#4a443f" />
          <Character x={480} y={1840} scale={1.2} expression="happy" lookX={0.6} lookY={0.3} armR={ip(t, [0, 0.4], [-10, -70], backOut)} blink={blinkAt(f)} frame={f} />
          <TimeMachine x={640} y={ip(t, [0, 0.4], [1700, 1600], backOut)} s={0.42} power={ip(t, [0.2, 0.6], [0, 1])} screen="boot" />
        </Camera>
      )}
      {s === 1 && (
        // over-the-shoulder close-up of the screen
        <Camera zoom={ip(t, [1.3, 3.3], [1.0, 1.15], linear)} focusX={540} focusY={1000} shake={t > 1.4 && t < 1.8 ? 6 : 0}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyAsh)" />
          <rect x={-200} y={-200} width={1480} height={2400} fill="rgba(255,40,30,0.18)" opacity={Math.floor(f / 6) % 2} />
          <TimeMachine x={560} y={950} s={2.1} rot={-4} screen="pompeii" />
          <Character x={-40} y={2250} scale={1.6} facing={1} expression="curious" lookX={0.8} lookY={-0.5} frame={f} />
        </Camera>
      )}
      {s === 2 && (
        // horror → portal opens and pulls him away
        <Camera zoom={ip(t, [3.3, 3.5], [2.4, 1.9], backOut)} focusX={540} focusY={1250} shake={12} rotate={Math.sin(f * 0.7) * 3}>
          <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyAsh)" />
          <Ruins y={1560} />
          <rect x={0} y={1600} width={1080} height={320} fill="#4a443f" />
          <Portal x={760} y={1150} open={portal} />
          <g transform={`translate(${suck * 300} ${-suck * 400}) rotate(${suck * 260} 480 1500)`}>
            <Character
              x={480}
              y={1840}
              scale={1.2 * (1 - suck * 0.8)}
              expression="scream"
              lookX={0.8}
              armL={160 + Math.sin(f * 1.4) * 15}
              armR={-160 - Math.sin(f * 1.4) * 15}
              capLift={10}
              squash={1 + suck * 0.4}
              shiver={5}
              frame={f}
            />
          </g>
          <TimeMachine x={620} y={1620 - suck * 500} s={0.42 * (1 - suck * 0.6)} screen="pompeii" />
        </Camera>
      )}
      {s === 2 && <SpeedLines opacity={0.6} cx={760} cy={960} color="rgba(200,240,255,0.8)" />}
      {s === 2 && <Burst x={540} y={420} text="NOT AGAIN!" t={t - 3.35} size={100} color="#7af7ff" />}
      {s === 3 && <EndCardArt t={t - 4.4} />}
    </Scene>
  );
};

/* ------------------------------------------------------- end screen */
const EndCardArt: React.FC<{t: number}> = ({t}) => {
  const f = useCurrentFrame();
  const wave = cycle(f, 0.3, 30);
  return (
    <g>
      <rect x={0} y={0} width={1080} height={1920} fill="#1a0b08" />
      <rect x={0} y={0} width={1080} height={1920} fill="url(#skyFire)" opacity={0.85} />
      <Skyline y={1400} color="#2a120c" />
      <FireWall x0={-100} x1={1180} y={1500} h={300} seed="end" lean={-50} step={180} intensity={0.6} />
      <rect x={0} y={1500} width={1080} height={420} fill="#1c0f0a" />
      <Embers count={50} wind={-4} rise={6} seed="end" />
      <Character x={540} y={1800} scale={1.05} expression="happy" armR={-150 + wave.armR * 0.8} armL={10} headTilt={Math.sin(f * 0.2) * 5} blink={blinkAt(f)} frame={f} />
      <g transform={`translate(860 1640) scale(${ip(t, [0.3, 0.6], [0, 0.32], backOut)})`}>
        <Portal x={0} y={0} open={1} />
      </g>
    </g>
  );
};

const EndCard: React.FC<{t: number}> = ({t}) => {
  const logo = ip(t, [0, 0.35], [0.3, 1], backOut);
  const btn = ip(t, [0.25, 0.55], [0, 1], backOut);
  return (
    <AbsoluteFill style={{alignItems: 'center', paddingTop: 300}}>
      <div
        style={{
          transform: `scale(${logo})`,
          background: '#fff',
          border: '12px solid #141414',
          borderRadius: 50,
          padding: '20px 60px 10px',
          textAlign: 'center',
          fontFamily: 'LuckiestGuy',
          lineHeight: 1,
          boxShadow: '0 16px 0 rgba(0,0,0,0.45)',
        }}
      >
        <div style={{fontSize: 150, color: '#e2231a', WebkitTextStroke: '6px #141414'}}>HISTORY</div>
        <div style={{fontSize: 150, color: '#2f7fa0', WebkitTextStroke: '6px #141414'}}>WORLD</div>
      </div>
      <div
        style={{
          marginTop: 60,
          transform: `scale(${btn})`,
          background: '#e2231a',
          border: '10px solid #141414',
          borderRadius: 80,
          padding: '22px 60px',
          fontFamily: 'LuckiestGuy',
          fontSize: 84,
          color: '#fff',
        }}
      >
        SUBSCRIBE 🔔
      </div>
      <div
        style={{
          marginTop: 40,
          padding: '0 60px',
          textAlign: 'center',
          fontFamily: 'LuckiestGuy',
          fontSize: 66,
          lineHeight: 1.1,
          color: '#ffd400',
          WebkitTextStroke: '10px #141414',
          paintOrder: 'stroke fill',
          opacity: ip(t, [0.5, 0.8], [0, 1]),
        }}
      >
        FOR MORE HISTORICAL ADVENTURES!
      </div>
    </AbsoluteFill>
  );
};
