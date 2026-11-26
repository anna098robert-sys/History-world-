import React from 'react';
import {Composition} from 'remotion';
import {Titanic} from './Video';
import {TitanicShort} from './short/ShortVideo';
import timeline from './timeline.json';
import shortTimeline from './short/timeline.json';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Titanic" component={Titanic} durationInFrames={timeline.frames} fps={timeline.fps} width={1920} height={1080} />
    <Composition id="TitanicShort" component={TitanicShort} durationInFrames={shortTimeline.frames} fps={shortTimeline.fps} width={1080} height={1920} />
  </>
);
