import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {cycle} from '../components/Character';
import {Camera, Dust, Flash, SpeedLines, Vignette} from '../components/Effects';
import {CellBars, IronKey, Lantern, LightPool, Prisoner, PrisonCorridor, PrisonDeep, PrisonerFace, Rat, Scaffold} from '../components/France';
import {backOut, blinkAt, easeIn, easeOut, FPS, ip, linear, shot} from '../helpers';
import {Hero, Scene, handPos} from './common';

/** Front of a barred cell set into the corridor wall, dark inside. */
const CellFront: React.FC<{x0: number; x1: number; floorY?: number; open?: number}> = ({x0, x1, floorY = 1580, open = 0}) => (
  <g>
    <rect x={x0} y={floorY - 900} width={x1 - x0} height={900} fill="#07060a" />
    <CellBars x0={x0 + 30} x1={x1 - 20} y0={floorY - 900} y1={floorY} gap={110} open={open} />
  </g>
);

/** The prisoner's arm reaching out between the bars. */
const ReachingArm: React.FC<{x: number; y: number; reach: number; s?: number}> = ({x, y, reach, s = 1}) => {
  const f = useCurrentFrame();
  const len = 120 + reach * 230;
  const fing = Math.sin(f * 0.5) * 8;
  return (
    <g transform={`translate(${x} ${y}) scale(${s})`}>
      <line x1={0} y1={0} x2={-len} y2={20} stroke="#f4efe2" strokeWidth={40} strokeLinecap="round" />
      <line x1={0} y1={0} x2={-len} y2={20} stroke="#141414" strokeWidth={4} opacity={0.4} />
      <g transform={`translate(${-len - 20} 22)`}>
        <circle r={24} fill="#f0c9a6" stroke="#141414" strokeWidth={5} />
        {[-14, -4, 6, 16].map((fy, i) => (
          <line key={i} x1={-10} y1={fy * 0.8} x2={-46 - (i % 2) * 6} y2={fy * 1.3 + fing * (i % 2 ? 1 : -1)} stroke="#f0c9a6" strokeWidth={10} strokeLinecap="round" />
        ))}
      </g>
    </g>
  );
};

/* ===================================== SCENE 1 — SHOCKING HOOK (0–5s) */
export const Scene1Hook: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.1, 3.0]);
  const hx = 440;
  const hy = 1790;
  const hs = 1.1;
  const turned = s === 2;
  const armR = turned ? -70 : -105; // lantern raised toward the cell
  const hand = handPos(hx, hy, hs, 1, armR, 'R');
  const lightR = t > 4.5 ? ip(t, [4.5, 5.0], [700, 60], easeIn) : 700;
  const shadow = ip(t, [2.1, 3.0], [0, 1], easeOut);
  const zoom = s === 0 ? ip(t, [0, 2.1], [1.15, 1.35]) : s === 1 ? ip(t, [2.1, 3.0], [1.25, 1.1]) : ip(t, [3.0, 3.4], [1.3, 3.0], easeOut);
  return (
    <Scene
      overlay={
        <>
          <Vignette strength={0.9} color="0,0,0" />
          <Flash at={0} dur={5} color="#000" peak={1} />
          <Flash at={Math.round(3.35 * FPS)} dur={4} color="#ffffff" peak={0.35} />
        </>
      }
    >
      <Camera zoom={zoom} focusX={s === 2 ? hx + 10 : 600} focusY={s === 2 ? ip(t, [3.0, 3.4], [1300, 1430], easeOut) : 1250} shake={s === 1 ? 5 : s === 2 ? 8 : 1}>
        <PrisonCorridor scroll={0} />
        <CellFront x0={640} x1={1180} />
        {/* the mysterious prisoner: only glowing eyes and the reaching arm */}
        <g opacity={0.9}>
          <circle cx={860} cy={1150} r={7} fill="#fff1b0" />
          <circle cx={895} cy={1152} r={7} fill="#fff1b0" />
        </g>
        <ReachingArm x={720} y={1330} reach={ip(t, [0.3, 2.6], [0, 0.75], easeOut)} />
        {/* giant shadows swelling on the walls */}
        <g opacity={shadow * 0.85}>
          <g transform={`translate(${ip(shadow, [0, 1], [200, 120])} ${ip(shadow, [0, 1], [700, 520])}) scale(${0.8 + shadow * 1.8})`}>
            <path d="M0 80 L-60 60 L-140 20 L-150 0 L-60 30 L-130 -30 L-120 -50 L-40 0 L-90 -80 L-70 -90 L-10 -10 L-30 -100 L-8 -104 L20 -10 L40 -80 L60 -76 L50 20 L70 80 Z" fill="#000" />
          </g>
          {[0, 1, 2, 3, 4].map((k) => (
            <rect key={k} x={-200 + k * 140} y={300 + shadow * -80} width={40} height={1000} fill="#000" opacity={0.5} transform={`skewX(${-25})`} />
          ))}
        </g>
        <Hero
          x={hx}
          y={hy}
          scale={hs}
          facing={1}
          expression={s === 0 ? 'scared' : 'terrified'}
          lookX={turned ? 0 : s === 1 ? 0.9 : 0.6}
          lookY={turned ? 0.1 : 0}
          headTilt={turned ? 0 : 6}
          armR={armR}
          armL={s >= 1 ? 30 : 10}
          capLift={s === 2 ? ip(t, [3.0, 3.15, 3.6], [0, 45, 15], backOut) : 0}
          sweat
          shiver={s === 0 ? 2 : 4}
          frame={f}
        />
        <Lantern x={hand.x} y={hand.y} s={0.9} swing={Math.sin(f * 0.12) * 6} />
        <LightPool id="lp1" x={hand.x} y={hand.y + 70} r={lightR} dark={0.94} />
      </Camera>
      {s === 2 && <SpeedLines opacity={0.6} cy={950} color="rgba(255,220,160,0.5)" />}
    </Scene>
  );
};

