import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Camera, Flash, SpeedLines, Vignette} from '../components/Effects';
import {Embers, FireWall, SmokeColumn, SmokeHaze} from '../components/Fire';
import {Bakery, FleeingCrowd, House, HouseRow, Person, Skyline, Street} from '../components/London';
import {Caption, FireLight, Scene} from './common';
import {backOut, blinkAt, easeOut, FPS, ip, linear, shot} from './helpers';

/* ============================== SCENE 1 — SHOCKING HOOK (0–4s) */
export const Scene1Hook: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [1.6]);
  const cam =
    s === 0
      ? {zoom: ip(t, [0, 1.6], [1.05, 1.5], easeOut), fx: 540, fy: 1300, shake: 6}
      : {zoom: ip(t, [1.6, 4], [1.3, 1.05], easeOut), fx: 540, fy: 1150, shake: ip(t, [1.6, 2.2], [22, 6])};
  return (
    <Scene
      overlay={
        <>
          <Vignette strength={0.8} color="30,5,0" />
          <div
            style={{
              position: 'absolute',
              top: 130,
              left: 40,
              right: 40,
              textAlign: 'center',
              fontFamily: 'LuckiestGuy',
              fontSize: 86,
              lineHeight: 1.05,
              color: '#fff',
              WebkitTextStroke: '12px #141414',
              paintOrder: 'stroke fill',
              transform: `scale(${ip(t, [0, 0.2], [0.4, 1], backOut)}) rotate(-2deg)`,
              textShadow: '0 8px 0 rgba(0,0,0,0.5)',
            }}
          >
            I WITNESSED THE <span style={{color: '#ff8a1e'}}>GREAT FIRE OF LONDON!</span> 🔥
          </div>
          <Caption text="LONDON · SEPTEMBER 1666" show={ip(t, [1.8, 2.1], [0, 1])} top={390} />
          <Flash at={0} dur={5} color="#ffb347" peak={1} />
          <Flash at={Math.round(1.6 * FPS)} dur={6} color="#fff2c0" peak={0.8} />
        </>
      }
    >
      <Camera zoom={cam.zoom} focusX={cam.fx} focusY={cam.fy} shake={cam.shake}>
        <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" />
        <SmokeHaze y={420} opacity={0.9} color="40,20,15" />
        <Skyline y={1050} color="#2a120c" />
        <FireWall x0={-150} x1={1230} y={1150} h={760} seed="hookwall" lean={-90} step={160} />
        <HouseRow y={1560} count={7} seedBase={2} burnAt={() => 1} charred={0.35} lean={-90} />
        <Street y={1560} tint="rgba(255,90,20,0.18)" />
        {s === 1 && <FleeingCrowd y={1640} count={7} dir={-1} speed={16} s={0.8} seed="hk" />}
        <SmokeColumn x={900} y={1100} height={1200} width={300} drift={-600} seed="h1" />
        <Character
          x={s === 0 ? 540 : 360}
          y={s === 0 ? 1860 : 1820}
          scale={s === 0 ? 1.5 : 1.3}
          expression="terrified"
          lookX={s === 0 ? 0.1 : 0.7}
          armL={s === 1 ? 150 : 20}
          armR={s === 1 ? -150 : -30}
          capLift={s === 1 ? ip(t, [1.6, 1.75, 2.2], [0, 50, 15], backOut) : 0}
          sweat
          shiver={4}
          frame={f}
        />
        <Embers count={70} wind={-7} rise={8} seed="hk" />
        <FireLight strength={0.3} />
      </Camera>
      {s === 1 && <SpeedLines opacity={ip(t, [1.6, 1.8, 2.6], [0, 0.6, 0])} color="rgba(255,220,150,0.7)" />}
    </Scene>
  );
};

