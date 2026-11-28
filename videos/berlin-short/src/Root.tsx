import React from 'react';
import {Composition} from 'remotion';
import {BerlinShort} from './Video';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="BerlinShort" component={BerlinShort} durationInFrames={timeline.frames} fps={timeline.fps} width={1080} height={1920} />
);