/* ===================================== SCENE 2 — THE PRISON (5–13s) */
export const Scene2Prison: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.6, 5.3]);
  const walk = cycle(f, 0.28, 22);
  const hs = 1.1;
  if (s === 0 || s === 1) {
    const scroll = s === 0 ? f * 5 : 2.6 * FPS * 5;
    const hx = 420;
    const jump = s === 1 ? ip(t, [3.4, 3.6, 3.95], [0, 160, 0], easeOut) : 0;
    const hy = 1790 - (s === 0 ? walk.bob : 0) - jump;
    const armR = s === 0 ? -55 : t < 3.4 ? ip(t, [2.6, 3.0], [-55, -150], easeOut) : -170;
    const hand = handPos(hx, hy, hs, 1, armR, 'R');
    return (
      <Scene overlay={<Vignette strength={0.85} color="0,0,0" />}>
        <Camera zoom={s === 0 ? 1.15 : ip(t, [2.6, 5.3], [1.35, 1.45])} focusX={s === 0 ? 540 : 560} focusY={s === 0 ? 1250 : 1150} shake={jump > 10 ? 6 : 0}>
          <PrisonCorridor scroll={scroll} />
          {s === 1 && t > 3.3 && <Rat x={ip(t, [3.3, 4.6], [700, -200], linear)} y={1600} s={0.9} facing={-1} />}
          <Hero
            x={hx}
            y={hy}
            scale={hs}
            expression={s === 0 ? 'curious' : t < 3.4 ? 'curious' : t < 4.6 ? 'scream' : 'scared'}
            lookX={s === 1 && t < 3.4 ? 0.7 : s === 1 ? -0.6 : 0.5}
            lookY={s === 1 && t < 3.4 ? -0.6 : s === 1 ? 0.6 : 0}
            legL={s === 0 ? walk.legL : jump > 0 ? 20 : 0}
            legR={s === 0 ? walk.legR : jump > 0 ? -20 : 0}
            armR={armR}
            armL={s === 1 && t > 3.4 ? 150 : 10}
            capLift={jump > 0 ? jump * 0.3 : 0}
            blink={blinkAt(f)}
            frame={f}
          />
          <Lantern x={hand.x} y={hand.y} s={0.9} swing={s === 0 ? Math.sin(f * 0.28) * 14 : Math.sin(f * 0.6) * 4} />
          <LightPool id="lp2" x={hand.x} y={hand.y + 70} r={620} dark={0.92} />
        </Camera>
      </Scene>
    );
  }
  // head-on: tiptoeing down a long corridor of candles and iron doors
  const tip = cycle(f, 0.22, 12);
  const hx = 540;
  const hy = 1820 - tip.bob;
  const armR = -60;
  const hand = handPos(hx, hy, 1.15, 1, armR, 'R');
  return (
    <Scene overlay={<Vignette strength={0.85} color="0,0,0" />}>
      <Camera zoom={ip(t, [5.3, 8], [1.0, 1.12], linear)} focusX={540} focusY={1150}>
        <PrisonDeep travel={(t - 5.3) * 0.6} vpY={960} />
        <Hero x={hx} y={hy} scale={1.15} expression="scared" lookX={Math.sin(f * 0.1) * 0.7} legL={tip.legL} legR={tip.legR} armR={armR} armL={60} bodyTilt={6} frame={f} />
        <Lantern x={hand.x} y={hand.y} s={0.95} swing={Math.sin(f * 0.22) * 8} />
        <LightPool id="lp3" x={hand.x} y={hand.y + 70} r={760} dark={0.9} />
        <Dust count={20} color="rgba(255,220,160,0.35)" />
      </Camera>
    </Scene>
  );
};

