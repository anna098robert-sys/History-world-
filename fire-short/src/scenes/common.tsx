import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Stage} from '../components/Effects';
import {FireDefs} from '../components/Fire';
import {LondonDefs} from '../components/London';
import {MachineDefs} from '../components/TimeMachine';

export const Scene: React.FC<{children: React.ReactNode; overlay?: React.ReactNode; bg?: string}> = ({children, overlay, bg = '#120806'}) => (
  <AbsoluteFill>
    <Stage bg={bg}>
      <FireDefs />
      <LondonDefs />
      <MachineDefs />
      {children}
    </Stage>
    {overlay}
  </AbsoluteFill>
);

/** Warm firelight wash that sits over a whole shot. */
export const FireLight: React.FC<{strength?: number}> = ({strength = 0.25}) => (
  <rect x={0} y={0} width={1080} height={1920} fill="#ff6a1a" opacity={strength} style={{mixBlendMode: 'overlay'}} />
);

/** On-screen historical caption (date / place). */
export const Caption: React.FC<{text: string; sub?: string; show: number; top?: number}> = ({text, sub, show, top = 330}) => {
  if (show <= 0) return null;
  return (
    <div
      style={{
        position: 'absolute',
        top,
        left: 0,
        right: 0,
        display: 'flex',
        justifyContent: 'center',
        opacity: show,
        transform: `translateY(${(1 - show) * -30}px)`,
      }}
    >
      <div
        style={{
          background: 'rgba(20,12,8,0.82)',
          border: '5px solid #e8c37a',
          borderRadius: 18,
          padding: '14px 34px',
          textAlign: 'center',
          fontFamily: 'Georgia, "Times New Roman", serif',
          color: '#f6e7c4',
          boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
        }}
      >
        <div style={{fontSize: 50, fontWeight: 700, letterSpacing: 3}}>{text}</div>
        {sub && <div style={{fontSize: 34, fontStyle: 'italic', marginTop: 4, color: '#e8c37a'}}>{sub}</div>}
      </div>
    </div>
  );
};
