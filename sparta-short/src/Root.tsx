import React from 'react';
import {Composition} from 'remotion';
import {SpartaShort} from './SpartaShort';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition
    id="SpartaShort"
    component={SpartaShort}
    durationInFrames={Math.round(timeline.durationSec * timeline.fps)}
    fps={timeline.fps}
    width={1080}
    height={1920}
  />
);