/* ===================================== SCENE 3 — THE MYSTERIOUS PRISONER (13–22s) */
export const Scene3Prisoner: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0, 7.0]);
  const shake = t < 2.0 ? Math.sin(f * 1.6) * 6 : 0;
  return (
    <Scene overlay={<Vignette strength={0.85} color="0,0,0" />}>
      {s === 0 && (
        // the young man grabs the bars and begs
        <Camera zoom={ip(t, [0, 2.5], [1.25, 1.4])} focusX={540} focusY={1150} shake={t < 1.5 ? 4 : 0}>
          <rect x={-500} y={-500} width={2080} height={2920} fill="#1d1b24" />
          <rect x={-500} y={1580} width={2080} height={800} fill="#2a2730" />
          <Prisoner x={540 + shake} y={1640} s={1.2} expr="beg" armL={-160} armR={160} tears={1} />
          <CellBars x0={140} x1={940} y0={300} y1={1700} gap={130} />
          {/* hands gripping the bars */}
          {[410 + shake, 670 + shake].map((hx) => (
            <circle key={hx} cx={hx} cy={1010} r={24} fill="#f0c9a6" stroke="#141414" strokeWidth={5} />
          ))}
          <LightPool id="lp4" x={360} y={1150} r={900} dark={0.88} />
        </Camera>
      )}
      {s === 1 && (
        // two-shot: our hero approaches, confused and sympathetic
        <Camera zoom={ip(t, [2.5, 5], [1.15, 1.25])} focusX={560} focusY={1250}>
          <PrisonCorridor scroll={1200} />
          <CellFront x0={600} x1={1200} />
          <Prisoner x={860} y={1560} s={0.95} facing={-1} expr="beg" armL={-150} armR={150} tears={0.8} />
          <CellBars x0={630} x1={1180} y0={680} y1={1580} gap={110} />
          {(() => {
            const hx = ip(t, [2.5, 4], [200, 400], easeOut);
            const armR = -110;
            const h = handPos(hx, 1790, 1.1, 1, armR, 'R');
            return (
              <>
                <Hero x={hx} y={1790} scale={1.1} expression="curious" lookX={0.8} headTilt={ip(t, [3.5, 4.2], [0, 14], backOut)} armR={armR} armL={10} blink={blinkAt(f)} frame={f} />
                <Lantern x={h.x} y={h.y} s={0.9} swing={Math.sin(f * 0.1) * 5} />
                <LightPool id="lp5" x={h.x} y={h.y + 70} r={720} dark={0.9} />
              </>
            );
          })()}
        </Camera>
      )}
      {s === 2 && (
        // close-up: tears; through the cell window, the scaffold waits at dawn
        <Camera zoom={2.2} focusX={540} focusY={1000} shake={1}>
          <rect x={-500} y={-500} width={2080} height={2920} fill="#1d1b24" />
          <g>
            <rect x={640} y={560} width={260} height={220} fill="#3a4a7a" stroke="#141414" strokeWidth={10} />
            <Scaffold x={770} y={780} s={0.45} color="#141420" />
            {[690, 770, 850].map((bx) => (
              <rect key={bx} x={bx - 8} y={560} width={16} height={220} fill="#2a2530" />
            ))}
          </g>
          <g transform="translate(470 1010) scale(1.6)">
            <PrisonerFace expr="beg" tears={1} f={f} />
          </g>
          <CellBars x0={260} x1={860} y0={600} y1={1500} gap={150} />
          <LightPool id="lp6" x={380} y={1050} r={650} dark={0.85} />
        </Camera>
      )}
      {s === 3 && (
        // close-up: the hero's sympathetic face in the lantern light
        <Camera zoom={2.3} focusX={540} focusY={1420}>
          <PrisonCorridor scroll={1200} />
          <Hero x={520} y={1800} scale={1.1} expression="scared" lookX={0.7} headTilt={10} armR={-55} armL={10} blink={blinkAt(f, 40)} frame={f} />
          <LightPool id="lp7" x={640} y={1500} r={600} dark={0.85} />
        </Camera>
      )}
    </Scene>
  );
};