/* ============================== SCENE 2 — THE BEGINNING (4–11s) */
export const Scene2Street: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.3, 4.6]);
  const walk = cycle(f, 0.3, 24);
  const scroll = s === 0 ? -f * 6 : -2.3 * FPS * 6; // walking west (left)
  const smoke = ip(t, [3.5, 7], [0, 1], linear);
  const turned = s === 2 || (s === 1 && t > 3.8);
  return (
    <Scene overlay={<Vignette strength={0.7} />}>
      <Camera
        zoom={s === 0 ? 1.08 : s === 1 ? ip(t, [2.3, 4.6], [1.0, 1.15]) : ip(t, [4.6, 7], [1.25, 1.0], easeOut)}
        focusX={540}
        focusY={s === 2 ? ip(t, [4.6, 6.2], [1350, 900], easeOut) : 1150}
        shake={s === 2 && t > 4.9 && t < 5.4 ? 10 : 0}
      >
        <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyDawn)" />
        <rect x={-200} y={-200} width={1480} height={2400} fill="url(#skyFire)" opacity={smoke * 0.75} />
        <Skyline y={1000} color="#3a2c34" scroll={scroll * 0.2} />
        {/* smoke rising above the rooftops to the east (right) */}
        <SmokeColumn x={880} y={1000} height={1300} width={300} drift={-450} dark={0.7} seed="s2" opacity={smoke} lit={0.9} />
        <SmokeColumn x={1050} y={1000} height={1100} width={240} drift={-450} dark={0.6} seed="s2b" opacity={smoke} lit={0.9} />
        <HouseRow y={1560} x0={-1400} count={14} seedBase={0} scroll={scroll} />
        <Street y={1560} scroll={scroll} />
        {/* calm townsfolk at first */}
        {s === 0 && (
          <>
            <Person x={120 + f * 1.5} y={1600} kind="woman" s={0.85} facing={1} run={f * 0.25} />
            <Person x={900 + f * 6} y={1610} kind="merchant" s={0.85} facing={-1} />
          </>
        )}
        {s >= 1 && <FleeingCrowd y={1620} count={s === 1 ? 6 : 4} dir={-1} speed={18} s={0.85} seed="st" start={69} />}
        <Character
          x={430}
          y={1700 - (s === 0 ? walk.bob : 0)}
          scale={1.15}
          facing={turned ? 1 : -1}
          expression={s === 0 ? 'happy' : s === 1 ? (t < 3.2 ? 'curious' : 'scared') : 'terrified'}
          lookX={s === 1 ? (t > 3.0 ? -0.9 : 0.4) : s === 2 ? 0.6 : 0.3}
          lookY={s === 2 ? -0.9 : 0}
          headTilt={s === 2 ? -10 : 0}
          legL={s === 0 ? walk.legL : 0}
          legR={s === 0 ? walk.legR : 0}
          armL={s === 0 ? walk.armL * 0.6 : s === 2 ? 30 : 10}
          armR={s === 0 ? walk.armR * 0.6 : s === 2 ? -40 : -10}
          capLift={s === 2 ? ip(t, [4.85, 5.0, 5.4], [0, 45, 10], backOut) : 0}
          sweat={s === 2}
          blink={blinkAt(f)}
          frame={f}
        />
        {smoke > 0.3 && <Embers count={25} wind={-5} rise={5} seed="s2e" size={0.8} />}
      </Camera>
    </Scene>
  );
};

/* ============================== SCENE 3 — THE FIRST FLAMES (11–18s) */
export const Scene3Bakery: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.3, 4.6]);
  const burn = ip(t, [0, 2.3, 3.2], [0.12, 0.2, 1], linear);
  const neighbour = (i: number) => ip(t, [4.9 + i * 0.8, 5.6 + i * 0.8], [0, 1], linear);
  return (
    <Scene
      overlay={
        <>
          <Vignette strength={0.8} />
          <Caption text="2 SEPTEMBER 1666" sub="Thomas Farriner's bakery, Pudding Lane" show={ip(t, [0.2, 0.5, 2.1, 2.3], [0, 1, 1, 0])} top={300} />
          <Flash at={Math.round(2.3 * FPS)} dur={6} color="#ffcf6a" peak={0.8} />
        </>
      }
    >
      <Camera
        zoom={s === 0 ? ip(t, [0, 2.3], [1.0, 1.15]) : s === 1 ? ip(t, [2.3, 4.6], [1.55, 1.35]) : ip(t, [4.6, 7], [1.0, 0.82], easeOut)}
        focusX={s === 2 ? ip(t, [4.6, 7], [540, 760]) : 540}
        focusY={s === 1 ? 1050 : 1150}
        shake={s === 1 ? ip(t, [2.3, 2.8], [16, 3]) : s === 2 && t > 6.2 ? 8 : 0}
      >
        <rect x={-600} y={-600} width={2400} height={3200} fill="#100b1c" />
        <rect x={-600} y={-600} width={2400} height={3200} fill="url(#skyFire)" opacity={ip(t, [2.3, 7], [0.1, 0.8])} />
        <Skyline y={1000} color="#1a1220" withStPauls={false} />
        {/* neighbours, wooden and packed tight */}
        <House x={-330} y={1600} w={300} floors={3} seed={1} burn={0} />
        <House x={1000} y={1600} w={300} floors={4} seed={4} burn={neighbour(0)} />
        <House x={1350} y={1600} w={280} floors={3} seed={6} burn={neighbour(1)} />
        <House x={1680} y={1600} w={300} floors={4} seed={2} burn={neighbour(2)} />
        <Bakery x={540} y={1600} burn={burn} s={1.1} />
        {/* lane name board */}
        <g transform="translate(70 1180)">
          <rect x={-10} y={-50} width={260} height={70} rx={8} fill="#2b1d12" stroke="#e8c37a" strokeWidth={5} />
          <text x={120} y={0} textAnchor="middle" fontFamily="Georgia, serif" fontWeight={700} fontSize={30} fill="#f6e7c4">
            PUDDING LANE
          </text>
        </g>
        <Street y={1600} />
        <SmokeColumn x={540} y={900} height={1100} width={260} drift={-500} seed="bk" opacity={ip(t, [2.5, 4], [0, 1])} lit={1} />
        {s === 2 && (
          <Character
            x={ip(t, [4.6, 7], [180, 360])}
            y={1900}
            scale={1.25}
            facing={1}
            expression={t > 6.2 ? 'terrified' : 'scared'}
            lookX={0.8}
            lookY={-0.6}
            armL={20}
            armR={-30}
            sweat
            frame={f}
          />
        )}
        <Embers count={s === 0 ? 8 : 55} wind={-7} rise={7} seed="bke" />
        <FireLight strength={ip(t, [2.3, 4], [0.05, 0.28])} />
      </Camera>
    </Scene>
  );
};
