// The full film: one <Sequence> per shot (driven by src/timeline.json), narration audio per shot,
// a music + sound-effects bed, short crossfades / white flashes between shots, and subtitles.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import './fonts';
import timeline from './timeline.json';
import {SHOTS} from './scenes';
import {Subtitles} from './Subtitles';
import {W, H} from './lib';

const XFADE = 8;
const FLASH = new Set(['title', 'map', 'kennedy', 'home', 'outro']);

type Shot = (typeof timeline.shots)[number];

const makeCue = (shot: Shot) => (text: string, frac?: number) => {
  for (const [a, b, s] of shot.sents as [number, number, string][]) {
    if (s.includes(text)) return frac === undefined ? a : a + (b - a) * frac;
  }
  throw new Error(`cue "${text}" not found in shot ${shot.id}`);
};

const ShotView: React.FC<{shot: Shot; index: number}> = ({shot, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const Comp = SHOTS[shot.id];
  const cue = React.useMemo(() => makeCue(shot), [shot]);
  const fadeIn = index === 0 || FLASH.has(shot.id) ? 1 : Math.min(1, frame / XFADE);
  const flash = index > 0 && FLASH.has(shot.id) ? Math.max(0, 1 - frame / 10) : 0;
  return (
    <AbsoluteFill style={{opacity: fadeIn}}>
      <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
        <Comp t={frame / fps} D={shot.dur} cue={cue} />
        {flash > 0 && <rect x={0} y={0} width={W} height={H} fill="#fff" opacity={flash} />}
      </svg>
    </AbsoluteFill>
  );
};

export const BerlinWall: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#0b1230'}}>
      {timeline.shots.map((shot, i) => {
        const isLast = i === timeline.shots.length - 1;
        return (
          <Sequence key={shot.id} from={Math.round(shot.start * fps)} durationInFrames={Math.round(shot.dur * fps) + (isLast ? 0 : XFADE)} name={shot.id}>
            <ShotView shot={shot} index={i} />
          </Sequence>
        );
      })}
      {timeline.shots.map((shot) =>
        shot.vo ? (
          <Sequence key={'vo' + shot.id} from={Math.round((shot.start + shot.voOff) * fps)} durationInFrames={Math.ceil((shot.voDur + 0.3) * fps)} name={'vo:' + shot.id}>
            <Audio src={staticFile(shot.vo)} />
          </Sequence>
        ) : null,
      )}
      <Audio src={staticFile('audio/bed.mp3')} />
      <Subtitles />
    </AbsoluteFill>
  );
};
