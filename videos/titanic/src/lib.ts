// Math, easing and colour helpers shared by every scene.
export const W = 1920;
export const H = 1080;

export const clamp = (x: number, a = 0, b = 1) => (x < a ? a : x > b ? b : x);
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
export const prog = (t: number, t0: number, t1: number) => (t1 <= t0 ? (t >= t1 ? 1 : 0) : clamp((t - t0) / (t1 - t0)));
export const ease = (x: number) => {
  x = clamp(x);
  return x * x * (3 - 2 * x);
};
export const easeOut = (x: number) => 1 - Math.pow(1 - clamp(x), 3);
export const easeIn = (x: number) => Math.pow(clamp(x), 3);
export const backOut = (x: number, s = 1.70158) => {
  const y = clamp(x) - 1;
  return y * y * ((s + 1) * y + s) + 1;
};

/** deterministic pseudo random generator (so every render is identical) */
export const rng = (seed: number) => {
  let s = seed * 9301 + 49297;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
};

/** natural blinking: returns 1 while the eyes are shut */
export const blinkAt = (t: number, seed = 0) => {
  const period = 3.1 + (seed % 3) * 0.7;
  const ph = (t + seed * 0.77) % period;
  return ph < 0.12 ? 1 : 0;
};

export const C = {
  ink: '#121214',
  white: '#ffffff',
  shade: '#d4dbe6',
  red: '#ed3338',
  redD: '#c2292e',
  redL: '#ff4046',
  gold: '#ffd64d',
  goldD: '#b8892a',
  navy: '#1c2a48',
  sea: '#2f7fc4',
  seaD: '#1f5c94',
  night: '#0b1230',
  nightB: '#26305e',
  hull: '#16161c',
  hullRed: '#9a2a22',
  deck: '#c9955a',
  deckD: '#a8763f',
  cream: '#f6efe0',
  funnel: '#e3a23a',
};

export const mixHex = (a: string, b: string, t: number) => {
  const pa = [1, 3, 5].map((i) => parseInt(a.slice(i, i + 2), 16));
  const pb = [1, 3, 5].map((i) => parseInt(b.slice(i, i + 2), 16));
  return '#' + pa.map((v, i) => Math.round(lerp(v, pb[i], clamp(t))).toString(16).padStart(2, '0')).join('');
};

export const deg = (rad: number) => (rad * 180) / Math.PI;
