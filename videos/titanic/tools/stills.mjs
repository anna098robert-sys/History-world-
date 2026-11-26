// Render review contact sheets: N frames per shot -> one PNG per shot.  node tools/stills.mjs <outdir> [shotId ...]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'fs';
import path from 'path';
import {execFileSync} from 'child_process';

const out = process.argv[2] || 'out/stills';
const only = process.argv.slice(3);
fs.mkdirSync(out, {recursive: true});
const COMP = process.env.COMP || 'Titanic';
const timeline = JSON.parse(fs.readFileSync(COMP === 'Titanic' ? 'src/timeline.json' : 'src/short/timeline.json', 'utf8'));
const shell = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
const browserExecutable = fs.existsSync(shell) ? shell : null;
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const composition = await selectComposition({serveUrl, id: COMP, browserExecutable});
for (const [i, shot] of timeline.shots.entries()) {
  if (only.length && !only.includes(shot.id)) continue;
  const files = [];
  const n = 6;
  for (let k = 0; k < n; k++) {
    const frame = Math.round((shot.start + (shot.dur * (k + 0.5)) / n) * timeline.fps);
    const f = path.join(out, `_${shot.id}_${k}.png`);
    await renderStill({composition, serveUrl, output: f, frame, browserExecutable, scale: 0.5});
    files.push(f);
  }
  const sheet = path.join(out, `${String(i).padStart(2, '0')}_${shot.id}.png`);
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', ...files.flatMap((f) => ['-i', f]), '-filter_complex',
    `[0][1][2]hstack=3[a];[3][4][5]hstack=3[b];[a][b]vstack=2`, sheet]);
  files.forEach((f) => fs.unlinkSync(f));
  console.log('sheet', sheet);
}
process.exit(0);
