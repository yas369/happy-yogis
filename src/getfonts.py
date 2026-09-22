import re, subprocess, os
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

def css(url):
    return subprocess.run(["curl", "-sS", "-A", UA, url],
                          capture_output=True, text=True, check=True).stdout

FACE = re.compile(r"/\*\s*([\w-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", re.S)

def faces(sheet):
    for subset, block in FACE.findall(sheet):
        style = re.search(r"font-style:\s*(\w+)", block).group(1)
        url = re.search(r"url\((https://[^)]+)\)", block).group(1)
        rng = re.search(r"unicode-range:\s*([^;]+);", block).group(1).strip()
        yield subset, style, url, rng

WANT = {
    "cormorant": ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:"
                  "ital,wght@0,300..600;1,300..500&display=swap",
                  {"latin", "latin-ext"}),
    "notoseriftamil": ("https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:"
                       "wght@300..600&display=swap",
                       {"tamil"}),
}
out = {}
for name, (url, keep) in WANT.items():
    sheet = css(url)
    print(f"\n=== {name}: subsets offered ->",
          sorted({s for s, _, _, _ in faces(sheet)}))
    for subset, style, u, rng in faces(sheet):
        if subset not in keep:
            continue
        fn = f"{name}-{subset}-{style}.woff2"
        subprocess.run(["curl", "-sS", "-A", UA, u, "-o", fn], check=True)
        sz = os.path.getsize(fn)
        out[fn] = (sz, rng)
        print(f"  {fn:44s} {sz:7,d} bytes")
print(f"\nTOTAL new font bytes: {sum(s for s, _ in out.values()):,}")
import json
json.dump({k: v[1] for k, v in out.items()}, open("font-ranges.json", "w"), indent=1)
