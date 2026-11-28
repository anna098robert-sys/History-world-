import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {Character, cycle} from '../components/Character';
import {CityStreet, Citizen, CrownIcon, FriendIcon, General, IconBubble, Official, Scroll, Sharpener, Arrow} from '../components/City';
import {Camera, Dust, Flash, SpeedLines, Vignette} from '../components/Effects';
import {Embers, FireWall, SmokeColumn} from '../components/Fire';
import {DustClouds, Hoplite, Phalanx} from '../components/Greece';
import {backOut, blinkAt, easeIn, easeOut, FPS, ip, linear, shot} from '../helpers';
import {Scene, handPos} from './common';

/** Burning battlefield used by the hook and the ending. */
export const Battlefield: React.FC<{f: number; blur?: boolean}> = ({f, blur}) => (
  <g filter={blur ? 'url(#bgBlur)' : undefined}>
    <defs>
      <filter id="bgBlur">
        <feGaussianBlur stdDeviation={6} />
      </filter>
    </defs>
    <rect x={-400} y={-400} width={1880} height={2800} fill="url(#warSky)" />
    <path d="M-400 1150 L-100 860 L200 1000 L520 820 L840 980 L1180 880 L1480 1150 Z" fill="#5a3a30" />
    <FireWall x0={-200} x1={1300} y={1160} h={520} seed="bf" lean={-50} step={190} intensity={0.85} />
    <SmokeColumn x={200} y={1100} height={1200} width={260} drift={-300} seed="bs1" lit={0.8} />
    <SmokeColumn x={880} y={1080} height={1200} width={300} drift={-300} seed="bs2" lit={0.8} />
    <rect x={-400} y={1150} width={1880} height={1200} fill="#b08850" />
    <rect x={-400} y={1150} width={1880} height={1200} fill="rgba(120,40,10,0.25)" />
    {/* clashing phalanxes: front lines locked, spears jabbing */}
    <Phalanx side="sparta" frontX={500 + Math.sin(f * 0.4) * 12} y={1480} ranks={3} files={6} s={0.85} march spear={1} frame={f} />
    <Phalanx side="athens" frontX={580 - Math.sin(f * 0.4) * 12} y={1480} ranks={3} files={6} s={0.85} march spear={1} frame={f + 5} />
    <DustClouds y={1500} x0={-100} x1={1180} amount={0.8} seed="bfd" />
    <Embers count={60} wind={-5} rise={7} seed="bfe" />
  </g>
);

/* ===================================== SCENE 1 — SHOCKING HOOK (0–5s) */
export const Scene1Hook: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.2, 3.1, 4.3]);
  const facing: 1 | -1 = s === 0 ? -1 : 1;
  const zoom = s === 0 ? ip(t, [0, 2.2], [1.3, 1.15], easeOut) : s === 1 ? 1.2 : s === 2 ? ip(t, [3.1, 3.45], [1.25, 3.1], easeOut) : 3.15;
  const fy = s >= 2 ? ip(t, [3.1, 3.45], [1350, 1420], easeOut) : 1330;
  const rewind = s === 3 ? ip(t, [4.3, 5], [0, 1], linear) : 0;
  return (
    <Scene
      bg="#2a1a18"
      overlay={
        <>
          <Vignette strength={0.8} color="30,5,0" />
          <Flash at={0} dur={6} color="#ffb347" peak={1} />
          {/* rewind into the flashback: VHS lines + sepia + horizontal jitter */}
          {rewind > 0 && (
            <AbsoluteFill style={{backdropFilter: `sepia(${rewind}) saturate(${1 + rewind}) hue-rotate(${-rewind * 20}deg)`}}>
              <AbsoluteFill style={{background: 'repeating-linear-gradient(0deg, rgba(255,255,255,0.12) 0 4px, rgba(0,0,0,0) 4px 12px)', opacity: rewind}} />
              <AbsoluteFill style={{background: '#fff', opacity: ip(t, [4.8, 5], [0, 0.9])}} />
            </AbsoluteFill>
          )}
        </>
      }
    >
      <g transform={rewind > 0 ? `translate(${Math.sin(f * 3.3) * 40 * rewind} 0)` : undefined}>
        <Camera zoom={zoom} focusX={540} focusY={fy} shake={s === 0 ? 6 : s === 2 ? 10 : 3}>
          <Battlefield f={rewind > 0 ? -f * 3 : f} />
          <Character
            x={540}
            y={1800}
            scale={1.15}
            facing={facing}
            expression={s === 0 ? 'terrified' : 'shocked'}
            lookX={s === 0 ? 0.8 : s === 1 ? ip(t, [2.2, 2.6], [0.8, 0]) : 0}
            lookY={s >= 2 ? 0.15 : 0}
            headTilt={s === 1 ? ip(t, [2.2, 2.6], [8, 0], backOut) : 0}
            armL={s === 0 ? 30 : 12}
            armR={s === 0 ? -40 : -12}
            capLift={s === 2 ? ip(t, [3.1, 3.25, 3.6], [0, 50, 18], backOut) : 0}
            squash={s === 1 ? ip(t, [2.2, 2.35, 2.6], [1, 0.92, 1]) : 1}
            sweat
            shiver={s === 0 ? 4 : 2}
            frame={f}
          />
        </Camera>
      </g>
      {s === 2 && <SpeedLines opacity={0.85} cy={960} color="rgba(255,230,180,0.85)" />}
    </Scene>
  );
};

