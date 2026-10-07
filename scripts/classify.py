import sys, re, os, json, collections
d = sys.argv[1]
SIMPLE = re.compile(r"^\s*%\{?gpgverify\}?\s+(--keyring=\S+\s+--signature=\S+\s+--data=\S+|--keyring=\S+\s+--data=\S+\s+--signature=\S+)\s*$")
cats = collections.Counter(); out = {}
for f in sorted(os.listdir(d)):
    if not f.endswith('.spec'): continue
    t = open(os.path.join(d,f), errors='replace').read()
    body = t.split('\n%changelog',1)[0]
    lines = body.splitlines()
    # join continuation lines
    joined=[]; buf=''
    for l in lines:
        if l.rstrip().endswith('\\'): buf += l.rstrip()[:-1]+' '; continue
        joined.append(buf+l); buf=''
    calls = [l for l in joined if re.search(r'%\{?gpgverify\b', l) and not l.lstrip().startswith('#')]
    raw = [l for l in joined if re.search(r'(^|[\s/;(])(gpgv2?|gpg2?)\s+-', l) and not l.lstrip().startswith('#') and 'gpgverify' not in l]
    sigsrc = re.search(r'(?im)^Source\d*:.*\.(asc|sig|sign)\s*$', body)
    tags=[]
    if calls:
        simple = all(SIMPLE.match(c) for c in calls)
        tags.append('macro-simple' if simple and len(calls)==1 else 'macro-multi' if simple else 'macro-complex')
        if re.search(r'(?i)sha\d+sums?|checksum', ' '.join(calls)): tags.append('signed-checksums')
    if raw: tags.append('raw-gpg')
    if not calls and not raw and sigsrc: tags.append('sig-unverified')
    if re.search(r'\.kbx\b', body): tags.append('kbx')
    if re.search(r'(?im)^%if.*\n(.*\n){0,3}.*gpgverify', body): tags.append('conditional')
    if tags:
        out[f[:-5]] = tags
        for x in tags: cats[x]+=1
for k,v in cats.most_common(): print(f"{v:5d}  {k}")
json.dump(out, open(sys.argv[2],'w'), indent=1)
