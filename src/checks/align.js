const { chromium } = require('playwright');
const fs = require('fs');
const path=require('path');
// Site root derived from this file's location, so a clone works anywhere.
const ROOT = process.env.HAPPY_YOGIS_ROOT || path.resolve(__dirname,'..','..');
const pages=[...fs.readdirSync(ROOT).filter(f=>f.endsWith('.html')),
             ...fs.readdirSync(ROOT+'/ta').filter(f=>f.endsWith('.html')).map(f=>'ta/'+f)];
const WIDTHS=[1280,768,390];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 const agg={edge:[],row:[],width:[]};
 for (const w of WIDTHS) for (const f of pages) {
  const p=await b.newPage({viewport:{width:w,height:900},deviceScaleFactor:1,isMobile:w<500,hasTouch:w<500});
  await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
  await p.goto('http://127.0.0.1:8123/'+f,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  await p.evaluate(()=>document.querySelectorAll('.reveal,.up').forEach(e=>e.classList.add('is-in','in')));
  await p.waitForTimeout(250);
  const r=await p.evaluate(()=>{
    const out={edge:[],row:[],width:[]};
    const vis=e=>{const c=getComputedStyle(e);
      return c.display!=='none'&&c.visibility!=='hidden'&&+c.opacity>0.01&&e.getBoundingClientRect().width>0;};
    const label=e=>e.tagName.toLowerCase()+(typeof e.className==='string'&&e.className
      ?'.'+e.className.trim().split(/\s+/).slice(0,2).join('.'):'');

    /* 1. The main content rail: every top-level text block on the page should
          start on the same x. Near misses (1-12px) are what read as "off". */
    const rails={};
    document.querySelectorAll('main h1, main h2, main p, main h3').forEach(e=>{
      if(!vis(e)) return;
      const r=e.getBoundingClientRect();
      if (r.width < 80) return;
      // ignore things deliberately inset: list items, cards, figures
      if (e.closest('li,figure,blockquote,aside,form,nav,table,.rev-slide')) return;
      const x=Math.round(r.left);
      rails[x]=(rails[x]||0)+1;
    });
    const xs=Object.entries(rails).sort((a,b)=>b[1]-a[1]);
    if (xs.length>1){
      const main=+xs[0][0];
      for (const [x,n] of xs.slice(1)){
        const d=Math.abs(+x-main);
        if (d>0 && d<=12) out.edge.push(`${n} block(s) at x=${x}, main rail x=${main} (off by ${d}px)`);
      }
    }
    /* 2. Grid/flex siblings that should share a top edge but do not. */
    document.querySelectorAll('main .grid, main .flex').forEach(c=>{
      if(!vis(c)) return;
      const cs=getComputedStyle(c);
      if (cs.flexWrap==='wrap'||cs.display==='block') return;
      if (!['start','flex-start','normal','stretch'].includes(cs.alignItems)) return;
      const kids=[...c.children].filter(vis);
      if (kids.length<2) return;
      const tops=kids.map(k=>Math.round(k.getBoundingClientRect().top));
      const spread=Math.max(...tops)-Math.min(...tops);
      if (spread>0 && spread<=10) out.row.push(`${label(c)} children tops differ by ${spread}px`);
    });
    /* 3. Equal-column grids whose items came out unequal widths. */
    document.querySelectorAll('main .grid').forEach(c=>{
      if(!vis(c)) return;
      const t=getComputedStyle(c).gridTemplateColumns.split(' ').filter(Boolean);
      if (t.length<2) return;
      const uniq=[...new Set(t.map(v=>Math.round(parseFloat(v))))];
      if (uniq.length>1 && Math.max(...uniq)-Math.min(...uniq)<=6)
        out.width.push(`${label(c)} columns nearly-but-not-equal: ${t.join(' | ')}`);
    });
    return out;
  });
  r.edge.forEach(x=>agg.edge.push(`${w}px ${f}: ${x}`));
  r.row.forEach(x=>agg.row.push(`${w}px ${f}: ${x}`));
  r.width.forEach(x=>agg.width.push(`${w}px ${f}: ${x}`));
  await p.close();
 }
 for (const [k,t] of [['edge','CONTENT RAIL NEAR-MISSES'],['row','ROW TOP-EDGE DRIFT'],['width','UNEQUAL GRID COLUMNS']]){
   const u=[...new Set(agg[k])];
   console.log(`\n=== ${t}: ${agg[k].length} instance(s), ${u.length} distinct ===`);
   u.slice(0,12).forEach(x=>console.log('  '+x));
 }
 await b.close();})();
