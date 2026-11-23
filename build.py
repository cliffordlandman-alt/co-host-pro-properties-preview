import json, sys, datetime
cfg = json.load(open('listings.config.json'))
pms = {r['id']: r for r in json.load(open(sys.argv[1]))}
today = datetime.date.today()
out = []
for u in cfg['units']:
    if u.get('hidden'):
        continue
    s = {k: v for k, v in u.items() if not k.startswith('_') and k not in ('pms_id', 'status_override')}
    r = pms.get(u['pms_id']) if u.get('pms_id') else None
    st, until = 'unknown', None            # unknown = no badge shown
    if u.get('status_override'):
        st, until = u['status_override']['status'], u['status_override'].get('until')
    elif r and r['pms_status'] == 'active':
        if not r['busy_until']:
            st = 'available'
        else:
            far = (datetime.date.fromisoformat(r['busy_until']) - today).days > 120
            # Long stretch (blocks with unknown reasons) -> unavailable, no date. Otherwise: free from the end date.
            st, until = ('unavailable', None) if far else ('from', r['busy_until'])
    s['status'], s['until'] = st, until
    out.append(s)
json.dump({'updated': datetime.datetime.now().strftime('%d %b %Y, %H:%M'), 'units': out},
          open('availability.json', 'w'), indent=1, ensure_ascii=False)
for s in out: print(s['group'], s['name'], s['status'], s['until'])
