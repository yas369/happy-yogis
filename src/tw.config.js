// Mirrors the inline tailwind.config in build.py head() - screenshots only.
module.exports = {
  content: ['/home/user/happy-yogis/*.html'],
  theme: { extend: {
    // Cool paper and the brand indigo. sky/muted/clay are the darkened,
    // text-safe members - each clears 4.5:1 on sand, the lightest ground
    // they sit on. sage/amber are decorative only and never carry text;
    // deep is the dark band the hero and closing sections sit on.
    colors: { ink:'#10263A', blue:'#1F4E79', sky:'#21709C', sand:'#E3EDF5',
              paper:'#F2F6FA', line:'#D3E0EA', muted:'#5A6B7B',
              clay:'#81663D', amber:'#B08D57', sage:'#4DA8DA', deep:'#0E2740' },
    fontFamily: { display:['Cormorant Garamond','Georgia','Times New Roman','serif'],
                  body:['DM Sans','system-ui','-apple-system','Segoe UI','sans-serif'] },
    fontSize: { d1:['clamp(3rem,7.2vw,5.25rem)',{lineHeight:'1.06',letterSpacing:'-.008em'}],
                d2:['clamp(2.1rem,3.9vw,3.2rem)',{lineHeight:'1.1',letterSpacing:'-.005em'}],
                d3:['clamp(1.4rem,1.9vw,1.7rem)',{lineHeight:'1.28',letterSpacing:'0'}],
                d4:['1.25rem',{lineHeight:'1.35'}] }
  }}
};
