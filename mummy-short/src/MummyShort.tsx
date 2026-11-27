import React, {useState} from 'react';
import {AbsoluteFill, Audio, continueRender, delayRender, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {Subtitles} from './components/Subtitles';
import {Scene1Hook} from './scenes/Scene1Hook';
import {Scene2Tomb} from './scenes/Scene2Tomb';
import {Scene3Coffin} from './scenes/Scene3Coffin';
import {Scene4Awake} from './scenes/Scene4Awake';
import {Scene5Chase} from './scenes/Scene5Chase';
import {Scene6Ending} from './scenes/Scene6Ending';
import timeline from './timeline.json';
import durations from './voiceDurations.json';

const FPS = timeline.fps;
const sec = (s: number) => Math.round(s * FPS);

const SCENES: Record<string, React.FC> = {
  hook: Scene1Hook,
  tomb: Scene2Tomb,
  coffin: Scene3Coffin,
  awake: Scene4Awake,
  chase: Scene5Chase,
  ending: Scene6Ending,
};

// Load the bundled comic font before rendering any frame.
const useFont = () => {
  const [handle] = useState(() => delayRender('Loading font'));
  useState(() => {
    const font = new FontFace('LuckiestGuy', `url(${staticFile('fonts/LuckiestGuy.woff2')}) format('woff2')`);
    font
      .load()
      .then(() => {
        document.fonts.add(font);
        continueRender(handle);
      })
      .catch(() => continueRender(handle));
    return null;
  });
};

const VO_WINDOWS = timeline.vo.map((v) => [v.at, v.at + (durations as Record<string, number>)[v.id]]);

/** Background music ducks under the narration. */
const musicVolume = (frame: number) => {
  const t = frame / FPS;
  const speaking = VO_WINDOWS.some(([a, b]) => t > a - 0.1 && t < b + 0.15);
  const base = speaking ? 0.22 : 0.42;
  const fadeIn = interpolate(frame, [0, 6], [0, 1], {extrapolateRight: 'clamp'});
  return base * fadeIn;
};

/** Short whip transition overlay at every scene cut. */
const CutTransition: React.FC = () => {
  const frame = useCurrentFrame();
  const t = frame / FPS;
  let best = 99;
  for (const s of timeline.scenes.slice(1)) best = Math.min(best, Math.abs(t - s.start));
  if (best > 0.17) return null;
  const o = interpolate(best, [0, 0.17], [1, 0]);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,240,200,0.9) 50%, rgba(255,255,255,0) 100%)', opacity: o, transform: `translateX(${(t * 4000) % 2160 - 1080}px) skewX(-15deg)`}} />
      <AbsoluteFill style={{background: '#000', opacity: o * 0.6}} />
    </AbsoluteFill>
  );
};

export const MummyShort: React.FC = () => {
  useFont();
  return (
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
      <Subtitles />

      {/* audio */}
      <Audio src={staticFile('audio/music.wav')} volume={musicVolume} />
      {timeline.vo.map((v) => (
        <Sequence key={v.id + v.at} from={sec(v.at)} name={`vo ${v.id}`}>
          <Audio src={staticFile(`audio/vo_${v.id}.wav`)} volume={1} />
        </Sequence>
      ))}
      {timeline.sfx.map((x, i) => (
        <Sequence key={i} from={sec(x.at)} name={`sfx ${x.id}`}>
          <Audio src={staticFile(`audio/sfx_${x.id}.wav`)} volume={x.vol * 0.8} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
