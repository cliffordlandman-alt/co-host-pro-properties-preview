# co-host.pro Properties page: PREVIEW (not live)

- `index.html`: Properties page in the live co-host.pro style. Two groups: **Monthly homes** and **Short stays** (dark band; drop the group by setting its units to `"hidden": true`). Click a card for photos, description and highlights.
- `site-config.js`: the single WhatsApp number used by every button (`971586444285` now; alternative `971544785481`).
- `listings.config.json`: display content per unit (from Jayson's 23 Nov content pack). No prices, no Airbnb links. Unknown facts are left out, not shown as placeholders.
- `availability.json`: what the page reads (built by `build.py`). Status: available / rented (+ until date) / unknown (no badge).
- `availability.sql` + `refresh.sh`: read-only pull of current stays from YallaPMS.
- `img/<unit>/NN.webp` (1600 px) and `NN-sm.webp` (720 px): web-optimised photos, metadata stripped.
- Inquire = WhatsApp with the property name prefilled.
