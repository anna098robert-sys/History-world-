import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Scene1Hook, Scene2Mission, Scene3Tension} from './scenes/Scenes1to3';
import {Scene4Mistake, Scene5Chaos, Scene6Explain, Scene7Ending} from './scenes/Scenes4to7';
import timeline from './timeline.json';
import durations from './voiceDurations.json';

const FPS = timeline.fps;
const sec = (s: number) => Math.round(s * FPS);

const SCENES: Record<string, React.FC> = {
  hook: Scene1Hook,
  mission: Scene2Mission,
  tension: Scene3Tension,
  mistake: Scene4Mistake,
  chaos: Scene5Chaos,
  explain: Scene6Explain,
  ending: Scene7Ending,
};

const VO_WINDOWS = timeline.vo.map((v) => [v.at, v.at + (durations as Record<string, number>)[v.id]]);

/** Music dips a little under the spoken lines. */
const musicVolume = (frame: number) => {
  const t = frame / FPS;
  const speaking = VO_WINDOWS.some(([a, b]) => t > a - 0.1 && t < b + 0.15);
  return (speaking ? 0.28 : 0.5) * interpolate(frame, [0, 4], [0, 1], {extrapolateRight: 'clamp'});
};

/** Quick whip-pan transition at every scene cut (no text). */
const CutTransition: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  let best = 99;
  for (const s of timeline.scenes.slice(1)) {
    if (s.id === 'mission') continue; // the hook has its own rewind transition
    best = Math.min(best, Math.abs(t - s.start));
  }
  if (best > 0.15) return null;
  const o = interpolate(best, [0, 0.15], [1, 0]);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill
        style={{
          background: 'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,245,220,0.95) 50%, rgba(255,255,255,0) 100%)',
          opacity: o,
          transform: `translateX(${(t * 5000) % 2160 - 1080}px) skewX(-15deg)`,
        }}
      />
      <AbsoluteFill style={{backdropFilter: `blur(${o * 14}px)`}} />
    </AbsoluteFill>
  );
};

export const WarShort: React.FC = () => (
  <AbsoluteFill style={{background: '#000'}}>
    {timeline.scenes.map((s) => {
      const C = SCENES[s.id];
      return (
        <Sequence key={s.id} from={sec(s.start)} durationInFrames={sec(s.end) - sec(s.start)} name={s.id}>
          <C />
        </Sequence>
      );
    })}
    <CutTransition />
    <Audio src={staticFile('audio/music.wav')} volume={musicVolume} />
    {timeline.vo.map((v) => (
      <Sequence key={v.id} from={sec(v.at)} name={`vo ${v.id}`}>
        <Audio src={staticFile(`audio/vo_${v.id}.wav`)} volume={1} />
      </Sequence>
    ))}
    {timeline.sfx.map((x, i) => (
      <Sequence key={i} from={sec(x.at)} durationInFrames={'len' in x && x.len ? sec(x.len as number) : undefined} name={`sfx ${x.id}`}>
        <Audio src={staticFile(`audio/sfx_${x.id}.wav`)} volume={x.vol * 0.8} />
      </Sequence>
    ))}
  </AbsoluteFill>
);
