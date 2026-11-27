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
        html, text = pg.content(), pg.inner_text('body')
        reviews = []
        try:   # open "Show all N reviews" (guest tab is the default) and load every page
            pg.keyboard.press('Escape'); pg.wait_for_timeout(500)
            pg.click('button:has-text("Show all"):has-text("reviews")', timeout=5000); pg.wait_for_timeout(3000)
            for _ in range(15):
                btn = pg.locator('[role=dialog] button:has-text("Show more reviews"):visible')
                if btn.count() == 0: break
                btn.first.click(timeout=5000); pg.wait_for_timeout(2200)
            reviews = pg.evaluate(r'''()=>[...document.querySelectorAll('[role=dialog] [role=group][aria-labelledby$="-GUEST"]')].map(g=>{
                const id=g.getAttribute('aria-labelledby'), body=document.getElementById(id);
                const alt=(g.querySelector('[aria-label$="User Profile"]')||{}).getAttribute?.('aria-label')||'';
                const t=g.innerText, d=t.match(/(January|February|March|April|May|June|July|August|September|October|November|December) \d{4}/);
                const r=t.match(/Rating (\d) out of 5/);
                const lines=t.split('\n').map(x=>x.trim()).filter(x=>x.length>1);
                return {name:(alt.replace(/ User Profile$/,'').trim()||lines[0]||'').split(/\s+/)[0], date:d?d[0]:'', rating:r?+r[1]:null, text:body?body.innerText.trim():''}})''')
        except Exception as e:
            print('reviews not read:', e, file=sys.stderr)
        b.close()
    ids = sorted(set(re.findall(r'/rooms/(\d{6,})', html)))
    rev = re.search(r'(\d+)\s*reviews', text); rat = re.search(r'([0-9.]+) out of 5 rating', text)
    if not ids or not rev: raise RuntimeError('profile did not render')
    d = {'profile_url': PROFILE, 'checked': datetime.datetime.now().strftime('%d %b %Y, %H:%M'),
         'live_listings': len(ids), 'listing_ids': ids, 'superhost': 'Superhost' in text,
         'reviews': int(rev.group(1)), 'rating': float(rat.group(1)) if rat else None}
    def excerpt(t, n=190):
        t = re.sub(r'\s+', ' ', t).strip()
        if len(t) <= n: return t
        cut = t[:n]; k = max(cut.rfind('. '), cut.rfind('! '))
        return (cut[:k+1] if k > 80 else cut[:cut.rfind(' ')] + '…')
    good = [{'name': r['name'], 'date': r['date'], 'rating': r['rating'], 'text': excerpt(r['text'])}
            for r in reviews if r.get('name') and r.get('date') and len(r.get('text', '')) >= 20]
    if good:
        d['guest_reviews'] = good
    else:   # last-good fallback
        try: d['guest_reviews'] = json.load(open(OUT)).get('guest_reviews', [])
        except Exception: d['guest_reviews'] = []
    json.dump(d, open(OUT, 'w'), indent=1, ensure_ascii=False); print('airbnb ok', d['live_listings'], 'listings', d['reviews'], 'reviews', d['rating'], '|', len(d['guest_reviews']), 'review texts')
except Exception as e:
    print('airbnb check failed, keeping previous numbers:', e, file=sys.stderr)
