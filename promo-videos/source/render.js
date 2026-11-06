const { chromium } = require('playwright');
const [,,page,mode,W,H,out] = process.argv; // mode: still|video
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width:+W, height:+H }, deviceScaleFactor: 1 });
  await p.goto('file://' + page); await p.evaluate(() => window.ready); await p.waitForTimeout(500);
  const total = await p.evaluate(() => TOTAL);
  const times = mode==='still' ? await p.evaluate(() => window.__stills || []) : [...Array(Math.round(total*30)).keys()].map(i=>i/30);
  let i=0;
  for (const t of times) { await p.evaluate(t => render(t), t);
    await p.screenshot({ path: `${out}/f${String(i++).padStart(4,'0')}.jpg`, type:'jpeg', quality: 92 }); }
  console.log('total', total, 'frames', i);
  await b.close();
})();
