import React from 'react';
import {Composition} from 'remotion';
import {PompeiiShort} from './Video';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="PompeiiShort" component={PompeiiShort} durationInFrames={timeline.frames} fps={timeline.fps} width={1080} height={1920} />
);
