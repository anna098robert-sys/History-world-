import React from 'react';
import {useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {Arrow, CityStreet, Citizen, CrownIcon, Horseman, IconBubble, King, OpenLetter, Scroll, Table, Throne, ThroneRoom} from '../components/City';
import {Camera, Dust, Flash, SpeedLines, Vignette} from '../components/Effects';
import {Embers, SmokeColumn, SmokeHaze} from '../components/Fire';
import {DustClouds, Hoplite} from '../components/Greece';
import {backOut, blinkAt, easeIn, easeOut, FPS, ip, linear, shot} from '../helpers';
import {Battlefield} from './Scenes1to3';
import {Blush, Clash, Scene, handPos} from './common';

/* ===================================== SCENE 4 — THE TERRIBLE MISTAKE (20–30s) */
export const Scene4Mistake: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 3.0, 4.0, 5.2, 7.5]);
  const walk = cycle(f, 0.3, 22);
  const rage = ip(t, [4.0, 5.2], [0.2, 1]);
  const kingSeated = t < 5.2;
  // hero walk-in + bow + offering the (wrong!) red letter
  const heroX = ip(t, [0, 1.3], [-120, 330], easeOut);
  const offer = ip(t, [1.4, 1.9], [0, 1], easeOut);
  const heroArm = -10 - offer * 80;
  const hand = handPos(heroX, 1760, 1.0, 1, heroArm, 'R');
  return (
    <Scene
      bg="#5a3a2a"
      overlay={
        <>
          <Vignette strength={0.75} color="20,5,0" />
          <Flash at={Math.round(5.2 * FPS)} dur={5} color="#fff" peak={0.6} />
          <Flash at={Math.round(7.6 * FPS)} dur={6} color="#ff5a3a" peak={0.5} />
        </>
      }
    >
      {s === 0 && (
        // throne room: the scowling king; messenger walks in, bows, offers the RED letter
        <Camera zoom={ip(t, [0, 2.5], [1.1, 1.2])} focusX={ip(t, [0, 2.5], [480, 560])} focusY={1250}>
          <ThroneRoom />
          <Throne x={720} y={1600} s={1.05} />
          <King x={720} y={1600} s={1.05} seated rage={0.2} armR={-20 + Math.sin(f * 1.2) * 8} eyes="squint" />
          <Hoplite x={1000} y={1620} side="athens" s={0.9} />
          <Table x={420} y={1620} w={300} />
          <Character
            x={heroX}
            y={1760 - (t < 1.3 ? walk.bob : 0)}
            scale={1.0}
            expression="happy"
            legL={t < 1.3 ? walk.legL : 0}
            legR={t < 1.3 ? walk.legR : 0}
            armR={heroArm}
            armL={10}
            bodyTilt={t > 1.3 && t < 1.8 ? 12 : 0}
            blink={blinkAt(f)}
            frame={f}
          />
          <Scroll x={hand.x} y={hand.y} seal="red" s={0.6} />
        </Camera>
      )}
      {s === 1 && (
        // snap zoom on the RED seal — the wrong letter
        <Camera zoom={3.2} focusX={hand.x} focusY={hand.y} shake={4}>
          <ThroneRoom />
          <Character x={heroX} y={1760} scale={1.0} expression="happy" armR={heroArm} armL={10} frame={f} />
          <Scroll x={hand.x} y={hand.y} seal="red" s={0.6} />
          <rect x={-300} y={-300} width={1680} height={2600} fill="rgba(200,0,0,0.12)" />
        </Camera>
      )}
      {s === 2 && (
        // the king cracks the seal and unrolls the letter
        <Camera zoom={1.7} focusX={700} focusY={1180}>
          <ThroneRoom />
          <Throne x={720} y={1600} s={1.05} />
          <King x={720} y={1600} s={1.05} seated rage={0.3} armR={-100} armL={-90} eyes="squint" />
          <Scroll x={720 - 110} y={1290} seal="red" s={0.7} broken={t > 2.6} />
        </Camera>
      )}
      {s === 3 && (
        // king's POV: the doodle with donkey ears
        <Camera zoom={ip(t, [4.0, 5.2], [1.0, 1.12], linear)} focusX={540} focusY={1000}>
          <rect x={-300} y={-300} width={1680} height={2600} fill="#3a2418" />
          {/* king's furious face rises over the top of the letter */}
          <g transform={`translate(0 ${ip(t, [4.5, 4.9], [500, 0], easeOut)})`}>
            <King x={540} y={1080} s={1.25} seated rage={rage} eyes="wide" facing={1} />
          </g>
          <OpenLetter x={540} y={1000} s={1.25} unroll={ip(t, [4.0, 4.4], [0.1, 1], easeOut)} />
        </Camera>
      )}
      {s >= 4 && (
        // SLAM! … then he stands and roars for war
        <Camera
          zoom={s === 4 ? ip(t, [5.2, 5.35], [1.5, 1.3], backOut) : ip(t, [7.5, 7.7, 10], [1.0, 1.5, 1.6], backOut)}
          focusX={s === 4 ? 560 : 700}
          focusY={s === 4 ? 1300 : 1150}
          shake={s === 4 ? ip(t, [5.2, 5.6], [24, 0]) : t > 7.6 ? ip(t, [7.6, 8.4], [26, 6]) : 0}
          rotate={s === 5 ? -4 : 0}
        >
          <ThroneRoom />
          <Throne x={720} y={1600} s={1.05} />
          <Hoplite x={1000} y={1620} side="athens" s={0.9} spear={s === 5 && t > 8.2 ? 0 : 0} />
          <Hoplite x={120} y={1640} side="athens" s={0.9} />
          <Table x={460} y={1620} w={360} jump={s === 4 ? ip(t, [5.2, 5.4, 5.7], [0, 1, 0], easeOut) : 0} />
          <Scroll x={460} y={1405 - (s === 4 ? ip(t, [5.2, 5.4, 5.6], [0, 30, 0]) : 0)} seal="red" s={0.8} broken rot={8} />
          <King
            x={720}
            y={kingSeated ? 1600 : 1640}
            s={1.05}
            seated={kingSeated}
            rage={1}
            armR={s === 4 ? ip(t, [5.0, 5.2], [-150, -40], easeIn) : ip(t, [7.4, 7.6], [-30, -125], backOut)}
            armL={s === 5 ? 30 : 20}
            mouth={s === 5 ? ip(t, [7.6, 7.75, 8.4, 8.6], [0, 1, 1, 0.3]) : 0.2}
            eyes="angry"
          />
          {/* our hero cowers at the side */}
          <Character
            x={230}
            y={1790}
            scale={0.95}
            expression={s === 5 && t > 7.6 ? 'terrified' : 'shocked'}
            lookX={0.8}
            squash={s === 5 && t > 7.6 ? 0.88 : 1}
            capLift={s === 5 ? ip(t, [7.6, 7.8], [0, 45], backOut) : ip(t, [5.2, 5.4, 5.8], [0, 40, 10], backOut)}
            armL={s === 5 && t > 7.6 ? 128 : 10}
            armR={s === 5 && t > 7.6 ? -128 : -10}
            shiver={s === 5 ? 4 : 1}
            sweat
            frame={f}
          />
        </Camera>
      )}
      {s === 5 && t > 7.6 && <SpeedLines opacity={ip(t, [7.6, 7.8, 9.5], [0, 0.9, 0.2])} cx={700} cy={760} color="rgba(255,120,80,0.75)" />}
    </Scene>
  );
};

