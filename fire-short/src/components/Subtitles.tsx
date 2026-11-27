import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import timeline from '../timeline.json';
import durations from '../voiceDurations.json';

type Word = {text: string; start: number; end: number};
type Chunk = {words: Word[]; start: number; end: number};

const MAX_WORDS = 3;

/**
 * Build caption chunks. Word timings are distributed across each recorded
 * line proportionally to syllable-ish weight (letters), with pauses after
 * punctuation, which lines up closely with the TTS delivery.
 */
const buildChunks = (): Chunk[] => {
  const chunks: Chunk[] = [];
  for (const line of timeline.vo) {
    const dur = (durations as Record<string, number>)[line.id];
    const raw = line.text.split(/\s+/).filter(Boolean);
    const weights = raw.map((w) => {
      const letters = w.replace(/[^A-Za-z0-9]/g, '').length;
      const num = /3,000/.test(w) ? 9 : 0; // "three-thousand-year-old"
      const pause = /[…!?.]$/.test(w) ? 4 : /,$/.test(w) ? 2 : 0;
      return 2 + letters + num + pause;
    });
    const total = weights.reduce((a, b) => a + b, 0);
    let t = line.at;
    const words: Word[] = raw.map((w, i) => {
      const d = (weights[i] / total) * dur;
      const word = {text: w, start: t, end: t + d};
      t += d;
      return word;
    });
    // group: break after punctuation or at MAX_WORDS
    let cur: Word[] = [];
    const flush = () => {
      if (cur.length) {
        chunks.push({words: cur, start: cur[0].start, end: cur[cur.length - 1].end});
        cur = [];
      }
    };
    words.forEach((w) => {
      cur.push(w);
      if (cur.length >= MAX_WORDS || /[…!?.,]$/.test(w.text)) flush();
    });
    flush();
  }
  // hold each chunk until the next one begins (max +0.4s) so captions don't blink
  chunks.forEach((c, i) => {
    const next = chunks[i + 1];
    c.end = Math.min(next ? next.start : c.end + 0.4, c.end + 0.4);
  });
  return chunks;
};

const CHUNKS = buildChunks();

export const Subtitles: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const chunk = CHUNKS.find((c) => t >= c.start && t < c.end);
  if (!chunk) return null;
  const local = (t - chunk.start) * fps;
  const pop = interpolate(local, [0, 4, 7], [0.6, 1.12, 1], {extrapolateRight: 'clamp'});
  const shout = chunk.words.some((w) => /^[A-Z!?]{3,}/.test(w.text.replace(/[^A-Za-z!?]/g, '')));
  return (
    <div
      style={{
        position: 'absolute',
        left: 60,
        right: 60,
        top: 1360,
        display: 'flex',
        justifyContent: 'center',
        flexWrap: 'wrap',
        gap: 0,
        transform: `scale(${pop}) rotate(${shout ? -3 : 0}deg)`,
        fontFamily: 'LuckiestGuy, Impact, sans-serif',
        fontSize: shout ? 128 : 104,
        lineHeight: 1.15,
        textAlign: 'center',
        textTransform: 'uppercase',
        letterSpacing: 2,
      }}
    >
      {chunk.words.map((w, i) => {
        const active = t >= w.start && t < w.end + 0.05;
        const said = t >= w.start;
        return (
          <span
            key={i}
            style={{
              color: active ? '#ffd400' : said ? '#ffffff' : 'rgba(255,255,255,0.92)',
              WebkitTextStroke: '14px #141414',
              paintOrder: 'stroke fill',
              textShadow: '0 10px 0 rgba(0,0,0,0.55)',
              display: 'inline-block',
              margin: '0 24px',
              transform: active ? 'translateY(-6px) scale(1.08)' : 'none',
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
