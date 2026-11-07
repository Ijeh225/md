const { chromium } = require('playwright');
const [,,page,mode,out,times] = process.argv;
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width:1080, height:1920 } });
  await p.goto('file://' + page); await p.evaluate(() => window.ready); await p.waitForTimeout(400);
  const total = await p.evaluate(() => TOTAL);
  const ts = mode==='still' ? times.split(',').map(Number) : [...Array(Math.round(total*30)).keys()].map(i=>i/30);
  let i=0; for (const t of ts) { await p.evaluate(t => renderAsync(t), t);
    await p.screenshot({ path: `${out}/f${String(i++).padStart(4,'0')}.jpg`, type:'jpeg', quality: 92 }); }
  console.log('total', total, 'frames', i); await b.close();
})();
