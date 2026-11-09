// The real Tailwind config: buildall.py compiles the stylesheet from this.
// The :root block at the top of build.py mirrors these tokens for the
// hand-written components, and the two must not drift.
module.exports = {
  // buildall.py passes --content explicitly (a snapshot of the CSS-free
  // pass, Tamil included), so this is only the fallback for running the CLI
  // by hand. Relative, so a clone anywhere works.
  content: ['../*.html', '../ta/*.html'],
  theme: { extend: {
    // Near-white paper. paper and sand were walked up (F2F6FA -> FAFCFE,
    // E3EDF5 -> EEF4F9) for the airier look; `line` deliberately did not
    // follow. A hairline at E2EAF1 measures 1.18:1 against the new paper,
    // which is a rule you cannot see - held at D3E0EA it reads 1.31:1, so
    // the rules got crisper as the grounds got lighter. All five text
    // tokens still clear 4.5:1 on the lightest ground.
    //
    // `sand` then went the other way: at EEF4F9 it measured 1.078:1 against
    // paper, which is a band you cannot see you have entered, and the page
    // read as one undifferentiated scroll. At E4EDF6 it is 1.151:1 - still
    // pale, now legible as a band. That is the darkest it can go: clay, the
    // weakest text token, lands at 4.55:1 on it, so clay was deepened to
    // 755C36 to buy margin. Worst pairing anywhere is now sky on sand, 4.59.
    // Cool paper and the brand indigo. sky/muted/clay are the darkened,
    // text-safe members - each clears 4.5:1 on sand, the lightest ground
    // they sit on. sage/amber are decorative only and never carry text;
    // deep is the dark band the hero and closing sections sit on.
    colors: { ink:'#10263A', blue:'#1F4E79', sky:'#21709C', sand:'#E4EDF6',
              paper:'#FAFCFE', line:'#D3E0EA', muted:'#5A6B7B',
              clay:'#755C36', amber:'#B08D57', sage:'#4DA8DA', deep:'#0E2740' },
    fontFamily: { display:['Cormorant Garamond','Georgia','Times New Roman','serif'],
                  body:['DM Sans','system-ui','-apple-system','Segoe UI','sans-serif'] },
    // Display sizes. d1 is deliberately far larger than a sans headline
    // would dare: Cormorant at 300 gets thinner as it grows, so the weight
    // the eye reads falls as the size rises. The leading tightens with it -
    // 1.06 at 5rem opens gaps you can see through at 7rem.
    //
    // The ceiling came back from 7rem to 6rem when both centres moved under
    // the hero: at 7rem the headline alone pushed them off the first screen,
    // and where the classes are is worth more than the last rem of display
    // type.
    fontSize: { d1:['clamp(2.9rem,7.4vw,6rem)',{lineHeight:'1.0',letterSpacing:'-.014em'}],
                d2:['clamp(2.2rem,4.4vw,3.65rem)',{lineHeight:'1.07',letterSpacing:'-.008em'}],
                d3:['clamp(1.45rem,2.05vw,1.8rem)',{lineHeight:'1.26',letterSpacing:'0'}],
                d4:['1.3rem',{lineHeight:'1.35'}] }
  }}
};
