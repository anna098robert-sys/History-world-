import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {cycle} from '../components/Character';
import {Camera, Dust, Flash, SpeedLines, Vignette} from '../components/Effects';
import {Candle, DarkRoom, Guard, IronKey, LightPool, MarketStall, Parisian, ParisSquare, Poster, Prisoner, Scaffold, Stool} from '../components/France';
import {backOut, blinkAt, easeIn, easeOut, FPS, ip, linear, shot} from '../helpers';
import {Hero, Scene, handPos} from './common';

const Crowd: React.FC<{y: number; count: number; s?: number; seed: string; speed?: number; dir?: 1 | -1}> = ({y, count, s = 1, seed, speed = 2, dir = 1}) => {
  const f = useCurrentFrame();
  const span = 1700;
  return (
    <g>
      {new Array(count).fill(0).map((_, i) => {
        const off = (i * 997 + seed.length * 131) % span;
        const sp = speed * (0.7 + ((i * 37) % 10) / 10);
        let x = ((off + f * sp * dir) % span + span) % span - 300;
        return <Parisian key={i} x={x} y={y + ((i * 53) % 4) * 18 * s} s={s * (0.9 + ((i * 29) % 3) * 0.06)} seed={i + seed.length} facing={dir} walk={f * 0.3 + i} />;
      })}
    </g>
  );
};

/* ===================================== SCENE 5 — THE BIG REVEAL (32–43s) */
export const Scene5Reveal: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0, 7.5]);
  const walk = cycle(f, 0.28, 22);
  const posterX = 760;
  const posterY = 1180;
  const zoom = s === 0 ? ip(t, [0, 2.5], [1.0, 1.08]) : s === 1 ? 1.2 : s === 2 ? ip(t, [5.0, 7.5], [1.4, 3.0], easeIn) : ip(t, [7.5, 7.75], [2.0, 2.7], backOut);
  const fx = s === 2 ? posterX : s === 3 ? 390 : 540;
  const fy = s === 2 ? posterY - 40 : s === 3 ? 1420 : 1250;
  const heroX = s === 0 ? ip(t, [0, 2.5], [-100, 330], linear) : 380;
  return (
    <Scene
      bg="#f2c9a0"
      overlay={
        <>
          <Vignette strength={s >= 2 ? 0.75 : 0.4} color="20,10,0" />
          <Flash at={0} dur={10} color="#fff6dc" peak={1} />
          <Flash at={Math.round(7.5 * FPS)} dur={4} peak={0.5} />
        </>
      }
    >
      <Camera zoom={zoom} focusX={fx} focusY={fy} shake={s === 3 ? ip(t, [7.5, 8.2], [14, 2]) : 0}>
        <ParisSquare groundY={1500} />
        {/* the scaffold in the far square — always distant, never shown in use */}
        <Scaffold x={560} y={1440} s={0.55} color="#5a4a50" />
        <Crowd y={1520} count={6} s={0.7} seed="far" speed={1.5} dir={-1} />
        {/* poster pasted on the wall by the arcade */}
        <Poster x={posterX} y={posterY} s={0.75} rot={-3} who="prisoner" />
        <Crowd y={1640} count={5} s={0.95} seed="near" speed={2.2} />
        <Hero
          x={heroX}
          y={1800 - (s === 0 ? walk.bob : 0)}
          scale={1.1}
          expression={s === 0 ? (t > 1.0 && t < 1.8 ? 'scream' : 'happy') : s === 1 ? 'curious' : 'terrified'}
          lookX={s >= 1 ? 0.9 : 0.3}
          lookY={s === 1 ? -0.4 : s === 3 ? -0.2 : 0}
          legL={s === 0 ? walk.legL : 0}
          legR={s === 0 ? walk.legR : 0}
          armL={s === 0 && t > 1.0 && t < 1.8 ? 150 : 10}
          armR={s === 0 && t > 1.0 && t < 1.8 ? -150 : -10}
          capLift={s === 3 ? ip(t, [7.6, 7.75, 8.3], [0, 55, 20], backOut) : 0}
          sweat={s === 3}
          shiver={s === 3 ? 3 : 0}
          blink={s < 2 ? blinkAt(f) : 0}
          frame={f}
        />
      </Camera>
      {s === 3 && <SpeedLines opacity={0.7} cy={900} color="rgba(255,255,255,0.8)" />}
    </Scene>
  );
};

