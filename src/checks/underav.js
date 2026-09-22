const { chromium } = require('playwright');
const fs=require('fs');
const path=require('path');
// Site root derived from this file's location, so a clone works anywhere.
const ROOT = process.env.HAPPY_YOGIS_ROOT || path.resolve(__dirname,'..','..');
const pages=[...fs.readdirSync(ROOT).filter(f=>f.endsWith('.html')),
             ...fs.readdirSync(ROOT+'/ta').filter(f=>f.endsWith('.html')).map(f=>'ta/'+f)];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 let bad=0;
 for (const w of [320,390,1280]) for (const f of pages) {
  const p=await b.newPage({viewport:{width:w,height:900},deviceScaleFactor:2,isMobile:w<500,hasTouch:w<500});
  await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
  await p.goto('http://127.0.0.1:8123/'+f,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in')));
  await p.waitForTimeout(150);
  const r=await p.evaluate(()=>{
    const nav=document.querySelector('nav.fixed'); if(!nav) return null;
    const nb=nav.getBoundingClientRect();
    const h1=document.querySelector('main h1'); if(!h1) return null;
    /* Measure the first element that actually paints text, not its padded
       container: a breadcrumb wrapper legitimately starts under the bar while
       its own pt-8 keeps every glyph clear of it. */
    let first=null;
    const walk=document.createTreeWalker(document.querySelector('main'),NodeFilter.SHOW_TEXT);
    for (let n; (n=walk.nextNode());) {
      if (!n.textContent.trim()) continue;
      const el=n.parentElement, c=getComputedStyle(el);
      if (c.display==='none'||c.visibility==='hidden'||+c.opacity<0.01) continue;
      const r=el.getBoundingClientRect(); if (r.height===0) continue;
      first=el; break;
    }
    if (!first) return null;
    const fb=first.getBoundingClientRect();
    return {navBottom:Math.round(nb.bottom), firstTop:Math.round(fb.top),
            tag:first.tagName, clear:fb.top >= nb.bottom};
  });
  if (r && !r.clear) { bad++; console.log(`UNDER NAV ${w}px ${f}: <${r.tag}> top ${r.firstTop} vs nav bottom ${r.navBottom}`); }
  await p.close();
 }
 console.log(bad?`\n${bad} pages with content behind the fixed nav`:'\nCLEAN: first heading clears the fixed nav on every page at 320/390/1280');
 await b.close();})();
