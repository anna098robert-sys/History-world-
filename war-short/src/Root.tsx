import React from 'react';
import {Composition} from 'remotion';
import {WarShort} from './WarShort';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="WarShort"
    component={WarShort}
    durationInFrames={Math.round(timeline.durationSec * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
