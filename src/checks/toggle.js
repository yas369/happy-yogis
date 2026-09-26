const { chromium } = require('playwright');
const pairs = [
  ['index.html','ta/index.html'],
  ['blog.html','ta/blog.html'],
  ['yoga-for-back-pain-chennai.html','ta/yoga-for-back-pain-chennai.html'],
  ['yoga-classes-tambaram.html','ta/yoga-classes-tambaram.html'],
];
const noPair = ['hatha-yoga-in-chennai.html','privacy-policy.html'];
(async () => {
  const b = await chromium.launch({ executablePath:'/opt/pw-browsers/chromium' });
  let bad = 0;
  for (const [en, ta] of pairs) {
    for (const [from, expect, lang] of [[en, ta, 'en'], [ta, en, 'ta']]) {
      const p = await b.newPage({ viewport:{width:1280,height:900} });
      await p.goto('http://127.0.0.1:8123/'+from, { waitUntil:'domcontentloaded' });
      const t = await p.evaluate(() => {
        const g = document.querySelector('#navbar .lang-toggle');
        if (!g) return null;
        const cur = g.querySelector('[aria-current]');
        const link = g.querySelector('a');
        return { active: cur && cur.textContent.trim(),
                 other: link && link.textContent.trim(),
                 href: link && new URL(link.getAttribute('href'), location.href).pathname };
      });
      if (!t) { bad++; console.log(`  ${from}: NO TOGGLE`); await p.close(); continue; }
      // clicking it must land on the counterpart
      await p.click('#navbar .lang-toggle a');
      await p.waitForLoadState('domcontentloaded');
      const landed = new URL(p.url()).pathname.replace(/^\//,'') || 'index.html';
      const want = expect === 'index.html' ? '' : expect;
      const ok = landed === expect || (expect === 'index.html' && landed === 'index.html');
      if (!ok) { bad++; console.log(`  ${from} -> ${landed}, expected ${expect}`); }
      else console.log(`  ${from.padEnd(38)} [${t.active}|${t.other}] -> ${landed}`);
      await p.close();
    }
  }
  for (const f of noPair) {
    const p = await b.newPage({ viewport:{width:1280,height:900} });
    await p.goto('http://127.0.0.1:8123/'+f, { waitUntil:'domcontentloaded' });
    const has = await p.evaluate(() => !!document.querySelector('.lang-toggle'));
    if (has) { bad++; console.log(`  ${f}: has a toggle but no Tamil counterpart`); }
    else console.log(`  ${f.padEnd(38)} correctly has no toggle`);
    await p.close();
  }
  console.log(bad ? `\n${bad} problem(s)` : '\nall toggles correct in both directions');
  await b.close();
})();
