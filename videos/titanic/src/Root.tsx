import React from 'react';
import {Composition} from 'remotion';
import {Titanic} from './Video';
import timeline from './timeline.json';

export const RemotionRoot: React.FC = () => (
  <Composition id="Titanic" component={Titanic} durationInFrames={timeline.frames} fps={timeline.fps} width={1920} height={1080} />
);
