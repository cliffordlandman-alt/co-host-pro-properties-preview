#!/usr/bin/env bash
# Pulls availability from YallaPMS (read-only query) and rebuilds availability.json. Run from the box.
set -euo pipefail
cd "$(dirname "$0")"
ssh -i ~/.ssh/oracle_launchriot ubuntu@145.241.118.107 \
  "sudo -u postgres psql -d launchriot -At -v ON_ERROR_STOP=1 -c 'set default_transaction_read_only=on' -f -" < availability.sql \
  | tail -1 > /tmp/pms_avail.json
python3 build.py /tmp/pms_avail.json
python3 gen_available.py
