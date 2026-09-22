const { chromium } = require('playwright');
const fs = require('fs');
const path=require('path');
// Site root derived from this file's location, so a clone works anywhere.
const ROOT = process.env.HAPPY_YOGIS_ROOT || path.resolve(__dirname,'..','..');
const root=ROOT;
const pages=[...fs.readdirSync(root).filter(f=>f.endsWith('.html')),
             ...fs.readdirSync(root+'/ta').filter(f=>f.endsWith('.html')).map(f=>'ta/'+f)];
// 320 = Galaxy Fold / iPhone SE 1st gen; 360 = commonest Android; 390 = iPhone
const WIDTHS=[320,360,390];
(async () => {
  const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
  const agg={overflow:[],tap:[],tiny:[],zoom:[],cramped:[]};
  for (const w of WIDTHS) {
    for (const f of pages) {
      const p=await b.newPage({viewport:{width:w,height:800},deviceScaleFactor:2,
                               isMobile:true,hasTouch:true});
      await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
      await p.goto('http://127.0.0.1:8123/'+f,{waitUntil:'networkidle'});
      await p.evaluate(()=>document.fonts.ready); await p.waitForTimeout(200);
      const r=await p.evaluate(() => {
        const out={overflow:null,tap:[],tiny:[],zoom:[]};
        const vw=document.documentElement.clientWidth;
        if (document.documentElement.scrollWidth > vw+1)
          out.overflow = document.documentElement.scrollWidth;
        const vis=e=>{const c=getComputedStyle(e);
          return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.01&&e.getBoundingClientRect().width>0;};
        // interactive things people tap
        for (const e of document.querySelectorAll('a,button,input,select,textarea,[role=button]')) {
          if (!vis(e)) continue;
          const b=e.getBoundingClientRect();
          const label=(e.textContent||e.getAttribute('aria-label')||e.tagName).trim().slice(0,28);
          // WCAG 2.2 AA minimum is 24x24 CSS px
          if (b.width<24||b.height<24) out.tap.push(`${label} ${Math.round(b.width)}x${Math.round(b.height)}`);
        }
        // body text under 12px is hard work on a phone
        for (const e of document.querySelectorAll('p,li,dd,figcaption,span,label,td')) {
          if (!vis(e) || !e.textContent.trim()) continue;
          if ([...e.children].some(c=>c.textContent.trim()===e.textContent.trim())) continue;
          const fs=parseFloat(getComputedStyle(e).fontSize);
          if (fs < 12) out.tiny.push(`${fs}px "${e.textContent.trim().slice(0,26)}"`);
        }
        // iOS zooms the page when a focused input is under 16px
        for (const e of document.querySelectorAll('input,select,textarea')) {
          if (!vis(e)) continue;
          const fs=parseFloat(getComputedStyle(e).fontSize);
          if (fs < 16) out.zoom.push(`${e.id||e.tagName} ${fs}px`);
        }
        return out;
      });
      if (r.overflow) agg.overflow.push(`${w}px ${f}: scrollWidth ${r.overflow}`);
      r.tap.forEach(t=>agg.tap.push(`${w}px ${f}: ${t}`));
      r.tiny.forEach(t=>agg.tiny.push(`${w}px ${f}: ${t}`));
      r.zoom.forEach(t=>agg.zoom.push(`${w}px ${f}: ${t}`));
      await p.close();
    }
  }
  const uniq=a=>[...new Set(a.map(x=>x.replace(/^\d+px /,'')))];
  for (const [k,label] of [['overflow','HORIZONTAL OVERFLOW'],['tap','TAP TARGETS UNDER 24x24'],
                           ['tiny','TEXT UNDER 12px'],['zoom','INPUTS UNDER 16px (iOS zooms on focus)']]) {
    console.log(`\n=== ${label} : ${agg[k].length} instances, ${uniq(agg[k]).length} distinct ===`);
    uniq(agg[k]).slice(0,10).forEach(x=>console.log('  '+x));
  }
  await b.close();
})();
