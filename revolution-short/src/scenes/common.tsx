import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Character, CharacterProps} from '../components/Character';
import {Stage} from '../components/Effects';
import {FranceDefs} from '../components/France';

export const Scene: React.FC<{children: React.ReactNode; overlay?: React.ReactNode; bg?: string}> = ({children, overlay, bg = '#0b0a10'}) => (
  <AbsoluteFill>
    <Stage bg={bg}>
      <FranceDefs />
      {children}
    </Stage>
    {overlay}
  </AbsoluteFill>
);

/**
 * The History World doodle guy in his French Revolution outfit. Every scene
 * uses this wrapper, so face, proportions, clothing and red cap never change.
 */
export const Hero: React.FC<CharacterProps> = (p) => <Character {...p} outfit="revolution" />;

/** World position of the hero's hand (mirrors the limb maths in Character.tsx). */
export const handPos = (x: number, y: number, s: number, facing: 1 | -1, angleDeg: number, arm: 'L' | 'R') => {
  const a = (angleDeg * Math.PI) / 180;
  const sx = arm === 'L' ? -34 : 34;
  return {x: x + facing * s * (sx - 104 * Math.sin(a)), y: y + s * (-238 + 104 * Math.cos(a))};
};
