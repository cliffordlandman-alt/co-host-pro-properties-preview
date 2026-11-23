# co-host.pro Properties page: PREVIEW (not live)

- `index.html`: the Properties page in the style of the live co-host.pro site (navy/copper, Playfair Display + Outfit). No Airbnb links.
- `availability.json`: what the page reads: name, area, beds, stay type, photo, status (available / rented / confirm), until date. No guest data, no prices.
- `listings.config.json`: display details per unit; `pms_id` links to YallaPMS `properties.id`.
- `availability.sql` + `refresh.sh` + `build.py`: read-only pull from YallaPMS that rebuilds `availability.json`.
- `img/`: current photos (from the live site backup and YallaPMS). New units show "Photos coming soon" until Jayson's content lands.
- Inquire = WhatsApp +971 58 644 4285 with the property name prefilled (same as the live site's WhatsApp buttons).