/* ===================================== SCENE 5 — TOTAL CHAOS (30–40s) */
export const Scene5Chaos: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.4, 5.0, 7.5]);
  return (
    <Scene bg="#2a1a18" overlay={<Vignette strength={0.8} color="30,5,0" />}>
      {s === 0 && (
        // hoplites charging through the streets
        <Camera zoom={1.05} focusX={540} focusY={1250} rotate={2} shake={6}>
          <CityStreet scroll={f * 30} sky="url(#warSky)" shutters={1} />
          <SmokeHaze y={500} opacity={0.8} color="50,25,18" speed={-6} />
          {[0, 1, 2, 3, 4, 5].map((i) => (
            <Hoplite key={i} x={((i * 260 + f * 14) % 1600) - 260} y={1660 + (i % 2) * 40} side={i % 2 ? 'athens' : 'sparta'} s={0.9} march={f * 0.8 + i} spear={0.6} seed={i} />
          ))}
          <DustClouds y={1700} x0={-200} x1={1280} amount={0.8} seed="c0" />
          <Embers count={40} wind={-6} rise={6} seed="c0e" />
        </Camera>
      )}
      {s === 1 && (
        // cavalry gallops past
        <Camera zoom={ip(t, [2.4, 5], [1.15, 1.0])} focusX={540} focusY={1250} shake={8}>
          <CityStreet scroll={2600} sky="url(#warSky)" shutters={1} />
          <SmokeColumn x={300} y={1000} height={1000} width={220} drift={-300} seed="c1" lit={0.8} />
          <Citizen x={ip(t, [2.4, 5], [900, 1300])} y={1600} seed={2} female run={f * 0.6} mood="scared" />
          {[0, 1, 2].map((i) => (
            <Horseman key={i} x={ip(t, [2.4 + i * 0.25, 4.6 + i * 0.25], [-400, 1500], linear)} y={1720 + i * 40} s={0.85 - i * 0.05} phase={f * 0.7 + i} coat={['#7a4a2a', '#3a2a1a', '#c9a27a'][i]} cloak={i === 1 ? '#2a5d9a' : '#b3201a'} />
          ))}
          <DustClouds y={1760} x0={-300} x1={1300} amount={1} seed="c1d" />
        </Camera>
      )}
      {s === 2 && (
        // shields collide, sparks, smoke
        <Camera zoom={ip(t, [5, 7.5], [1.6, 1.8])} focusX={540} focusY={1300} shake={ip((t - 5) % 0.75, [0, 0.15], [16, 2])}>
          <rect x={-300} y={-300} width={1680} height={2600} fill="url(#warSky)" />
          <SmokeHaze y={900} opacity={1} color="60,30,20" speed={-10} />
          <rect x={-300} y={1500} width={1680} height={800} fill="#8a6a3a" />
          {(() => {
            const push = Math.sin(((t - 5) / 0.75) * Math.PI * 2) * 30;
            return (
              <>
                <Hoplite x={360 + push} y={1620} side="sparta" s={1.15} spear={1} seed={1} march={f * 0.3} />
                <Hoplite x={720 - push} y={1620} side="athens" s={1.15} spear={1} seed={2} march={f * 0.3 + 1} />
                <Clash x={540} y={1400} t={(t - 5.1) % 0.75} s={1.2} />
              </>
            );
          })()}
          <Embers count={60} wind={-3} rise={10} seed="c2e" size={1.2} />
        </Camera>
      )}
      {s === 3 && (
        // the hero frozen in the middle of it all, guilty, still holding the BLUE letter
        <Camera zoom={ip(t, [7.5, 10], [1.25, 1.7], easeOut)} focusX={540} focusY={ip(t, [7.5, 10], [1350, 1420])} rotate={ip(t, [7.5, 10], [-3, 3])}>
          <CityStreet scroll={3200} sky="url(#warSky)" shutters={1} />
          <SmokeHaze y={600} opacity={0.9} color="50,25,18" speed={-4} />
          <SmokeColumn x={850} y={1100} height={1000} width={240} drift={-300} seed="c3" lit={0.8} />
          {[0, 1, 2, 3].map((i) => (
            <Hoplite key={`b${i}`} x={((i * 400 - f * 18) % 1700 + 1700) % 1700 - 300} y={1560} side={i % 2 ? 'athens' : 'sparta'} s={0.7} march={f * 0.8 + i} spear={0.5} seed={i} />
          ))}
          <Character
            x={540}
            y={1790}
            scale={1.15}
            expression={t > 8.8 ? 'shocked' : 'scared'}
            lookX={t > 8.8 ? 0.4 : 0}
            lookY={t > 8.8 ? 0.8 : 0}
            headTilt={t > 8.8 ? 10 : 0}
            armR={-40}
            armL={10}
            sweat
            shiver={2}
            frame={f}
          />
          {(() => {
            const h = handPos(540, 1790, 1.15, 1, -40, 'R');
            return <Scroll x={h.x} y={h.y} seal="blue" s={0.65} rot={-20} />;
          })()}
          {[0, 1, 2].map((i) => (
            <Hoplite key={`f${i}`} x={((i * 600 + f * 34) % 1900) - 400} y={1960} side={i % 2 ? 'sparta' : 'athens'} s={1.3} march={f * 0.9 + i} spear={0.4} seed={i + 5} />
          ))}
          <Embers count={50} wind={-5} rise={7} seed="c3e" />
        </Camera>
      )}
    </Scene>
  );
};

