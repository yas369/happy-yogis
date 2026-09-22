const { chromium } = require('playwright');
const fs=require('fs');
const path=require('path');
// Site root derived from this file's location, so a clone works anywhere.
const ROOT = process.env.HAPPY_YOGIS_ROOT || path.resolve(__dirname,'..','..');
const pages=fs.readdirSync(ROOT+'/ta').filter(f=>f.endsWith('.html')).map(f=>'ta/'+f);
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const rows=[];
 for (const f of pages) {
  const p=await b.newPage({viewport:{width:+process.env.W||320,height:800},deviceScaleFactor:2,isMobile:true,hasTouch:true});
  await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
  await p.goto('http://127.0.0.1:8123/'+f,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(250);
  rows.push(...await p.evaluate(() => {
   const probe=document.createElement('span');
   probe.style.cssText='position:absolute;visibility:hidden;white-space:nowrap;left:-9999px';
   document.body.appendChild(probe);
   const out=[];
   for (const h of document.querySelectorAll('h1,h2,h3,.display')) {
     const c=getComputedStyle(h);
     if (c.display==='none'||!h.textContent.trim()) continue;
     const avail=h.getBoundingClientRect().width; if(!avail) continue;
     probe.style.font=c.font||`${c.fontWeight} ${c.fontSize}/${c.lineHeight} ${c.fontFamily}`;
     probe.style.fontFamily=c.fontFamily; probe.style.fontSize=c.fontSize; probe.style.fontWeight=c.fontWeight;
     let worst='',ww=0;
     for (const w of h.textContent.trim().split(/\s+/)) {
       probe.textContent=w; const x=probe.getBoundingClientRect().width;
       if(x>ww){ww=x;worst=w;}
     }
     if (ww>avail+0.5) out.push(`${h.tagName} ${c.fontSize} avail ${Math.round(avail)} word ${Math.round(ww)} "${worst}"`);
   }
   probe.remove(); return out;
  }).then(a=>a.map(x=>f+': '+x)));
  await p.close();
 }
 console.log(rows.length?rows.join('\n'):`no Tamil heading has a word wider than its box at ${+process.env.W||320}px`);
 console.log('\ntotal:',rows.length);
 await b.close();})();
