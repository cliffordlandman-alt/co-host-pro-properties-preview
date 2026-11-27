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
units_pub = [s for s in out if s['id'] != 'sunrise-bay-monthly']   # generic ad card overlaps the individual Sunrise Bay units
stats = {'homes': len(units_pub),
         'dubai': sum(1 for s in units_pub if s['group'] != 'short-sa'),
         'south_africa': sum(1 for s in units_pub if s['group'] == 'short-sa'),
         'monthly': sum(1 for s in units_pub if s['group'] == 'monthly'),
         'short': sum(1 for s in units_pub if s['group'] != 'monthly'),
         'available_now': sum(1 for s in units_pub if s['status'] == 'available'),
         'available_soon': sum(1 for s in units_pub if s['status'] == 'from')}
reviews = []
try:
    ab = json.load(open('airbnb_profile.json'))
    stats.update(airbnb_live_listings=ab['live_listings'], airbnb_reviews=ab['reviews'], airbnb_rating=ab['rating'],
                 airbnb_superhost=ab['superhost'], airbnb_profile=ab['profile_url'], airbnb_checked=ab['checked'])
    reviews = ab.get('guest_reviews', [])
    live = set(ab['listing_ids'])
    for r in pms.values():
        if r.get('pms_status') == 'active' and r.get('airbnb_listing_id') and r['airbnb_listing_id'] not in live:
            print('NOTE: YallaPMS property', r['id'], 'is not live on the Airbnb profile', file=sys.stderr)
    known = {r.get('airbnb_listing_id') for r in pms.values()}
    for i in live - known:
        print('NOTE: Airbnb listing', i, 'is not in YallaPMS - add it to listings.config.json', file=sys.stderr)
except FileNotFoundError:
    reviews = []
json.dump({'updated': datetime.datetime.now().strftime('%d %b %Y, %H:%M'), 'stats': stats, 'reviews': reviews, 'units': out},
          open('availability.json', 'w'), indent=1, ensure_ascii=False)
for s in out: print(s['group'], s['name'], s['status'], s['until'])