/* ===================================== SCENE 6 — THE EXPLANATION (40–48s) */
export const Scene6Explain: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.5]);
  const close = ip(t, [0.2, 0.6], [0, 1], backOut);
  // arms: both letters held up, then waving them about, then a nervous shrug
  const wave = s === 1 ? Math.sin(f * 0.5) * 25 : 0;
  const armL = s === 0 ? 128 : s === 1 ? 110 + wave : 60;
  const armR = s === 0 ? -128 : s === 1 ? -110 + wave : -60;
  const hx = 540;
  const hy = 1800;
  const hs = 1.1;
  const swap = s === 1 ? ip(t, [3.2, 4.2], [0, 1], easeOut) : s === 2 ? 1 : 0;
  const pL = handPos(hx, hy, hs, 1, armL, 'L');
  const pR = handPos(hx, hy, hs, 1, armR, 'R');
  // during the swap the letters trade hands to show the mix-up
  const redP = {x: pR.x + (pL.x - pR.x) * swap, y: pR.y + (pL.y - pR.y) * swap - Math.sin(swap * Math.PI) * 120};
  const blueP = {x: pL.x + (pR.x - pL.x) * swap, y: pL.y + (pR.y - pL.y) * swap - Math.sin(swap * Math.PI) * 120};
  return (
    <Scene bg="#2a1a18" overlay={<Vignette strength={0.8} color="30,5,0" />}>
      <Camera zoom={s === 0 ? ip(t, [0, 2.5], [1.0, 1.15]) : s === 1 ? 1.45 : ip(t, [5.5, 8], [1.15, 1.25])} focusX={540} focusY={s === 1 ? 1350 : 1300} shake={t < 0.6 ? 6 : 0}>
        <CityStreet scroll={3200} sky="url(#warSky)" shutters={1} />
        <SmokeHaze y={600} opacity={0.8} color="50,25,18" speed={-3} />
        {/* ring of soldiers closing in, spears pointed at him */}
        <Hoplite x={ip(close, [0, 1], [-200, 140])} y={1600} side="sparta" s={0.95} spear={1} seed={1} />
        <Hoplite x={ip(close, [0, 1], [1280, 940])} y={1600} side="athens" s={0.95} spear={1} seed={2} />
        <Hoplite x={ip(close, [0, 1], [-100, 300])} y={1520} side="athens" s={0.8} spear={0.9} seed={3} />
        <Hoplite x={ip(close, [0, 1], [1180, 780])} y={1520} side="sparta" s={0.8} spear={0.9} seed={4} />
        <Character
          x={hx}
          y={hy}
          scale={hs}
          expression={s === 2 ? 'happy' : 'scared'}
          lookX={s === 1 ? Math.sin(f * 0.3) * 0.8 : 0}
          armL={armL}
          armR={armR}
          headTilt={s === 2 ? 8 : 0}
          sweat
          shiver={s === 0 ? 3 : 1}
          frame={f}
        />
        <Scroll x={redP.x} y={redP.y} seal="red" s={0.65} rot={20} />
        <Scroll x={blueP.x} y={blueP.y} seal="blue" s={0.65} rot={-20} />
        {/* picture bubble: "I swapped them!" */}
        {s === 1 && (
          <IconBubble x={540} y={760} s={ip(t, [2.6, 2.8], [0, 0.85], backOut)} tail="left">
            <Scroll x={-110} y={-60} seal="red" s={0.75} />
            <Scroll x={-110} y={30} seal="blue" s={0.75} />
            <path d="M-20 -60 Q40 -15 -20 30" stroke="#e2231a" strokeWidth={10} fill="none" />
            <path d="M-20 30 L-34 6 M-20 30 L4 22" stroke="#e2231a" strokeWidth={10} fill="none" strokeLinecap="round" />
            <CrownIcon x={100} y={-15} s={1} />
          </IconBubble>
        )}
        {/* blank stares; one soldier scratches his helmet */}
        {s === 2 && (
          <g>
            <g transform={`translate(940 1250) rotate(${Math.sin(f * 0.6) * 10})`}>
              <circle r={18} fill="#e8b58a" stroke="#141414" strokeWidth={4} />
            </g>
          </g>
        )}
      </Camera>
    </Scene>
  );
};

