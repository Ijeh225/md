const { chromium } = require('playwright');
const [,,D,mode,W,H,out] = process.argv; // mode: still|video
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width:+W, height:+H }, deviceScaleFactor: 1 });
  await p.goto('file://' + D + '/ad.html'); await p.evaluate(() => window.ready); await p.waitForTimeout(500);
  const times = mode==='still' ? [1.8,3.8,6.3,9.0,11.2,14.5] : [...Array(450).keys()].map(i=>i/30);
  let i=0;
  for (const t of times) { await p.evaluate(t => render(t), t);
    await p.screenshot({ path: `${out}/f${String(i++).padStart(4,'0')}.jpg`, type:'jpeg', quality: 92 }); }
  await b.close();
})();
