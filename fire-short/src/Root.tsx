import React from 'react';
import {Composition} from 'remotion';
import {FireShort} from './FireShort';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="FireShort"
    component={FireShort}
    durationInFrames={Math.round(timeline.durationSec * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
