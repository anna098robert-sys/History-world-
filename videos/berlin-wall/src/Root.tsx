import React from 'react';
import {Composition} from 'remotion';
import {BerlinWall} from './Video';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="BerlinWall" component={BerlinWall} durationInFrames={timeline.frames} fps={timeline.fps} width={1920} height={1080} />
);
