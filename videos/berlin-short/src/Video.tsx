// The vertical Short: scenes from src/short/timeline.json, narration, music/SFX bed and big vertical subtitles.
import React from 'react';
import {AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import './fonts';
import timeline from './timeline.json';
import {SHOTS, VW, VH} from './scenes';

const XFADE = 6;
type Shot = (typeof timeline.shots)[number];

const makeCue = (shot: Shot) => (text: string, frac?: number) => {
  for (const [a, b, s] of shot.sents as [number, number, string][]) if (s.includes(text)) return frac === undefined ? a : a + (b - a) * frac;
  throw new Error(`cue "${text}" not found in ${shot.id}`);
};

const ShotView: React.FC<{shot: Shot; index: number}> = ({shot, index}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const Comp = SHOTS[shot.id];
  const cue = React.useMemo(() => makeCue(shot), [shot]);
  const fade = index === 0 || shot.id === 'b_crowd' ? 1 : Math.min(1, frame / XFADE);
  return (
    <AbsoluteFill style={{opacity: fade}}>
      <svg width={VW} height={VH} viewBox={`0 0 ${VW} ${VH}`} style={{position: 'absolute', inset: 0}}>
        <Comp t={frame / fps} D={shot.dur} cue={cue} />
      </svg>
    </AbsoluteFill>
  );
};

type Word = {w: string; a: number; b: number};
const chunks: Word[][] = [];
for (const shot of timeline.shots) {
  for (const [a, b, sent] of shot.sents as [number, number, string][]) {
    const words = sent.replace(/\.\.\./g, '… ').split(/\s+/).filter(Boolean);
    const wts = words.map((w) => w.length + 2);
    const tot = wts.reduce((x, y) => x + y, 0);
    let t = shot.start + a;
    let cur: Word[] = [];
    words.forEach((w, i) => {
      const d = ((b - a) * wts[i]) / tot;
      cur.push({w, a: t, b: t + d});
      t += d;
      if (cur.length === 3 || /[,.!?…]$/.test(w) || i === words.length - 1) {
        chunks.push(cur);
        cur = [];
      }
    });
  }
}
const KEY = /wall|destroying|1989|berlin|thousands|concrete|28|years|east|west|divided|november|unbelievable|border|crying|laughing|hammers|smashing|hug|families|decades|time|machine|flashing|subscribe|history|world/i;

const BigSubs: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const T = frame / fps;
  const i = chunks.findIndex((c, k) => c[0].a <= T && T < Math.min(k + 1 < chunks.length ? chunks[k + 1][0].a : 1e9, c[c.length - 1].b + 0.5));
  if (i < 0) return null;
  const c = chunks[i];
  const k = Math.min(1, (T - c[0].a) / 0.12);
  return (
    <div style={{position: 'absolute', left: 40, right: 40, top: 1520, display: 'flex', justifyContent: 'center', flexWrap: 'wrap',
      transform: `scale(${0.75 + 0.25 * k})`, fontFamily: 'Luckiest Guy, Impact, sans-serif', fontSize: 96,
      lineHeight: 1.1, textAlign: 'center'}}>
      {c.map((w, j) => {
        const active = T >= w.a && T < w.b + 0.05;
        return (
          <span key={j} style={{color: KEY.test(w.w) ? '#ffd84d' : '#ffffff', WebkitTextStroke: '6px #121214', paintOrder: 'stroke fill',
            textShadow: '0 8px 0 rgba(0,0,0,0.45)', display: 'inline-block', margin: '0 16px', transform: active ? 'scale(1.12) rotate(-2deg)' : 'none'}}>
            {w.w.toUpperCase()}
          </span>
        );
      })}
    </div>
  );
};

export const BerlinShort: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#0b1230'}}>
      {timeline.shots.map((shot, i) => (
        <Sequence key={shot.id} from={Math.round(shot.start * fps)} durationInFrames={Math.round(shot.dur * fps) + (i < timeline.shots.length - 1 ? XFADE : 0)}>
          <ShotView shot={shot} index={i} />
        </Sequence>
      ))}
      {timeline.shots.map((shot) => (
        <Sequence key={'vo' + shot.id} from={Math.round((shot.start + shot.voOff) * fps)} durationInFrames={Math.ceil((shot.voDur + 0.3) * fps)}>
          <Audio src={staticFile(shot.vo)} />
        </Sequence>
      ))}
      <Audio src={staticFile('audio/bed.mp3')} />
      <BigSubs />
    </AbsoluteFill>
  );
};
