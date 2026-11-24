#!/usr/bin/env bash
# Scheduled job (also regenerates /available/ every run) (run on the box): read-only availability pull from YallaPMS, then publish ONLY if a status/date changed.
set -euo pipefail
cd "$(dirname "$0")"
git pull -q --ff-only
old=$(python3 -c "import json;print(json.dumps(json.load(open('availability.json'))['units'],sort_keys=True))")
./refresh.sh >/dev/null
new=$(python3 -c "import json;print(json.dumps(json.load(open('availability.json'))['units'],sort_keys=True))")
git add available/index.html
if [ "$old" = "$new" ] && git diff --cached --quiet; then git checkout -q -- availability.json; echo "no change"; exit 0; fi
if [ "$old" = "$new" ]; then git checkout -q -- availability.json; fi
git add availability.json available/index.html
git -c user.name="Khalid (Grok Bot)" -c user.email="bot@launchriot.online" commit -qm "Availability refresh $(date '+%Y-%m-%d %H:%M') Dubai"
git push -q && echo "published change"
python3 -c "import json;[print(u['name'],u['status'],u['until']) for u in json.load(open('availability.json'))['units']]"