/* ===================================== SCENE 7 — THE FUNNY ENDING (48–54s) */
export const Scene7Ending: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  // close-up; he slowly hides the letters behind his back, whistles innocently
  const hide = ip(t, [0.6, 2.4], [0, 1]);
  const armL = ip(hide, [0, 1], [-40, -10]); // hands meet behind his back
  const armR = ip(hide, [0, 1], [-60, 30]);
  const hx = 540;
  const hy = 1800;
  const hs = 1.15;
  const pL = handPos(hx, hy, hs, 1, armL, 'L');
  const pR = handPos(hx, hy, hs, 1, armR, 'R');
  // dun… dun… DUN! crash zooms
  const z = t < 4.4 ? ip(t, [0, 4.4], [2.0, 2.15]) : t < 4.75 ? 2.6 : t < 5.1 ? 3.1 : 3.8;
  const shiftEyes = t > 1.4 && t < 3.6 ? Math.sign(Math.sin(f * 0.25)) * 0.9 : 0;
  return (
    <Scene
      bg="#2a1a18"
      overlay={
        <>
          <Vignette strength={t > 4.4 ? 0.95 : 0.7} color="20,0,0" />
          <Flash at={Math.round(4.4 * FPS)} dur={3} peak={0.5} />
          <Flash at={Math.round(4.75 * FPS)} dur={3} peak={0.5} />
          <Flash at={Math.round(5.1 * FPS)} dur={4} peak={0.7} />
        </>
      }
    >
      <Camera zoom={z} focusX={545} focusY={t < 4.4 ? 1380 : 1440} shake={t > 5.1 ? 8 : 0}>
        <Battlefield f={f} blur />
        {/* letters drawn BEHIND him once hidden */}
        {hide > 0.6 && (
          <>
            <Scroll x={pL.x} y={pL.y} seal="blue" s={0.5} rot={90} />
            <Scroll x={pR.x} y={pR.y} seal="red" s={0.5} rot={84} />
          </>
        )}
        <Character
          x={hx}
          y={hy}
          scale={hs}
          expression={t > 3.6 && t < 4.4 ? 'smug' : t >= 4.4 ? 'shocked' : 'happy'}
          lookX={shiftEyes}
          lookY={t < 1.4 ? 0.1 : 0}
          armL={armL}
          armR={armR}
          headTilt={t < 3.6 ? 6 : 0}
          capLift={t > 5.1 ? 20 : 0}
          blink={t < 1.4 ? blinkAt(f, 10) : 0}
          sweat={t > 3.6}
          frame={f}
        />
        {hide <= 0.6 && (
          <>
            <Scroll x={pL.x} y={pL.y} seal="blue" s={0.6} rot={-20} />
            <Scroll x={pR.x} y={pR.y} seal="red" s={0.6} rot={20} />
          </>
        )}
        <Blush x={hx} y={hy} s={hs} o={ip(t, [0.4, 1.0], [0, 0.85])} />
        {/* whistle notes */}
        {t > 1.4 && t < 3.6 &&
          [0, 1, 2].map((i) => {
            const p = ((t - 1.4 + i * 0.35) % 1.05) / 1.05;
            return (
              <g key={i} transform={`translate(${hx + 120 + p * 80} ${hy - 380 - p * 120})`} opacity={1 - p}>
                <ellipse cx={0} cy={0} rx={10} ry={8} fill="#141414" />
                <line x1={9} y1={0} x2={9} y2={-34} stroke="#141414" strokeWidth={4} />
              </g>
            );
          })}
      </Camera>
      {t > 4.4 && <SpeedLines opacity={0.8} cy={900} color="rgba(255,255,255,0.8)" />}
    </Scene>
  );
};
