import {Easing, interpolate} from 'remotion';

export const FPS = 30;

/** clamped interpolate in SECONDS of local scene time */
export const ip = (
  t: number,
  input: number[],
  output: number[],
  easing: (n: number) => number = Easing.inOut(Easing.cubic),
) => interpolate(t, input, output, {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});

export const easeOut = Easing.out(Easing.cubic);
export const easeIn = Easing.in(Easing.cubic);
export const backOut = Easing.out(Easing.back(2));
export const linear = (n: number) => n;

/** shot selector: returns index of the active shot given cut times */
export const shot = (t: number, cuts: number[]) => {
  let i = 0;
  while (i < cuts.length && t >= cuts[i]) i++;
  return i;
};

/** blink every few seconds */
export const blinkAt = (frame: number, offset = 0) => {
  const p = (frame + offset) % 95;
  return p < 2 ? 1 : p < 4 ? 0.5 : 0;
};
