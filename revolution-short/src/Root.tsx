import React from 'react';
import {Composition} from 'remotion';
import {RevolutionShort} from './RevolutionShort';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="RevolutionShort"
    component={RevolutionShort}
    durationInFrames={Math.round(timeline.durationSec * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
