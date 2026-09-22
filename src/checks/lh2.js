const { chromium } = require('playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
 for (const url of ['index.html','ta/index.html','yoga-for-back-pain-chennai.html']) {
  const ctx=await b.newContext({viewport:{width:412,height:823},deviceScaleFactor:1.75,isMobile:true,hasTouch:true});
  const p=await ctx.newPage();
  const cdp=await ctx.newCDPSession(p); await cdp.send('Network.enable');
  await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:150,
    downloadThroughput:1638400/8,uploadThroughput:675000/8});
  await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
  await p.route(/googletagmanager/,r=>r.fulfill({status:200,contentType:'application/javascript',body:''}));
  const got=[];
  p.on('response',r=>{const u=r.url().replace('http://127.0.0.1:8123/','');
    if(/\.(webp|jpe?g)$/.test(u)) got.push(u);});
  await p.goto('http://127.0.0.1:8123/'+url,{waitUntil:'load'});
  await p.waitForTimeout(5500);
  const m=await p.evaluate(()=>new Promise(r=>{
    let lcp=null, cls=0;
    new PerformanceObserver(l=>{const e=l.getEntries(); lcp=e[e.length-1];}).observe({type:'largest-contentful-paint',buffered:true});
    new PerformanceObserver(l=>{for(const e of l.getEntries()) if(!e.hadRecentInput) cls+=e.value;}).observe({type:'layout-shift',buffered:true});
    setTimeout(()=>{const f=performance.getEntriesByName('first-contentful-paint')[0];
      const kb=performance.getEntriesByType('resource').reduce((a,x)=>a+(x.encodedBodySize||0),0);
      r({fcp:Math.round(f.startTime), lcp:lcp?Math.round(lcp.startTime):null,
         lcpUrl:lcp&&lcp.url?lcp.url.split('/').pop():'(text)',
         cls:+cls.toFixed(4), kb:Math.round(kb/1024)});},400);
  }));
  const hero=got.filter(u=>u.startsWith('ima6'));
  console.log(url.padEnd(34), `FCP ${String(m.fcp).padStart(4)}  LCP ${String(m.lcp).padStart(4)}  CLS ${m.cls}  ${m.kb}KB  LCP=${m.lcpUrl}`);
  if (hero.length) console.log(' '.repeat(34), 'hero variants fetched:', hero.join(', '));
  await ctx.close();
 }
 await b.close();})();
