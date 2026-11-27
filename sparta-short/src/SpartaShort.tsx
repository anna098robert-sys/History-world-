import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Character} from './components/Character';
import {Camera, Dust, Stage, Vignette} from './components/Effects';
import {Banner, DustClouds, GreeceDefs, Landscape, Phalanx} from './components/Greece';
import {backOut, blinkAt, easeOut, FPS, ip, linear} from './helpers';
import timeline from './timeline.json';

const B = timeline.beats;
const sec = (s: number) => Math.round(s * FPS);

/**
 * Peloponnesian War, 431 BC. The doodle guy is stuck between a Spartan
 * phalanx (left) and an Athenian phalanx (right) as they advance.
 * No text, subtitles or voice — pure animation, music and sound.
 */
const Battlefield: React.FC = () => {
  const f = useCurrentFrame();
  const t = f / FPS;

  // armies
  const advance = ip(t, [B.marchStart, timeline.durationSec], [0, 1], linear);
  const spear = ip(t, [B.marchStart - 0.2, B.marchStart + 0.8], [0, 1], easeOut);
  const shout = Math.max(ip(t, [B.warCry, B.warCry + 0.15, B.warCry + 1.4], [0, 1, 0]), ip(t, [9.0, 9.15, 10.4], [0, 1, 0]));
  const marching = t >= B.marchStart;
  const raised = t >= B.warCry && t < B.marchStart; // spears shaken in the air during the war cry
  const shake = raised ? Math.sin(f * 1.2) * 12 : 0;
  const spartaX = 300 + advance * 210 + shake;
  const athensX = 780 - advance * 210 - shake;

  // camera: medium shot → slow dramatic push into close-up
  const zoom = t < B.marchStart ? ip(t, [0, B.marchStart], [1.32, 1.4]) : ip(t, [B.marchStart, 9.0, 12], [1.4, 2.3, 2.45]);
  const focusY = t < B.marchStart ? ip(t, [0, B.marchStart], [1380, 1390]) : ip(t, [B.marchStart, 9.0], [1390, 1400]);
  const stomp = marching ? Math.max(0, Math.sin(((t - B.marchStart) / 0.42) * Math.PI)) ** 8 * ip(t, [B.marchStart, 12], [2, 7]) : 0;
  const warShake = ip(t, [B.warCry, B.warCry + 0.1, B.warCry + 0.6], [0, 10, 0]);

  // hero performance
  const lookPhase = t < B.lookLeft ? 'front' : t < B.lookRight ? 'left' : t < B.eyesWiden ? 'right' : 'front';
  const facing: 1 | -1 = lookPhase === 'left' ? -1 : 1;
  const flinch = ip(t, [B.warCry, B.warCry + 0.08, B.warCry + 0.4], [1, 0.9, 1]);
  const pop = ip(t, [B.eyesWiden, B.eyesWiden + 0.12, B.eyesWiden + 0.5], [0, 55, 20], backOut);
  const hands = ip(t, [B.handsUpStart, B.handsUpEnd], [0, 1]);
  const headTurn = lookPhase === 'left' || lookPhase === 'right' ? ip(t % 1.1, [0, 0.25], [0, 1], easeOut) : 0;
  const idle = Math.sin(f * 0.08) * 3;
  let expression: 'happy' | 'curious' | 'shocked' | 'scared' | 'terrified' = 'happy';
  if (t >= B.warCry - 0.05) expression = 'shocked';
  if (t >= B.warCry + 0.6) expression = 'curious';
  if (t >= B.lookLeft) expression = 'scared';
  if (t >= B.eyesWiden) expression = 'terrified';
  if (t >= B.gulp && t < B.gulp + 0.4) expression = 'scared';

  return (
    <Stage bg="#9fd0f0">
      <GreeceDefs />
      <Camera zoom={zoom} focusX={540} focusY={focusY} shake={stomp + warShake}>
        <Landscape horizon={1080} />
        <DustClouds y={1180} x0={-100} x1={1180} amount={0.5} seed="far" />
        {/* banners carried behind each phalanx */}
        <Banner x={spartaX - 520} y={1300} side="sparta" s={0.9} />
        <Banner x={spartaX - 200} y={1310} side="sparta" s={0.8} />
        <Banner x={athensX + 520} y={1300} side="athens" s={0.9} />
        <Banner x={athensX + 200} y={1310} side="athens" s={0.8} />
        <Phalanx side="sparta" frontX={spartaX} y={1520} ranks={3} files={6} s={0.95} march={marching} spear={spear} shout={shout} frame={f} />
        <Phalanx side="athens" frontX={athensX} y={1520} ranks={3} files={6} s={0.95} march={marching} spear={spear} shout={shout} frame={f + 7} />
        <DustClouds y={1560} x0={-200} x1={1280} amount={marching ? ip(t, [B.marchStart, 6], [0.2, 0.9]) : 0.15} seed="near" />
        {/* the hero, caught in the middle */}
        <Character
          x={540}
          y={1790}
          scale={1.15}
          facing={facing}
          expression={expression}
          lookX={lookPhase === 'front' ? 0 : 0.9 * headTurn}
          lookY={t > B.eyesWiden ? -0.1 : 0}
          headTilt={lookPhase === 'left' || lookPhase === 'right' ? 6 * headTurn : idle * 0.6}
          armL={interpolate(hands, [0, 1], [10, 128]) + (hands > 0.95 ? Math.sin(f * 1.4) * 4 : 0)}
          armR={interpolate(hands, [0, 1], [-10, -128]) - (hands > 0.95 ? Math.sin(f * 1.4) * 4 : 0)}
          bodyTilt={idle * 0.4}
          squash={flinch * (1 + Math.sin(f * 0.08) * 0.01)}
          capLift={pop}
          sweat={t > B.lookRight}
          shiver={t > B.eyesWiden ? ip(t, [B.eyesWiden, 11], [1, 4]) : 0}
          blink={t < B.lookLeft ? blinkAt(f, 30) : 0}
          frame={f}
        />
        <Dust count={40} color="rgba(255,235,190,0.65)" />
      </Camera>
    </Stage>
  );
};

export const SpartaShort: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    <Battlefield />
    <Vignette strength={0.55} color="40,20,0" />
    <Audio src={staticFile('audio/music.wav')} volume={0.5} />
    {timeline.sfx.map((x, i) => (
      <Sequence key={i} from={sec(x.at)} name={`sfx ${x.id}`}>
        <Audio src={staticFile(`audio/sfx_${x.id}.wav`)} volume={x.vol * 0.85} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