/* ===================================== SCENE 6 — THE CONSEQUENCES (43–53s) */
export const Scene6Consequence: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0, 7.5]);
  return (
    <Scene bg="#c9a88a" overlay={<Vignette strength={0.7} color="20,10,0" />}>
      {s === 0 && (
        // the escaped man melts into the crowd
        <Camera zoom={ip(t, [0, 2.5], [1.3, 1.15])} focusX={560} focusY={1350}>
          <ParisSquare groundY={1400} scroll={200} />
          <Crowd y={1440} count={9} s={0.75} seed="a" speed={1.8} dir={-1} />
          <g opacity={ip(t, [1.4, 2.3], [1, 0])}>
            <Prisoner x={ip(t, [0, 2.5], [500, 760], linear)} y={1560} s={0.75} facing={1} expr="sly" cloak run={f * 0.4} />
          </g>
          <Crowd y={1600} count={8} s={0.95} seed="ab" speed={2.6} />
          <Crowd y={1780} count={6} s={1.15} seed="abc" speed={3.4} dir={-1} />
        </Camera>
      )}
      {s === 1 && (
        // National Guard soldiers push through the streets, searching faces
        <Camera zoom={ip(t, [2.5, 5], [1.1, 1.2])} focusX={540} focusY={1300} shake={2}>
          <ParisSquare groundY={1450} scroll={600} />
          <Crowd y={1480} count={7} s={0.75} seed="b" speed={1.2} dir={-1} />
          {[0, 1, 2].map((i) => (
            <Guard key={i} x={ip(t, [2.5, 5], [-150 + i * 220, 450 + i * 220], linear)} y={1720 + (i % 2) * 30} s={1.0} walk={f * 0.4 + i} look={Math.sin(f * 0.15 + i) * 1} />
          ))}
          <Crowd y={1800} count={4} s={1.15} seed="bb" speed={1.5} dir={-1} />
        </Camera>
      )}
      {(s === 2 || s === 3) && (
        // hiding behind a market stall as the soldiers pass
        <Camera zoom={s === 2 ? 1.2 : ip(t, [7.5, 10], [2.0, 2.3])} focusX={s === 2 ? 540 : 520} focusY={s === 2 ? 1300 : 1260} shake={s === 3 ? 2 : 0}>
          <ParisSquare groundY={1450} scroll={1000} />
          {(() => {
            const peek = s === 2 ? (t < 3.9 ? ip(t, [5.0, 5.4], [0, 1]) : 1) : ip(t, [7.5, 7.9, 9.5, 9.8], [1, 0.6, 0.6, 0.2]);
            return (
              <Hero
                x={520}
                y={1780 + (1 - peek) * 220}
                scale={1.1}
                expression={s === 2 ? 'scared' : t > 9.0 ? 'terrified' : 'shocked'}
                lookX={s === 2 ? Math.sin(f * 0.2) * 0.9 : 0}
                armL={10}
                armR={-10}
                sweat
                shiver={s === 3 ? 3 : 1}
                frame={f}
              />
            );
          })()}
          <MarketStall x={540} y={1860} s={1.15} />
          {s === 2 && [0, 1].map((i) => <Guard key={i} x={ip(t, [5.6 + i * 0.3, 7.5 + i * 0.3], [1300, -200], linear)} y={1960} s={1.2} facing={-1} walk={f * 0.4 + i} look={0.6} />)}
        </Camera>
      )}
    </Scene>
  );
};

/* ===================================== SCENE 7 — THE FINAL TWIST (53–58.5s) */
export const Scene7Twist: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const slide = ip(t, [1.2, 1.9], [0, 1], easeOut);
  const lookCam = t > 2.4;
  const candleOut = t > 4.4;
  const black = ip(t, [4.4, 5.3], [0, 1]);
  // seated on the stool, key in hand
  const sx = 420;
  const seatY = 1520;
  const hs = 1.1;
  const hy = seatY + 120 * hs;
  const armR = -70;
  const hand = handPos(sx, hy, hs, 1, armR, 'R');
  return (
    <Scene
      overlay={
        <>
          <Vignette strength={0.9} color="0,0,0" />
          <AbsoluteFill style={{background: '#000', opacity: black}} />
        </>
      }
    >
      {/* insert: the poster on the floor — it's HIM */}
      {t >= 1.9 && t < 2.4 && (
        <Camera zoom={ip(t, [1.9, 2.4], [1.0, 1.15])} focusX={540} focusY={960} shake={4}>
          <rect x={-500} y={-500} width={2080} height={2920} fill="#2a2224" />
          <Poster x={540} y={960} s={2.2} rot={4} who="hero" />
          <LightPool id="lpIns" x={600} y={900} r={1000} dark={0.75} />
        </Camera>
      )}
      {(t < 1.9 || t >= 2.4) && <Camera zoom={lookCam ? ip(t, [2.4, 4.6], [1.6, 2.6], easeIn) : ip(t, [0, 2.4], [1.1, 1.3])} focusX={lookCam ? sx + 10 : 560} focusY={lookCam ? 1150 : 1300}>
        <DarkRoom />
        <Stool x={sx} y={1650} s={1} />
        <Hero
          x={sx}
          y={hy}
          scale={hs}
          expression={t < 1.9 ? 'scared' : t < 2.4 ? 'shocked' : 'confused'}
          lookX={t > 1.9 && t < 2.4 ? 0.9 : 0}
          lookY={t < 1.2 ? 0.7 : t < 2.4 ? 0.5 : 0}
          headTilt={t < 1.2 ? 12 : lookCam ? -6 : 0}
          legL={-70}
          legR={-55}
          armR={armR}
          armL={20}
          sweat={t > 1.9}
          frame={f}
        />
        <IronKey x={hand.x + 30} y={hand.y - 6} s={0.85} rot={-15} />
        {/* the poster slides in under the door — with HIS face */}
        <g transform={`translate(${ip(slide, [0, 1], [1000, 760])} ${1590}) skewX(-30) scale(1 0.35)`}>
          <Poster x={0} y={0} s={0.45} who="hero" />
        </g>
        {!candleOut && <Candle x={640} y={1650} s={0.9} />}
        {candleOut && (
          <g opacity={ip(t, [4.4, 5.2], [0.8, 0])}>
            <path d={`M640 1600 q-20 -60 0 -120 q20 -60 0 -120`} stroke="#9a9aa0" strokeWidth={10} fill="none" transform={`translate(0 ${-(t - 4.4) * 80})`} />
          </g>
        )}
        <LightPool id="lp11" x={640} y={1560} r={candleOut ? 260 : 820} dark={0.9} />
      </Camera>}
    </Scene>
  );
};
