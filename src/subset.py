import subprocess, os
# Headings and labels only - never body copy - so basic Latin plus the
# typographic punctuation the site actually sets is the whole requirement.
# Latin-1 Supplement is kept so accented names never fall back mid-heading.
UNI = ("U+0020-007E,U+00A0-00FF,U+0131,U+0152-0153,"
       "U+2013-2014,U+2018-201A,U+201C-201E,U+2026,U+2039-203A,"
       "U+00B7,U+2022,U+20B9,U+2122,U+00D7")
jobs = [("cormorant-latin-normal.woff2", "cormorant.woff2"),
        ("cormorant-latin-italic.woff2", "cormorant-italic.woff2")]
for src, dst in jobs:
    before = os.path.getsize(src)
    subprocess.run(["pyftsubset", src, f"--output-file={dst}",
                    f"--unicodes={UNI}", "--flavor=woff2",
                    "--layout-features=kern,liga,clig,calt,onum,tnum",
                    "--desubroutinize", "--no-hinting",
                    "--drop-tables+=DSIG"], check=True)
    after = os.path.getsize(dst)
    print(f"{dst:26s} {before:7,d} -> {after:6,d} bytes  ({100-after*100//before}% smaller)")
tam = os.path.getsize("notoseriftamil-tamil-normal.woff2")
print(f"{'noto-serif-tamil (as-is)':26s} {tam:7,d} bytes")
print(f"\nEnglish pages add: {os.path.getsize('cormorant.woff2')+os.path.getsize('cormorant-italic.woff2'):,} bytes")
print(f"Tamil pages add:   {os.path.getsize('cormorant.woff2')+os.path.getsize('cormorant-italic.woff2')+tam:,} bytes")