/* ===================================== SCENE 2 — THE MISSION (5–12s) */
export const Scene2Mission: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.3, 4.4]);
  const run = cycle(f, 0.7, 50);
  // the hand-over: scrolls travel from the official to the hero
  const give = ip(t, [1.9, 2.3], [0, 1], easeOut);
  const hx = 380;
  const hy = 1720;
  const hs = 1.1;
  const salute = s === 0 && t < 1.6;
  const armR = s === 0 ? (salute ? -150 : ip(t, [1.6, 1.9], [-150, -70])) : s === 1 ? (t < 3.9 ? -120 : -60) : 140 + Math.sin(f * 0.6) * 10;
  const armL = s === 0 ? ip(t, [1.6, 1.9], [10, -60]) : s === 1 ? -50 : -150;
  const hR = handPos(hx, hy, hs, 1, armR, 'R');
  const hL = handPos(hx, hy, hs, 1, armL, 'L');
  return (
    <Scene overlay={<><Vignette strength={0.45} /><Flash at={0} dur={6} peak={0.7} /></>}>
      {s <= 1 && (
        <Camera zoom={s === 0 ? ip(t, [0, 2.3], [1.15, 1.25]) : ip(t, [2.3, 4.4], [1.6, 1.7])} focusX={s === 0 ? 560 : 420} focusY={s === 0 ? 1300 : 1370} shake={0}>
          <CityStreet scroll={400} />
          <Official
            x={760}
            y={1740}
            s={1.15}
            armR={ip(t, [0.6, 1.0], [-20, -110])}
            armL={t < 1.9 ? ip(t, [0.6, 1.0], [20, 110]) : 20}
            talk={t > 0.7 && t < 1.9 ? Math.abs(Math.sin(f * 0.8)) : 0}
          />
          {/* official's instructions as picture bubbles: blue → king, red → his friend */}
          {s === 0 && (
            <>
              <IconBubble x={760} y={760} s={ip(t, [0.9, 1.1], [0, 0.8], backOut)} tail="left">
                <Scroll x={-100} y={-30} seal="blue" s={0.9} />
                <Arrow x={10} y={-30} s={1} />
                <CrownIcon x={110} y={-30} s={1.1} />
              </IconBubble>
              <IconBubble x={760} y={1060} s={ip(t, [1.5, 1.7], [0, 0.8], backOut)} tail="left">
                <Scroll x={-100} y={-30} seal="red" s={0.9} />
                <Arrow x={10} y={-30} s={1} />
                <FriendIcon x={110} y={-30} s={1.1} />
              </IconBubble>
            </>
          )}
          {/* scrolls: in the official's hands, then handed over */}
          <Scroll x={ip(give, [0, 1], [640, hL.x])} y={ip(give, [0, 1], [1400, hL.y])} seal="blue" s={0.75} rot={-10} />
          <Scroll x={ip(give, [0, 1], [880, hR.x])} y={ip(give, [0, 1], [1360, hR.y])} seal="red" s={0.75} rot={10} />
          <Character
            x={hx}
            y={hy}
            scale={hs}
            expression={s === 0 ? 'happy' : 'smug'}
            lookX={0.5}
            armL={armL}
            armR={armR}
            squash={s === 1 && t > 3.9 ? ip(t, [3.9, 4.1, 4.4], [1, 0.85, 1.15]) : 1}
            blink={blinkAt(f)}
            frame={f}
          />
          {s === 1 && t > 2.3 && t < 2.9 && (
            <g transform={`translate(560 ${1080 - (t - 2.3) * 80})`} opacity={1 - (t - 2.3) / 0.6}>
              <path d="M0 -30 L8 -8 L30 0 L8 8 L0 30 L-8 8 L-30 0 L-8 -8 Z" fill="#ffd400" stroke="#141414" strokeWidth={4} />
            </g>
          )}
        </Camera>
      )}
      {s === 2 && (
        // sprinting through the city, juggling the two letters (foreshadowing!)
        <Camera zoom={1.1} focusX={540} focusY={1300} rotate={-3}>
          <CityStreet scroll={f * 24} />
          <Citizen x={((900 - f * 24) % 1600 + 1600) % 1600} y={1600} seed={1} facing={1} />
          <Citizen x={((1300 - f * 24) % 1600 + 1600) % 1600} y={1610} seed={2} female facing={-1} />
          <Citizen x={((500 - f * 24) % 1600 + 1600) % 1600} y={1600} seed={3} facing={-1} />
          {(() => {
            const cx = 480;
            const cy = 1720 - run.bob;
            const jug = ip(t, [5.2, 6.4], [0, 1], linear);
            const a = jug * Math.PI * 2;
            return (
              <>
                <DustClouds y={1720} x0={cx - 260} x1={cx - 60} amount={0.8} seed="rd" />
                <Character x={cx} y={cy} scale={1.1} expression={t > 5.3 && t < 6.3 ? 'scared' : 'happy'} legL={run.legL} legR={run.legR} armL={-150} armR={-160} bodyTilt={-10} capLift={10} frame={f} />
                <Scroll x={cx + 40 + Math.cos(a) * 110} y={cy - 560 - Math.abs(Math.sin(a)) * 160} rot={f * 25} seal="blue" s={0.7} />
                <Scroll x={cx + 40 - Math.cos(a) * 110} y={cy - 560 - Math.abs(Math.sin(a + 1)) * 160} rot={-f * 25} seal="red" s={0.7} />
              </>
            );
          })()}
          <Dust count={20} color="rgba(255,240,200,0.6)" />
        </Camera>
      )}
    </Scene>
  );
};

