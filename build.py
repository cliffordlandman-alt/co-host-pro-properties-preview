import json, sys, datetime
cfg = json.load(open('listings.config.json'))
pms = {r['id']: r for r in json.load(open(sys.argv[1]))}
out = []
for u in cfg['units']:
    s = {'name': u['name'], 'area': u['area'], 'beds': u['beds'], 'stay': u['stay'], 'photo': u['photo'], 'region': 'sa' if any(k in u['area'] for k in ('Cape Town','Gqeberha','South Africa')) else 'dubai'}
    r = pms.get(u['pms_id']) if u['pms_id'] else None
    if u.get('manual_status'):
        s['status'], s['until'] = u['manual_status'], u.get('manual_until')
    elif r is None or r['pms_status'] != 'active':
        s['status'], s['until'] = 'confirm', None
    elif r['busy_until']:
        far = (datetime.date.fromisoformat(r['busy_until']) - datetime.date.today()).days > 330
        s['status'], s['until'] = 'rented', (None if far else r['busy_until'])
    else:
        s['status'], s['until'] = 'available', None
    out.append(s)
json.dump({'updated': datetime.datetime.now().isoformat(timespec='minutes'), 'whatsapp': cfg['whatsapp'], 'units': out},
          open('availability.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
