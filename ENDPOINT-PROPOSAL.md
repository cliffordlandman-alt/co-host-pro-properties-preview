# Proposed live availability feed (NOT deployed)

Option A (no server change, recommended first): a box routine runs `./refresh.sh` (read-only SQL) every few hours and
publishes the new `availability.json` next to the page. Site host only serves static files.

Option B (needs Clifford's OK + backup first): add one read-only public route to YallaPMS (launchriot.service, VM1):

    GET /public/availability.json  ->  [{ "id": 5, "status": "rented", "until": "2026-12-19" }, ...]

- Runs the query in `availability.sql` (only property id, active/planned state, end date of the stay/block covering today).
- No guest names, phones, emails, prices, channel IDs or iCal URLs. CORS limited to https://co-host.pro. Cache 15 min.
- The page would then fetch this URL instead of the static file; names/photos stay in `listings.config.json`.
