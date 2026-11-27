# Reads Clifford's PUBLIC Airbnb host profile (headless Chrome) and saves public numbers only:
# live listing count, Superhost flag, review count, rating. Keeps the previous file if the check fails.
import json, re, datetime, sys
PROFILE = "https://www.airbnb.ae/users/profile/1470016653640626482"
OUT = "airbnb_profile.json"
try:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--disable-blink-features=AutomationControlled'])
        pg = b.new_page(viewport={'width': 1280, 'height': 900}, locale='en-US',
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36")
        pg.goto(PROFILE, wait_until='domcontentloaded', timeout=60000); pg.wait_for_timeout(8000)
        for _ in range(4): pg.mouse.wheel(0, 2500); pg.wait_for_timeout(1200)
        try: pg.click('text=/Show all.*listings/i', timeout=3000); pg.wait_for_timeout(4000)
        except Exception: pass
        html, text = pg.content(), pg.inner_text('body'); b.close()
    ids = sorted(set(re.findall(r'/rooms/(\d{6,})', html)))
    rev = re.search(r'(\d+)\s*reviews', text); rat = re.search(r'([0-9.]+) out of 5 rating', text)
    if not ids or not rev: raise RuntimeError('profile did not render')
    d = {'profile_url': PROFILE, 'checked': datetime.datetime.now().strftime('%d %b %Y, %H:%M'),
         'live_listings': len(ids), 'listing_ids': ids, 'superhost': 'Superhost' in text,
         'reviews': int(rev.group(1)), 'rating': float(rat.group(1)) if rat else None}
    json.dump(d, open(OUT, 'w'), indent=1); print('airbnb ok', d['live_listings'], 'listings', d['reviews'], 'reviews', d['rating'])
except Exception as e:
    print('airbnb check failed, keeping previous numbers:', e, file=sys.stderr)
