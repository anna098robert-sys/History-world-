// Load the two cartoon fonts from /public before any frame is rendered.
import {continueRender, delayRender, staticFile} from 'remotion';

const handle = delayRender('Loading fonts');
const faces = [
  new FontFace('Luckiest Guy', `url(${staticFile('fonts/LuckiestGuy.woff2')}) format('woff2')`),
  new FontFace('Patrick Hand', `url(${staticFile('fonts/PatrickHand.woff2')}) format('woff2')`),
];
Promise.all(faces.map((f) => f.load()))
  .then((loaded) => {
    loaded.forEach((f) => (document.fonts as unknown as {add: (f: FontFace) => void}).add(f));
    continueRender(handle);
  })
  .catch((err) => {
    console.error('font loading failed', err);
    continueRender(handle);
  });