/* ===================================== SCENE 4 — THE DANGEROUS DECISION (22–32s) */
export const Scene4Decision: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0, 7.5]);
  return (
    <Scene overlay={<Vignette strength={0.85} color="0,0,0" />}>
      {s <= 1 && (
        <Camera zoom={s === 0 ? 1.45 : ip(t, [2.5, 5], [1.9, 2.1])} focusX={500} focusY={s === 0 ? 1300 : 1360}>
          <PrisonCorridor scroll={1200} />
          <CellFront x0={700} x1={1250} />
          {(() => {
            const facing: 1 | -1 = s === 0 ? (t < 1.2 ? -1 : 1) : 1;
            const armR = s === 0 ? -55 : ip(t, [2.5, 3.0], [10, -125], backOut);
            const armL = s === 0 ? 10 : -40;
            const hR = handPos(460, 1790, 1.1, facing, armR, 'R');
            const hL = handPos(460, 1790, 1.1, facing, armL, 'L');
            return (
              <>
                <Hero
                  x={460}
                  y={1790}
                  scale={1.1}
                  facing={facing}
                  expression={s === 0 ? 'scared' : 'smug'}
                  lookX={s === 0 ? 0.9 : 0.3}
                  lookY={s === 1 ? -0.4 : 0}
                  armR={armR}
                  armL={armL}
                  sweat
                  frame={f}
                />
                {s === 0 ? (
                  <Lantern x={hR.x} y={hR.y} s={0.9} />
                ) : (
                  <>
                    <Lantern x={hL.x} y={hL.y} s={0.9} />
                    <IronKey x={hR.x + 30} y={hR.y - 20} s={0.9} rot={-30} glint={ip(t, [2.95, 3.1, 3.4], [0, 1.4, 0])} />
                  </>
                )}
                <LightPool id="lp8" x={(s === 0 ? hR.x : hL.x)} y={(s === 0 ? hR.y : hL.y) + 70} r={600} dark={0.9} />
              </>
            );
          })()}
        </Camera>
      )}
      {s === 2 && (
        // extreme close-up: the key turns in the lock
        <Camera zoom={1.0} focusX={540} focusY={960} shake={t > 5.9 && t < 6.1 ? 6 : 0}>
          <rect x={-500} y={-500} width={2080} height={2920} fill="#2a2730" />
          {[180, 900].map((bx) => (
            <rect key={bx} x={bx - 50} y={-200} width={100} height={2400} fill="#3a3530" stroke="#141414" strokeWidth={10} />
          ))}
          <rect x={300} y={700} width={480} height={560} rx={30} fill="#6e6a66" stroke="#141414" strokeWidth={12} />
          <circle cx={540} cy={900} r={40} fill="#0a0a0a" />
          <path d="M520 920 L560 920 L580 1060 L500 1060 Z" fill="#0a0a0a" />
          {[340, 740].map((rx) =>
            [740, 1220].map((ry) => <circle key={`${rx}${ry}`} cx={rx} cy={ry} r={16} fill="#8a8580" stroke="#141414" strokeWidth={5} />),
          )}
          <g transform={`translate(${ip(t, [5.0, 5.4], [1300, 700], easeOut)} 930) rotate(${t > 5.6 ? ip(t, [5.6, 5.9], [0, 90]) : 0} -140 0)`}>
            <IronKey x={0} y={0} s={3.2} rot={180} />
          </g>
          <LightPool id="lp9" x={560} y={900} r={900} dark={0.7} />
        </Camera>
      )}
      {s === 3 && (
        // the door swings open and the prisoner bolts into the dark
        <Camera zoom={ip(t, [7.5, 10], [1.2, 1.35])} focusX={600} focusY={1250} shake={t < 8.2 ? 4 : 0}>
          <PrisonCorridor scroll={1200} />
          <CellFront x0={700} x1={1250} open={ip(t, [7.5, 7.9], [0.6, 1], easeOut)} />
          <Prisoner x={ip(t, [7.6, 9.2], [900, 1700], easeIn)} y={1600} s={0.95} facing={1} expr="fear" run={f * 0.8} />
          {(() => {
            const armR = -55;
            const h = handPos(400, 1790, 1.1, 1, armR, 'R');
            return (
              <>
                <Hero x={400} y={1790} scale={1.1} expression={t > 8.0 ? 'shocked' : 'curious'} lookX={0.9} armR={armR} armL={10} capLift={ip(t, [8.0, 8.15, 8.5], [0, 40, 10], backOut)} frame={f} />
                <Lantern x={h.x} y={h.y} s={0.9} swing={Math.sin(f * 0.5) * ip(t, [7.5, 10], [20, 4])} />
                <LightPool id="lp10" x={h.x} y={h.y + 70} r={ip(t, [9.6, 10], [700, 500])} dark={0.92} />
              </>
            );
          })()}
          <Dust count={24} color="rgba(255,220,160,0.4)" />
        </Camera>
      )}
    </Scene>
  );
};
