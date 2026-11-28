import {Config} from '@remotion/cli/config';

// use the system Chromium headless shell when available (no browser download needed)
const SYSTEM_SHELL = '/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell';
import fs from 'fs';
if (fs.existsSync(SYSTEM_SHELL)) {
  Config.setBrowserExecutable(SYSTEM_SHELL);
}
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setConcurrency(4);
