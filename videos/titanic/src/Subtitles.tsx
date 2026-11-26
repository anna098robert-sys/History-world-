// Synchronised English subtitles: the current narration sentence is split into short chunks
// (max ~7 words); the word being spoken is highlighted in yellow.
import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from './timeline.json';

type Word = {w: string; a: number; b: number};
const chunks: Word[][] = [];
for (const shot of timeline.shots) {
  for (const [a, b, sent] of shot.sents as [number, number, string][]) {
    const words = sent.replace(/\.\.\./g, '… ').split(/\s+/).filter(Boolean);
    const weights = words.map((w) => w.length + 2);
    const tot = weights.reduce((x, y) => x + y, 0);
    let t = shot.start + a;
    const timed: Word[] = words.map((w, i) => {
      const d = ((b - a) * weights[i]) / tot;
      const item = {w, a: t, b: t + d};
      t += d;
      return item;
    });
    let cur: Word[] = [];
    timed.forEach((item, i) => {
      cur.push(item);
      const brk = /[,.!?…;:]$/.test(item.w) && cur.length >= 3;
      if (cur.length >= 7 || brk || i === timed.length - 1) {
        chunks.push(cur);
        cur = [];
      }
    });
  }
}

export const Subtitles: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const T = frame / fps;
  let cur: Word[] | null = null;
  for (let i = 0; i < chunks.length; i++) {
    const c = chunks[i];
    const next = i + 1 < chunks.length ? chunks[i + 1][0].a : Infinity;
    const end = Math.min(next, c[c.length - 1].b + 0.5);
    if (c[0].a <= T && T < end) {
      cur = c;
      break;
    }
  }
  if (!cur) return null;
  const k = Math.min(1, (T - cur[0].a) / 0.12);
  return (
    <div style={{position: 'absolute', left: 0, right: 0, bottom: 52, display: 'flex', justifyContent: 'center'}}>
      <div style={{
        fontFamily: 'Luckiest Guy, Impact, sans-serif', fontSize: 58, letterSpacing: 1, color: '#fff', padding: '14px 34px 8px',
        borderRadius: 26, background: 'rgba(8,8,16,0.62)', transform: `scale(${0.9 + 0.1 * k})`, opacity: k, textAlign: 'center',
        maxWidth: 1600, lineHeight: 1.15, WebkitTextStroke: '2px #121214', textShadow: '0 4px 0 rgba(0,0,0,0.5)',
      }}>
        {cur.map((w, i) => (
          <span key={i} style={{color: T >= w.a && T < w.b + 0.05 ? '#ffd84d' : '#ffffff', marginRight: i < cur!.length - 1 ? 18 : 0}}>
            {w.w.toUpperCase()}
          </span>
        ))}
      </div>
    </div>
  );
};
