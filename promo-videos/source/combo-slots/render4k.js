const { chromium } = require('playwright');
const [,,page,out,a,b] = process.argv;
(async () => {
  const br = await chromium.launch();
  const p = await br.newPage({ viewport: { width:1080, height:1920 }, deviceScaleFactor: 2 });
  await p.goto('file://' + page); await p.evaluate(() => window.ready); await p.waitForTimeout(400);
  for (let i=+a;i<+b;i++){ await p.evaluate(t => renderAsync(t), i/30);
    await p.screenshot({ path: `${out}/f${String(i).padStart(4,'0')}.png` }); }
  await br.close();
})();