/* ===================================== SCENE 3 — THE TENSION (12–20s) */
export const Scene3Tension: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;
  const s = shot(t, [2.5, 5.0]);
  return (
    <Scene bg="#3a2418" overlay={<Vignette strength={0.85} color="30,10,0" />}>
      {s === 0 && (
        // blades sharpened, sparks flying
        <Camera zoom={ip(t, [0, 2.5], [1.0, 1.15], linear)} focusX={540} focusY={1100} shake={2}>
          <rect x={-300} y={-300} width={1680} height={2600} fill="#4a2e1e" />
          <rect x={-300} y={-300} width={1680} height={2600} fill="url(#hall)" opacity={0.6} />
          {/* armoury racks: shields and spears */}
          {[0, 1, 2, 3].map((i) => (
            <g key={i}>
              <circle cx={150 + i * 260} cy={520} r={100} fill="url(#bronze)" stroke="#141414" strokeWidth={8} />
              <line x1={40 + i * 260} y1={200} x2={70 + i * 260} y2={900} stroke="#7a5228" strokeWidth={12} />
            </g>
          ))}
          <Hoplite x={260} y={1520} side="sparta" s={1.1} spear={0} seed={3} />
          <Sharpener x={600} y={1240} s={1.4} phase={f * 0.35} />
          <Sharpener x={420} y={1720} s={1.0} phase={f * 0.35 + 1.5} />
          <rect x={-300} y={-300} width={1680} height={2600} fill="rgba(255,120,40,0.12)" />
        </Camera>
      )}
      {s === 1 && (
        // war council: generals arguing over the map
        <Camera zoom={ip(t, [2.5, 5], [1.3, 1.45])} focusX={540} focusY={1250} shake={t > 3.6 && t < 3.9 ? 14 : 0}>
          <rect x={-300} y={-300} width={1680} height={2600} fill="url(#hall)" />
          <rect x={-300} y={1500} width={1680} height={800} fill="#6b4a2e" />
          <General x={250} y={1600} facing={1} armR={-80 + Math.sin(f * 0.5) * 20} shout={Math.abs(Math.sin(f * 0.7))} crest="#c41a12" />
          <General x={830} y={1600} facing={-1} armR={t > 3.5 && t < 3.7 ? -170 : t > 3.7 && t < 4.0 ? -40 : -90 + Math.sin(f * 0.6) * 15} shout={Math.abs(Math.sin(f * 0.65 + 1))} crest="#7a0f0a" />
          {/* map table: two rival cities, a river, little army tokens */}
          <g transform={`translate(540 1330) ${t > 3.6 && t < 3.8 ? 'translate(0 -10)' : ''}`}>
            <rect x={-330} y={-60} width={660} height={120} fill="#e8d6a8" stroke="#141414" strokeWidth={8} />
            <path d="M-300 -10 Q-100 40 0 -10 Q120 -50 300 20" stroke="#2f7fa0" strokeWidth={10} fill="none" />
            <g transform="translate(-200 -20) scale(0.5)">
              <CrownIcon x={0} y={0} />
            </g>
            <g transform="translate(200 0) scale(0.5)">
              <CrownIcon x={0} y={0} />
            </g>
            {[-140, -110, -80].map((p) => (
              <circle key={p} cx={p + Math.sin(f * 0.2) * 3} cy={20} r={10} fill="#c41a12" stroke="#141414" strokeWidth={3} />
            ))}
            {[80, 110, 140].map((p) => (
              <circle key={p} cx={p} cy={-20} r={10} fill="#2a5d9a" stroke="#141414" strokeWidth={3} />
            ))}
            <rect x={-350} y={60} width={40} height={300} fill="#6b4220" />
            <rect x={310} y={60} width={40} height={300} fill="#6b4220" />
          </g>
          <rect x={-300} y={-300} width={1680} height={2600} fill="rgba(255,120,40,0.1)" />
        </Camera>
      )}
      {s === 2 && (
        // frightened citizens, shutters slamming, enemy camp fires on the far hill
        <Camera zoom={ip(t, [5, 8], [1.1, 1.2])} focusX={ip(t, [5, 8], [500, 600])} focusY={1250}>
          <CityStreet scroll={1900} shutters={ip(t, [5.6, 5.8], [0, 1])} sky="url(#warSky)" />
          {/* enemy camp on the hill */}
          {[150, 380, 640, 900].map((cx, i) => (
            <g key={cx} transform={`translate(${cx} 940)`}>
              <path d="M-40 0 L0 -60 L40 0 Z" fill="#e8d6a8" stroke="#141414" strokeWidth={4} />
              <circle cx={60} cy={-8} r={10 + Math.sin(f * 0.8 + i) * 3} fill="#ffb347" />
            </g>
          ))}
          <SmokeColumn x={640} y={900} height={600} width={120} drift={-150} seed="camp" dark={0.4} opacity={0.7} />
          <Citizen x={220} y={1640} seed={3} female mood="scared" facing={1} />
          <Citizen x={300} y={1650} seed={2} child mood="scared" facing={1} />
          <Citizen x={860} y={1640} seed={1} mood="scared" facing={-1} />
          <Citizen x={700} y={1600} seed={0} facing={-1} mood="angry" />
          {/* our messenger dashes past, letters in hand */}
          {t > 6.8 && (
            <g>
              <Character x={ip(t, [6.8, 7.9], [-200, 1300], linear)} y={1800} scale={1.0} expression="happy" legL={Math.sin(f * 0.7) * 50} legR={-Math.sin(f * 0.7) * 50} armL={-60} armR={-80} bodyTilt={-10} frame={f} />
            </g>
          )}
        </Camera>
      )}
    </Scene>
  );
};
