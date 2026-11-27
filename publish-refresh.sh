#!/usr/bin/env bash
# Scheduled job (also regenerates /available/ every run) (run on the box): read-only availability pull from YallaPMS, then publish ONLY if a status/date changed.
set -euo pipefail
cd "$(dirname "$0")"
git pull -q --ff-only
old=$(python3 -c "import json;d=json.load(open('availability.json'));d.pop('updated',None);[d.get('stats',{}).pop(k,None) for k in ('airbnb_checked',)];print(json.dumps(d,sort_keys=True))")
./refresh.sh >/dev/null
new=$(python3 -c "import json;d=json.load(open('availability.json'));d.pop('updated',None);[d.get('stats',{}).pop(k,None) for k in ('airbnb_checked',)];print(json.dumps(d,sort_keys=True))")
# Keep the GitHub Pages custom domain on every rebuild
[ "$(cat CNAME 2>/dev/null)" = "properties.co-host.pro" ] || echo properties.co-host.pro > CNAME
git add CNAME available/index.html
if [ "$old" = "$new" ] && git diff --cached --quiet; then git checkout -q -- availability.json airbnb_profile.json 2>/dev/null || true; echo "no change"; exit 0; fi
if [ "$old" = "$new" ]; then git checkout -q -- availability.json airbnb_profile.json 2>/dev/null || true; fi
git add CNAME availability.json airbnb_profile.json available/index.html
git -c user.name="Khalid (Grok Bot)" -c user.email="bot@launchriot.online" commit -qm "Availability refresh $(date '+%Y-%m-%d %H:%M') Dubai"
git push -q && echo "published change"
python3 -c "import json;[print(u['name'],u['status'],u['until']) for u in json.load(open('availability.json'))['units']]"
