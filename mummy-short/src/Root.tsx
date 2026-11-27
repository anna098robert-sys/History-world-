import React from 'react';
import {Composition} from 'remotion';
import {MummyShort} from './MummyShort';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="MummyShort"
    component={MummyShort}
    durationInFrames={Math.round(timeline.durationSec * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
