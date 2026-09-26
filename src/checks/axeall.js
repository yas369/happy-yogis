const { chromium } = require('playwright');
const fs=require('fs');
const path=require('path');
// Site root derived from this file's location, so a clone works anywhere.
const ROOT = process.env.HAPPY_YOGIS_ROOT || path.resolve(__dirname,'..','..');
const pages=[...fs.readdirSync(ROOT).filter(f=>f.endsWith('.html')),
             ...fs.readdirSync(ROOT+'/ta').filter(f=>f.endsWith('.html')).map(f=>'ta/'+f)];
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 let bad=0;
 for (const w of [1280,390]) for (const f of pages) {
  const p=await b.newPage({viewport:{width:w,height:900},deviceScaleFactor:1,isMobile:w<500});
  await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
  await p.goto('http://127.0.0.1:8123/'+f,{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  // Kill the transition before revealing, or axe samples a half-faded colour
  // and reports contrast failures that only exist mid-animation.
  await p.evaluate(()=>{
    const st=document.createElement('style');
    st.textContent='*,*::before,*::after{transition:none!important;animation:none!important}';
    document.head.appendChild(st);
    document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'));
  });
  await p.waitForTimeout(600);
  await p.addScriptTag({path:require.resolve('axe-core')});
  const r=await p.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',
    values:['wcag2a','wcag2aa','wcag21a','wcag21aa','best-practice']}}));
  const v=r.violations.map(x=>`${x.id}(${x.nodes.length})`);
  if (v.length) { bad++; console.log(`${w}px ${f}: ${v.join(' ')}`); }
  await p.close();
 }
 console.log(bad? `\n${bad} page/width combos with violations` :
   `\nCLEAN: ${pages.length} pages x 2 widths - no axe violations, reveals included`);
 await b.close();})();
